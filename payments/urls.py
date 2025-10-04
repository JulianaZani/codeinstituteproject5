from django.urls import path
from .views import payment_view
from .webhooks import stripe_webhook

app_name = "payments"

urlpatterns = [
    path("<uuid:order_number>/", payment_view, name="pay"),

    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
]