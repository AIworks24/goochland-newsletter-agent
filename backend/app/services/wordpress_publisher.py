# backend/app/services/wordpress_publisher.py
import requests
from typing import Dict, Optional, List
from ..config import settings
from ..models import WordPressPost
import base64
import os

class WordPressPublisher:
    def __init__(self):
        self.wp_url = settings.wordpress_url.rstrip('/')
        self.username = settings.wordpress_username
        self.password = settings.wordpress_app_password
        self.auth = (self.username, self.password)
        self.headers = {'Content-Type': 'application/json'}
        
    def test_connection(self) -> Dict:
        """Test WordPress connection"""
        try:
            response = requests.get(
                f"{self.wp_url}/wp-json/wp/v2/users/me",
                auth=self.auth
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Connected to WordPress",
                    "user": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Connection failed: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    async def upload_image(self, image_path: str, alt_text: str = "") -> Optional[int]:
        """Upload image to WordPress media library"""
        
        try:
            with open(image_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(image_path), f, 'image/png')
                }
                
                response = requests.post(
                    f"{self.wp_url}/wp-json/wp/v2/media",
                    auth=self.auth,
                    files=files,
                    data={'alt_text': alt_text}
                )
                
                if response.status_code == 201:
                    return response.json()['id']
                else:
                    print(f"Image upload failed: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None
    
    async def create_draft_post(
        self, 
        newsletter_content: Dict,
        featured_image_id: Optional[int] = None
    ) -> Dict:
        """Create a draft post in WordPress"""
        
        try:
            # Prepare post data
            post_data = {
                'title': newsletter_content.get('title'),
                'content': newsletter_content.get('body'),
                'excerpt': newsletter_content.get('excerpt'),
                'status': 'draft',
                'meta': {
                    'ai_generated': True,
                    'sources': newsletter_content.get('sources', []),
                    'suggested_images': newsletter_content.get('suggested_images', [])
                }
            }
            
            if featured_image_id:
                post_data['featured_media'] = featured_image_id
            
            # Handle categories and tags
            category_id = await self._get_or_create_category(
                newsletter_content.get('category', 'Newsletter')
            )
            if category_id:
                post_data['categories'] = [category_id]
            
            # Create tags
            tag_ids = []
            for tag_name in newsletter_content.get('tags', []):
                tag_id = await self._get_or_create_tag(tag_name)
                if tag_id:
                    tag_ids.append(tag_id)
            if tag_ids:
                post_data['tags'] = tag_ids
            
            # Create the post
            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/posts",
                auth=self.auth,
                headers=self.headers,
                json=post_data
            )
            
            if response.status_code == 201:
                post = response.json()
                return {
                    'success': True,
                    'post_id': post['id'],
                    'edit_url': f"{self.wp_url}/wp-admin/post.php?post={post['id']}&action=edit",
                    'preview_url': post['link']
                }
            else:
                return {
                    'success': False,
                    'error': f"Post creation failed: {response.status_code}",
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Error creating post: {str(e)}"
            }
    
    async def _get_or_create_category(self, category_name: str) -> Optional[int]:
        """Get existing category or create new one"""
        
        try:
            # Search for existing
            response = requests.get(
                f"{self.wp_url}/wp-json/wp/v2/categories",
                params={'search': category_name},
                auth=self.auth
            )
            
            categories = response.json()
            if categories:
                return categories[0]['id']
            
            # Create new
            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/categories",
                auth=self.auth,
                json={'name': category_name}
            )
            
            if response.status_code == 201:
                return response.json()['id']
            
        except Exception as e:
            print(f"Error with category: {e}")
        
        return None
    
    async def _get_or_create_tag(self, tag_name: str) -> Optional[int]:
        """Get existing tag or create new one"""
        
        try:
            # Search for existing
            response = requests.get(
                f"{self.wp_url}/wp-json/wp/v2/tags",
                params={'search': tag_name},
                auth=self.auth
            )
            
            tags = response.json()
            if tags:
                return tags[0]['id']
            
            # Create new
            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/tags",
                auth=self.auth,
                json={'name': tag_name}
            )
            
            if response.status_code == 201:
                return response.json()['id']
            
        except Exception as e:
            print(f"Error with tag: {e}")
        
        return None