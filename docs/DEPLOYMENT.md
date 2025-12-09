# Deployment Guide

## Railway Deployment (Backend)

### 1. Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your repository
5. Select the backend directory

### 2. Configure Environment Variables

In Railway dashboard, add these variables:
```
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
WORDPRESS_URL=https://goochlandgop.org
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_password
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://your-frontend.vercel.app
```

### 3. Deploy

Railway will automatically deploy. Note your deployment URL.

## Vercel Deployment (Frontend)

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Deploy Frontend
```bash
cd frontend
vercel
```

Follow prompts:
- Set up and deploy: Yes
- Which scope: Your account
- Link to existing project: No
- Project name: goochland-newsletter-frontend
- Directory: ./
- Override settings: No

### 3. Configure Environment
```bash
vercel env add VITE_API_URL
# Enter your Railway backend URL
```

### 4. Update vercel.json

Edit `frontend/vercel.json` with your Railway URL:
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-railway-app.railway.app/api/$1"
    }
  ]
}
```

### 5. Redeploy
```bash
vercel --prod
```

## Post-Deployment

### 1. Update CORS

In Railway, update CORS_ORIGINS with your Vercel URL:
```
CORS_ORIGINS=https://your-app.vercel.app
```

### 2. Test Connection

Visit your Vercel URL and verify:
- WordPress connection shows green
- Can generate test newsletter
- Draft appears in WordPress

### 3. Update WordPress

If WordPress blocks requests, add to wp-config.php:
```php
define('WP_HTTP_BLOCK_EXTERNAL', false);
```

## Monitoring

### Railway
- View logs in Railway dashboard
- Set up alerts for errors
- Monitor resource usage

### Vercel
- Check function logs
- Monitor build times
- Set up deployment notifications

## Backup & Recovery

### Database Backups
Not required (stateless application)

### Configuration Backups
- Export environment variables from Railway
- Save to secure password manager
- Document in team wiki

### WordPress Backups
- Use WordPress backup plugin
- Schedule regular backups
- Test restoration process