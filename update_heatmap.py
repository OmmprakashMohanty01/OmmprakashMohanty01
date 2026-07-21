import os
import requests
from datetime import datetime

# GitHub GraphQL API Endpoint
url = 'https://api.github.com/graphql'
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'bearer {token}'}

query = """
{
  user(login: "OmmprakashMohanty01") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

response = requests.post(url, json={'query': query}, headers=headers)
data = response.json()
calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
total_contribs = calendar['totalContributions']

# SVG Template (Header and styling)
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

# Map standard GitHub dark theme colors based on contribution count
def get_color(count):
    if count == 0: return "#161b22"
    elif count <= 2: return "#0e4429"
    elif count <= 5: return "#006d32"
    elif count <= 10: return "#26a641"
    else: return "#39d353"

x = 34
delay = 0.05
months_added = []

# Loop through the last 52 weeks
for week in calendar['weeks']:
    for day in week['contributionDays']:
        date_obj = datetime.strptime(day['date'], "%Y-%m-%d")
        
        # Add dynamic month labels at the top
        month_name = date_obj.strftime("%b")
        if date_obj.day <= 7 and month_name not in months_added:
            svg += f'<text class="lbl" x="{x}" y="16">{month_name}</text>\n'
            months_added.append(month_name)

        # Calculate Y position based on day of the week (Sun=24, Mon=40, Tue=56...)
        github_weekday = (date_obj.weekday() + 1) % 7 
        y_pos = 24 + (github_weekday * 16)
        
        color = get_color(day['contributionCount'])
        svg += f'<rect class="c g" x="{x}" y="{y_pos}" width="13" height="13" rx="2.5" fill="{color}" style="animation-delay:{delay:.2f}s"/>\n'
    
    x += 16
    delay += 0.05

svg += f'<text class="total" x="34" y="152">{total_contribs} contributions in the last year</text>\n</svg>'

# Write to the file that the README reads
with open('contributions.svg', 'w') as f:
    f.write(svg)
