import functools
import json

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from jose import jwk as jose_jwk
from jose import jwt
from social_core.backends.oauth import BaseOAuth2

LOGGER = settings.LOGGER


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
        LOGGER.info(f"{response}")
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
