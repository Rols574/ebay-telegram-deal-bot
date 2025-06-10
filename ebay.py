"""eBay API integration for finding Buy-It-Now listings."""
import os
import time
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
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
    if not EBAY_APP_ID:
        raise ValueError("EBAY_APP_ID environment variable not set")

    headers = {
        "Authorization": f"Bearer {EBAY_APP_ID}",
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