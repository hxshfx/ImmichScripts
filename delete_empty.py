"""
This script deletes empty albums from Immich
The script requires the following arguments:
--email: Email for authentication
--password: Password for authentication
--url: Base URL of the Immich instance
The script retrieves all album IDs
Checks and deletes only empty albums
"""


## Imports
from argparse import ArgumentParser
import requests


## Configuration
parser = ArgumentParser(description="Delete empty albums from Immich")
parser.add_argument("--email", required=True, help="Email for authentication")
parser.add_argument("--password", required=True, help="Password for authentication")
parser.add_argument("--url", required=True, help="Base URL of the Immich instance")
args = parser.parse_args()

immich_url = args.url
email = args.email
password = args.password


## Authenticate
auth_response = requests.post(f"{immich_url}/api/auth/login", json={"email": email, "password": password})
access_token = auth_response.json()['accessToken']
headers = {"Authorization": f"Bearer {access_token}"}


## Retrieve all album IDs
albums_response = requests.get(f"{immich_url}/api/albums", headers=headers)
albums = albums_response.json()


## Check and delete only empty albums
for album in albums:
    album_id = album['id']
    album_details_response = requests.get(f"{immich_url}/api/albums/{album_id}", headers=headers)
    album_details = album_details_response.json()
    
    if album_details['assetCount'] == 0:
        delete_response = requests.delete(f"{immich_url}/api/albums/{album_id}", headers=headers)
        if delete_response.status_code == 200:
            print(f"Successfully deleted empty album with ID: {album_id}")
        else:
            print(f"Failed to delete empty album with ID: {album_id}, Status Code: {delete_response.status_code}")
    else:
        print(f"Album with ID: {album_id} is not empty, skipping deletion.")
    # END IF
# END FOR

print("All albums have been processed.")