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


class Plan(models.Model):
    Category_Choices = (
        ("promo", "promo"),
        ("regular", "regular"),
        ("vip", "vip")
    )

    category = models.CharField(max_length=40, choices=Category_Choices)
    name = models.CharField(
        max_length=40, help_text="name you wish to call the investment plan")
    slug = models.SlugField(blank=True)
    max_cost = models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True,
                                   help_text="maximum investment for thie plan,currency is USD")  # in $usd
    min_cost = models.DecimalField(max_digits=20, decimal_places=2,
                                   help_text="minimum investment for thie plan,currency is USD")  # in $usd
    duration = models.PositiveIntegerField(
        help_text="plan duration in days")  # in days
    interest_rate = models.FloatField(
        blank=False, null=False, help_text="in %,e.g 50,100,200")
    referral_percentage = models.FloatField(
        help_text="determines how much referal bonus a use gets when a referral makes deposit on this plan")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_interest(self, amount):
        return (self.interest_rate/100) * amount

    @property
    def max_interest(self):
        return self.get_interest(float(self.max_cost))

    @property
    def duration_verbose(self):
        return "{} hours".format(self.duration * 24)

    @property
    def default_cost(self):
        if self.max_cost:
            return int((self.max_cost + self.min_cost) / 2)
        else:
            return int(self.min_cost)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Plan, self).save(*args, **kwargs)

    class Meta():
        ordering = ['min_cost']


class Currency(models.Model):

    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Investment(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='investment', on_delete=models.CASCADE)
    # amount for the plan
    amount = models.FloatField(default=0.00)
    plan = models.ForeignKey(Plan, related_name='plan_investment',
                             null=True, blank=True, on_delete=models.SET_NULL)
    plan_start = models.DateTimeField(null=True)
    plan_end = models.DateTimeField(null=True)

    # date created
    date = models.DateTimeField(auto_now_add=True)
    expected_earning = models.FloatField(
        default=0.00, blank=True)  # at the end of the plan
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    class Meta():
        ordering = ['-plan_start']

    def days_to_seconds(self, days):
        return days * 24 * 60 * 60

    def approve_investments(self):
        # checks the state of admin settings for approving
        # investments
        try:
            _setting = AdminSetting.objects.all()[0]
            return _setting.approve_investment
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expected_earning = self.plan.get_interest(self.amount)

            # check if admnin wants to be approving investmets generally or individually
            if not self.approve_investments():
                # check if individual
                if self.user.user_wallet.allow_automatic_investment:
                    self.plan_start = timezone.now()
                    self.plan_end = timezone.now() + timezone.timedelta(days=self.plan.duration)
            else:
                # dont start the plan, start on approval
                pass
            # deduct from balance for the plan
            self.user.user_wallet.debit(self.amount)

        super(Investment, self).save(*args, **kwargs)
    
    
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
        # when admin approves am investment
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
        # move to wallet
        self.user.user_wallet.credit(self.amount + self.expected_earning)
        self.user.user_wallet.save()
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
    allow_automatic_investment = models.BooleanField(default=True)

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
        active_investments = self.user.investment.filter(is_active=True)
        if active_investments:
            for inv in active_investments:
                investment_pnl = inv.current_earning % 24
                total_pnl += investment_pnl
        return round(total_pnl, 2)

    @property
    def total_past_earning(self):
        query = self.user.investment.filter(is_active=False)
        accumulated = query.aggregate(
            expected_earning=Sum("expected_earning")
        )['expected_earning'] or 0

        return accumulated

    @property
    def get_active_investment_balance(self):
        query = self.user.investment.filter(is_active=True)
        capitals = query.aggregate(
            investment_bal=Sum("amount")
        )['investment_bal'] or 0
        current_interests = 0
        for inv in query:
            current_interests += inv.current_earning
        return capitals + current_interests

    @property
    def get_pending_withdrawal_debits(self):
        return self.user.pending_withdrawal.filter(
            status="PENDING",
            balance_type="Main",

        ).aggregate(
            total_pending_debits=Sum("amount")
        )['total_pending_debits'] or 0.00

    @property
    def current_balance(self):
        return round(self.initial_balance + self.get_active_investment_balance + self.funded_earning - self.withdrawals, 2)

    @property
    def available_balance(self):
        return round(self.initial_balance + self.funded_earning - self.withdrawals - self.get_pending_withdrawal_debits, 2)

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
    t_choices = (('WITHDRAWAL', 'WITHDRAWAL'), ('DEPOSIT', 'DEPOSIT'), ("BONUS",
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



class WithdrawalApplication(models.Model):
    wallet_choices = (
        ("BTC", "BTC"),
        ("ETH", "ETH"),
        ("USDT", "USDT"),
        ("LTC", "LTC")
    )
    balance_type_choices = (('Referral', 'Referral'), ('Main', 'Main'))
    status_choices = (('PENDING', 'PENDING'), ('APPROVED',
                      'APPROVED'), ('DECLINED', 'DECLINED'))
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='pending_withdrawal')
    amount = models.FloatField()  # in $
    balance_type = models.CharField(
        max_length=10, choices=balance_type_choices)
    status = models.CharField(
        max_length=20, choices=status_choices, default='PENDING')
    amount_paid = models.FloatField(blank=True, null=True)
    is_received = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
        # payment wallet
    wallet_name = models.CharField(
        max_length=10, null=True, choices=wallet_choices)
    wallet_address = models.CharField(
        max_length=100, null=True, help_text="BEP20 address")


    def __str__(self):
        return self.user.nick_name

    def save(self, *args, **kwargs):
        # debit user balance
        
        super(WithdrawalApplication, self).save(*args, **kwargs)

    def on_approve(self):
        self.status = "APPROVED"

        if self.balance_type == "Referral":
            self.user.user_wallet.debit(self.amount, bal_type="referral")
        else:
            self.user.user_wallet.debit(self.amount)

        self.save()
