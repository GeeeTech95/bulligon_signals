# Generated by Django 4.2.13 on 2024-07-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_kyc_face_capture_kyc_id_upload_kyc_proof_of_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kyc',
            name='is_verified',
        ),
        migrations.AddField(
            model_name='kyc',
            name='status',
            field=models.CharField(choices=[('created', 'created'), ('processing', 'processing'), ('approved', 'approved'), ('denied', 'denied')], default='created', max_length=10),
        ),
    ]