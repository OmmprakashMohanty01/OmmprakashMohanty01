import os
import re

assets_dir = "/Users/ommprakashmohanty/.gemini/antigravity-ide/scratch/ommprakashmohanty/assets"

replacements = {
    # Names and Global
    "UDIT GUPTA": "OMMPRAKASH MOHANTY",
    "UDIT": "OMMPRAKASH",
    "GUPTA": "MOHANTY",
    "Udit": "Ommprakash",
    "Gupta": "Mohanty",
    "@Ug0510": "@OmmprakashMohanty01",
    "Ug0510": "OmmprakashMohanty01",
    "UG0510": "OMMPRAKASHMOHANTY01",
    "UG /": "OM /",
    "UG": "OM",
    
    # Titles and Bio
    "SDE @ Amazon": "Software Engineer &amp; Data Analyst",
    "SDE @ AMAZON": "SOFTWARE ENGINEER",
    "Tech Mentor": "Data Analyst",
    "Creator of Grow with Udit": "Computer Vision",
    "Tier-3 to FAANG": "AI &amp; Data Analytics",
    "Building scalable software &amp; helping engineers": "Building scalable software and",
    "crack tech careers.": "backend operations.",
    
    # Location
    "BENGALURU, IN": "BHUBANESWAR, IN",
    "Bengaluru": "Bhubaneswar",
    "BENGALURU / INDIA": "BHUBANESWAR / INDIA",
    "Amazon": "Data Analyst",
    
    # Stats matching for inject_stats.py
    "12 stars": "{{STARS}} stars",
    "50 repos": "{{REPOS}} repos",
    "TOPMATE": "followers", # to match {{FOLLOWERS}} followers if we want, but let's just make it 'followers'
    
    # connect.svg
    "Grow with Udit": "Ommprakash Mohanty",
    "@grow.with_udit": "@OmmprakashMohanty01",
    "topmate.io/udit_gupta5": "mailto:ommprakashmohanty@gmail.com",
    "Topmate": "Email",
    
    # about-life.svg
    "Modern Web &amp; App Dev": "Modern Web Development",
    "From first interaction to production.": "Building scalable applications.",
    "AI &amp; Cloud Integration": "AI Evaluation &amp; Data Analytics",
    "Scalable systems. Useful intelligence.": "Extracting insights from data.",
    "Community Mentorship": "Backend Operations",
    "Making the next step less uncertain.": "Automating workflows and analytics.",
    "Creating Tech Content": "Continuous Learning",
    "Tech lessons, made human.": "Always exploring new technologies.",
    "1:1 Career Mentorship": "Systems Design",
    "A clearer roadmap. A stronger engineer.": "Building robust backend systems.",
    "Competitive Programming": "Computer Vision Research",
    "For the joy of a problem, solved.": "Cross-view player association.",
    
    # stack.svg
    "Java": "Python",
    "Python": "SQL", # Need to be careful here: Java->Python, Python->SQL
    # Let's handle stack replacements sequentially but safely
}

stack_replacements = {
    "Java": "Python",
    "TypeScript": "TypeScript",
    "Python": "SQL", 
    "React": "React.js",
    "Next.js": "Next.js",
    "Node.js": "FastAPI",
    "Express": "Cloud Native",
    "AWS": "Docker",
    "LLM APIs": "Computer Vision"
}

dashboard_replacements = {
    "professional-resume-builder": "Cross-View Player Association",
    "CS-Council-Website": "Backend Sales Tracker",
    "CurrencyConverter": "Market Analytics Tool",
    "Gemini-Clone": "Business RAG QA Bot",
    "Building scalable software at Amazon": "Building scalable backend systems.",
    "Sharing the roadmap through Grow with Udit.": "Evaluating AI models and analyzing data.",
    "PUBLIC GITHUB": "repos",
    "RECEIVED": "stars"
}

style_injection = """
<style>
  @media (prefers-color-scheme: light) {
    /* Invert main text for light mode */
    text { fill: #1a202c !important; }
    .mono { fill: #4a5568 !important; }
    /* Invert backgrounds */
    rect[fill="#070b16"], rect[fill="#0b1323"] { fill: #f7fafc !important; stroke: #e2e8f0 !important; }
    path[stroke="#193057"], path[stroke="#24334d"] { stroke: #cbd5e0 !important; }
  }
  
  /* CSS Animations */
  @keyframes pulseBlue {
    0% { r: 4; opacity: 1; }
    50% { r: 6; opacity: 0.4; }
    100% { r: 4; opacity: 1; }
  }
  .pulse { animation: pulseBlue 1.5s infinite ease-in-out; }
  
  @keyframes slowRotate {
    from { transform: rotate(0deg); transform-origin: center; }
    to { transform: rotate(360deg); transform-origin: center; }
  }
  .rotate-bg { animation: slowRotate 60s linear infinite; }
</style>
"""

for file in os.listdir(assets_dir):
    if file.endswith(".svg"):
        file_path = os.path.join(assets_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Apply global replacements
        for old_str, new_str in replacements.items():
            content = content.replace(old_str, new_str)
            
        # Apply specific replacements based on filename
        if file == "stack.svg":
            # Avoid the Python -> SQL replacing the Java -> Python
            # Replace old ones with temporary strings
            temp_stack = {}
            for k, v in stack_replacements.items():
                temp_k = f"TEMP_{k}_TEMP"
                content = content.replace(k, temp_k)
                temp_stack[temp_k] = v
            for temp_k, new_v in temp_stack.items():
                content = content.replace(temp_k, new_v)
                
        if file == "id-dashboard.svg":
            for k, v in dashboard_replacements.items():
                content = content.replace(k, v)
                
        # Ensure image hrefs are easily swappable
        content = re.sub(r'<image[^>]*href="data:image[^>]*>', '<!-- PLACEHOLDER_FOR_YOUR_IMAGE: <image x="0" y="0" width="100%" height="100%" href="[YOUR_BASE64_OR_URL]" clip-path="url(#hero-outer)"/> -->', content)
        
        # Inject CSS
        if "<style>" not in content:
            if "</defs>" in content:
                content = content.replace("</defs>", f"</defs>\n{style_injection}")
            else:
                content = re.sub(r'(<svg[^>]*>)', r'\1\n' + style_injection, content, count=1)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("SVG text successfully customized for Ommprakash.")
