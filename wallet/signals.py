from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from wallet.models import Investment, Transaction,WithdrawalApplication,PendingDeposit
from core.communication import TransactionMail


@receiver(post_save, sender=Transaction)
def transaction_handler(sender, instance, created, **kwargs):

    if created:
 
        #send mail
        mail = TransactionMail(instance)
        mail.send_transaction_mail()




@receiver(post_save, sender=WithdrawalApplication)
def withdrawal_handler(sender, instance, created, **kwargs):
   
    if not created and instance.is_approved :
        pass
    
    #send mail on creation and approval
    if created   :
        instance.wallet_address = instance.user.wallet_address
        instance.wallet_name = instance.user.wallet_name
        #send mail
        mail = TransactionMail(instance)
        mail.send_withdrawal_application_mail()




@receiver(post_save, sender=Investment)
def investment_handler(sender, instance, created, **kwargs):
    #send mail on creation and approval
    if  instance.is_approved  :
        #send mail
        mail = TransactionMail(instance)
        mail.send_investment_mail()



@receiver(post_save, sender=PendingDeposit)
def deposit_handler(sender, instance, created, **kwargs):
    #send mail on creation and approval
    if created   :
        #send mail
        mail = TransactionMail(instance)
        mail.send_deposit_mail()



