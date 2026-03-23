# AI-Powered Student Productivity Assistant

A complete web application that integrates four AI-powered features to help students with their academic and career needs.

## 🚀 Features

### 1️⃣ AI Study Assistant Chatbot
- Virtual tutor for academic questions
- Explains concepts in simple language
- Maintains chat history
- Real-time responses

### 2️⃣ Resume Builder using GenAI
- Generate professional resumes
- Input: Name, Education, Skills, Projects, Experience
- AI-powered content generation
- Copy to clipboard functionality

### 3️⃣ AI Code Explainer
- Explains code snippets line-by-line
- Supports multiple languages (Python, JavaScript, Java, C, C++, C#)
- Beginner-friendly explanations
- Conceptual understanding

### 4️⃣ Notes Generator from PDF/Text
- Generate concise study notes
- Accepts text input or PDF upload
- Creates bullet points and key takeaways
- Highlights important concepts

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **AI Integration**: OpenAI API (GPT-3.5-turbo)
- **PDF Processing**: PyPDF2
- **Styling**: Custom CSS with dark mode support
- **Icons**: Font Awesome

## 📁 Project Structure

```
ai-student-assistant/
├── app.py                      # Flask backend with all routes
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css          # Complete styling with dark mode
│   └── js/
│       └── script.js          # Frontend JavaScript logic
├── templates/
│   └── index.html             # Main HTML template
└── uploads/                   # Temporary PDF storage
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Step 1: Clone or Download the Project
```bash
cd ai-student-assistant
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### Step 5: Run the Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

## 🎯 Usage Guide

### AI Study Assistant Chatbot
1. Click on "Study Chatbot" in the sidebar
2. Type your academic question in the input field
3. Press Enter or click the send button
4. View AI responses in real-time
5. Use "Clear Chat" to start a new conversation

### Resume Builder
1. Navigate to "Resume Builder"
2. Fill in your details:
   - Full Name (required)
   - Education
   - Skills
   - Projects
   - Experience
3. Click "Generate Resume"
4. View the professionally formatted resume
5. Use "Copy" button to copy to clipboard

### Code Explainer
1. Go to "Code Explainer"
2. Select programming language from dropdown
3. Paste your code snippet
4. Click "Explain Code"
5. Read the detailed explanation
6. Copy explanation if needed

### Notes Generator
1. Select "Notes Generator"
2. Choose input method:
   - **Text Input**: Paste your study material
   - **PDF Upload**: Upload a PDF file
3. Click "Generate Notes"
4. View concise study notes with key points
5. Copy notes for later use

## 🎨 Features

### UI/UX Features
- ✅ Responsive design (mobile-friendly)
- ✅ Dark mode toggle
- ✅ Smooth animations and transitions
- ✅ Loading spinners during AI processing
- ✅ Copy-to-clipboard functionality
- ✅ Clean card-based layout
- ✅ Sidebar navigation
- ✅ Modern gradient design

### Technical Features
- ✅ Session-based chat history
- ✅ Error handling
- ✅ File upload validation
- ✅ JSON API responses
- ✅ Secure file handling
- ✅ Environment variable configuration

## 🔑 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/chat` | POST | Send message to chatbot |
| `/clear-chat` | POST | Clear chat history |
| `/resume` | POST | Generate resume |
| `/explain-code` | POST | Explain code snippet |
| `/generate-notes` | POST | Generate study notes |

## 📝 Request/Response Examples

### Chat Request
```json
{
  "message": "Explain edge detection in simple terms"
}
```

### Resume Request
```json
{
  "name": "John Doe",
  "education": "B.Tech in Computer Science",
  "skills": "Python, JavaScript, React",
  "projects": "E-commerce Website",
  "experience": "Intern at ABC Company"
}
```

### Code Explanation Request
```json
{
  "code": "for i in range(10):\n    print(i)",
  "language": "Python"
}
```

## 🚨 Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "OpenAI API key not found"
**Solution**: Check that `.env` file exists and contains valid API key

### Issue: PDF upload not working
**Solution**: Ensure `uploads/` folder exists and has write permissions

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

## 🔒 Security Notes

- Never commit `.env` file to version control
- Keep your OpenAI API key private
- Uploaded PDFs are automatically deleted after processing
- Session data is stored server-side

## 🌟 Future Enhancements

- [ ] User authentication system
- [ ] Save chat history to database
- [ ] Export notes as PDF
- [ ] Multiple AI model support
- [ ] Voice input for chatbot
- [ ] Code syntax highlighting
- [ ] Resume templates selection
- [ ] Multi-language support

## 📄 License

This project is open-source and available for educational purposes.

## 👨‍💻 Developer

Built with ❤️ for students by students

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

---

**Note**: This application requires an active internet connection and valid OpenAI API key to function properly.
