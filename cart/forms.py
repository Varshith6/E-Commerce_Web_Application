from django import forms


PAYMENT_CHOICES = (
    ('A', 'All payment options'),
    ('P', 'PayU')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=True)
    shipping_address2 = forms.CharField(required=True)
    City = forms.CharField(empty_value='Hyderabad',disabled=True,required=False,widget=forms.TextInput(attrs={
        'readonly':'readonly',
        'value':'Hyderabad',
        'class': 'form-control'
    }))
    State = forms.CharField(empty_value='Telangana',disabled=True,required=False, widget=forms.TextInput(attrs={
        'readonly':'readonly',
        'value': 'Telangana',
        'class': 'form-control'
    }))
    shipping_Pincode = forms.CharField(required=True)


    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_Pincode = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget = forms.RadioSelect, choices=PAYMENT_CHOICES,required=False)
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    altmobile = forms.CharField(required=False)
    email = forms.EmailField(required=False)


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True)




