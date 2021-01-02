from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from configparser import ConfigParser
from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True)
class Credentials:
    user: str
    password: str
    email: str


class CredentialsFactoryLoader:
    def __init__(self, config_file, credentials_class: TypeVar("Credentials") = None, loader_class=None):
        self.credentials_class = credentials_class
        self.loader_class = loader_class(config_file)

    def read_config_for_verification_status(self, verification_status: str) -> dict:
        return self.loader_class.read_config_for_verification_status(verification_status)


class ConfigFileLoader:
    def __init__(self, config_file: str):
        self.config = ConfigParser()
        self.config.read(config_file)

    def read_config_for_verification_status(self, verification_status: str) -> dict:
        config_settings_for_verification_type = self.config[verification_status]
        return dict(
            username=force_text(config_settings_for_verification_type["username"]),
            password=force_text(config_settings_for_verification_type["password"]),
            email=force_text(config_settings_for_verification_type["email"]),
            otp_verified=config_settings_for_verification_type.getboolean("otp_verified"),
            email_verified=config_settings_for_verification_type.getboolean("email_verified")
        )


class UserTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        config_file = "apps/auth_zero/config/test_config.ini"
        self.creds_obj = CredentialsFactoryLoader(config_file, Credentials, ConfigFileLoader)
        self.users = {
            verification_status: self.user_model.objects.create_user(**self.creds_obj.read_config_for_verification_status(verification_status))
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
