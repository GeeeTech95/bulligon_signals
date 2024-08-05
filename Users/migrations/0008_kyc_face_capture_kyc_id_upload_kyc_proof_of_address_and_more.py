# Generated by Django 4.2.13 on 2024-07-12 12:47

import Users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_delete_dashboard_rename_otp_security_otc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='face_capture',
            field=models.FileField(default='', upload_to=Users.models.KYC.get_kyc_upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kyc',
            name='id_upload',
            field=models.FileField(default='', upload_to=Users.models.KYC.get_kyc_upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kyc',
            name='proof_of_address',
            field=models.FileField(default='', upload_to=Users.models.KYC.get_kyc_upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kyc',
            name='proof_of_address_type',
            field=models.CharField(choices=[('Utility Bill', 'Utility Bill'), ('Bank Statement', 'Bank Statement')], default='', max_length=20),
            preserve_default=False,
        ),
    ]
