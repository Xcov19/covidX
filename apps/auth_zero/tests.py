from django.test import TestCase
from django.contrib.auth import get_user_model
from configparser import ConfigParser


class UserTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.confg = ConfigParser()
        self.confg.read("apps/auth_zero/config/test_config.ini")
        self.users = {
            verification_status: self.user_model.objects.create_user(**dict(self.confg[verification_status]))
            for verification_status in self.confg.sections()
        }

    def test_fully_unverified_user(self):
        self.assertFalse(self.users["fully_unverified"].is_verified)

    def test_partially_verfied_users(self):
        self.assertFalse(self.users["only_otp_verified"].is_verified)
        self.assertFalse(self.users["only_email_verified"].is_verified)

    def test_fully_verified_user(self):
        self.assertTrue(self.users["fully_verified"].is_verified)
