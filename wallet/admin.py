from django.contrib import admin
#from django.contrib.auth import LoginRequiredMixin,UserPassesTestMixin
from .models import *


admin.site.register(PendingDeposit)
admin.site.register(Plan)
admin.site.register(PlanCategory)
admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Subscription)


class  WithdrawalDetail()  :
    pass


class WithdrawalList() :
    pass




     

