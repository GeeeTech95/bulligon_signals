from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import Sum
from Users.models import Notification
from myadmin.models import MyAdmin, Settings as AdminSetting
import random
import math
import uuid


class PlanCategory(models.Model) :
    Category_Choices = (
        ("VIP PROFITABLE ZONE", "VIP PROFITABLE ZONE"),
        ("VVIP BULLIGON SIGNALS", "VVIP BULLIGON SIGNALS")
    )
     
    name = models.CharField(max_length=50, choices=Category_Choices )
    slug = models.CharField(max_length=50)

    def __str__(self) :
        return self.name




class Plan(models.Model):
   

    DURATION_CHOICES = (
    (30, "Monthly"), # indays 
    (120, "Quarterly"),
    (365, "Annually"),
    (730, "Biannually"),
    (3650, "Lifetime"),  #life time is more like 10 years for now
)


    category = models.ForeignKey(PlanCategory,related_name='plans',on_delete=models.PROTECT,null = True)
    name = models.CharField(
        max_length=40, help_text="name you wish to call the  plan")
    slug = models.SlugField(blank=True)
    cost = models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True,
                                   help_text="cost of the plan, currency is USD")  # in $usd
    duration =  models.PositiveIntegerField(choices = DURATION_CHOICES)
    features = models.TextField() #comma seperated features


    referral_percentage = models.FloatField(
        help_text="determines how much referal bonus a use gets when a referral makes deposit on this plan")
    
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


    @property
    def duration_verbose(self):
        return "{} hours".format(self.duration * 24)
    
    @property
    def duration_slug(self) :
        return {key: value for key, value in self.DURATION_CHOICES}[self.duration]
    
    @property
    def features_list(self) :
        return self.features.split(",")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Plan, self).save(*args, **kwargs)

    class Meta():
        ordering = ['cost']


class Signal(models.Model):
    CATEGORY_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('hold', 'Hold'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    ]

   
    asset = models.CharField(max_length=50)  # e.g., BTC/USD, ETH/USDT
    signal_type = models.CharField(max_length=4, choices=CATEGORY_CHOICES)
    entry_price = models.DecimalField(max_digits=15, decimal_places=2)
    take_profit = models.DecimalField(max_digits=15, decimal_places=2)
    stop_loss = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='pending')
    issued_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    exclude_for = models.ManyToManyField(PlanCategory, blank=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.asset} - {self.signal_type} signal"




class Currency(models.Model):

    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name







class Subscription(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='subscription', on_delete=models.CASCADE)

    plan = models.ForeignKey(Plan, related_name='plan_subscription',
                             null=True, blank=True, on_delete=models.SET_NULL)
    plan_start = models.DateTimeField(null=True)
    plan_end = models.DateTimeField(null=True)

    # date created
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    

    class Meta():
        ordering = ['-plan_start']

    

    def days_to_seconds(self, days):
        return days * 24 * 60 * 60

    def approve_subscription(self):
        # checks the state of admin settings for approving
        # subscriptions
        try:
            _setting = AdminSetting.objects.all()[0]
            return _setting.approve_subscription
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.pk:
           

            # check if admnin wants to be approving investmets generally or individually
            if not self.approve_subscription():
                # check if individual
                if self.user.user_wallet.allow_automatic_subscription:
                    self.plan_start = timezone.now()
                    self.plan_end = timezone.now() + timezone.timedelta(days=self.plan.duration)
            else:
                # dont start the plan, start on approval
                pass
            # deduct from balance for the plan
            self.user.user_wallet.debit(self.amount)

        super(Subscription, self).save(*args, **kwargs)
    
    
    def add_referee_earning(self):
        
        if self.user.referee:
            earning = (self.plan.referral_percentage/100) * self.amount
            referee_wallet = self.user.referee.user_wallet
            referee_wallet.referral_earning += earning
            referee_wallet.save()
            # notify
            msg = "You have been credited with a referral bonus of ${}, for your referral {}.".format(
                earning,
                self.user.nick_name
            )
            Notification.objects.create(
                user=self.user.referee,
                message=msg
            )
            #seld mail
           


    def on_approve(self):
        # when admin approves am subscription
        if not self.is_approved:
            self.plan_start = timezone.now()
            self.plan_end = timezone.now() + timezone.timedelta(days=self.plan.duration)
            self.is_approved = True
            self.is_active = True
            self.save()
            self.add_referee_earning()
        return self

    @property
    def _due(self):
        if timezone.now() >= self.plan_end:
            return True
        return False

    @property
    def current_earning(self):
        if not self.plan:
            return 0.00
        else:
            # calcculate what the balance should be for the plan
            today = timezone.now()
            curr_diff = today - self.plan_start
            curr_diff_in_seconds = curr_diff.total_seconds()
            total_diff = self.plan_end - self.plan_start
            total_diff_in_seconds = total_diff.total_seconds()
            earning = (curr_diff_in_seconds/total_diff_in_seconds) * \
                self.expected_earning

            # bal = self.amount + extra
            # incase of overshoot show max earning
            bal = min(earning, self.expected_earning)
            return round(bal, 2)

    @property
    def plan_progress(self):
        if self.is_active:
            today = timezone.now()
            curr_diff = today - self.plan_start
            curr_diff_in_seconds = curr_diff.total_seconds()
            total_diff = self.plan_end - self.plan_start
            total_diff_in_seconds = total_diff.total_seconds()
            progress = (curr_diff_in_seconds/total_diff_in_seconds) * 100
            # in terms of overshoot
            return round(min(progress, 100), 2)
        else:
            return 0

    def on_plan_complete(self):

        # deactivate plan
        self.is_active = False
        self.save()

    def __str__(self):
        return "{}-{}".format(self.user.name, self.plan)

    class Meta():
        ordering = ['date']





class Wallet(models.Model):

    wallet_id = models.UUIDField(
        default=uuid.uuid4, editable=False, null=False)
    user = models.OneToOneField(
        get_user_model(), related_name='user_wallet', on_delete=models.CASCADE)

    # deposits go in here
    initial_balance = models.FloatField(default=0.00, blank=True,)
    # bonus_amount = models.FloatField(blank = True,null = True)  #fadmin can set amount to override current balance calculation
    referral_earning = models.FloatField(default=0.00)
    # for bouses and have nots
    funded_earning = models.FloatField(default=0.00)
    withdrawals = models.FloatField(default=0.00)
    withdrawal_allowed = models.BooleanField(default=False)
    allow_automatic_subscription = models.BooleanField(default=True)

    def debit(self, amount, bal_type="initial"):
        """ bal type signifies the balance to credit
        defaults to intial balance
        """
        if bal_type == "initial":
            self.initial_balance -= amount

        elif bal_type == "referral":
            self.referral_earning -= amount

        # send mail
        self.save()

    def credit(self, amount):
        self.initial_balance += amount
        # send mail
        self.save()

    @property
    def today_PNL(self):
        # calculate all accured profit/loss from 12.00 am to the exact point the user
        # is making the request
        total_pnl = 0.00
        active_subscriptions = self.user.subscription.filter(is_active=True)
        if active_subscriptions:
            for inv in active_subscriptions:
                subscription_pnl = inv.current_earning % 24
                total_pnl += subscription_pnl
        return round(total_pnl, 2)

    @property
    def total_past_earning(self):
        query = self.user.subscription.filter(is_active=False)
        accumulated = query.aggregate(
            expected_earning=Sum("expected_earning")
        )['expected_earning'] or 0

        return accumulated



    @property
    def current_balance(self):
        return round(self.initial_balance + self.funded_earning - self.withdrawals, 2)

    @property
    def available_balance(self):
        return round(self.initial_balance + self.funded_earning - self.withdrawals , 2)

    def __str__(self):
        return "{}-wallet".format(self.user.name)

    def save(self, *args, **kwargs):
        super(Wallet, self).save(*args, **kwargs)


class Transaction(models.Model):

    def get_transaction_id(self):
        PREFIX = "TD"
        number = random.randrange(10000000, 999999999)
        number = PREFIX + str(number)
        if Transaction.objects.filter(transaction_id=number).exists():
            self.get_transaction_id()
        return number

    status = (('Approved', 'Approved'), ('Declined',
              'Declined'), ('Pending', 'Pending'))
    t_choices = (('DEPOSIT', 'DEPOSIT'), ("BONUS",
                 "BONUS"), ("AIR DROP", "AIR DROP"), ("REFERAL EARNING", "REFERAL EARNING"))
    transaction_id = models.CharField(max_length=15, editable=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_transaction')
    transaction_type = models.CharField(max_length=20, choices=t_choices)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=status, default='Pending')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=False)
    coin = models.CharField(blank=True, null=True, max_length=10,default="USDT(BEP20)")
    
    @property
    def batch(self) :
        return  str(uuid.uuid1()).replace("-","") +  str(uuid.uuid1()).replace("-","")[:10]
    
    def __str__(self):
        return self.transaction_id

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.get_transaction_id()
        super(Transaction, self).save(*args, **kwargs)

    class Meta():
        ordering = ['-date']


class PendingDeposit(models.Model):
    method_choices = (("USDT(BEP20)", "USDT(BEP20)"), ("USDT(TRC20)",
                      "USDT(TRC20)"), ("ETH", "ETH"), ("BTC", "BTC"), ("LTC", "LTC"))

    def get_path(instance, file_name):
        ext = file_name.split(".")[1]
        return "{}/deposits/{}.{}".format(instance.user, instance.pk, ext)

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_pending_deposit')
    amount = models.PositiveIntegerField(null=False)
    deposit_address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_declined = models.BooleanField(default=False)
    # reason for declining
    decline_reason = models.TextField(null=True)
    payment_method = models.CharField(max_length=20, choices=method_choices)
    #payment_proof = models.FileField(upload_to=get_path)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

    def on_approve(self):
        # credit wallet
        self.user.user_wallet.credit(self.amount)

        self.is_active = False
        self.delete()

    def save(self, *args, **kwargs):
        super(PendingDeposit, self).save(*args, **kwargs)

    class Meta():
        ordering = ['-date']


