import stripe
from decimal import Decimal
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent_for_order(order):
    amount_cents = int((order.total or Decimal("0.00")) * 100)

    if order.payment_intent_id:
        pi = stripe.PaymentIntent.modify(
            order.payment_intent_id,
            amount=amount_cents,
            currency="eur",
            metadata={"order_number": order.order_number},
        )
    else:
        pi = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="eur",
            metadata={"order_number": order.order_number},
            automatic_payment_methods={"enabled": True},
        )
        order.payment_intent_id = pi.id
        order.save(update_fields=["payment_intent_id"])

    return pi
