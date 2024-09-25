from django.urls import path, include
from .dashboard import Dashboard, Settings
from .members import MemberDetail, Members
from .investment import (
    CreatePlan,
    AllPlans,
    DepositNotice,
    ApproveDeposit,

    SubscriptionNotice,
    ApproveSubscription


)

from .wallet import AddCoin, CoinList, DeleteCoin, EditCoin
from .transaction import CreateTransaction, TransactionHistory
from .email import SendCustomMail


urlpatterns = [
    # DASHBOARD
    path('', Dashboard.as_view(), name='admin-dashboard'),
    path('members/', Members.as_view(), name='my-members'),
    path('member/<int:pk>/', MemberDetail.as_view(), name='member-detail'),
    path('settings/', Settings.as_view(), name='admin-settings'),


    # MEMBERS
    path('member/<int:pk>/', MemberDetail.as_view(), name='member-detail'),



    # PLAN
    path('plans/create/', CreatePlan.as_view(), name='create-plan'),
    path('plans/delete/', AllPlans.as_view(), name='delete-plan'),
    path('plans/', AllPlans.as_view(), name='plans-admin'),

    # DEPOSIT
    path('deposit-notice/', DepositNotice.as_view(), name='deposit-notice'),
    path('deposit-notice/approve/',
         ApproveDeposit.as_view(), name='approve-deposit'),

    # INVESTMENT
    path('investment-notice/', SubscriptionNotice.as_view(),
         name='investment-notice'),
    path('approve-investment/', ApproveSubscription.as_view(),
         name='approve-investment'),

    # COIN
    path('coin-address/add/', AddCoin.as_view(), name='add-coin'),
    path('coin-address/delete/', DeleteCoin.as_view(), name='delete-coin'),
    path('coin-address/edit/', EditCoin.as_view(), name='edit-coin'),
    path('coin-address/', CoinList.as_view(), name='coin-list'),

    # TRANSACTION
    path('transaction/create/<str:wallet_id>/',
         CreateTransaction.as_view(), name='create-transaction'),
    path('transactions/', TransactionHistory.as_view(),
         name='transaction-history'),
 
    # EMAIL
    path('mail/send-custom-email/',
         SendCustomMail.as_view(), name='send-custom-mail'),



]
