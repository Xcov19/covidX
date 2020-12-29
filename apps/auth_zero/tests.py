from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_unverified_user(self):
        unverified_user = self.user_model.objects.create_user(
            username="unverifiedUser",
            email="unverifiedUser@mail.com",
            password="unverifiedUserPassword")
        self.assertFalse(unverified_user.otp_verified)
        self.assertFalse(unverified_user.email_verified)
        self.assertFalse(unverified_user.is_verified)
