from django.http.response import JsonResponse
from django.views.generic import CreateView,View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseRedirect
from .models import WalletAddress
from .dashboard import AdminBase


class AddCoin(AdminBase,CreateView) :
    template_name = 'form.html'
    model = WalletAddress
    success_url = reverse_lazy('coin-list')
    fields = ['coin_name','coin_code','address']

    def form_valid(self,form) :
        form.save(commit = False)
        form.instance.admin = self.request.user.user_admin
        form.save()
        return HttpResponseRedirect(self.success_url)


class CoinList(AdminBase,ListView) : 
    template_name = 'coin-list.html'  
    context_object_name = 'coins'  
    model  = WalletAddress

    def get_queryset(self)  :
        return self.model.objects.filter(admin = self.request.user.user_admin)


class DeleteCoin(AdminBase,View) :
    model = WalletAddress

    def get(self,request,*args,**kwargs) :
        feedback = {}
        pk = request.GET.get('pk',None)
        if not pk :
            feedback['error'] = "pk cannot be empty"
            return JsonResponse(feedback)
        try : coin  = self.model.objects.get(pk = pk)  
        except self.model.DoesNotExist : 
            feedback['error'] = "pk is not valid"
            return JsonResponse(feedback)    
        if coin.admin == self.admin :
            coin.delete()
            feedback['success'] = "Wallet address deleted successfully"   
            pass
        else : feedback['error'] = "You have no permission to perform this action"
        
        return JsonResponse(feedback) 



    


class EditCoin(AdminBase,UpdateView) :
    pass
 



class ApproveDeposit(View) :
    pass


class DeclineDeposit() :
    pass


class Transaction() :
    class Create() :
        pass


    class Delete() :
        pass


    class Edit() :
        pass



