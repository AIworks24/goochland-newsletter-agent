# backend/app/routes/wordpress.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..services.wordpress_publisher import WordPressPublisher

router = APIRouter(prefix="/api/wordpress", tags=["wordpress"])

wordpress_publisher = WordPressPublisher()


@router.get("/test-connection")
async def test_wordpress_connection():
    """Test WordPress API connection"""
    result = wordpress_publisher.test_connection()
    
    if result['success']:
        return JSONResponse(content=result)
    else:
        raise HTTPException(status_code=500, detail=result.get('error'))


@router.get("/categories")
async def get_categories():
    """Get all WordPress categories"""
    try:
        import requests
        response = requests.get(
            f"{wordpress_publisher.wp_url}/wp-json/wp/v2/categories",
            auth=wordpress_publisher.auth
        )
        
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch categories")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tags")
async def get_tags():
    """Get all WordPress tags"""
    try:
        import requests
        response = requests.get(
            f"{wordpress_publisher.wp_url}/wp-json/wp/v2/tags",
            auth=wordpress_publisher.auth
        )
        
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch tags")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/posts/drafts")
async def get_draft_posts():
    """Get all draft posts"""
    try:
        import requests
        response = requests.get(
            f"{wordpress_publisher.wp_url}/wp-json/wp/v2/posts",
            params={'status': 'draft'},
            auth=wordpress_publisher.auth
        )
        
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch drafts")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))