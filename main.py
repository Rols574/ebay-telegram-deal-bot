"""Main script for eBay deal-to-Telegram bot."""
import tomli
from ebay import get_top_listing
from telegram import send_alert
import requests

def load_config() -> dict:
    """Load configuration from config.toml."""
    with open("config.toml", "rb") as f:
        return tomli.load(f)

def main():
    """Find a deal and send it to Telegram."""
    try:
        # Load configuration
        config = load_config()
        
        # Get top matching listing
        listing = get_top_listing(
            term=config["search_term"],
            max_price=config["max_price"],
            blocked_words=config["blocked_words"],
        )

        if not listing:
            print("No matching listings found today")
            return

        # Send alert to Telegram
        price = float(listing["price"])
        success = send_alert(
            title=listing["title"],
            price=price,
            image_url=listing["image_url"],
            item_id=listing["id"],
            web_url=listing["web_url"],
        )

        print(f"send_alert returned: {success}")

        if not success:
            print("Failed to send Telegram alert")
            return

        print("Deal alert sent successfully!")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
