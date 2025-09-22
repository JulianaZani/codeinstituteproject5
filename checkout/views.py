from decimal import Decimal
from checkout.models import Order, OrderLineItem, Coupon
from checkout.services import choose_tax_rate
from courses.models import Course

def create_order_from_cart(request):
    user = request.user if request.user.is_authenticated else None
    billing_country = request.POST.get("billing_country", "IE")
    coupon_code = request.POST.get("coupon", "").strip().upper() or None

    order = Order.objects.create(
        user=user,
        full_name=request.POST.get("full_name", "Customer"),
        email=request.POST.get("email", "customer@example.com"),
        billing_address=request.POST.get("billing_address", ""),
        billing_city=request.POST.get("billing_city", ""),
        billing_country=billing_country,
        tax_rate=choose_tax_rate(billing_country),
    )

    course = Course.objects.get(pk=request.POST["course_id"])
    OrderLineItem.objects.create(order=order, course=course, quantity=1, unit_price=course.price)

    if coupon_code:
        try:
            order.coupon = Coupon.objects.get(code=coupon_code, active=True)
        except Coupon.DoesNotExist:
            pass
        order.save()

    return order
