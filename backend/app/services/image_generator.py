# backend/app/services/image_generator.py
from openai import OpenAI
from typing import Optional
import requests
from ..config import settings
import os

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        
    async def generate_image(
        self, 
        description: str, 
        style: str = "professional"
    ) -> str:
        """Generate an image using DALL-E 3"""
        
        # Refine prompt for political appropriateness
        refined_prompt = self._refine_prompt(description, style)
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=refined_prompt,
                size="1792x1024",
                quality="standard",
                n=1
            )
            
            return response.data[0].url
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Return placeholder or raise
            raise Exception(f"Image generation failed: {str(e)}")
    
    def _refine_prompt(self, description: str, style: str) -> str:
        """Refine image prompt for political appropriateness"""
        
        base_style = "Professional, clean, modern digital illustration. "
        
        # Add safety constraints
        constraints = """
        Avoid: Specific political figures, partisan symbols, controversial imagery.
        Include: Abstract concepts, Virginia landmarks, community themes, patriotic colors.
        Style: Clean, professional, inclusive, appropriate for government/political newsletter.
        """
        
        return f"{base_style}{description}. {constraints}"
    
    async def download_image(self, image_url: str, save_path: str) -> str:
        """Download generated image to local storage"""
        
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return save_path
            
        except Exception as e:
            raise Exception(f"Image download failed: {str(e)}")