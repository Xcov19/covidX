import requests
from django.conf import settings
from jose import jwt
from social_core.backends.oauth import BaseOAuth2


class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""

    name = "auth0"
    SCOPE_SEPARATOR = " "
    ACCESS_TOKEN_METHOD = settings.SOCIAL_AUTH_ACCESS_TOKEN_METHOD
    REDIRECT_STATE = False
    EXTRA_DATA = [("picture", "picture"), ("email", "email")]

    def authorization_url(self):
        return f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/authorize"

    def access_token_url(self):
        return f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        print(response)
        return details["user_id"]

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        id_token = response.get("id_token")
        jwks = requests.get(
            f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/.well-known/jwks.json"
        )
        issuer = f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/"
        audience = settings.SOCIAL_AUTH_AUTH0_KEY  # CLIENT_ID
        payload = jwt.decode(
            id_token,
            jwks.content,
            algorithms=["RS256"],
            audience=audience,
            issuer=issuer,
        )
        return {
            "username": payload["nickname"],
            "first_name": payload["name"],
            "picture": payload["picture"],
            "user_id": payload["sub"],
            "email": payload["email"],
        }
