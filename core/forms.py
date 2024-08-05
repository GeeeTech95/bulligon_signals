from django import forms
from django.core.exceptions import ValidationError


class OtpForm(forms.Form) :
    code = forms.CharField(required=True,help_text="Enter the code sent to your email,click resend if you dint get any after some time")
    

    def __init__(self,user=None,*args,**kwargs) :
        self.user = user
        super(OtpForm,self).__init__(*args,**kwargs)

     
    def clean_code(self) :
       pass

