# Generated by Django 4.2.13 on 2024-07-15 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0017_alter_transaction_coin'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawalapplication',
            name='wallet_address',
            field=models.CharField(help_text='BEP20 address', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='withdrawalapplication',
            name='wallet_name',
            field=models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('USDT', 'USDT'), ('LTC', 'LTC')], max_length=10, null=True),
        ),
    ]