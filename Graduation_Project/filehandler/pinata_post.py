import requests
import os
from django.conf import settings

PINATA_API_KEY = settings.PINATA_API_KEY
PINATA_SECRET_API_KEY = settings.PINATA_SECRET_API_KEY
PINATA_BASE_URL = 'https://api.pinata.cloud/'

def upload_to_pinata(file_path):
    url = f"{PINATA_BASE_URL}pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
    }
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file),
        }
        try:
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            return response.json().get('IpfsHash')
        except requests.exceptions.RequestException as e:
            print(f"Error uploading to Pinata: {e}")
            return None


