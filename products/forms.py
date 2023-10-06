from django import forms
from .models import ProductEnquiry
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class ProductEnquiryForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = ProductEnquiry
        fields = [
            'full_name', 'email', 'phone', 'existing_customer',
            'product_interested_in', 'estimated_quantity', 'specifications',
            'project_based', 'needed_by', 'captcha'
        ]
