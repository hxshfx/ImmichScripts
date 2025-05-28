"""
This script assigns assets to albums in Immich
The script requires the following arguments:
--gallery-dir: Directory containing the gallery
--email: Email for authentication
--password: Password for authentication
--url: Base URL of the Immich instance
The script calculates the number of files in the gallery directory
Retrieves every already scanned asset data
Retrieves all existing albums
Iterates over each folder, creates albums if doesn't exist, and assigns assets
Identifies missing assets
"""


## Imports
from argparse import ArgumentParser
import math
import os
import requests
import subprocess


## Configuration
parser = ArgumentParser(description="Assign assets to albums in Immich")
parser.add_argument("--gallery-dir", required=True, help="Directory containing the gallery")
parser.add_argument("--email", required=True, help="Email for authentication")
parser.add_argument("--password", required=True, help="Password for authentication")
parser.add_argument("--url", required=True, help="Base URL of the Immich instance")
args = parser.parse_args()

gallery_dir = args.gallery_dir
immich_url = args.url
email = args.email
password = args.password


## Authenticate
auth_response = requests.post(f"{immich_url}/api/auth/login", json={"email": email, "password": password})
access_token = auth_response.json()['accessToken']
headers = {"Authorization": f"Bearer {access_token}"}
print("Successfully authenticated.")


## Calculate the number of files in the gallery directory
result = subprocess.run(['find', gallery_dir, '-type', 'f'], stdout=subprocess.PIPE)
file_count = len(result.stdout.decode().splitlines())

# Round up to the nearest hundred
asset_count = math.ceil(file_count / 100.0) * 100
print(f"Found {file_count} (aprox {asset_count}) files in the gallery directory")


## Retrieve every already scanned asset data
asset_response = requests.get(f"{immich_url}/api/assets/random?count={asset_count}", headers=headers)
assets = asset_response.json()
print(f"Retrieved {len(assets)} assets from Immich.")


## Initialize variables to keep track of assets and those being added or found
added_assets = set()
total_assets_added = 0
total_assets_overall = 0


## Retrieve all existing albums
albums_response = requests.get(f"{immich_url}/api/albums", headers=headers)
albums = albums_response.json()
print(f"Retrieved {len(albums)} albums from Immich.")

# Create dictionaries to quickly lookup albums and assets
album_lookup = {album['albumName']: album['id'] for album in albums if album['id'] is not None}
asset_lookup = {asset['originalFileName']: asset['id'] for asset in assets if asset['id'] is not None}


## Iterate over each folder, create albums if doesn't exist, and assign assets
for folder_name in os.listdir(gallery_dir):
    folder_path = os.path.join(gallery_dir, folder_name)
    if os.path.isdir(folder_path) and not folder_name.startswith('.'):


        ## Check if the album already exists, create otherwise
        if folder_name in album_lookup:
            album_id = album_lookup[folder_name]
            print(f"Album '{folder_name}' already exists with ID: {album_id}")
        else:
            album_response = requests.post(f"{immich_url}/api/albums", headers=headers, json={"albumName": folder_name})
            album_id = album_response.json()['id']
        # END IF


        ## Assign assets to the album
        asset_ids = []
        for file_name in os.listdir(folder_path):
            if file_name in asset_lookup and not file_name.endswith('.db'):
                asset_id = asset_lookup[file_name]
                asset_ids.append(asset_id)
                added_assets.add(asset_id)
            # END IF
        # END FOR


        ## Retrieve existing assets in the album and filter those assets that are not already in the album
        existing_assets_response = requests.get(f"{immich_url}/api/albums/{album_id}", headers=headers)
        existing_assets = existing_assets_response.json().get('assets', [])
        existing_asset_ids = {asset['id'] for asset in existing_assets}
        new_asset_ids = [asset_id for asset_id in asset_ids if asset_id not in existing_asset_ids]


        ## Add new assets to the album
        if new_asset_ids:
            requests.put(f"{immich_url}/api/albums/{album_id}/assets", headers=headers, json={"ids": new_asset_ids})
            print(f"{len(new_asset_ids)} assets assignated to album '{folder_name}'.")
            
            # Increment the total assets counter
            total_assets_added += len(new_asset_ids)
        else:
            print(f"Album '{folder_name}' already contains all existing assets.")
        # END IF

        total_assets_overall += len(asset_ids)
    # END IF
# END FOR


## Print the total number of assets added to all albums
print(f"Total assets added across all albums: {total_assets_added}")
print(f"Total assets overall: {total_assets_overall}")


## Identify missing assets
all_asset_ids = set(asset_lookup.values())
missing_assets = all_asset_ids - added_assets

# Print the missing assets
print(f"Missing assets ({len(missing_assets)}):")
missing_asset_names = [name for name, id in asset_lookup.items() if id in missing_assets]
for asset_name in missing_asset_names:
    print(f"- Name: {asset_name}")
# END FOR