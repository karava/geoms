from django import forms
from .models import ProductEnquiry
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class ProductEnquiryForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]

    existing_customer = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES, 
    )

    def __init__(self, *args, **kwargs):
        super(ProductEnquiryForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""

        self.fields['full_name'].label = 'Full Name'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Enter your full name'

        self.fields['email'].widget.attrs['placeholder'] = 'Youremail@email.com'

        self.fields['phone'].widget.attrs['placeholder'] = '+03 1111 1111'

        self.fields['existing_customer'].label = 'Are Your Existing Customers?'

        self.fields['product_interested_in'].label = 'What Product Are You Interested In?'
        self.fields['product_interested_in'].widget.attrs['placeholder'] = 'Enter the product name'

        self.fields['estimated_quantity'].label = 'Estimated Quantity Required (Square, Metres, Rolls, Etc.)'
        self.fields['estimated_quantity'].widget.attrs['placeholder'] = 'i.e 2.000 m2'

        self.fields['specifications'].label = 'Any Particular Specifications?'
        self.fields['specifications'].widget.attrs['placeholder'] = 'Enter any specifics requirements'
        self.fields['specifications'].widget.attrs['rows'] = '1'

        self.fields['project_based'].label = 'What Is your Project Based?'
        self.fields['project_based'].widget.attrs['placeholder'] = 'Enter the project based'
        self.fields['project_based'].widget.attrs['rows'] = '1'

        self.fields['needed_by'].label = 'When Do You Need The Product By?'
        self.fields['needed_by'].widget.attrs['placeholder'] = 'i.e 2 months'

        self.fields['captcha'].label = ''
        
        for visible in self.visible_fields():
            if visible.field != self.fields['existing_customer']:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductEnquiry
        fields = [
            'full_name', 'email', 'phone', 'existing_customer',
            'product_interested_in', 'estimated_quantity', 'specifications',
            'project_based', 'needed_by', 'captcha'
        ]
