# Setup Guide

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Docker and Docker Compose (optional)
- GitHub account
- Anthropic API key
- OpenAI API key
- WordPress site with admin access

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/goochland-newsletter-agent.git
cd goochland-newsletter-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. WordPress Configuration

1. Log into your WordPress admin panel
2. Go to Users → Profile
3. Scroll to "Application Passwords"
4. Create new application password named "Newsletter Agent"
5. Copy the password (format: xxxx xxxx xxxx xxxx)
6. Add to your .env file

### 5. Run with Docker (Recommended)
```bash
# From project root
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 6. Run Manually

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## Testing the Setup

1. Open http://localhost:3000
2. Check WordPress connection status
3. Try generating a test newsletter with research topic: "Test Newsletter"
4. Verify draft appears in WordPress

## Troubleshooting

### WordPress Connection Failed
- Verify WordPress URL is correct (no trailing slash)
- Check application password is properly formatted
- Ensure WordPress REST API is enabled
- Test manually: `curl -u username:password https://yoursite.com/wp-json/wp/v2/users/me`

### API Key Errors
- Verify API keys are correctly set in .env
- Check for extra spaces or quotes
- Ensure keys have proper permissions

### File Upload Issues
- Check upload directory exists and is writable
- Verify MAX_UPLOAD_SIZE setting
- Ensure file types are supported (PDF, DOCX, TXT)