from django import forms
from .models import ProductEnquiry

class ProductEnquiryForm(forms.ModelForm):
    class Meta:
        model = ProductEnquiry
        fields = [
            'full_name', 'email', 'phone', 'existing_customer',
            'product_interested_in', 'estimated_quantity', 'specifications',
            'project_based', 'needed_by'
        ]
