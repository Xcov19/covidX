import functools
import json
import operator
import random
import sys
from typing import Dict

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from jose import jwk as jose_jwk
from jose import jwt
from social_core.backends.auth0 import Auth0OAuth2

LOGGER = settings.LOGGER


class Auth0(Auth0OAuth2):
    """Auth0 OAuth authentication backend"""

    # REDIRECT_STATE = False
    EXTRA_DATA = [("picture", "picture"), ("email", "email")]

    @staticmethod
    def authorization_url():
        return f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/authorize"

    @staticmethod
    def access_token_url():
        return f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/oauth/token"

    @staticmethod
    def get_user_id(details, response):
        """Return current user id."""
        LOGGER.info(f"{response}")
        return details["user_id"]

    def get_user_details(self, response):
        """Obtain JWT and the keys to validate the signature."""
        id_token = response.get("id_token")
        jwks = requests.get(
            f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/.well-known/jwks.json"
        ).json()
        issuer = f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/"
        audience = settings.SOCIAL_AUTH_AUTH0_KEY  # CLIENT_ID
        payload = jwt.decode(
            id_token,
            jwks,
            algorithms=["RS256"],
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
        LOGGER.info(f"{response}")
        return response

    @staticmethod
    def process_roles(details, user, **kwargs):
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

    audience = settings.AUDIENCE
    # TODO(@codecakes): add scope later.
    # scope = settings.AUTH_SCOPE
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    client_secret = settings.SOCIAL_AUTH_AUTH0_SECRET
    # redirect_uri = settings.AUTH_REDIRECT_URI

    @staticmethod
    def authorization_url():
        """Request user's authorization and return an authorization code.

        The format is like:
            https://domain/authorize?
            response_type=code&
            client_id=client_id&
            redirect_uri=http://localhost:8090/redirect_uri/&
            scope=SCOPE&
            audience=API_AUDIENCE&
            state=STATE

        Returns:
            HTTP 302 response.
        """
        authorization_url = super().authorization_url()
        payload = {
            "response_type": "code",
            "client_id": Auth0CodeFlow.client_id,
            # "redirect_uri": Auth0CodeFlow.redirect_uri,
            # TODO(@codecakes): add scope later.
            # 'scope': Auth0CodeFlow.scope,
            "audience": Auth0CodeFlow.audience,
            "state": gen_state(),
        }
        return requests.get(authorization_url, data=payload)

    @staticmethod
    def access_token_url(**kwargs: Dict[str, str]):
        """Exchange your authorization code for tokens.
        Args:
            **kwargs: dict, keyword parameters like auth code.
        Returns:
            HTTP 200 response with a payload containing access_token,
            refresh_token, id_token, and token_type values.
        """
        access_token_url = super().access_token_url(**kwargs)
        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "authorization_code",
            "client_id": Auth0CodeFlow.client_id,
            "client_secret": Auth0CodeFlow.client_secret,
            # "redirect_uri": Auth0CodeFlow.redirect_uri,
            **kwargs,
        }
        return requests.post(access_token_url, data=payload, headers=headers)


def jwt_get_username_from_payload_handler(payload):
    """Authenticates from RemoteUserBackend and create remote django user."""
    username = payload.get("sub").replace("|", ".")
    authenticate(remote_user=username)
    return username


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
            token = get_token_auth_header(args[0])
            decoded = jwt_decode_token(token, **dict(verify_signature=False))
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
    jwks = requests.get("https://{}/.well-known/jwks.json".format(domain)).json()

    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            key_data = json.dumps(jwk)
            rsa_key_obj = jose_jwk.construct(key_data)
            public_key = rsa_key_obj.public_key()

    if public_key is None:
        raise Exception("Public key not found.")

    issuer = "https://{}/".format(domain)
    return jwt.decode(
        token,
        public_key,
        audience=audience,
        issuer=issuer,
        algorithms=["RS256"],
        options=options,
    )


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header."""
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def gen_state():
    """Create a random state token from first ten characters."""
    rand = random.Random()
    _, arr, _ = rand.getstate()
    arr_sum = functools.reduce(operator.add, arr)
    return arr_sum.to_bytes(arr_sum.bit_length(), sys.byteorder, signed=True).hex()[:10]
