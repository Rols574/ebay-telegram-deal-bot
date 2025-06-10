"""Tests for eBay API integration."""
import pytest
from ebay import get_top_listing

def test_get_top_listing_missing_app_id():
    """Test that get_top_listing raises error when EBAY_APP_ID is not set."""
    with pytest.raises(ValueError, match="EBAY_APP_ID environment variable not set"):
        get_top_listing("test", 100.0, ["broken"])

def test_deep_link_format():
    """Test that deep link is formatted correctly."""
    from telegram import deep_link
    item_id = "123456789"
    expected = "ebay://com.ebay.mobile/ebay/link/?nav=item.view&id=123456789"
    assert deep_link(item_id) == expected 