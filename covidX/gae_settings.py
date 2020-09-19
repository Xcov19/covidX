import os

from google.cloud import secretmanager


def access_secret_key_version():
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    if not os.getenv("GAE_APPLICATION"):
        return None

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    secret_id = os.getenv("SECRET_ID")

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    return response.payload.data.decode("UTF-8")
