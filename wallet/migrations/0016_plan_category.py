# Generated by Django 4.2.13 on 2024-06-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0015_auto_20220526_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='category',
            field=models.CharField(choices=[('promo', 'promo'), ('regular', 'regular'), ('vip', 'vip')], default='', max_length=40),
            preserve_default=False,
        ),
    ]