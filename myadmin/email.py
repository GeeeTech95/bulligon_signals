from django.conf import settings
from django.views.generic import View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from core.communication import AccountMail


from .forms import SendMailForm
from .dashboard import AdminBase
from wallet.models import Wallet


class SendCustomMail(AdminBase,View) :
    form_class = SendMailForm
    success_url = reverse_lazy('admin-dashboard')
    template_name = 'form.html'



    def  get(self,request,*args,**kwargs)  :
        wallet_id = kwargs.get('wallet_id',None)
        if not wallet_id : 
            pass
        form = self.form_class()
        form_title = 'Send Custom Email'
        return render(request,self.template_name,locals())



    def  post(self,request,*args,**kwargs)  :
       
        form = self.form_class(request.POST) 
        ctx = {}
        if form.is_valid() :
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']  
            message = form.cleaned_data['message']  
            name = form.cleaned_data.get('name',None)
            mail = AccountMail(send_type="support")
            ctx['text'] = message
            ctx['subject'] = subject
           
            if name : 
                ctx["name"] = name
            mail.send_html_AccountMail([email],subject=subject,ctx = ctx)
            return HttpResponseRedirect(self.success_url)

        else : 
            return render(request,self.template_name,locals())




