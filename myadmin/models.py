from django.db import models
from Users.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
import random
import socket
from django.db.models  import  Sum
from django.utils import timezone
from django.conf import settings


class MyAdmin(models.Model) :
    
    def get_reg(self) :
        _id = random.randrange(9999999,999999999999)
        if MyAdmin.objects.filter(reg_id = _id).exists() :
            self.get_reg()
        return _id        
   
    user = models.OneToOneField(get_user_model(),on_delete = models.CASCADE,related_name='user_admin')
    #secret_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    reg_id = models.CharField(max_length=40,editable=False)
    total_revenue  = models.FloatField(default = 0.00)
    is_active = models.BooleanField(default  = True)
    #points admins use on the platform
    points = models.FloatField(default = 0.00)
    is_subscribed = models.BooleanField(default = False)
    subscription_expiry = models.DateTimeField(null = False,blank = False)
    free_plan_expired = models.BooleanField(default = False)
    secret_pin = models.CharField(max_length=4,default = "0000")
  
    
   
        

    def save(self,*args,**kwargs) :
        if not self.pk :
            self.subscription_expiry = timezone.now() + timezone.timedelta(days = settings.FREE_PLAN_DURATION)
        if not self.reg_id :
            self.reg_id= self.get_reg()
        super(MyAdmin,self).save(*args,**kwargs)


   
    
    @property
    def reg_link(self) :
        return "{}?reg_id={}".format(reverse('register'),self.reg_id)

    @property
    def reg_and_ref_link(self) :
        return "{}?reg_id={}&ref_id={}".format(reverse('register'),self.reg_id,self.user.referral_id)    

    @property
    def revenue(self) :
        from wallet.models import Transaction
        deposits = Transaction.objects.filter(user__user_admin = self,transaction_type ="DEPOSIT").aggregate(total = Sum('amount'))
        withdrawals = Transaction.objects.filter(user__user_admin = self,transaction_type ="WITHDRAWAL").aggregate(total = Sum('amount'))
        deposit = deposits['total'] or 0.00
        withdrawal = withdrawals['total'] or 0.00
        revenue =  deposit - withdrawal 
        return revenue
        
    @property
    def allow_access(self) :
        if  self.is_active :
            return True
        elif not self.free_plan_expired :
            return True   
        return False    

    def __str__(self) :
        return self.user.nick_name 



class WalletAddress(models.Model) :
    admin = models.ForeignKey(MyAdmin,on_delete = models.CASCADE,related_name='wallet_address')
    coin_name = models.CharField(max_length=30,help_text= 'full name of coin,e.g Bitcoin')
    coin_code = models.CharField(max_length=15,help_text= 'coin code w.g BTC')
    address = models.CharField(max_length=200,help_text ='enter your own wallet address for this,ensure its correct')

    def __str__(self,*args,**Kwargs) :
        return self.coin_code

    def save(self,**kwargs) :
        self.coin_name = self.coin_name.upper()
        self.coin_code = self.coin_code.upper()
        super(WalletAddress,self).save(**kwargs)



class Settings(models.Model)  :
    reg_email_verify = models.BooleanField(default = False,help_text="enable email verification on registration")       
    enable_newsletters = models.BooleanField(default = False)
    enable_transaction_emails = models.BooleanField(default = False)
    enable_referral_bonus = models.BooleanField(default = False)
    enable_watsapp_chat =  models.BooleanField(default = False)
    enable_social_links = models.BooleanField(default = False)
    enable_registration_emails = models.BooleanField(default = False,help_text ="send emails to users upon registration") 
    enable_withdrawal = models.BooleanField(default=False)
    approve_investment = models.BooleanField(default=False,verbose_name="Stop automatic investments")
    def __str__(self) :
        return "control-site"
        
        

class Subscription(models.Model) :
    admin = models.ForeignKey(MyAdmin, on_delete=models.CASCADE)
    transaction_reference = models.TextField()
    is_approved = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null = True,blank = True)

    def __str__(self) :
        return self.admin.user.nick_name


    def on_approval(self) :
        self.admin.is_subscribed  = True
        self.admin.subscription_expiry = timezone.now() + timezone.timedelta(days=settings.SUBSCRIPTION_DURATION)
        self.date_approved = timezone.now()
        
    def save(self,*args,**kwargs) :
        if self.is_approved and not self.date_approved :
            self.on_approval()   
        super(Subscription,self).save(*args,**kwargs)    



