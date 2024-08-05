from django import forms
from django.contrib.auth.password_validation import validate_password
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit

from .models import Investment, PendingDeposit, WithdrawalApplication as WA


class WithdrawalForm(forms.ModelForm):
    password = forms.CharField(required=False, strip=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(WithdrawalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            try:
                if field.errors:
                    field.widget.attrs['class'] = 'field-error'
            except:
                pass

    class Meta():

        model = WA
        fields = ['balance_type', 'amount']

    def clean_amount(self):
        amt = self.cleaned_data.get('amount', None)

        # check if balance is available up to amt for the
        # particular balance_type\

        balance_type = self.clean_balance_type()
        if balance_type == "Referral":
            if amt > self.user.user_wallet.referral_earning:
                err = "Your referral balance is insufficient to make this withdrawal, enter a lower amount"
                raise forms.ValidationError(err)

        elif amt > self.user.user_wallet.available_balance:
            err = "Your main balance is insufficient to make this withdrawal, enter a lower amount"
            raise forms.ValidationError(err)
        return amt

    def clean_balance_type(self):
        b_type = self.cleaned_data.get('balance_type', None)
        # check for pending withrawal under the balance type
        if WA.objects.filter(user=self.user, balance_type=b_type, status="PENDING").exists():
            err = "You already have a pending withdrawal request on your {} balance, you can't create another".format(
                b_type)
            raise forms.ValidationError(err)

        # check if plan is due if bal type is main
        """if b_type == "Main" and not self.user.user_wallet.plan_is_due :
            err = "You cannot withdraw from your main balance as your plan is not yet due."
            raise forms.ValidationError(err)"""
        return b_type

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        # verify password
        if password and not self.user.check_password(password):
            raise forms.ValidationError("Password does not match")
        return password


class DepositForm(forms.ModelForm):


    class Meta():
        model = PendingDeposit
        fields = ['payment_method', 'amount', 'deposit_address']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return amount


class InvestmentForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta():
        model = Investment
        fields = ['plan', 'amount']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        plan = self.cleaned_data['plan']

        if not plan:
            raise forms.ValidationError(
                "An unspecified error occured,please try again later")

        if plan.max_cost and amount > plan.max_cost:
            raise forms.ValidationError(
                "Amount must be the specified limits or select another plan")

        if amount < plan.min_cost:
            raise forms.ValidationError(
                "Amount must be the specified limits or select another plan")

        # check if user has enough balance
        if not self.user.user_wallet.available_balance >= amount:
            raise forms.ValidationError(
                "Insufficient balance, Your available wallet balance is too low !")

        return amount
