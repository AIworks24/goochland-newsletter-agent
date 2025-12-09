# tests/test_generation.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.newsletter_generator import NewsletterGenerator
from app.models import ContentType

@pytest.mark.asyncio
async def test_newsletter_generator_initialization():
    """Test generator initializes correctly"""
    generator = NewsletterGenerator()
    assert generator.client is not None

@pytest.mark.asyncio
async def test_generate_research_newsletter():
    """Test research-based newsletter generation"""
    generator = NewsletterGenerator()
    
    input_data = {
        'topic': 'Test Topic',
        'raw_content': 'Test research content about politics',
        'context': 'Test context'
    }
    
    result = await generator.generate_newsletter(
        content_type=ContentType.RESEARCH,
        input_data=input_data,
        word_count=500
    )
    
    assert result is not None
    assert result.title is not None
    assert result.body is not None