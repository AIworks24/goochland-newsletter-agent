# backend/app/services/document_processor.py
import PyPDF2
from docx import Document
from anthropic import Anthropic
from typing import Dict, Optional
import json
from ..config import settings
import os

class DocumentProcessor:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        
    async def process_document(self, file_path: str, file_type: str) -> Dict:
        """Process uploaded document and extract structured information"""
        
        # Extract text based on file type
        if file_type in ['application/pdf', 'pdf']:
            text = self._extract_pdf_text(file_path)
        elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx']:
            text = self._extract_docx_text(file_path)
        elif file_type in ['text/plain', 'txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Use Claude to structure the information
        structured_data = await self._structure_document(text)
        
        return structured_data
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from Word document"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        
        return text
    
    async def _structure_document(self, text: str) -> Dict:
        """Use Claude to extract structured data from document"""
        
        prompt = f"""Analyze the following meeting minutes or document and extract structured information:

DOCUMENT TEXT:
{text[:15000]}  # Limit to ~15k chars to stay within context

Extract the following information in JSON format:
{{
    "document_type": "meeting_minutes|report|general",
    "date": "YYYY-MM-DD if available",
    "title": "Document title or meeting name",
    "attendees": ["list of attendees if applicable"],
    "key_decisions": ["list of major decisions made"],
    "action_items": [
        {{"item": "description", "owner": "responsible party", "deadline": "date if mentioned"}}
    ],
    "discussions": ["main topics discussed"],
    "upcoming_events": [
        {{"event": "name", "date": "date", "details": "description"}}
    ],
    "important_announcements": ["any significant announcements"],
    "summary": "2-3 sentence summary of the document"
}}

Be thorough and extract all relevant information. If a field doesn't apply, use an empty array or null."""

        message = self.client.messages.create(
            model=settings.default_model,
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract JSON from response
        response_text = message.content[0].text
        
        # Try to extract JSON
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                structured_data = json.loads(json_match.group())
            else:
                structured_data = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, create basic structure
            structured_data = {
                "document_type": "general",
                "summary": response_text[:500],
                "raw_content": text[:5000]
            }
        
        # Add full text for reference
        structured_data["full_text"] = text
        
        return structured_data