import abc
from configparser import ConfigParser
from typing import TypeVar

from django.utils.encoding import force_text


class InterfaceConfigLoader(metaclass=abc.ABCMeta):
    """Enforce abstract interface for class capability."""

    impl_methods = ("read_config",)

    @classmethod
    def __subclasshook__(cls, subclass: object):
        """A subclass hooks to methods in impl_methods or NotImplemented."""
        return all(map(cls.get_implementation, cls.impl_methods)) or NotImplemented

    @staticmethod
    def get_implementation(subclass, attr_name: str) -> bool:
        """Fetch an implemented method."""
        return hasattr(subclass, attr_name)

    @abc.abstractmethod
    def read_config(self, verification_status: str) -> dict:
        raise NotImplementedError


IConfigLoader_T = TypeVar("IConfigLoader_T", bound=InterfaceConfigLoader)


class CredentialsLoader:
    """Loads credentials from config file using custom loader class"""

    def __init__(
        self, config_file: str, loader_class: TypeVar("ConfigFileLoader")
    ) -> IConfigLoader_T:
        """Initialises custom loader class."""
        self.__loader_class = loader_class(config_file)

    @property
    def loader_class(self):
        return self.__loader_class


class ConfigFileLoader(InterfaceConfigLoader):
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
