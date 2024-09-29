from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from wallet.models import Subscription, Transaction,PendingDeposit
from core.communication import TransactionMail


@receiver(post_save, sender=Transaction)
def transaction_handler(sender, instance, created, **kwargs):

    if created:
 
        #send mail
        mail = TransactionMail(instance)
        mail.send_transaction_mail()





@receiver(post_save, sender=Subscription)
def subscription_handler(sender, instance, created, **kwargs):
    #send mail on creation and approval
    if  instance.is_approved  :
        #send mail
        mail = TransactionMail(instance)
        mail.send_subscription_mail()



@receiver(post_save, sender=PendingDeposit)
def deposit_handler(sender, instance, created, **kwargs):
    #send mail on creation and approval
    if created   :
        #send mail
        mail = TransactionMail(instance)
        mail.send_deposit_mail()



