from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Order


class OrderForm(forms.ModelForm):
    coupon = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "billing_address",
            "billing_city",
            "billing_country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        placeholders = {
            "full_name": "Full name",
            "email": "Email address",
            "billing_address": "Billing address",
            "billing_city": "City",
            "billing_country": "Country code (e.g. IE)",
            "coupon": "Coupon code (optional)",
        }

        if "full_name" in self.fields:
            self.fields["full_name"].widget.attrs["autofocus"] = True

        for name, field in self.fields.items():
            placeholder = placeholders.get(name, "")
            if field.required and placeholder:
                placeholder = f"{placeholder} *"
            field.widget.attrs["placeholder"] = placeholder
            field.widget.attrs["class"] = "form-control"
            field.label = False

        self.fields["coupon"].widget.attrs["placeholder"] = placeholders["coupon"]
        self.fields["coupon"].widget.attrs["class"] = "form-control"
        self.fields["coupon"].label = False
