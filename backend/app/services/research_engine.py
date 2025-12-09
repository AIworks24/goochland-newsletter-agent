# backend/app/services/research_engine.py
from anthropic import Anthropic
from typing import List, Dict, Optional
import json
from ..config import settings

class ResearchEngine:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        
    async def research_topic(
        self, 
        topic: str, 
        context: Optional[str] = None,
        sources: Optional[List[str]] = None
    ) -> Dict:
        """
        Research a topic using Claude
        """
        
        # Build research prompt
        prompt = self._build_research_prompt(topic, context, sources)
        
        # Call Claude WITHOUT web search for now (simpler)
        message = self.client.messages.create(
            model=settings.default_model,
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Process response
        research_data = await self._process_research_response(message)
        
        return research_data
    
    def _build_research_prompt(
        self, 
        topic: str, 
        context: Optional[str], 
        sources: Optional[List[str]]
    ) -> str:
        """Build comprehensive research prompt"""
        
        prompt = f"""Research and provide comprehensive information on the following topic for a Republican political newsletter targeting Goochland County, Virginia constituents:

TOPIC: {topic}
"""
        
        if context:
            prompt += f"\nADDITIONAL CONTEXT: {context}"
        
        if sources and len(sources) > 0:
            prompt += f"\nPRIORITY SOURCES TO REFERENCE: {', '.join(sources)}"
        
        prompt += """

Please provide:
1. Recent factual developments and news on this topic
2. Relevant legislation, policy updates, or government actions
3. Local Virginia/Goochland implications
4. Conservative perspective and analysis
5. Supporting statistics and data (use your training knowledge)
6. Key stakeholders and their positions

Format your response as a research summary that includes:
- Main findings
- Key facts and statistics
- Relevant quotes or statements
- Implications for Goochland County residents
- Conservative policy perspective

Note: Use your knowledge through early 2025. Focus on factual, well-sourced information."""
        
        return prompt
    
    async def _process_research_response(self, message) -> Dict:
        """Extract and structure research findings"""
        
        research_data = {
            "findings": [],
            "citations": [],
            "key_points": [],
            "raw_content": ""
        }
        
        # Process content blocks
        for block in message.content:
            if block.type == "text":
                research_data["raw_content"] += block.text
                research_data["findings"].append(block.text)
        
        return research_data