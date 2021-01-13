from django.utils.encoding import force_text
from configparser import ConfigParser
from dataclasses import dataclass
from typing import TypeVar
from io import BytesIO

@dataclass(frozen=True)
class Credentials:
    user: str
    password: str
    email: str


class CredentialsFactoryLoader:
    def __init__(self, config_file, credentials_class: TypeVar("Credentials") = None, loader_class=None):
        self.credentials_class = credentials_class
        self.loader_class = loader_class(config_file)

    def read_config(self, verification_status: str) -> dict:
        return self.loader_class.read_config(verification_status)


class ConfigByteLoader():
    def __init__(self, config_file: str):
        with open(config_file, "rb") as f:
            self.byte_stream = BytesIO(f.read())

    def read_config(self, verification_status: str) -> dict:
        # config_settings_for_verification_status = not sure how to do
        return dict(
            username=force_text(config_settings_for_verification_status["username"]),
            password=force_text(config_settings_for_verification_status["password"]),
            email=force_text(config_settings_for_verification_status["email"]),
            otp_verified=config_settings_for_verification_status.getboolean("otp_verified"),
            email_verified=config_settings_for_verification_status.getboolean("email_verified")
        )
        

class ConfigFileLoader:
    def __init__(self, config_file: str):
        self.config = ConfigParser()
        self.config.read(config_file)

    def read_config(self, verification_status: str) -> dict:
        config_settings_for_verification_status = self.config[verification_status]
        return dict(
            username=force_text(config_settings_for_verification_status["username"]),
            password=force_text(config_settings_for_verification_status["password"]),
            email=force_text(config_settings_for_verification_status["email"]),
            otp_verified=config_settings_for_verification_status.getboolean("otp_verified"),
            email_verified=config_settings_for_verification_status.getboolean("email_verified")
        )
