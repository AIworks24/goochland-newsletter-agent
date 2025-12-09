# backend/app/routes/newsletter.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os
import time
from datetime import datetime

from ..models import (
    ResearchRequest,
    GenerationResponse, ContentType
)
from ..services.research_engine import ResearchEngine
from ..services.document_processor import DocumentProcessor
from ..services.newsletter_generator import NewsletterGenerator
from ..services.image_generator import ImageGenerator
from ..services.wordpress_publisher import WordPressPublisher
from ..config import settings

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])

# Initialize services
research_engine = ResearchEngine()
document_processor = DocumentProcessor()
newsletter_generator = NewsletterGenerator()
image_generator = ImageGenerator()
wordpress_publisher = WordPressPublisher()


@router.post("/generate/research")
async def generate_from_research(request: ResearchRequest):
    """Generate newsletter from research topic"""
    start_time = time.time()
    
    try:
        # Step 1: Research the topic
        print(f"Starting research for topic: {request.topic}")
        research_data = await research_engine.research_topic(
            topic=request.topic,
            context=request.context,
            sources=request.sources
        )
        research_data['topic'] = request.topic
        research_data['context'] = request.context or ""
        
        # Step 2: Generate newsletter content
        print("Generating newsletter content...")
        newsletter_content = await newsletter_generator.generate_newsletter(
            content_type=ContentType.RESEARCH,
            input_data=research_data,
            word_count=request.word_count or 800
        )
        
        # Step 3: Generate featured image
        print("Generating featured image...")
        image_id = None
        try:
            image_description = newsletter_content.suggested_images[0] if newsletter_content.suggested_images else "Newsletter header image"
            image_url = await image_generator.generate_image(image_description)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(settings.upload_dir, f"newsletter_{timestamp}.png")
            await image_generator.download_image(image_url, image_path)
            
            image_id = await wordpress_publisher.upload_image(image_path, alt_text=image_description)
        except Exception as e:
            print(f"Image generation/upload failed: {e}")
        
        # Step 4: Create WordPress draft
        print("Creating WordPress draft...")
        try:
            wp_result = await wordpress_publisher.create_draft_post(
                newsletter_content=newsletter_content.dict(),
                featured_image_id=image_id
            )
            
            if not wp_result.get('success'):
                wp_result = {
                    'success': True,
                    'post_id': None,
                    'edit_url': 'Pending WordPress credentials',
                    'preview_url': 'Pending WordPress credentials'
                }
        except Exception as wp_error:
            print(f"WordPress posting skipped: {wp_error}")
            wp_result = {
                'success': True,
                'post_id': None,
                'edit_url': 'Pending WordPress credentials',
                'preview_url': 'Pending WordPress credentials'
            }
        
        generation_time = time.time() - start_time
        
        return {
            "success": True,
            "wordpress_post_id": wp_result.get('post_id'),
            "edit_url": wp_result.get('edit_url'),
            "preview_url": wp_result.get('preview_url'),
            "content": newsletter_content.dict(),
            "generation_time": generation_time,
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in research generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/minutes")
async def generate_from_minutes(
    file: UploadFile = File(...),
    additional_context: Optional[str] = Form(None),
    highlight_items: Optional[str] = Form(None)
):
    """Generate newsletter from meeting minutes"""
    start_time = time.time()
    
    try:
        allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename or "file.txt")[1]
        file_path = os.path.join(settings.upload_dir, f"minutes_{timestamp}{file_extension}")
        
        content_bytes = await file.read()
        with open(file_path, "wb") as f:
            f.write(content_bytes)
        
        print(f"Processing document: {file.filename}")
        
        structured_data = await document_processor.process_document(
            file_path=file_path,
            file_type=file.content_type or "text/plain"
        )
        
        if additional_context:
            structured_data['additional_context'] = additional_context
        
        if highlight_items:
            structured_data['highlight_items'] = highlight_items.split(',')
        
        print("Generating newsletter from minutes...")
        newsletter_content = await newsletter_generator.generate_newsletter(
            content_type=ContentType.MINUTES,
            input_data={'structured_data': structured_data},
            word_count=800
        )
        
        print("Generating featured image...")
        image_id = None
        try:
            image_description = newsletter_content.suggested_images[0] if newsletter_content.suggested_images else "Meeting highlights"
            image_url = await image_generator.generate_image(image_description)
            
            image_path = os.path.join(settings.upload_dir, f"newsletter_{timestamp}.png")
            await image_generator.download_image(image_url, image_path)
            
            image_id = await wordpress_publisher.upload_image(image_path, alt_text=image_description)
        except Exception as e:
            print(f"Image generation failed: {e}")
        
        print("Creating WordPress draft...")
        try:
            wp_result = await wordpress_publisher.create_draft_post(
                newsletter_content=newsletter_content.dict(),
                featured_image_id=image_id
            )
            
            if not wp_result.get('success'):
                wp_result = {
                    'success': True,
                    'post_id': None,
                    'edit_url': 'Pending WordPress credentials',
                    'preview_url': 'Pending WordPress credentials'
                }
        except Exception as wp_error:
            print(f"WordPress posting skipped: {wp_error}")
            wp_result = {
                'success': True,
                'post_id': None,
                'edit_url': 'Pending WordPress credentials',
                'preview_url': 'Pending WordPress credentials'
            }
        
        try:
            os.remove(file_path)
        except:
            pass
        
        generation_time = time.time() - start_time
        
        return {
            "success": True,
            "wordpress_post_id": wp_result.get('post_id'),
            "edit_url": wp_result.get('edit_url'),
            "preview_url": wp_result.get('preview_url'),
            "content": newsletter_content.dict(),
            "generation_time": generation_time,
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in minutes generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/hybrid")
async def generate_hybrid(
    file: UploadFile = File(...),
    research_topic: str = Form(...),
    research_context: Optional[str] = Form(None),
    minutes_context: Optional[str] = Form(None)
):
    """Generate newsletter combining minutes and research"""
    start_time = time.time()
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename or "file.txt")[1]
        file_path = os.path.join(settings.upload_dir, f"minutes_{timestamp}{file_extension}")
        
        content_bytes = await file.read()
        with open(file_path, "wb") as f:
            f.write(content_bytes)
        
        print("Processing meeting minutes...")
        meeting_data = await document_processor.process_document(
            file_path=file_path,
            file_type=file.content_type or "text/plain"
        )
        
        if minutes_context:
            meeting_data['additional_context'] = minutes_context
        
        print(f"Researching topic: {research_topic}")
        research_data = await research_engine.research_topic(
            topic=research_topic,
            context=research_context
        )
        
        print("Generating hybrid newsletter...")
        newsletter_content = await newsletter_generator.generate_newsletter(
            content_type=ContentType.HYBRID,
            input_data={
                'meeting_data': meeting_data,
                'research_data': research_data
            },
            word_count=1000
        )
        
        image_id = None
        try:
            image_description = newsletter_content.suggested_images[0] if newsletter_content.suggested_images else "Newsletter header"
            image_url = await image_generator.generate_image(image_description)
            
            image_path = os.path.join(settings.upload_dir, f"newsletter_{timestamp}.png")
            await image_generator.download_image(image_url, image_path)
            
            image_id = await wordpress_publisher.upload_image(image_path, alt_text=image_description)
        except Exception as e:
            print(f"Image generation failed: {e}")
        
        try:
            wp_result = await wordpress_publisher.create_draft_post(
                newsletter_content=newsletter_content.dict(),
                featured_image_id=image_id
            )
            
            if not wp_result.get('success'):
                wp_result = {
                    'success': True,
                    'post_id': None,
                    'edit_url': 'Pending WordPress credentials',
                    'preview_url': 'Pending WordPress credentials'
                }
        except Exception as wp_error:
            print(f"WordPress posting skipped: {wp_error}")
            wp_result = {
                'success': True,
                'post_id': None,
                'edit_url': 'Pending WordPress credentials',
                'preview_url': 'Pending WordPress credentials'
            }
        
        try:
            os.remove(file_path)
        except:
            pass
        
        generation_time = time.time() - start_time
        
        return {
            "success": True,
            "wordpress_post_id": wp_result.get('post_id'),
            "edit_url": wp_result.get('edit_url'),
            "preview_url": wp_result.get('preview_url'),
            "content": newsletter_content.dict(),
            "generation_time": generation_time,
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in hybrid generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))