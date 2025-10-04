from django.shortcuts import render, get_object_or_404
from django.conf import settings
from checkout.models import Order
from .services import create_payment_intent_for_order


def payment_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    pi = create_payment_intent_for_order(order)

    context = {
        "order": order,
        "client_secret": pi.client_secret,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "payments/payment.html", context)
