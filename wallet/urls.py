from django.urls import include,path
from .transaction import Deposit, Plans,Withdrawal,Invest


urlpatterns = [
    path('fund-wallet/',Deposit.as_view(),name ='deposit'),
    path('withdraw/',Withdrawal.as_view(),name ='withdraw'),
    #path('plans/',Plans.as_view(),name ='plans'),
    path('<slug:slug>/invest/',Invest.as_view(),name ='invest'),
    
    
]