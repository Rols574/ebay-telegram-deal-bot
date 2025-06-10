"""Telegram bot integration for sending deal alerts."""
import os
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TG_API_URL = f"https://api.telegram.org/bot{TG_BOT_TOKEN}"


def deep_link(item_id: str) -> str:
    """
    Generate an eBay deep link for the item.
    Opens directly in the eBay app if installed.
    """
    return f"ebay://com.ebay.mobile/ebay/link/?nav=item.view&id={item_id}"


def send_alert(
    title: str,
    price,                    # can arrive as str or float
    image_url: Optional[str],
    item_id: str,
    web_url: str,
) -> bool:
    """
    Send a deal alert to Telegram.

    Args:
        title:      Listing title
        price:      Listing price (string or float)
        image_url:  First picture URL (can be None/empty)
        item_id:    eBay item ID
        web_url:    Normal web URL fallback

    Returns:
        True if the message was accepted by Telegram, otherwise False.
    """
    if not TG_BOT_TOKEN or not CHAT_ID:
        raise ValueError("TG_BOT_TOKEN and CHAT_ID must be set as secrets")

    print(f"DEBUG: price before float conversion: {repr(price)}")

    try:
        price = float(price)
    except ValueError:
        print(f"ERROR: Could not convert price to float: {repr(price)}")
        raise

    caption = (
        f"🎯 *eBay Deal Alert*\n\n"
        f"*{title}*\n"
        f"💰 ${price:.2f}\n\n"
        f"[Open in eBay App]({deep_link(item_id)})\n"
        f"[View on Web]({web_url})"
    )

    payload = {
        "chat_id": CHAT_ID,
        "parse_mode": "Markdown",
    }

    try:
        if image_url:
            payload.update({"photo": image_url, "caption": caption})
            url = f"{TG_API_URL}/sendPhoto"
        else:
            payload.update({"text": caption})
            url = f"{TG_API_URL}/sendMessage"

        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True

    except requests.RequestException as e:
        print(f"Telegram API error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Telegram API response: {e.response.text}")
        return False
