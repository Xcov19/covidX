from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_fully_unverified_user(self):
        fully_unverified_user = self.user_model.objects.create_user(
            username="fullyUnverifiedUser",
            email="fullyUnverifiedUser@mail.com",
            password="fullyUnverifiedUserPassword")
        fully_unverified_user.save()
        self.assertFalse(fully_unverified_user.otp_verified)
        self.assertFalse(fully_unverified_user.email_verified)
        self.assertFalse(fully_unverified_user.is_verified)

    def test_partially_verfied_users(self):
        only_otp_verified_user = self.user_model.objects.create_user(
            username="onlyOTPVerifiedUser",
            email="onlyOTPVerifiedUser@mail.com",
            password="onlyOTPVerifiedUserPassword",
            otp_verified=True
        )
        only_otp_verified_user.save()
        self.assertTrue(only_otp_verified_user.otp_verified)
        self.assertFalse(only_otp_verified_user.email_verified)
        self.assertFalse(only_otp_verified_user.is_verified)

        only_email_verified_user = self.user_model.objects.create_user(
            username="onlyEmailVerifiedUser",
            email="onlyEmailVerifiedUser@mail.com",
            password="onlyEmailVerifiedUserPassword",
            email_verified=True
        )
        only_email_verified_user.save()
        self.assertFalse(only_email_verified_user.otp_verified)
        self.assertTrue(only_email_verified_user.email_verified)
        self.assertFalse(only_email_verified_user.is_verified)

    def test_fully_verified_user(self):
        fully_verified_user = self.user_model.objects.create_user(
            username="fullyVerifiedUser",
            email="fullyVerifiedUser@mail.com",
            password="fullyVerifiedUserPassword",
            otp_verified=True,
            email_verified=True
        )
        fully_verified_user.save()
        self.assertTrue(fully_verified_user.otp_verified)
        self.assertTrue(fully_verified_user.email_verified)
        self.assertTrue(fully_verified_user.is_verified)
