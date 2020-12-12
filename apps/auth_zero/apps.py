from django.apps import AppConfig


class Auth0LoginConfig(AppConfig):
    name = "apps.auth_zero"
    label = "auth_zero"


class Singleton:
    __shared_state = {}

    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__shared_state


class Store(Singleton):
    __instance = None

    def __init__(self, *args, **cache):
        super().__init__(*args, **cache)
        self.args = args
        self.cache = cache

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance
