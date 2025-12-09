# tests/test_wordpress.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.wordpress_publisher import WordPressPublisher

def test_wordpress_publisher_initialization():
    """Test WordPress publisher initializes"""
    publisher = WordPressPublisher()
    assert publisher.wp_url is not None
    assert publisher.auth is not None

def test_wordpress_connection():
    """Test WordPress connection"""
    publisher = WordPressPublisher()
    result = publisher.test_connection()
    
    # This may fail if WordPress isn't configured
    assert 'success' in result