from Users.models import Notification
from django.views.generic import CreateView,View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseRedirect
from .models import WalletAddress
from .dashboard import AdminBase
from .forms import TransactionForm
from wallet.models import Transaction, Wallet
from core.notification import Notification



class CreateTransaction(AdminBase,CreateView) :
    model = Transaction 
    template_name = 'form.html'
    form_class = TransactionForm
    success_url = reverse_lazy('my-members')

    def get(self,request,*args,**kwargs) :
        try :
            user = Wallet.objects.get(wallet_id = kwargs.get('wallet_id',None))
        except :
            return HttpResponse("Invalid request")    
        form = self.form_class(initial = {'user' : user,'status' : 'Approved'})
        form_title = "Create Transaction"
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :
        form = self.form_class(data=request.POST) 
        if form.is_valid() :
            form.save(commit  = False) 
            user = form.cleaned_data['user']
            funded = user.user_wallet.funded_earning 
            user.user_wallet.funded_earning = funded + form.cleaned_data['amount']
            user.user_wallet.save() 
            form.instance.status  = "Approved"
            transact = form.save()
            msg = "Congratulations!, A {} transaction of {} just ocurred on your wallet".format(transact.transaction_type,transact.amount)
            #send user notification
            Notification.notify(user,msg)   
            return HttpResponseRedirect(self.success_url)

        else :
            form = self.form_class(admin=request.user,initial = {'user' : request.user,'status' : 'Approved'})
            return render(request,self.template_name,locals())    
    


class TransactionHistory(ListView) :
    model = Transaction
    context_object_name = 'transaction_history'
    template_name = 'transaction-history.html'

    def get_queryset(self) :
        return self.model.objects.filter(user__admin = self.request.user).order_by('-date')
