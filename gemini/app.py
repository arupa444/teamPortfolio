from flask import Flask, render_template, request, flash, jsonify, send_file, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'icelit_dev_key')

# --- ENHANCED DATA CONTEXT ---
# Using a dictionary with slugs as keys for O(1) lookup
TEAM_DATA = {
    "arupa-swain": {
        "name": "Arupa Nanda Swain",
        "role": "CTO & Systems Architect",
        "tagline": "Architecting the impossible with sparse matrix optimization.",
        "superpower": "High-Performance Backend Engineering",
        "bio": "A computer science visionary obsessed with efficiency. Arupa doesn't just write code; he redefines storage formats. With research-backed expertise in Sparse Matrix storage (30-50% memory reduction), he bridges the gap between theoretical algorithms and high-scale production systems.",
        "core_metrics": [
            {"label": "Memory Reduced", "value": "50%"},
            {"label": "Perf. Increase", "value": "10x"},
            {"label": "Stack Depth", "value": "Full"}
        ],
        "skills": ["Go", "FastAPI", "System Architecture", "C/C++", "Algorithm Design", "LLM Pipelines"],
        "experience": [
            {"company": "OMICS International", "role": "AI Developer", "period": "06/2025 - 10/2025", "desc": "Designed LLM solutions with Gemini/Groq reducing manual workload by 60%."},
            {"company": "The Little Journal", "role": "Full-Stack Developer", "period": "04/2024 - 06/2025", "desc": "Architected a CMS handling Times of India clients; automated PDF generation."},
            {"company": "Coincent.ai", "role": "Full-Stack Developer", "period": "04/2023 - 07/2023", "desc": "Optimized appointment booking platforms increasing traffic by 300+ monthly."}
        ],
        "projects": [
            {"title": "Sparse Matrix Storage (Research)", "desc": "Invented 'Contiguous Clustering' format tailored for diagonally dominant matrices."},
            {"title": "Compound AI Journal System", "desc": "Orchestrated multi-LLM pipelines for automated research article generation."}
        ],
        "socials": {"linkedin": "#", "github": "#", "twitter": "#"},
        "resume_link": "arupa_resume.pdf"
    },
    "ashutosh-mishra": {
        "name": "Ashutosh Mishra",
        "role": "Head of AI Research",
        "tagline": "Defining the future of Multi-Agent Systems.",
        "superpower": "Agentic AI & LLM Orchestration",
        "bio": "Ashutosh lives at the cutting edge of Generative AI. Specializing in autonomous agents and RAG pipelines, he builds systems that don't just answer questions—they perform complex intellectual labor. His work in reducing content creation time by 80% proves the power of agentic workflows.",
        "core_metrics": [
            {"label": "Automation", "value": "80%"},
            {"label": "Accuracy", "value": "94%"},
            {"label": "Agents Built", "value": "Multi"}
        ],
        "skills": ["LLMs", "Multi-Agent Systems", "TensorFlow", "Prompt Engineering", "RAG", "NLP"],
        "experience": [
            {"company": "OMICS International", "role": "AI Developer", "period": "07/2025 - Present", "desc": "Engineered multi-agent systems increasing operational effectiveness by 40%."},
            {"company": "Exposys Data Labs", "role": "Data Science Intern", "period": "05/2024 - 06/2024", "desc": "Developed regression models forecasting startup profitability with 98% accuracy."}
        ],
        "projects": [
            {"title": "Semi-AI Agent System", "desc": "Integrated Google Gemini and Groq LLaMA for coherence improvements of 35%."},
            {"title": "Transformer Model Study", "desc": "Comprehensive benchmarking of transformer architectures on Amazon datasets."}
        ],
        "socials": {"linkedin": "#", "github": "#"},
        "resume_link": "ashutosh_resume.pdf"
    },
    "bavisetti-daniel": {
        "name": "Bavisetti Daniel",
        "role": "Lead ML Engineer & MLOps",
        "tagline": "Bringing AI to the Edge with high-throughput precision.",
        "superpower": "Scalable Pipelines & Computer Vision",
        "bio": "Daniel ensures AI works in the real world. From processing 100k+ data records to deploying computer vision models on edge IoT hardware at 24 FPS, he is the master of the pipeline. He focuses on robustness, speed, and deployment architecture.",
        "core_metrics": [
            {"label": "Throughput", "value": "100k+"},
            {"label": "Edge Speed", "value": "24 FPS"},
            {"label": "Uptime", "value": "99.9%"}
        ],
        "skills": ["MLOps", "Computer Vision", "IoT", "Docker/Kubernetes", "Data Engineering", "YOLO"],
        "experience": [
            {"company": "OMICS International", "role": "AI Developer", "period": "08/2025 - Present", "desc": "Built high-throughput scrapers validating 5,000+ entries with 98% integrity."},
            {"company": "Labmentix", "role": "AI/ML Intern", "period": "07/2025 - 08/2025", "desc": "CSAT prediction system analysis on 85k+ customer records."}
        ],
        "projects": [
            {"title": "Smart Vehicle Detection", "desc": "IoT-based system with real-time license plate recognition (95% accuracy)."},
            {"title": "Mass-Scale Email Automation", "desc": "SMTP routing system handling dynamic templates and DNS validation."}
        ],
        "socials": {"linkedin": "#", "github": "#", "portfolio": "#"},
        "resume_link": "daniel_resume.pdf"
    }
}

PROJECTS_SUMMARY = [
    {"title": "Autonomous Research Agent", "category": "GenAI / NLP", "desc": "Multi-LLM orchestration pipeline utilizing Gemini & LLaMA.", "impact": "80% Reduction in time", "stack": ["LangChain", "FastAPI", "Groq"]},
    {"title": "Edge-Native VisionFlow", "category": "Computer Vision", "desc": "Real-time object detection optimized for IoT hardware.", "impact": "98% Accuracy @ 24FPS", "stack": ["YOLO", "OpenCV", "IoT"]},
    {"title": "High-Scale Data Extraction", "category": "Data Engineering", "desc": "Three-phase verification scraper processing 10k+ entities.", "impact": "100k+ Validated Records", "stack": ["Python", "SMTP", "Distributed"]}
]

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def home():
    # Pass summary data to home
    team_summary = []
    for slug, data in TEAM_DATA.items():
        team_summary.append({
            "name": data["name"],
            "role": data["role"],
            "bio": data["bio"][:100] + "...", # Short preview
            "skills": data["skills"][:3],
            "slug": slug
        })
    return render_template('index.html', team=team_summary, projects=PROJECTS_SUMMARY)

@app.route('/team/<slug>')
def profile(slug):
    member = TEAM_DATA.get(slug)
    if not member:
        abort(404)
    return render_template('profile.html', member=member)

@app.route('/download/<filename>')
def download_resume(filename):
    return f"Simulating download for {filename}... (Place PDFs in static/docs folder)"

@app.route('/contact', methods=['POST'])
def contact():
    return jsonify({'status': 'success', 'message': 'Intelligence request received.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)