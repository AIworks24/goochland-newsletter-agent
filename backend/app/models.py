# backend/app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    RESEARCH = "research"
    MINUTES = "minutes"
    HYBRID = "hybrid"
    EVENT_BASED = "event_based"

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="Main topic for research")
    context: Optional[str] = Field(None, description="Additional context")
    sources: Optional[List[str]] = Field(default=[], description="Specific source URLs")
    word_count: Optional[int] = Field(800, description="Target word count")

class MinutesRequest(BaseModel):
    additional_context: Optional[str] = Field(None, description="Additional context for minutes")
    highlight_items: Optional[List[str]] = Field(default=[], description="Specific items to highlight")

class HybridRequest(BaseModel):
    research_topic: str
    research_context: Optional[str] = None
    minutes_context: Optional[str] = None
    integration_style: str = "balanced"  # balanced, research_heavy, minutes_heavy

class NewsletterContent(BaseModel):
    title: str
    subtitle: Optional[str] = None
    body: str  # HTML formatted
    excerpt: str
    suggested_images: List[str]
    sources: List[Dict[str, str]]
    tags: List[str]
    category: str
    metadata: Dict[str, Any] = {}

class GenerationResponse(BaseModel):
    success: bool
    newsletter_id: Optional[str] = None
    wordpress_post_id: Optional[int] = None
    edit_url: Optional[str] = None
    preview_url: Optional[str] = None
    content: Optional[NewsletterContent] = None
    error: Optional[str] = None
    generation_time: float
    created_at: datetime = Field(default_factory=datetime.now)

class WordPressPost(BaseModel):
    title: str
    content: str
    excerpt: str
    status: str = "draft"
    post_type: str = "post"
    categories: List[int] = []
    tags: List[int] = []
    featured_media: Optional[int] = None
    meta: Dict[str, Any] = {}