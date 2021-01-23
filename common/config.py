from configparser import ConfigParser
from typing import TypeVar
from django.utils.encoding import force_text


class CredentialsLoader:
    """Loads credentials from config file using custom loader class"""

    def __init__(self, config_file: str, loader_class: TypeVar("ConfigFileLoader")):
        """Initialises custom loader class."""
        self.loader_class = loader_class(config_file)

    def read_config(self, verification_status: str) -> dict:
        return self.loader_class.read_config(verification_status)


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
