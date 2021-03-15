# Generated by Django 3.0.7 on 2020-12-27 15:14

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("auth_zero", "0003_auto_20201211_1219"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_otp",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="mobile",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="otp_verified",
            field=models.BooleanField(default=False),
        ),
    ]
