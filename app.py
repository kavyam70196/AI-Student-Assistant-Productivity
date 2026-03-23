from flask import Flask, render_template, request, jsonify, session, send_file
import os
from dotenv import load_dotenv
import PyPDF2
from werkzeug.utils import secure_filename
import secrets
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from datetime import datetime
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Groq
GROQ_API_KEY = "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"
MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)

def query_ai(prompt):
    """Query Groq AI"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for students."},
                {"role": "user", "content": prompt}
            ],
            model=MODEL,
            temperature=0.7,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        return "AI response generated."

def get_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return session['chat_history']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        chat_history = get_chat_history()
        
        prompt = f"You are a helpful tutor. Student asks: {user_message}\nProvide a clear, simple answer:"
        assistant_message = query_ai(prompt)
        
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": assistant_message})
        session['chat_history'] = chat_history
        
        return jsonify({'response': assistant_message, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear-chat', methods=['POST'])
def clear_chat():
    session['chat_history'] = []
    return jsonify({'success': True})

@app.route('/resume', methods=['POST'])
def generate_resume():
    try:
        data = request.json
        session['resume_data'] = data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scan-resume', methods=['POST'])
def scan_resume():
    try:
        data = request.json
        
        # Build resume summary for AI
        resume_text = f"""
Name: {data.get('name', 'N/A')}
Email: {data.get('email', 'N/A')}
Phone: {data.get('phone', 'N/A')}
Location: {data.get('location', 'N/A')}
LinkedIn: {data.get('linkedin', 'N/A')}
Portfolio: {data.get('portfolio', 'N/A')}

Career Objective: {data.get('objective', 'N/A')}

Education: {data.get('education', 'N/A')}

Technical Skills: {data.get('technicalSkills', 'N/A')}
Soft Skills: {data.get('softSkills', 'N/A')}

Experience: {data.get('experience', 'N/A')}

Projects: {data.get('projects', 'N/A')}

Certifications: {data.get('certifications', 'N/A')}

Achievements: {data.get('achievements', 'N/A')}
"""
        
        prompt = f"""You are an expert resume reviewer. Analyze this resume and provide:

{resume_text}

1. A score out of 100 (just the number)
2. List of strengths (what's good)
3. List of improvements needed
4. Formatting suggestions

Format your response EXACTLY like this:
SCORE: [number]
STRENGTHS:
- [strength 1]
- [strength 2]
IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
FORMATTING:
- [format tip 1]
- [format tip 2]"""
        
        ai_response = query_ai(prompt)
        
        return jsonify({'analysis': ai_response, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-resume', methods=['GET'])
def download_resume():
    try:
        data = session.get('resume_data', {})
        
        if not data:
            return "No resume data found", 400
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.25*inch, bottomMargin=0.25*inch, leftMargin=0.4*inch, rightMargin=0.4*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        from reportlab.lib.colors import black
        from reportlab.platypus import HRFlowable
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, alignment=TA_CENTER, spaceAfter=1, spaceBefore=0, leading=16)
        contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontSize=7, alignment=TA_CENTER, spaceAfter=3, leading=8)
        heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=9, spaceAfter=1, spaceBefore=2, bold=True, leading=10)
        content_style = ParagraphStyle('Content', parent=styles['Normal'], fontSize=7, spaceAfter=1, leading=8)
        
        story.append(Paragraph(data.get('name', 'Your Name'), title_style))
        
        contact = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}"
        if data.get('linkedin'):
            contact += f" | {data.get('linkedin')}"
        if data.get('portfolio'):
            contact += f" | {data.get('portfolio')}"
        story.append(Paragraph(contact, contact_style))
        story.append(HRFlowable(width="100%", thickness=1, color=black, spaceAfter=2))
        
        if data.get('objective'):
            story.append(Paragraph("CAREER OBJECTIVE", heading_style))
            story.append(Paragraph(data['objective'].replace('\n', ' ')[:200], content_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=black, spaceAfter=1))
        
        if data.get('education'):
            story.append(Paragraph("EDUCATION", heading_style))
            story.append(Paragraph(data['education'].replace('\n', '<br/>'), content_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=black, spaceAfter=1))
        
        if data.get('technicalSkills') or data.get('softSkills'):
            story.append(Paragraph("SKILLS", heading_style))
            skills_text = ""
            if data.get('technicalSkills'):
                skills_text += f"<b>Technical:</b> {data['technicalSkills'].replace(chr(10), ', ')[:150]}"
            if data.get('softSkills'):
                skills_text += f" | <b>Soft:</b> {data['softSkills'].replace(chr(10), ', ')[:80]}"
            story.append(Paragraph(skills_text, content_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=black, spaceAfter=1))
        
        if data.get('experience'):
            story.append(Paragraph("EXPERIENCE", heading_style))
            story.append(Paragraph(data['experience'].replace('\n', '<br/>'), content_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=black, spaceAfter=1))
        
        if data.get('projects'):
            story.append(Paragraph("PROJECTS", heading_style))
            story.append(Paragraph(data['projects'].replace('\n', '<br/>'), content_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=black, spaceAfter=1))
        
        if data.get('certifications'):
            story.append(Paragraph("CERTIFICATIONS", heading_style))
            story.append(Paragraph(data['certifications'].replace('\n', ', '), content_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=black, spaceAfter=1))
        
        if data.get('achievements'):
            story.append(Paragraph("ACHIEVEMENTS", heading_style))
            story.append(Paragraph(data['achievements'].replace('\n', ', '), content_style))
        
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{data.get('name', 'resume').replace(' ', '_')}_resume.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

import ast

# Python Knowledge Base
PYTHON_KNOWLEDGE = {
    'libraries': {
        # Built-in Libraries
        'os': 'Built-in library for working with files and directories',
        'sys': 'Built-in library for system-related operations',
        'math': 'Built-in library for mathematical calculations',
        'random': 'Built-in library for generating random numbers',
        'datetime': 'Built-in library for handling date and time',
        'json': 'Built-in library for working with JSON data',
        're': 'Built-in library for regular expressions',
        'collections': 'Built-in library for advanced data structures',
        'itertools': 'Built-in library for efficient looping',
        'functools': 'Built-in library for functional programming tools',
        
        # Data Handling
        'numpy': 'NumPy is used for numerical computing and working with arrays and matrices',
        'pandas': 'Pandas is used for data analysis and working with tables using DataFrames. Useful for CSV and Excel files',
        
        # Data Visualization
        'matplotlib': 'Matplotlib is used to create basic graphs and plots',
        'seaborn': 'Seaborn is built on Matplotlib and used for advanced statistical visualization',
        'plotly': 'Plotly is used to create interactive graphs',
        
        # Machine Learning
        'sklearn': 'Scikit-learn supports classification, regression, clustering, and model evaluation',
        'scikit-learn': 'Scikit-learn supports classification, regression, clustering, and model evaluation',
        'xgboost': 'XGBoost is used for boosting algorithms and high-performance machine learning',
        'lightgbm': 'LightGBM is used for boosting algorithms and high-performance machine learning tasks',
        
        # Deep Learning
        'tensorflow': 'TensorFlow is a powerful framework for building neural networks and deep learning models',
        'keras': 'Keras is a high-level API that runs on TensorFlow and makes deep learning easier',
        'pytorch': 'PyTorch is a deep learning framework popular in research and development',
        
        # Natural Language Processing
        'nltk': 'NLTK is used for basic text processing tasks like tokenization and stemming',
        'spacy': 'SpaCy is a faster and more advanced NLP library',
        'transformers': 'Transformers from Hugging Face provides pretrained AI models for text generation, translation, and QA',
        
        # Computer Vision
        'opencv': 'OpenCV is used for image and video processing',
        'cv2': 'OpenCV (cv2) is used for image and video processing',
        'pillow': 'Pillow is used for opening, editing, and saving image files',
        'pil': 'PIL (Pillow) is used for opening, editing, and saving image files',
        
        # Web Development
        'flask': 'Flask is a lightweight web framework suitable for small projects and APIs',
        'django': 'Django is a full-stack web framework for building large and secure web applications',
        
        # API Handling and Automation
        'requests': 'Requests library is used to send HTTP requests',
        'beautifulsoup': 'BeautifulSoup is used for web scraping',
        'bs4': 'BeautifulSoup (bs4) is used for web scraping',
        'selenium': 'Selenium is used for browser automation',
        
        # Database Operations
        'sqlite3': 'Built-in library for working with SQLite databases',
        'sqlalchemy': 'SQLAlchemy is used as an Object Relational Mapper (ORM)',
        'psycopg2': 'Psycopg2 is used to connect Python with PostgreSQL databases',
    },
    'keywords': {
        'def': 'Defines a function',
        'class': 'Defines a class',
        'if': 'Conditional statement',
        'elif': 'Else if condition',
        'else': 'Alternative condition',
        'for': 'For loop for iteration',
        'while': 'While loop',
        'return': 'Returns value from function',
        'import': 'Imports a module or library',
        'from': 'Imports specific items from module',
        'try': 'Starts exception handling block',
        'except': 'Catches exceptions',
        'with': 'Context manager',
        'lambda': 'Anonymous function',
        'yield': 'Generator function',
        'async': 'Asynchronous function',
        'await': 'Waits for async operation',
    },
    'patterns': {
        'list_comprehension': '[x for x in range(10)] - Creates list using comprehension',
        'dict_comprehension': '{k: v for k, v in items} - Creates dictionary',
        'file_handling': 'with open(file) as f: - Safe file handling',
        'string_formatting': 'f"Hello {name}" - F-string formatting',
        'error_handling': 'try/except block - Handles errors gracefully',
    },
    'functions': {
        # NumPy functions
        'np.array': 'Creates a NumPy array from a list or tuple',
        'np.mean': 'Calculates the average/mean of array elements',
        'np.sum': 'Calculates the sum of all array elements',
        'np.max': 'Returns the maximum value in the array',
        'np.min': 'Returns the minimum value in the array',
        'np.std': 'Calculates standard deviation',
        'np.reshape': 'Changes the shape/dimensions of an array',
        
        # Pandas functions
        'pd.DataFrame': 'Creates a DataFrame (table) from data',
        'pd.read_csv': 'Reads data from a CSV file into DataFrame',
        '.head': 'Shows first 5 rows of DataFrame',
        '.tail': 'Shows last 5 rows of DataFrame',
        '.describe': 'Generates statistical summary of data',
        '.groupby': 'Groups data by specified column(s)',
        
        # Matplotlib functions
        'plt.plot': 'Creates a line plot with x and y coordinates',
        'plt.scatter': 'Creates a scatter plot',
        'plt.bar': 'Creates a bar chart',
        'plt.xlabel': 'Sets label for x-axis',
        'plt.ylabel': 'Sets label for y-axis',
        'plt.title': 'Sets title for the plot',
        'plt.show': 'Displays the plot window',
        'plt.savefig': 'Saves the plot as an image file',
        
        # Scikit-learn functions
        'LinearRegression': 'Creates a linear regression model',
        '.fit': 'Trains the model with training data (X, y)',
        '.predict': 'Makes predictions on new data',
        '.score': 'Returns accuracy/R² score of the model',
        'train_test_split': 'Splits data into training and testing sets',
        
        # TensorFlow/Keras functions
        'tf.keras.Sequential': 'Creates a sequential neural network model',
        'Dense': 'Adds a fully connected layer to the network',
        '.compile': 'Configures the model with optimizer and loss function',
        '.fit': 'Trains the neural network model',
        '.evaluate': 'Tests the model performance',
        
        # PyTorch functions
        'torch.tensor': 'Creates a PyTorch tensor (multi-dimensional array)',
        'nn.Linear': 'Creates a linear/fully connected layer',
        'nn.ReLU': 'Applies ReLU activation function',
        'torch.optim.Adam': 'Adam optimizer for training',
        
        # OpenCV functions
        'cv2.imread': 'Reads/loads an image file from disk',
        'cv2.imshow': 'Displays an image in a window',
        'cv2.imwrite': 'Saves an image to a file',
        'cv2.waitKey': 'Waits for a keyboard input',
        'cv2.destroyAllWindows': 'Closes all OpenCV windows',
        'cv2.cvtColor': 'Converts image color space (RGB, Grayscale, etc.)',
        
        # Requests functions
        'requests.get': 'Sends HTTP GET request to fetch data from URL',
        'requests.post': 'Sends HTTP POST request to submit data',
        '.json': 'Parses response as JSON data',
        '.status_code': 'Returns HTTP status code (200, 404, etc.)',
        
        # NLTK functions
        'word_tokenize': 'Splits text into individual words/tokens',
        'sent_tokenize': 'Splits text into sentences',
        'pos_tag': 'Tags words with parts of speech',
        
        # Flask functions
        'Flask': 'Creates a Flask web application instance',
        '@app.route': 'Decorator that maps URL to a function',
        'app.run': 'Starts the Flask development server',
        'render_template': 'Renders HTML template files',
        'jsonify': 'Converts Python dict to JSON response',
    }
}

def analyze_python_code(code):
    """Analyze Python code and provide detailed explanation"""
    lines = code.strip().split('\n')
    explanation = "PYTHON CODE EXPLANATION\n" + "="*60 + "\n\n"
    
    # Detect libraries
    libraries_used = []
    for lib, desc in PYTHON_KNOWLEDGE['libraries'].items():
        if lib in code.lower() or f'import {lib}' in code.lower():
            libraries_used.append(f"• {lib}: {desc}")
    
    if libraries_used:
        explanation += "LIBRARIES USED:\n" + "\n".join(libraries_used) + "\n\n"
    
    # Detect functions used
    functions_found = []
    for func, desc in PYTHON_KNOWLEDGE['functions'].items():
        if func in code:
            functions_found.append(f"• {func}(): {desc}")
    
    if functions_found:
        explanation += "FUNCTIONS DETECTED:\n" + "\n".join(functions_found) + "\n\n"
    
    explanation += "LINE-BY-LINE BREAKDOWN:\n"
    
    for i, line in enumerate(lines, 1):
        if line.strip():
            explanation += f"\nLine {i}: {line}\n"
            
            # Check for specific functions in this line
            line_functions = []
            for func, desc in PYTHON_KNOWLEDGE['functions'].items():
                if func in line:
                    line_functions.append(f"  → {func}: {desc}")
            
            if line_functions:
                explanation += "\n".join(line_functions) + "\n"
            else:
                # Check for keywords
                found_keyword = False
                for keyword, desc in PYTHON_KNOWLEDGE['keywords'].items():
                    if keyword in line.split():
                        explanation += f"  → {desc}\n"
                        found_keyword = True
                        break
                
                if not found_keyword:
                    if '=' in line and '==' not in line:
                        explanation += "  → Variable assignment\n"
                    elif 'print(' in line:
                        explanation += "  → Prints output to console\n"
    
    explanation += "\n\nKEY CONCEPTS:\n"
    explanation += "• This Python code demonstrates standard programming practices\n"
    explanation += "• Follow Python PEP 8 style guidelines\n"
    explanation += "• Uses Python's built-in features and syntax\n"
    
    return explanation

@app.route('/explain-code', methods=['POST'])
def explain_code():
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python').lower()
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        # Use AI for all languages
        if language == 'python':
            stored_explanation = analyze_python_code(code)
            prompt = f"""Explain this Python code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key Python concepts used
4. Best practices and tips

Keep it beginner-friendly."""
            ai_explanation = query_ai(prompt)
            full_explanation = stored_explanation + "\n\n" + "AI ENHANCED EXPLANATION:\n" + "="*60 + "\n" + ai_explanation
        
        elif language == 'c':
            prompt = f"""Explain this C code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key C concepts used (pointers, memory, functions, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'html':
            prompt = f"""Explain this HTML code in detail:

{code}

Provide:
1. What the HTML structure does
2. Explanation of each tag and attribute
3. Key HTML concepts used
4. Best practices for semantic HTML

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'css':
            prompt = f"""Explain this CSS code in detail:

{code}

Provide:
1. What the styles do
2. Explanation of each selector and property
3. Key CSS concepts used (box model, flexbox, grid, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'dsa':
            prompt = f"""Explain this Data Structures and Algorithms code in detail:

{code}

Provide:
1. What algorithm/data structure is being used
2. Time and space complexity analysis
3. Step-by-step explanation of how it works
4. Use cases and when to use this approach
5. Optimization tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'java':
            prompt = f"""Explain this Java code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key Java concepts used (OOP, classes, methods, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'javascript':
            prompt = f"""Explain this JavaScript code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key JavaScript concepts used (async/await, promises, DOM, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'c++':
            prompt = f"""Explain this C++ code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key C++ concepts used (OOP, STL, templates, pointers, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'kotlin':
            prompt = f"""Explain this Kotlin code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key Kotlin concepts used (null safety, coroutines, data classes, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        elif language == 'r':
            prompt = f"""Explain this R code in detail:

{code}

Provide:
1. What the code does (overview)
2. How it works (step by step)
3. Key R concepts used (data frames, vectors, statistical functions, etc.)
4. Best practices and tips

Keep it beginner-friendly."""
            full_explanation = query_ai(prompt)
        
        else:
            prompt = f"""Explain this {language} code in detail:

{code}

Provide a clear, beginner-friendly explanation."""
            full_explanation = query_ai(prompt)
        
        return jsonify({'explanation': full_explanation, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-notes', methods=['POST'])
def generate_notes():
    try:
        text_content = ''
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                with open(filepath, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
                
                os.remove(filepath)
        else:
            text_content = request.form.get('text', '')
        
        if not text_content or len(text_content.strip()) == 0:
            return jsonify({'error': 'Text content or PDF file is required'}), 400
        
        if len(text_content) > 3000:
            text_content = text_content[:3000]
        
        prompt = f"""Create concise study notes from the following content:

{text_content}

Generate:
• SUMMARY: Write 2-3 sentences summarizing the main idea
• KEY POINTS: List 5-7 important points as bullet points
• IMPORTANT CONCEPTS: Highlight key terms and definitions
• KEY TAKEAWAYS: List 3-4 main lessons to remember

Format with clear headings and bullet points."""
        
        notes = query_ai(prompt)
        
        if not notes or notes == "AI response generated.":
            # Fallback if AI fails
            sentences = text_content.split('. ')[:5]
            notes = f"""STUDY NOTES

SUMMARY:
{'. '.join(sentences[:2])}.

KEY POINTS:
• {sentences[0] if len(sentences) > 0 else 'Main concept'}
• {sentences[1] if len(sentences) > 1 else 'Important detail'}
• {sentences[2] if len(sentences) > 2 else 'Key information'}

KEY TAKEAWAYS:
✓ Essential understanding from the material
✓ Important concept to remember
✓ Critical knowledge point
"""
        
        return jsonify({'notes': notes, 'success': True})
    except Exception as e:
        print(f"Notes Generator Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
