#!/usr/bin/env python3
import json
import sys
import datetime

if len(sys.argv) < 3:
    print("Usage: python generate_streak_svg.py <username> <output.svg>")
    sys.exit(1)

USERNAME = sys.argv[1]
OUT_FILE = sys.argv[2]

try:
    with open("data/contributions.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: data/contributions.json not found. Run fetch_contributions.py first.")
    sys.exit(1)

days = data["days"]
total_contribs = data["total_contributions"]

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="888" height="158" viewBox="0 0 888 158" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">
<style>
  text.lbl { fill:#7d8590; font-size:13px; font-weight:600; }
  text.total { fill:#e6edf3; font-size:15px; font-weight:700; }
  .c { transform-box:fill-box; transform-origin:center; opacity:0; animation:pop 0.55s ease-out both; }
  .g { animation:pop 0.55s ease-out both, flash 0.70s ease-out both; }
  @keyframes pop { 0%{opacity:0;transform:scale(.2)} 60%{opacity:1;transform:scale(1.1)} 100%{opacity:1;transform:scale(1)} }
  @keyframes flash { 0%{filter:brightness(2.4)} 45%{filter:brightness(2.4)} 100%{filter:brightness(1)} }
  @media (prefers-reduced-motion: reduce) { .c { opacity:1 !important; animation:none !important; } }
</style>
<rect width="888" height="158" fill="none"/>
<text class="lbl" x="2" y="51">Mon</text><text class="lbl" x="2" y="83">Wed</text><text class="lbl" x="2" y="115">Fri</text>
'''

def get_color(count):
    if count == 0: return "#161b22"
    elif count <= 2: return "#0e4429"
    elif count <= 5: return "#006d32"
    elif count <= 10: return "#26a641"
    else: return "#39d353"

x = 34
delay = 0.05
months_added = []

# Group flat days list into weeks (starting on Sunday)
weeks = []
current_week = []
for d in days:
    date_obj = datetime.datetime.strptime(d["date"], "%Y-%m-%d")
    weekday = (date_obj.weekday() + 1) % 7 # 0=Sun, 1=Mon...
    current_week.append((date_obj, d["count"], weekday))
    if weekday == 6: # Saturday ends the week
        weeks.append(current_week)
        current_week = []
if current_week:
    weeks.append(current_week)

# Draw the SVG
for week in weeks:
    added_month = False
    for date_obj, count, weekday in week:
        month_name = date_obj.strftime("%b")
        
        # FIX: Place label immediately when a new month is encountered in a column
        if month_name not in months_added and not added_month:
            svg += f'<text class="lbl" x="{x}" y="16">{month_name}</text>\n'
            months_added.append(month_name)
            added_month = True
            
        y_pos = 24 + (weekday * 16)
        color = get_color(count)
        classes = "c g" if count > 0 else "c"
        svg += f'<rect class="{classes}" x="{x}" y="{y_pos}" width="13" height="13" rx="2.5" fill="{color}" style="animation-delay:{delay:.2f}s"/>\n'
        
    x += 16
    delay += 0.05

svg += f'<text class="total" x="34" y="152">{total_contribs} contributions in the last year</text>\n</svg>'

with open(OUT_FILE, "w") as f:
    f.write(svg)
print(f"Successfully generated {OUT_FILE}")
