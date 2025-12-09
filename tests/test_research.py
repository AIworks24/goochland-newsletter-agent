# tests/test_research.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.research_engine import ResearchEngine
from app.config import settings

@pytest.mark.asyncio
async def test_research_engine_initialization():
    """Test that research engine initializes correctly"""
    engine = ResearchEngine()
    assert engine.client is not None

@pytest.mark.asyncio
async def test_research_topic():
    """Test basic research functionality"""
    engine = ResearchEngine()
    
    # Simple test query
    result = await engine.research_topic(
        topic="Test topic",
        context="Test context"
    )
    
    assert result is not None
    assert 'raw_content' in result
    assert isinstance(result, dict)

@pytest.mark.asyncio
async def test_research_with_sources():
    """Test research with specific sources"""
    engine = ResearchEngine()
    
    result = await engine.research_topic(
        topic="Virginia politics",
        sources=["https://virginia.gov"]
    )
    
    assert result is not None
    assert 'citations' in result