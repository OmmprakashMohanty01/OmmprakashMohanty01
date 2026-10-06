import os
import re

assets_dir = "/Users/ommprakashmohanty/.gemini/antigravity-ide/scratch/ommprakashmohanty/assets"

for file in os.listdir(assets_dir):
    if file.endswith(".svg"):
        with open(os.path.join(assets_dir, file), "r", encoding="utf-8") as f:
            content = f.read()
        texts = re.findall(r'>([^<]+)</text>', content)
        print(f"--- {file} ---")
        for t in texts:
            if t.strip() and not t.strip().startswith('0510'):
                print(t.strip())
