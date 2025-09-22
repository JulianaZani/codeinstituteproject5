import uuid
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from courses.models import Course  # your Course model


# ---------- Coupons ----------
class Coupon(models.Model):
    class Type(models.TextChoices):
        PERCENT = "percent", "Percent"
        FIXED = "fixed", "Fixed amount"

    code = models.CharField(max_length=32, unique=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    value = models.DecimalField(max_digits=9, decimal_places=2, help_text="For percent, use 0-100")
    active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(null=True, blank=True, help_text="Global usage limit (optional)")
    uses = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    def clean(self):
        self.code = self.code.upper().strip()
        if self.type == self.Type.PERCENT and (self.value < 0 or self.value > 100):
            raise ValidationError("Percent coupons must be between 0 and 100.")

    @property
    def is_currently_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        if not self.active:
            return False
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        if self.max_uses is not None and self.uses >= self.max_uses:
            return False
        return True

    def compute_discount(self, amount: Decimal) -> Decimal:
        """Return the discount to apply for a given pre-tax amount."""
        amount = amount or Decimal("0.00")
        if self.type == self.Type.PERCENT:
            return (amount * (self.value / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return min(self.value, amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ---------- Orders ----------
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="orders"
    )

    full_name = models.CharField(max_length=120)
    email = models.EmailField()

    # Minimal billing info for receipts/tax
    billing_address = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=80, blank=True)
    billing_country = models.CharField(max_length=2, blank=True)  # ISO-3166 (e.g., US, GB, IE)

    # Monetary fields
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("0.00"))
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"),
        help_text="VAT/Tax rate as percent (e.g., 23.00 for 23%)"
    )
    tax_amount = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("0.00"))

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    coupon = models.ForeignKey("Coupon", null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")

    # Payments (Stripe-friendly)
    payment_intent_id = models.CharField(max_length=255, blank=True)
    charge_id = models.CharField(max_length=255, blank=True)

    # For auditing/reprocessing
    original_cart = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number

    # ---- helpers ----
    def _recompute_discounts_and_taxes(self):
        """
        subtotal already reflects the sum of line items.
        This recomputes discount_amount, tax_amount, and total.
        """
        pre_tax_amount = self.subtotal

        # discount
        discount = Decimal("0.00")
        if self.coupon and self.coupon.is_currently_valid:
            discount = self.coupon.compute_discount(pre_tax_amount)

        discounted_amount = max(Decimal("0.00"), pre_tax_amount - discount)

        # tax on discounted base
        tax_amount = (discounted_amount * (self.tax_rate / Decimal("100"))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        self.discount_amount = discount
        self.tax_amount = tax_amount
        self.total = (discounted_amount + tax_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        # detect status change for enrollment creation
        old_status = None
        if self.pk:
            old_status = Order.objects.only("status").get(pk=self.pk).status

        if not self.order_number:
            self.order_number = uuid.uuid4().hex.upper()

        # Ensure totals are consistent before saving
        self._recompute_discounts_and_taxes()
        super().save(*args, **kwargs)

        # After save: if status transitioned to PAID, increment coupon usage and grant access
        if old_status != self.Status.PAID and self.status == self.Status.PAID:
            if self.coupon_id:
                Coupon.objects.filter(pk=self.coupon_id).update(uses=models.F("uses") + 1)
            self.grant_access_to_user()

    @property
    def is_paid(self) -> bool:
        return self.status == self.Status.PAID

    def grant_access_to_user(self):
        """
        Create Enrollment records for each purchased course when the order is paid.
        Idempotent: if enrollment exists, it won't duplicate.
        """
        # Import here to avoid circular imports
        from enrollments.models import Enrollment  # make sure the app exists before marking orders as PAID

        if not self.user:
            # Optionally: create an account or send a claim-link flow for guests
            return

        with transaction.atomic():
            for li in self.lineitems.select_related("course").all():
                for _ in range(li.quantity):
                    Enrollment.objects.get_or_create(user=self.user, course=li.course)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lineitems")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="order_lines")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField(max_digits=9, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.course} x {self.quantity} ({self.order.order_number})"

    def save(self, *args, **kwargs):
        # lock the course price at purchase time
        if not self.unit_price:
            self.unit_price = getattr(self.course, "price", Decimal("0.00"))
        self.line_total = (self.unit_price or Decimal("0.00")) * self.quantity
        super().save(*args, **kwargs)


# ---------- signals to keep subtotal in sync with line items ----------
def _recalculate_order_subtotal(order: Order):
    agg = order.lineitems.aggregate(s=Sum("line_total"))
    order.subtotal = agg["s"] or Decimal("0.00")
    # recompute discounts/taxes/total
    order._recompute_discounts_and_taxes()
    # update without triggering Order.save() again
    Order.objects.filter(pk=order.pk).update(
        subtotal=order.subtotal,
        discount_amount=order.discount_amount,
        tax_amount=order.tax_amount,
        total=order.total,
        updated_at=datetime.now(timezone.utc),
    )


@receiver(post_save, sender=OrderLineItem)
def update_order_totals_on_save(sender, instance, **kwargs):
    _recalculate_order_subtotal(instance.order)


@receiver(post_delete, sender=OrderLineItem)
def update_order_totals_on_delete(sender, instance, **kwargs):
    _recalculate_order_subtotal(instance.order)
