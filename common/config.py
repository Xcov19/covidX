from configparser import ConfigParser
from dataclasses import dataclass
from typing import TypeVar
from io import BytesIO
from django.utils.encoding import force_text


@dataclass(frozen=True)
class Credentials:
    user: str
    password: str
    email: str


class CredentialsLoader:
    """Loads credentials from config file using custom credentials and loader classes"""

    def __init__(
        self,
        config_file,
        credentials_class: TypeVar("Credentials") = None,
        loader_class=None,
    ):
        """Initialises custom credentials and loader classes."""
        self.credentials_class = credentials_class
        self.loader_class = loader_class(config_file)

    def read_config(self, verification_status: str) -> dict:
        return self.loader_class.read_config(verification_status)


class ConfigByteLoader:
    """Loads data from byte stream input"""

    def __init__(self, config_file: str):
        """Reads byte stream input as binary file."""
        with open(config_file, "rb") as f:
            self.byte_stream = BytesIO(f.read())

    def read_config(self, verification_status: str) -> dict:
        pass
        # config_settings = not sure how to do
        # return dict(
        #     username=force_text(config_settings["username"]),
        #     password=force_text(config_settings["password"]),
        #     email=force_text(config_settings["email"]),
        #     otp_verified=config_settings.getboolean("otp_verified"),
        #     email_verified=config_settings.getboolean("email_verified")
        # )


class ConfigFileLoader:
    """Loads data from .ini file"""

    def __init__(self, config_file: str):
        """Initialises ConfigParser instance and reads inputted config file."""
        self.config = ConfigParser()
        self.config.read(config_file)

    def read_config(self, verification_status: str) -> dict:
        config_settings = self.config[verification_status]
        return dict(
            username=force_text(config_settings["username"]),
            password=force_text(config_settings["password"]),
            email=force_text(config_settings["email"]),
            otp_verified=config_settings.getboolean("otp_verified"),
            email_verified=config_settings.getboolean("email_verified"),
        )
