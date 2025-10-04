from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import OrderForm
from .models import Order, OrderLineItem, Coupon
from .services import choose_tax_rate
from cart.cart import Cart


def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user if request.user.is_authenticated else None
            billing_country = data["billing_country"] or "IE"

            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    full_name=data["full_name"],
                    email=data["email"],
                    billing_address=data["billing_address"],
                    billing_city=data["billing_city"],
                    billing_country=billing_country,
                    tax_rate=choose_tax_rate(billing_country),
                )

                for item in cart:
                    course = item["course"]
                    quantity = item["quantity"]
                    unit_price = item["price"]
                    OrderLineItem.objects.create(
                        order=order,
                        course=course,
                        quantity=quantity,
                        unit_price=unit_price,
                    )

                coupon_code = (data.get("coupon") or "").strip().upper()
                if coupon_code:
                    try:
                        order.coupon = Coupon.objects.get(code=coupon_code, active=True)
                        order.save()
                    except Coupon.DoesNotExist:
                        messages.warning(request, "Coupon not found or inactive.")

            messages.success(request, "Order created. Please complete the payment.")
            return redirect("payments:pay", order_number=order.order_number)
    else:
        form = OrderForm()

    return render(request, "checkout/checkout.html", {"form": form, "cart": cart})


def checkout_success(request, order_number):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout/checkout_success.html", {"order_number": order_number})