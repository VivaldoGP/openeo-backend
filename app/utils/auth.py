import openeo
from dotenv import load_dotenv
import os


def get_connection():
    load_dotenv()
    user = os.getenv("Client_ID")
    password = os.getenv("Client_secret")
    connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
    conn = connection.authenticate_oidc_client_credentials(
        client_id=user,
        client_secret=password
    )

    return conn
