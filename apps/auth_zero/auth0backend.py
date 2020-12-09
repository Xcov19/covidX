import functools
import json
import operator
import random
import sys
from typing import Dict
from typing import Union

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from jose import jwk as jose_jwk
from jose import jwt
from social_core.backends.auth0 import Auth0OAuth2

from apps.auth_zero.apps import Store

LOGGER = settings.LOGGER

CACHE_TOKEN = Store(**dict())


class Auth0(Auth0OAuth2):
    """Auth0 OAuth authentication backend"""

    REDIRECT_STATE = False
    EXTRA_DATA = [("picture", "picture"), ("email", "email")]

    def get_user_details(self, response):
        """Obtain JWT and the keys to validate the signature."""
        id_token = response.get("id_token")
        jwks = settings.AUTH0_JWKS
        issuer = settings.JWT_ISSUER
        audience = settings.SOCIAL_AUTH_AUTH0_KEY  # CLIENT_ID
        payload = jwt.decode(
            id_token,
            jwks,
            algorithms=settings.AUTH0_ALGORITHMS,
            audience=audience,
            issuer=issuer,
        )
        fullname, first_name, last_name = self.get_user_names(payload["name"])
        response = {
            "username": payload["nickname"],
            "fullname": fullname,
            "first_name": first_name,
            "last_name": last_name,
            "picture": payload["picture"],
            "user_id": payload["sub"],
            "email": payload["email"],
            "email_verified": payload.get("email_verified", False),
        }
        LOGGER.info(f"User login details: {response}")
        return response

    # TODO(codecakes): add auth0 roles rule
    @staticmethod
    def process_roles(details, user, _):
        """Make django aware of role set by Auth0 Rule."""
        if details["role"] == "admin":
            user.is_staff = True
            user.is_superuser = True
            user.save()


# TODO(codecakes): Implement after web flow successful run
class Auth0CodeFlow(Auth0):
    """Custom Web to Server Auth0 flow.

    See:
    https://auth0.com/docs/flows/call-your-api-using-the-authorization-code-flow
    #example-post-to-token-url

    """

    audience = settings.JWT_AUDIENCE
    scope = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    client_secret = settings.SOCIAL_AUTH_AUTH0_SECRET
    redirect_uri = settings.AUTH_REDIRECT_URI

    @staticmethod
    def jwt_get_username_from_payload_handler(payload) -> Union[None, str]:
        """Authenticates from RemoteUserBackend and create remote django user."""
        # pylint: disable=used-before-assignment
        if (subject := payload.get("sub")) and (username := subject.replace("|", ".")):
            authenticate(remote_user=username)
            return username
        return None

    @staticmethod
    def requires_scope(required_scope):
        """Determines if the required scope is present in the Access Token.

        Args:
            required_scope (str): The scope required to access the resource
        Returns:
            Function decorator.
        """

        def require_scope(f):
            @functools.wraps(f)
            def decorated(*args, **kwargs):
                token = Auth0CodeFlow.get_token_auth_header(args[0])
                decoded = Auth0CodeFlow.jwt_decode_token(
                    token, **dict(verify_signature=False)
                )
                if decoded.get("scope"):
                    token_scopes = decoded["scope"].split()
                    for token_scope in token_scopes:
                        if token_scope == required_scope:
                            return f(*args, **kwargs)
                response = JsonResponse(
                    {"message": "You don't have access to this resource"}
                )
                response.status_code = 403
                return response

            return decorated

        return require_scope

    @staticmethod
    def jwt_decode_token(token, **options):
        """Fetch JWKS from Auth0, verify and decode the incoming Access Token.

        Args:
            token: str, access token.
            **options: dict, jwt decode options.
        Returns:
            dict: The dict representation of the claims set, assuming the signature is valid
                and all requested data validation passes.
        Raises:
            JWTError: If the signature is invalid in any way.
            ExpiredSignatureError: If the signature has expired.
            JWTClaimsError: If any claim is invalid in any way.
        """
        audience = settings.JWT_AUDIENCE
        domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
        header = jwt.get_unverified_header(token)
        public_key = None
        key_data = None
        jwks = settings.AUTH0_JWKS

        for jwk in jwks["keys"]:
            if jwk["kid"] == header["kid"]:
                key_data = json.dumps(jwk)
                rsa_key_obj = jose_jwk.construct(key_data)
                public_key = rsa_key_obj.public_key()

        if public_key is None:
            raise Exception("Public key not found.")

        issuer = settings.JWT_ISSUER
        return jwt.decode(
            token,
            public_key,
            audience=audience,
            issuer=issuer,
            algorithms=settings.AUTH0_ALGORITHMS,
            options=options,
        )

    @staticmethod
    def get_token_auth_header(request) -> Union[None, str]:
        """Obtains the Access Token from the Authorization Header."""
        if auth := request.META.get("HTTP_AUTHORIZATION", None):
            parts = auth.split()
            token = parts[1]
            return token
        return None

    @staticmethod
    def gen_state():
        """Create a random state token from first ten characters."""
        rand = random.Random()
        _, arr, _ = rand.getstate()
        arr_sum = functools.reduce(operator.add, arr)
        return arr_sum.to_bytes(arr_sum.bit_length(), sys.byteorder, signed=True).hex()[
            :10
        ]
