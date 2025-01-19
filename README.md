# Immich Scripts

This project contains two Python scripts designed to interact with the Immich platform. These scripts help manage albums and assets within Immich.

## Scripts

### 1. `asset_assigner.py`

This script assigns assets to albums in Immich based on the directory structure of a specified gallery directory.

#### Usage

```sh
python asset_assigner.py --gallery-dir <gallery-directory> --email <your-email> --password <your-password> --url <immich-url>
```

#### Arguments

- `--gallery-dir`: Directory containing the gallery
- `--email`: Email for authentication
- `--password`: Password for authentication
- `--url`: Base URL of the Immich instance

### 2. `delete_empty.py`

This script deletes empty albums from Immich.

#### Usage

```sh
python delete_empty.py --email <your-email> --password <your-password> --url <immich-url>
```

#### Arguments

- `--email`: Email for authentication
- `--password`: Password for authentication
- `--url`: Base URL of the Immich instance

## Configuration

Both scripts require authentication to interact with the Immich API. Ensure you provide the correct email, password, and URL when running the scripts.
