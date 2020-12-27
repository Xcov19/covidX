from django.test import TestCase
from apps.auth_zero.models import User
import logging

class UserTestCase(TestCase):
    def setUp(self):
        pass

    def test_unverified_users(self):
        # unverified_user = User.objects.create_user("username", email="example@mail.com", password="password")
        unverified_user = User.objects.create(otp_verified=False, email_verified=False)
        self.assertFalse(unverified_user.is_verified)
    
    def test_partially_verfied_users(self):
        only_otp_verified_user = User.objects.create(otp_verified=True, email_verified=False)
        self.assertFalse(only_otp_verified_user.is_verified)
        
        only_email_verified_user = User.objects.create(otp_verified=False, email_verified=True)
        self.assertFalse(only_email_verified_user.is_verified)
    
    def test_verified_users(self):
        verified_user = User.objects.create(otp_verified=True, email_verified=True)
        self.assertTrue(unverified_user.is_verified)