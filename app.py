import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, abort, session
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')

# --- GEMINI CONFIGURATION ---
GENAI_KEY = os.environ.get("GEMINI_API_KEY")
if GENAI_KEY:
    genai.configure(api_key=GENAI_KEY)

# --- SYSTEM CONTEXT FOR CHATBOT (The "Brain") ---
# This string contains EVERYTHING from the resumes so the bot knows it.
# --- SYSTEM CONTEXT FOR CHATBOT (The "Brain") ---
SYSTEM_CONTEXT = """
You are the AI Concierge for icElit.ai and your name is IceBot. You are elite, professional, and technical.
Your tone is confident, futuristic, and precise.

/// COMPANY IDENTITY: icElit.ai
"Intelligence That Scales."
icElit.ai is a next-generation Artificial Intelligence company focused on bridging the gap between academic research and industrial-grade deployment. 
We specialize in Generative AI, Multi-Agent Systems, and High-Performance Computing.

/// TEAM EXPERIENCE & AUTHORITY (CRITICAL CONTEXT)
While icElit.ai is a fresh entity, the founding team possesses a deep, cumulative engineering background:
- **3-4 Years of Indirect Experience:** The founders have been deeply embedded in AI research, algorithm optimization, and complex system design during their rigorous academic tenures (Honors degrees) and internships at prestigious institutions (DRDO, ISRO, IITs).
- **1+ Year of Direct Production Experience:** The team has successfully deployed real-world solutions for US-based clients (OMICS International) and Indian enterprises, handling production traffic, payment gateways, and large-scale data pipelines.
- **Engineering Mindset:** We are not just script-kiddies; we are Systems Architects who build custom sparse matrix storage formats, optimize edge-native computer vision, and architect multi-agent orchestration layers.

/// FOUNDING TEAM PROFILES

1. ARUPA NANDA SWAIN (CTO & Systems Architect)
   - Phone: +91 7735460467 | Email: arupaswain7735@gmail.com
   - Location: Hyderabad, Telangana
   - Core Competency: High-Performance Backend & Storage Optimization.
   - Experience: 1+ Year Direct | 4 Years R&D.
   - Key Achievement: Invented 'Contiguous Clustering' Sparse Matrix format (30-50% memory reduction).
   - Tech Stack: Go, FastAPI, C/C++, System Design.

2. ASHUTOSH MISHRA (Head of AI Research)
   - Phone: +91 95718 21291 | Email: ashutoshmishra21oct2003@gmail.com
   - Location: Bhubaneswar, Odisha
   - Core Competency: LLM Agents, NLP, & Deep Learning Theory.
   - Experience: 1+ Year Direct | 3.5 Years R&D.
   - Key Achievement: Reduced manual content creation by 80% using Multi-Agent Systems.
   - Tech Stack: TensorFlow, PyTorch, LangChain, RAG Pipelines.

3. BAVISETTI DANIEL (Lead ML Engineer & MLOps)
   - Phone: +91 9121592164 | Email: daniel.bavisetti0579@gmail.com
   - Location: Hyderabad, India
   - Core Competency: Computer Vision, Edge AI, & MLOps Pipelines.
   - Experience: 1+ Year Direct | 3.5 Years R&D.
   - Key Achievement: Real-time IoT vehicle detection at 24 FPS on edge hardware.
   - Tech Stack: YOLO, OpenCV, Docker/Kubernetes, IoT.

/// SERVICES
- Custom LLM Agents & RAG Pipelines.
- Computer Vision for Edge/IoT.
- High-Throughput Data Scraping & Automation.
- Full-Stack AI Product Development.

If a user asks about experience, emphasize the "3-4 years of rigorous R&D and 1+ year of production deployment."

COMPANY MISSION: icElit.ai builds production-grade AI. We don't just wrap APIs; we build custom architectures, sparse matrix optimizations, and edge-native computer vision.
"""

# --- EXPANDED TEAM DATA ---
TEAM_DATA = {
    "arupa-swain": {
        "name": "Arupa Nanda Swain",
        "role": "CTO & Systems Architect",
        "image": "arupa.jpg",  # Ensure this file exists in static/assets/
        "tagline": "Redefining storage formats and backend scalability.",
        "bio": "Expert in full-stack development and algorithm optimization. Arupa demonstrated expertise in developing scalable web applications and conducting innovative research in sparse matrix optimization, achieving 30-50% memory reduction and 10x performance improvements.",
        "email": "arupaswain7735@gmail.com",
        "phone": "+91 7735460467",
        "socials": {"linkedin": "https://linkedin.com/in/arupa-nanda-swain", "github": "https://github.com/arupa444",
                    "twitter": "https://x.com/arupa_swain"},
        "skills": ["Go", "FastAPI", "Sparse Matrix", "C/C++", "System Design", "LangChain"],
        "experience": [
            {"role": "AI Developer", "company": "OMICS International", "time": "06/2025 - Present",
             "desc": "Designed LLM-powered solution integrating FastAPI, Gemini, and Groq models reducing manual workload by 60%."},
            {"role": "Full-Stack Developer", "company": "The Little Journal", "time": "04/2024 - 06/2025",
             "desc": "Architected literary publishing platform serving Times of India clients; implemented custom CMS with automated PDF generation."},
            {"role": "Full-Stack Developer", "company": "Coincent.ai", "time": "04/2023 - 07/2023",
             "desc": "Delivered doctor appointment booking platform achieving 300+ monthly appointment increase through optimized workflows."},
            {"role": "Microcontroller Programmer", "company": "CTTC", "time": "07/2021 - 03/2022",
             "desc": "Programmed Arduino-based motion control for 6-axis humanoid robot."}
        ],
        "projects": [
            {"title": "Sparse Matrix Storage (CC)", "tech": "C++ / Research",
             "desc": "Invented novel storage format enabling 30-50% memory savings and 10x acceleration in SpMV."},
            {"title": "Compound AI Journal System", "tech": "Gemini / Groq",
             "desc": "Orchestrated multi-LLM pipeline automating research article generation from metadata to HTML/PDF."},
            {"title": "Author Contact Extraction", "tech": "FastAPI / SMTP",
             "desc": "Built toolkit scraping contacts from PubMed with three-phase validation (DNS/MX) for 1,000+ contacts."},
            {"title": "Career Pilot AI", "tech": "Selenium / LLM",
             "desc": "Architected AI career assistant automating job discovery and application submission."},
            {"title": "SwaraVision", "tech": "TensorFlow / CNN",
             "desc": "Trained object detection model recognizing Indian classical music notes with 96%+ accuracy."},
            {"title": "DenseNet-201 Fine-Tuning", "tech": "FastAI",
             "desc": "Achieved 98% accuracy on image classification through one-cycle policy optimization."}
        ],
        "resume_link": "arupa_resume.pdf"
    },
    "ashutosh-mishra": {
        "name": "Ashutosh Mishra",
        "role": "Head of AI Research",
        "image": "ashutosh.jpg",
        "tagline": "Architecting Multi-Agent Systems & Deep Learning Logic.",
        "bio": "Specializing in Large Language Models and multi-agent systems. Ashutosh has a strong foundation in machine learning theory, optimization, and scalable model deployment using TensorFlow and Hugging Face. He builds systems that think.",
        "email": "ashutoshmishra21oct2003@gmail.com",
        "phone": "+91 95718 21291",
        "socials": {"linkedin": "https://linkedin.com/in/ashutosh-mishra-99b07b221",
                    "github": "https://github.com/Ashutosh-Mishra21"},
        "skills": ["Multi-Agent Systems", "LLMs", "TensorFlow", "RAG", "Prompt Engineering", "NLP"],
        "experience": [
            {"role": "AI Developer", "company": "OMICS International", "time": "07/2025 - Present",
             "desc": "Engineered multi-agent AI systems increasing operational effectiveness by 40%; reduced handwritten paperwork by 70%."},
            {"role": "Data Science Intern", "company": "Exposys Data Labs", "time": "05/2024 - 06/2024",
             "desc": "Created regression models to forecast startup profitability; performed EDA improving accuracy to 98%."}
        ],
        "projects": [
            {"title": "Compound AI System (Semi-AI Agent)", "tech": "Python / FastAPI / Gemini",
             "desc": "Designed multi-agent system reducing manual content creation by 80% and improving coherence by 35%."},
            {"title": "Transformer Model Study", "tech": "NLP / Hugging Face",
             "desc": "Benchmarked multiple Transformer architectures on Amazon product reviews for sentiment analysis."},
            {"title": "Neural Network From Scratch", "tech": "NumPy / Python",
             "desc": "Built a feed-forward NN with backpropagation achieving 94% accuracy on synthetic data."},
            {"title": "OCR System Using YOLO", "tech": "YOLO / OpenCV",
             "desc": "Created end-to-end OCR pipeline integrating object detection to localize text regions."},
            {"title": "L2 Regularization Implementation", "tech": "Math / Optimization",
             "desc": "Implemented custom gradient descent and L2 regularization reducing overfitting by 25%."}
        ],
        "resume_link": "ashutosh_resume.pdf"
    },
    "bavisetti-daniel": {
        "name": "Bavisetti Daniel",
        "role": "Lead ML Engineer & MLOps",
        "image": "daniel.jpg",
        "tagline": "High-throughput pipelines and Real-time Edge AI.",
        "bio": "Machine Learning Engineer specializing in Python, TensorFlow, and PyTorch. Daniel excels in high-throughput ML pipelines and real-time CV/NLP systems, optimizing edge-based inference on IoT hardware.",
        "email": "daniel.bavisetti0579@gmail.com",
        "phone": "+91 9121592164",
        "socials": {"linkedin": "https://linkedin.com/in/daniel-bavisetti",
                    "github": "https://github.com/Daniel-Bavisetti", "portfolio": "https://daniel-bavisetti.github.io"},
        "skills": ["MLOps", "Computer Vision", "IoT", "Docker", "Kubernetes", "Data Engineering"],
        "experience": [
            {"role": "AI Developer", "company": "OMICS International", "time": "08/2025 - Present",
             "desc": "Built LLM-powered summarization system and high-throughput scraper (5,000+ entries validated)."},
            {"role": "AI/ML Intern", "company": "Labmentix", "time": "07/2025 - 08/2025",
             "desc": "Developed CSAT prediction system on 85K+ records achieving 89.2% accuracy."},
            {"role": "Research Intern", "company": "NIT Rourkela", "time": "05/2024 - 07/2024",
             "desc": "Designed IoT Smart Parking System with YOLOv5 trained on 15,000+ images (95% accuracy)."}
        ],
        "projects": [
            {"title": "Smart Vehicle Detection", "tech": "YOLOv5 / IoT",
             "desc": "Deployed real-time multi-vehicle tracking pipeline processing 24 FPS on edge hardware."},
            {"title": "Web Scraper for Contact Extraction", "tech": "FastAPI / SMTP",
             "desc": "Extracted and validated 10k+ author contacts with a three-stage verification pipeline."},
            {"title": "Image Steganography", "tech": "MATLAB / Block-DCT",
             "desc": "Implemented pipeline using Block-DCT + Huffman encoding achieving 5+% distortion rate."},
            {"title": "MEMC-Net", "tech": "Deep Learning",
             "desc": "Motion Estimation and Motion Compensation network for video frame reconstruction."},
            {"title": "Resource Allocation Simulator", "tech": "Graph Theory",
             "desc": "Interactive tool handling 50+ nodes/processes for deadlock detection."},
            {"title": "Customer Support Data Analysis", "tech": "NLP / TF-IDF",
             "desc": "Achieved 89.2% accuracy in predicting CSAT from support records."}
        ],
        "resume_link": "daniel_resume.pdf"
    }
}
PROJECTS_SUMMARY = [
    {"title": "Autonomous Research Agent", "category": "GenAI / NLP", "desc": "Multi-LLM orchestration pipeline utilizing Gemini & LLaMA.", "impact": "80% Reduction in time", "stack": ["LangChain", "FastAPI", "Groq"]},
    {"title": "Edge-Native VisionFlow", "category": "Computer Vision", "desc": "Real-time object detection optimized for IoT hardware.", "impact": "98% Accuracy @ 24FPS", "stack": ["YOLO", "OpenCV", "IoT"]},
    {"title": "High-Scale Data Extraction", "category": "Data Engineering", "desc": "Three-phase verification scraper processing 10k+ entities.", "impact": "100k+ Validated Records", "stack": ["Python", "SMTP", "Distributed"]}
]


@app.route('/chat', methods=['POST'])
def chat():
    if not GENAI_KEY:
        return jsonify({'response': "AI System Offline (Missing API Key). Contact Admin."})

    user_msg = request.json.get('message', '')

    # --- CONTEXT LOGIC ---
    # Retrieve history from session or initialize empty list
    history = session.get('chat_history', [])

    # Create the prompt with history
    # We format history as a dialogue script to keep context
    conversation_so_far = ""
    for turn in history[-10:]:  # Keep last 10 turns to save tokens
        conversation_so_far += f"User: {turn['user']}\nAI: {turn['ai']}\n"

    full_prompt = f"{SYSTEM_CONTEXT}\n\nCONVERSATION HISTORY:\n{conversation_so_far}\n\nCURRENT USER QUERY: {user_msg}\nAI RESPONSE:"

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(full_prompt)
        ai_reply = response.text

        # Update History
        history.append({'user': user_msg, 'ai': ai_reply})
        session['chat_history'] = history

        return jsonify({'response': ai_reply})
    except Exception as e:
        return jsonify({'response': f"Neural Link Error: {str(e)}"})


# ... (Keep context_processor, home, profile routes the same)
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def home():
    team_summary = []
    for slug, data in TEAM_DATA.items():
        team_summary.append({
            "name": data["name"],
            "role": data["role"],
            "image": data["image"],
            "slug": slug,
            "skills": data["skills"][:4]
        })
    return render_template('index.html', team=team_summary, projects = PROJECTS_SUMMARY)


@app.route('/team/<slug>')
def profile(slug):
    member = TEAM_DATA.get(slug)
    if not member:
        abort(404)
    return render_template('profile.html', member=member)


@app.route('/download/<filename>')
def download_resume(filename):
    # Simulated download
    return f"Downloading {filename}..."


if __name__ == '__main__':
    app.run(debug=True, port=5000)