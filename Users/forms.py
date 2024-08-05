from cProfile import label
from dataclasses import fields
import email
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, NewsLaterSubscriber, Settings,KYC
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class SettingForm(ModelForm):

    class Meta():
        model = Settings
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'input__group form'
        self.helper.form_id = 'setting-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'input__group mb-23'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'email_on_transaction',
                'password_on_withdrawal',
              
            ),

            Submit('submit', 'Update', css_class='theme-btn blue width-full mt-5'),
        )
    

    def clean_email_on_transaction(self):
        e_t = self.cleaned_data.get("email_on_transaction", False)
        if e_t == "on":
            e_t = True
        return e_t


class VerifyEmailForm(forms.Form):
    email = forms.EmailField(
        help_text="We are sending a verification code to this email address, you can edit it before hitting the send button")

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(VerifyEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'input__group form'
        self.helper.form_id = 'setting-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'input__group mb-23'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'email',
           
              
            ),

            Submit('submit', 'Verify', css_class='theme-btn blue width-full mt-5'),
        )

class WalletForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'input__group form'
        self.helper.form_id = 'wallet-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'input__group mb-23'
        self.helper.layout = Layout(
            Fieldset(
                '',
                '_wallet_name',
                '_wallet_address',
              
            ),

            Submit('submit', 'Update', css_class='theme-btn blue width-full mt-5'),
        )


    class Meta():
        model = User
        fields = ["_wallet_name", "_wallet_address"]




class KYCForm(ModelForm):
  

    class Meta():
        model = KYC
        fields = ["face_capture","id_upload","proof_of_address_type","proof_of_address"]



class UserCreateForm(ModelForm):
    referral_id = forms.CharField(required=False)
    full_name = forms.CharField(required=True)
    password2 = forms.TextInput()

    def clean_password2(self):

        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if not password1 or not password2:
            raise forms.ValidationError("password cannot be empty")

        if password1 != password2:
            raise forms.ValidationError("password must match ")

        return password2

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


    class Meta():
        model = User
        fields = ['email', 'name', 'country',
                  'phone_number', 'password']


class ProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'input__group form'
        self.helper.form_id = 'profile-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.field_class = 'input__group mb-23'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'email',
                'phone_number',
                'country'
            ),

            Submit('submit', 'Update', css_class='theme-btn blue width-full mt-5'),
        )

    class Meta():
        model = User
        fields = ['name', 'email', 'phone_number', 'country']


class SubscribeForm(forms.ModelForm):

    class Meta():
        model = NewsLaterSubscriber
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.Meta.model.objects.filter(email=email).exists():
            raise forms.ValidationError("You have already subscribed !")
        return email
