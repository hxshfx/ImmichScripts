"""
This script scans a library in Immich.
The script requires the following arguments:
--library-name: Name of the library to scan
--email: Email for authentication
--password: Password for authentication
--url: Base URL of the Immich instance
"""


## Imports
from argparse import ArgumentParser
import requests


## Configuration
parser = ArgumentParser(description="Scan a library in Immich")
parser.add_argument("--library-name", required=True, help="Name of the library to scan")
parser.add_argument("--email", required=True, help="Email for authentication")
parser.add_argument("--password", required=True, help="Password for authentication")
parser.add_argument("--url", required=True, help="Base URL of the Immich instance")
args = parser.parse_args()

library_name = args.library_name
immich_url = args.url
email = args.email
password = args.password


## Authenticate
auth_response = requests.post(f"{immich_url}/api/auth/login", json={"email": email, "password": password})
access_token = auth_response.json()['accessToken']
headers = {"Authorization": f"Bearer {access_token}"}
print("Successfully authenticated.")


## Find the library ID
libraries_response = requests.get(f"{immich_url}/api/libraries", headers=headers)
libraries = libraries_response.json()

library_id = None
for library in libraries:
    if library_name.lower() in library['name'].lower():
        library_id = library['id']
        break
    # END IF
# END FOR

if not library_id:
    print(f"No library found with the name '{library_name}'.")
    exit(1)
# END IF

print(f"Library found: {library_name} with ID {library_id}.")


## Scan the library
scan_response = requests.post(f"{immich_url}/api/libraries/{library_id}/scan", headers=headers)
if scan_response.status_code == 204:
    print(f"Job for library scan with ID {library_id} successfully sent.")
else:
    print(f"Error scanning the library with ID {library_id}. Status code: {scan_response.status_code}")
# END IF