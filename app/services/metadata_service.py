from app.utils.metadata_utils import fetch_url_metadata


def fetch_metadata_logic(url: str) -> dict:
    # You can add more business logic here if needed
    return fetch_url_metadata(url)
