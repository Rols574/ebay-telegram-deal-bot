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
    Generate eBay deep link for the item.

    Args:
        item_id: eBay item ID

    Returns:
        Deep link URL that opens in the eBay app
    """
    return f"ebay://com.ebay.mobile/ebay/link/?nav=item.view&id={item_id}"

def send_alert(title: str, price: float, image_url: str, item_id: str, web_url: str) -> bool:
    """
    Send deal alert to Telegram.

    Args:
        title: Item title
        price: Item price
        image_url: URL of the first image
        item_id: eBay item ID
        web_url: Web URL of the listing

    Returns:
        True if message was sent successfully, False otherwise
    """
    if not all([TG_BOT_TOKEN, CHAT_ID]):
        raise ValueError("TG_BOT_TOKEN and CHAT_ID environment variables must be set")

    # Format message with deep link and web URL
    message = (
        f"🎯 *eBay Deal Alert*\n\n"
        f"*{title}*\n"
        f"💰 ${price:.2f}\n\n"
        f"[Open in eBay App]({deep_link(item_id)})\n"
        f"[View on Web]({web_url})"
    )

    try:
        # Try to send photo with caption
        if image_url:
            response = requests.post(
                f"{TG_API_URL}/sendPhoto",
                json={
                    "chat_id": CHAT_ID,
                    "photo": image_url,
                    "caption": message,
                    "parse_mode": "Markdown",
                },
            )
        else:
            # Fallback to text-only message
            response = requests.post(
                f"{TG_API_URL}/sendMessage",
                json={
                    "chat_id": CHAT_ID,
                    "text": message,
                    "parse_mode": "Markdown",
                },
            )

        response.raise_for_status()
        return True

    except requests.RequestException:
        return False 