"""Tests for eBay API integration."""
import os
import pytest
from ebay import get_app_token

def test_get_app_token_missing_env(monkeypatch):
    """Test that get_app_token raises error when credentials are missing."""
    monkeypatch.delenv("EBAY_CLIENT_ID", raising=False)
    monkeypatch.delenv("EBAY_CLIENT_SECRET", raising=False)
    with pytest.raises(KeyError):
        get_app_token()

def test_deep_link_format():
    """Test that deep link is formatted correctly."""
    from telegram import deep_link
    item_id = "123456789"
    expected = "ebay://com.ebay.mobile/ebay/link/?nav=item.view&id=123456789"
    assert deep_link(item_id) == expected 