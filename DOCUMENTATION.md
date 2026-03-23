# Project Documentation

## AI-Powered Student Productivity Assistant

### Complete Technical Documentation

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Backend Documentation](#backend-documentation)
5. [Frontend Documentation](#frontend-documentation)
6. [API Documentation](#api-documentation)
7. [Deployment Guide](#deployment-guide)

---

## Project Overview

This is a full-stack web application that provides four AI-powered tools for students:
- Study Assistant Chatbot
- Resume Builder
- Code Explainer
- Notes Generator

**Technology Stack:**
- Backend: Flask (Python)
- Frontend: HTML5, CSS3, Vanilla JavaScript
- AI: OpenAI GPT-3.5-turbo
- PDF Processing: PyPDF2

---

## Architecture

### System Architecture
```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │ ◄─────► │    Flask    │ ◄─────► │  OpenAI API │
│  (Frontend) │  HTTP   │  (Backend)  │  HTTPS  │             │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │   Session   │
                        │   Storage   │
                        └─────────────┘
```

### Request Flow
1. User interacts with frontend (HTML/CSS/JS)
2. JavaScript sends AJAX request to Flask backend
3. Flask processes request and calls OpenAI API
4. OpenAI returns AI-generated response
5. Flask sends response back to frontend
6. JavaScript updates UI with response

---

## File Structure

```
ai-student-assistant/
│
├── app.py                      # Main Flask application
│   ├── Route handlers
│   ├── OpenAI integration
│   └── Session management
│
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
│
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css         # Complete styling
│   └── js/
│       └── script.js         # Frontend logic
│
├── templates/                 # HTML templates
│   └── index.html            # Main page
│
├── uploads/                   # Temporary file storage
│
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
├── DOCUMENTATION.md          # This file
├── test_setup.py             # Setup verification
├── setup.bat                 # Windows setup script
└── setup.sh                  # Unix/Linux setup script
```

---

## Backend Documentation

### app.py Structure

#### Imports and Configuration
```python
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import PyPDF2
```

#### Key Components

**1. Flask App Initialization**
- Secret key for session management
- Upload folder configuration
- Max file size limit (16MB)

**2. OpenAI Client Setup**
- Loads API key from environment
- Initializes OpenAI client

**3. Route Handlers**

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Serve main page |
| `/chat` | POST | Handle chatbot messages |
| `/clear-chat` | POST | Clear chat history |
| `/resume` | POST | Generate resume |
| `/explain-code` | POST | Explain code |
| `/generate-notes` | POST | Generate notes |

**4. Session Management**
- Stores chat history per user session
- Maintains conversation context

---

## Frontend Documentation

### HTML Structure (index.html)

#### Main Components
1. **Sidebar Navigation**
   - Logo and branding
   - Navigation buttons
   - Dark mode toggle

2. **Main Content Area**
   - Dynamic header
   - Four content sections
   - Loading spinner overlay

3. **Content Sections**
   - Chatbot interface
   - Resume form
   - Code explainer form
   - Notes generator with tabs

### CSS Architecture (style.css)

#### CSS Variables
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --bg-color: #f8fafc;
    --card-bg: #ffffff;
    --text-color: #1e293b;
    /* ... more variables */
}
```

#### Key Features
- Responsive design with flexbox
- Dark mode support
- Smooth animations
- Custom scrollbar styling
- Mobile-first approach

### JavaScript Logic (script.js)

#### Main Functions

**1. Navigation Management**
```javascript
- switchSection()
- updateHeader()
- toggleDarkMode()
```

**2. Chatbot Functions**
```javascript
- sendMessage()
- addMessage()
- clearChat()
```

**3. Resume Builder**
```javascript
- generateResume()
- copyToClipboard()
```

**4. Code Explainer**
```javascript
- explainCode()
- copyExplanation()
```

**5. Notes Generator**
```javascript
- generateNotes()
- handleFileUpload()
- switchTab()
```

---

## API Documentation

### 1. Chat Endpoint

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "message": "string"
}
```

**Response:**
```json
{
  "success": true,
  "response": "AI generated response"
}
```

**Error Response:**
```json
{
  "error": "Error message"
}
```

---

### 2. Resume Generation Endpoint

**Endpoint:** `POST /resume`

**Request Body:**
```json
{
  "name": "string",
  "education": "string",
  "skills": "string",
  "projects": "string",
  "experience": "string"
}
```

**Response:**
```json
{
  "success": true,
  "resume": "Generated resume content"
}
```

---

### 3. Code Explanation Endpoint

**Endpoint:** `POST /explain-code`

**Request Body:**
```json
{
  "code": "string",
  "language": "Python|JavaScript|Java|C|C++|C#"
}
```

**Response:**
```json
{
  "success": true,
  "explanation": "Code explanation"
}
```

---

### 4. Notes Generation Endpoint

**Endpoint:** `POST /generate-notes`

**Request Body (Form Data):**
- `text`: string (for text input)
- `file`: file (for PDF upload)

**Response:**
```json
{
  "success": true,
  "notes": "Generated study notes"
}
```

---

## Deployment Guide

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API key

# Run application
python app.py
```

### Production Deployment

#### Option 1: Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

#### Option 2: AWS EC2
1. Launch EC2 instance (Ubuntu)
2. Install Python and dependencies
3. Clone repository
4. Set up environment variables
5. Use Gunicorn as WSGI server
6. Configure Nginx as reverse proxy

#### Option 3: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## Security Considerations

1. **API Key Protection**
   - Never commit .env file
   - Use environment variables
   - Rotate keys regularly

2. **File Upload Security**
   - Validate file types
   - Limit file size
   - Delete files after processing

3. **Session Security**
   - Use secure session keys
   - Implement HTTPS in production
   - Set session timeout

4. **Input Validation**
   - Sanitize user inputs
   - Validate file uploads
   - Limit request sizes

---

## Performance Optimization

1. **Frontend**
   - Minify CSS/JS in production
   - Use CDN for Font Awesome
   - Implement lazy loading

2. **Backend**
   - Cache API responses
   - Use connection pooling
   - Implement rate limiting

3. **AI API**
   - Set appropriate token limits
   - Implement request queuing
   - Monitor API usage

---

## Testing

### Manual Testing Checklist
- [ ] Chatbot responds correctly
- [ ] Resume generation works
- [ ] Code explanation accurate
- [ ] PDF upload and processing
- [ ] Text notes generation
- [ ] Dark mode toggle
- [ ] Copy to clipboard
- [ ] Mobile responsiveness
- [ ] Error handling

### Automated Testing
```python
# Run setup verification
python test_setup.py
```

---

## Troubleshooting

### Common Issues

**Issue: Module not found**
```bash
Solution: pip install -r requirements.txt
```

**Issue: API key error**
```bash
Solution: Check .env file exists and has valid key
```

**Issue: Port in use**
```python
# Change port in app.py
app.run(debug=True, port=5001)
```

---

## Future Enhancements

### Planned Features
1. User authentication system
2. Database integration (PostgreSQL)
3. Save chat history permanently
4. Export notes as PDF
5. Multiple AI model support
6. Voice input for chatbot
7. Code syntax highlighting
8. Resume template selection
9. Multi-language support
10. Analytics dashboard

### Technical Improvements
1. Add unit tests
2. Implement CI/CD pipeline
3. Add logging system
4. Implement caching
5. Add API rate limiting
6. Improve error handling
7. Add monitoring and alerts

---

## Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

---

## License

This project is open-source and available for educational purposes.

---

## Support

For issues and questions:
1. Check README.md
2. Review this documentation
3. Run test_setup.py
4. Check troubleshooting section

---

**Last Updated:** 2024
**Version:** 1.0.0
