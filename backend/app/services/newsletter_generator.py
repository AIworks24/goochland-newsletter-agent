# backend/app/services/newsletter_generator.py
# Correct fix for Anthropic SDK
from anthropic import Anthropic
from typing import Dict, Optional
import json
from ..config import settings
from ..models import ContentType, NewsletterContent
import yaml

class NewsletterGenerator:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.style_guidelines = self._load_style_guidelines()
        
    def _load_style_guidelines(self) -> str:
        """Load style guidelines from config"""
        try:
            with open('config/newsletter_config.yaml', 'r') as f:
                config = yaml.safe_load(f)
                return config.get('style', {}).get('guidelines', '')
        except:
            return """
            - Use clear, accessible language
            - Maintain factual accuracy with citations
            - Represent conservative values authentically
            - Avoid inflammatory or divisive language
            - Focus on local Goochland impact
            - Include calls-to-action when appropriate
            """
    
    async def generate_newsletter(
        self,
        content_type: ContentType,
        input_data: Dict,
        word_count: int = 800
    ) -> NewsletterContent:
        """Generate newsletter content based on input type"""
        
        if content_type == ContentType.RESEARCH:
            prompt = self._build_research_prompt(input_data, word_count)
        elif content_type == ContentType.MINUTES:
            prompt = self._build_minutes_prompt(input_data, word_count)
        elif content_type == ContentType.HYBRID:
            prompt = self._build_hybrid_prompt(input_data, word_count)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        # Generate newsletter
        message = self.client.messages.create(
            model=settings.default_model,
            max_tokens=settings.max_tokens,
            system=self._build_system_prompt(),
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # CORRECT FIX: Extract text properly
        response_text = ""
        for block in message.content:
            if block.type == "text":
                response_text += block.text
        
        # Parse response
        newsletter_data = self._parse_newsletter_response(response_text)
        
        return NewsletterContent(**newsletter_data)
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for newsletter generation"""
        return f"""You are a professional newsletter writer for the Goochland County Republican Committee (GCRC).

STYLE GUIDELINES:
{self.style_guidelines}

OUTPUT FORMAT:
You must respond with valid JSON in exactly this structure:
{{
    "title": "Compelling headline (60-80 characters)",
    "subtitle": "Optional subtitle providing context",
    "body": "Full article in HTML format with proper tags (<p>, <h2>, <h3>, <strong>, <em>, <ul>, <ol>, <a>)",
    "excerpt": "2-3 sentence summary (150-200 characters)",
    "suggested_images": ["Description 1", "Description 2"],
    "sources": [
        {{"title": "Source Name or Organization", "url": "", "accessed": ""}}
    ],
    "tags": ["tag1", "tag2", "tag3"],
    "category": "Newsletter|Events|Policy|Community"
}}

CONTENT REQUIREMENTS:
- Lead with the most newsworthy information
- Use AP style for formatting
- Include specific data and facts WITH SOURCE ATTRIBUTION IN THE TEXT
- Write at an 8th-10th grade reading level
- Include a clear call-to-action
- Make local connections explicit
- Suggest 2-3 relevant, professional images

IN THE BODY TEXT:
- When stating facts, include attribution: "According to the Heritage Foundation, ..."
- For statistics: "The U.S. Census Bureau reports that..."
- For policies: "The Virginia Department of Education announced..."

TONE:
Professional, informative, engaging, and respectful. Represent conservative values authentically while remaining inclusive to all Goochland residents."""

    def _build_research_prompt(self, data: Dict, word_count: int) -> str:
        """Build prompt for research-based newsletter"""
        
        research_findings = data.get('raw_content', '')
        topic = data.get('topic', 'Recent Developments')
        context = data.get('context', '')
        
        return f"""Create a newsletter article based on this research:

TOPIC: {topic}

RESEARCH FINDINGS:
{research_findings[:10000]}

ADDITIONAL CONTEXT:
{context}

TARGET LENGTH: {word_count} words

Create a compelling newsletter article that:
1. Opens with a strong hook relevant to Goochland residents
2. Explains the issue clearly and concisely
3. Provides specific examples and data WITH SOURCE CITATIONS in the text
4. Analyzes local impact and implications
5. Includes conservative perspective and values
6. Ends with a call-to-action (join, learn more, contact representatives, etc.)
7. CRITICAL: Includes 3-5 sources in the "sources" array based on organizations/publications mentioned in the research

IMPORTANT: In the body text, cite sources naturally:
- "According to [Source], ..."
- "The [Organization] reports that..."
- "[Government Agency] data shows..."

Then list those same sources in the "sources" array.

Remember to output valid JSON as specified in your system prompt."""

    def _build_minutes_prompt(self, data: Dict, word_count: int) -> str:
        """Build prompt for minutes-based newsletter"""
        
        structured_data = data.get('structured_data', {})
        
        return f"""Create a newsletter article from these meeting minutes:

MEETING INFORMATION:
{json.dumps(structured_data, indent=2)}

TARGET LENGTH: {word_count} words

Transform these meeting minutes into an engaging newsletter that:
1. Highlights the most significant decisions and their importance
2. Explains action items and how they benefit the community
3. Previews upcoming events in an exciting way
4. Recognizes key contributors and volunteers
5. Makes dry information engaging and relevant
6. Includes a call-to-action (attend next meeting, volunteer, etc.)
7. Lists "Goochland County Republican Committee" as a source in the sources array

Use a narrative style that makes readers feel connected to the committee's work.

Remember to output valid JSON as specified in your system prompt."""

    def _build_hybrid_prompt(self, data: Dict, word_count: int) -> str:
        """Build prompt for hybrid newsletter"""
        
        meeting_data = data.get('meeting_data', {})
        research_data = data.get('research_data', {})
        
        return f"""Create a comprehensive newsletter article combining meeting updates with topical research:

MEETING SUMMARY:
{json.dumps(meeting_data, indent=2)}

RESEARCH TOPIC & FINDINGS:
{research_data.get('raw_content', '')[:8000]}

TARGET LENGTH: {word_count} words

Create a cohesive article that:
1. Integrates meeting highlights with broader context
2. Shows how local actions connect to larger issues
3. Balances internal updates with external relevance
4. Maintains narrative flow between sections
5. Provides clear value to readers
6. Includes multiple calls-to-action
7. Lists both "Goochland County Republican Committee" AND research sources (3-5 total)

Remember to output valid JSON as specified in your system prompt."""

    def _parse_newsletter_response(self, response_text: str) -> Dict:
        """Parse Claude's response and extract newsletter data"""
        
        import re
        
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                newsletter_data = json.loads(json_match.group())
            else:
                newsletter_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            newsletter_data = {
                "title": "Newsletter Article",
                "body": f"<p>{response_text}</p>",
                "excerpt": response_text[:200],
                "suggested_images": ["Newsletter header image"],
                "sources": [],
                "tags": ["Newsletter"],
                "category": "Newsletter"
            }
        
        if "sources" not in newsletter_data:
            newsletter_data["sources"] = []
        
        return newsletter_data