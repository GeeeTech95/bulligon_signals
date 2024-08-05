from django.shortcuts import render
from django.views.generic import TemplateView,View,ListView
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from wallet.models import Plan
from .forms import ContactForm


class Index(TemplateView) :
    template_name = 'index.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(Index,self).get_context_data(*args,**kwargs) 
        context['plans'] = Plan.objects.all()
        return context



class About(TemplateView) :
    template_name = 'about.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(About,self).get_context_data(*args,**kwargs) 
       
        return context

class Faq(TemplateView) :
    template_name = 'faq.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(Faq,self).get_context_data(*args,**kwargs) 
       
        return context        

class Plans(ListView) :
    template_name = 'plans.html'
    model = Plan
    context_object_name = "plans"



class TOS(TemplateView) :
    template_name  = 'terms-of-service.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(TOS,self).get_context_data(*args,**kwargs) 
       
        return context


class CookiePolicy(TemplateView) :
    template_name  = 'cookie-policy.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(CookiePolicy,self).get_context_data(*args,**kwargs) 
       
        return context
    

class PrivacyPolicy(TemplateView) :
    template_name  = 'privacy-policy.html'

    def get_context_data(self,*args,**kwargs) : 
        context = super(PrivacyPolicy,self).get_context_data(*args,**kwargs) 
       
        return context    

class Contact(View) :
    template_name = 'contact.html'
    form_class = ContactForm


    def get(self,request,*args,**kwargs) :
        ctx = {'cclass' : 'active','form' : self.form_class} 
        return render(request,self.template_name,ctx)

    def post(self,request,*args,**kwargs) :
        feedback = {}
        form = self.form_class(request.POST)  
        
        if form.is_valid() :
            
            name = form.cleaned_data.get('name','') 
            if len(name) > 0  : 
                name = "my name is {}.".format(name)
            title = form.cleaned_data.get('title')
            message = "{} {}".format(name,form.cleaned_data.get('message'))
            email = form.cleaned_data.get('email')
            ideal_email = settings.EMAIL_HOST_USER
            send_mail(
                title,
                message,
                email,
                [ideal_email],
                fail_silently = True

            )
            feedback['success'] = True
        else : feedback['error'] = "details failed validation"
        return JsonResponse(feedback)    
