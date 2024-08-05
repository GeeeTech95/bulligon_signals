from django import forms

class ContactForm(forms.Form) :
    name = forms.CharField(required = False)
    phone_number = forms.CharField(required = False)
    message = forms.CharField(required = True)
    title = forms.CharField()
    email = forms.EmailField(required = True)