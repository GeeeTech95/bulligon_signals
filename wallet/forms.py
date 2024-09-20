from django import forms
from django.contrib.auth.password_validation import validate_password
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit

from .models import Subscription, PendingDeposit


class DepositForm(forms.ModelForm):


    class Meta():
        model = PendingDeposit
        fields = ['payment_method', 'amount', 'deposit_address']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return amount


class SubscriptionForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta():
        model = Subscription
        fields = ['plan']

 