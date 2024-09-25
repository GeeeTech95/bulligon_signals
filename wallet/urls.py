from django.urls import include,path
from .transaction import Deposit, Plans,Subscribe


urlpatterns = [
    path('fund-wallet/',Deposit.as_view(),name ='deposit'),
    #path('plans/',Plans.as_view(),name ='plans'),
    path('<slug:slug>/subscribe/',Subscribe.as_view(),name ='subscribe-signal'),
    
]