from django import forms
from crispy_forms.helper import FormHelper
from .models import Emailupdate

class SubscribeForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False

    class Meta:
        model = Emailupdate
        fields = ['Email']
        

        def clean_Email(self):
            email = self.cleaned_data.get('Email')

            return email