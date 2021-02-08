from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.common.config import ConfigFileLoader, CredentialsLoader


class UserTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        config_file = "apps/auth_zero/config/test_config.ini"
        self.creds_obj = CredentialsLoader(config_file, ConfigFileLoader)
        self.users = {
            verification_status: self.user_model.objects.create_user(
                **self.creds_obj.read_config(verification_status)
            )
            for verification_status in [
                "fully_unverified",
                "only_otp_verified",
                "only_email_verified",
                "fully_verified",
            ]
        }

    def test_fully_unverified_user(self):
        self.assertFalse(self.users["fully_unverified"].is_verified)

    def test_partially_verfied_users(self):
        self.assertFalse(self.users["only_otp_verified"].is_verified)
        self.assertFalse(self.users["only_email_verified"].is_verified)

    def test_fully_verified_user(self):
        self.assertTrue(self.users["fully_verified"].is_verified)
