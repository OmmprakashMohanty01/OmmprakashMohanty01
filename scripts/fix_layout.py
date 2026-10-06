import os
import re

assets_dir = "/Users/ommprakashmohanty/.gemini/antigravity-ide/scratch/ommprakashmohanty/assets"

avatar_url = "https://avatars.githubusercontent.com/OmmprakashMohanty01"

for file in os.listdir(assets_dir):
    if not file.endswith(".svg"):
        continue
    filepath = os.path.join(assets_dir, file)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix Profile Photos (uncomment and replace URL)
    # The current state might be: <!-- PLACEHOLDER_FOR_YOUR_IMAGE: <image ... href="[YOUR_BASE64_OR_URL]" .../> -->
    # Or it might have been partially uncommented by the user. Let's just use regex.
    content = re.sub(r'<!-- PLACEHOLDER_FOR_YOUR_IMAGE: (<image[^>]*href=")[^"]*("[^>]*/>) -->', r'\1' + avatar_url + r'\2', content)

    # 2. Fix Giant Overlapping Name in hero.svg
    if file == "hero.svg":
        # First name
        content = re.sub(r'(>OMMPRAKASH</text>)', r'\1', content) # Find it
        content = re.sub(r'font-size="142"([^>]*)>OMMPRAKASH', r'font-size="75"\1>OMMPRAKASH', content)
        content = re.sub(r'y="293"([^>]*)>OMMPRAKASH', r'y="320"\1>OMMPRAKASH', content)
        
        # Last name
        content = re.sub(r'font-size="142"([^>]*)>MOHANTY', r'font-size="75"\1>MOHANTY', content)
        content = re.sub(r'y="412"([^>]*)>MOHANTY', r'y="410"\1>MOHANTY', content)
        
        # Background numbers "0510" -> "01"
        content = content.replace("0510", "01")

    # 3. Fix ID Card Name Overflow in id-dashboard.svg
    if file == "id-dashboard.svg":
        content = re.sub(r'font-size="40"([^>]*)>OMMPRAKASH MOHANTY', r'font-size="25"\1>OMMPRAKASH MOHANTY', content)
        
        # Background numbers "0510" -> "01"
        content = content.replace(">0510<", ">01<")
        
        # Grammar fix
        content = content.replace("Building scalable software at Data Analyst", "Building scalable software as a Data Analyst")

    # 4. Clean up typos caused by UG -> OM replacement
    if file == "about-life.svg":
        content = content.replace("THOOMHT", "THOUGHT")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Layouts fixed!")
