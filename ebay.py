"""eBay API integration for finding Buy-It-Now listings with OAuth."""
import os
import time
import base64
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

token_cache = {"access_token": None, "expires_at": 0}

def get_app_token() -> str:
    """Obtain and cache an eBay OAuth app access token."""
    import time
    if token_cache["access_token"] and token_cache["expires_at"] > time.time():
        return token_cache["access_token"]
    cid = os.environ["EBAY_CLIENT_ID"]
    secret = os.environ["EBAY_CLIENT_SECRET"]
    auth = base64.b64encode(f"{cid}:{secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    r = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers, data=data, timeout=10
    )
    r.raise_for_status()
    resp = r.json()
    token_cache["access_token"] = resp["access_token"]
    token_cache["expires_at"] = time.time() + int(resp.get("expires_in", 7200)) - 60
    return token_cache["access_token"]

EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

def get_top_listing(
    term: str, max_price: float, blocked_words: List[str]
) -> Optional[Dict]:
    """
    Get the first matching Buy-It-Now listing that meets all criteria.

    Args:
        term: Search term for the listing
        max_price: Maximum price in USD
        blocked_words: List of words to filter out

    Returns:
        Dict containing listing details or None if no match found
    """
    token = get_app_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }
    params = {
        "q": term,
        "filter": f"buyingOptions:{{FIXED_PRICE}},price:{{0..{max_price}}}",
        "sort": "price",
        "limit": 50,
    }

    for attempt in range(3):
        try:
            response = requests.get(EBAY_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get("itemSummaries", []):
                title = item.get("title", "").lower()
                
                # Skip if any blocked word is in the title
                if any(word.lower() in title for word in blocked_words):
                    continue

                # Skip if no images
                if not item.get("image", {}).get("imageUrl"):
                    continue

                return {
                    "id": item["itemId"],
                    "title": item["title"],
                    "price": item["price"]["value"],
                    "image_url": item["image"]["imageUrl"],
                    "web_url": item["itemWebUrl"],
                }

            return None

        except requests.RequestException as e:
            if attempt == 2:  # Last attempt
                raise
            time.sleep(5 * (attempt + 1))  # Exponential backoff

    return None 