import os
import re

assets_dir = "/Users/ommprakashmohanty/.gemini/antigravity-ide/scratch/ommprakashmohanty/assets"

formal_photo = "https://github.com/user-attachments/assets/bca1c636-c566-4ad4-9317-fd98ff7a75c8"
casual_photo = "https://github.com/user-attachments/assets/1ff9d08e-73bb-4480-a7eb-03fe29d389e6"

for file in os.listdir(assets_dir):
    if not file.endswith(".svg"):
        continue
    filepath = os.path.join(assets_dir, file)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if file == "hero.svg":
        # Replace the href in <image> tag
        content = re.sub(r'(<image[^>]*href=")[^"]*("[^>]*>)', r'\g<1>' + formal_photo + r'\g<2>', content)
    elif file in ["about-life.svg", "id-dashboard.svg", "connect.svg"]:
        # Replace the href in <image> tag
        content = re.sub(r'(<image[^>]*href=")[^"]*("[^>]*>)', r'\g<1>' + casual_photo + r'\g<2>', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Images updated!")
