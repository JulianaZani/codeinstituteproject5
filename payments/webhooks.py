import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from checkout.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        pi = event["data"]["object"]
        payment_intent_id = pi["id"]
        try:
            order = Order.objects.get(payment_intent_id=payment_intent_id)
            order.status = Order.Status.PAID
            order.charge_id = pi.get("latest_charge", "") or order.charge_id
            order.save()
        except Order.DoesNotExist:
            pass

    elif event["type"] == "payment_intent.payment_failed":
        pi = event["data"]["object"]
        payment_intent_id = pi["id"]
        try:
            order = Order.objects.get(payment_intent_id=payment_intent_id)
            order.status = Order.Status.FAILED
            order.save()
        except Order.DoesNotExist:
            pass

    return JsonResponse({"status": "ok"})
