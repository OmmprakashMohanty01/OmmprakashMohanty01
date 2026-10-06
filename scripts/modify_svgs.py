import os
import re

base_dir = "/Users/ommprakashmohanty/.gemini/antigravity-ide/scratch/ommprakashmohanty"
assets_dir = os.path.join(base_dir, "assets")

replacements = {
    "UDIT": "[FIRST_NAME]",
    "GUPTA": "[LAST_NAME]",
    "Udit": "[First_Name]",
    "Gupta": "[Last_Name]",
    "@Ug0510": "[YOUR_USERNAME]",
    "Ug0510": "[YOUR_USERNAME]",
    "SDE @ Amazon": "[PROFESSIONAL TITLE]",
    "Tier-3 to FAANG": "[YOUR BIO / TAGLINE]",
    "Bengaluru": "[LOCATION]",
    "12 stars": "{{STARS}} stars",
    "50 repos": "{{REPOS}} repos",
    "37 Topmate bookings": "{{FOLLOWERS}} followers",
    "Building scalable software & helping engineers": "[BIO LINE 1]",
    "crack tech careers.": "[BIO LINE 2]"
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
  @media (prefers-color-scheme: dark) {
    /* Explicit dark mode fallback */
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

# Modify SVG files
for file in os.listdir(assets_dir):
    if file.endswith(".svg"):
        file_path = os.path.join(assets_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Apply string replacements
        for old_str, new_str in replacements.items():
            content = content.replace(old_str, new_str)
        
        # Ensure image hrefs are easily swappable
        content = re.sub(r'<image[^>]*href="data:image[^>]*>', '<!-- PLACEHOLDER_FOR_YOUR_IMAGE: <image x="0" y="0" width="100%" height="100%" href="[YOUR_BASE64_OR_URL]" clip-path="url(#hero-outer)"/> -->', content)
        
        # Inject CSS
        if "<style>" not in content:
            # Inject right after <defs> or <svg ...>
            if "</defs>" in content:
                content = content.replace("</defs>", f"</defs>\n{style_injection}")
            else:
                content = re.sub(r'(<svg[^>]*>)', r'\1\n' + style_injection, content, count=1)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# Modify README.md
readme_path = os.path.join(base_dir, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    for old_str, new_str in replacements.items():
        readme_content = readme_content.replace(old_str, new_str)
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

print("Modification complete.")
