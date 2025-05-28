# Immich Scripts

This project contains three Python scripts designed to interact with the Immich platform. These scripts help manage albums and assets within Immich.

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

### 3. `library_scanner.py`

This script scans a library in Immich.

#### Usage

```sh
python library_scanner.py --library-name <library-name> --email <your-email> --password <your-password> --url <immich-url>
```

#### Arguments

- `--library-name`: Name of the library to scan
- `--email`: Email for authentication
- `--password`: Password for authentication
- `--url`: Base URL of the Immich instance

## Configuration

All scripts require authentication to interact with the Immich API. Ensure you provide the correct email, password, and URL when running the scripts.
