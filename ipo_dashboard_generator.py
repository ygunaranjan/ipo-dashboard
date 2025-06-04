import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import os

# Define sources
news_sources = {
    "Chittorgarh": "https://www.chittorgarh.com/ipo/ipo_news/",
    "ET Markets": "https://economictimes.indiatimes.com/markets/ipos/fpos",
    "Mint": "https://www.livemint.com/market/ipo",
    "Business Standard": "https://www.business-standard.com/category/markets/ipo-news-1020901.htm",
    "The Hindu Business Line": "https://www.thehindubusinessline.com/markets/stock-markets/",
    "Financial Times": "https://www.ft.com/markets"
}

keywords = [
    "file drhp", "planning to file drhp", "preparing drhp",
    "ipo-bound", "to go public", "files draft papers", "files draft prospectus",
    "appoints lead manager", "appoints investment bank", "appoints merchant banker"
]

results = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Scan each source for matches
for source, url in news_sources.items():
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        for keyword in keywords:
            matches = re.findall(rf'([^.]*{keyword}[^.]*\.)', text)
            for match in matches:
                results.append({
                    "Timestamp": timestamp,
                    "Source": source,
                    "Keyword": keyword,
                    "Snippet": match.strip().capitalize(),
                    "URL": url
                })
    except Exception as e:
        results.append({
            "Timestamp": timestamp,
            "Source": source,
            "Keyword": "ERROR",
            "Snippet": f"Failed to fetch: {e}",
            "URL": url
        })

# Create DataFrame
df = pd.DataFrame(results)

# Write HTML dashboard
html = df.to_html(index=False, render_links=True, escape=False, justify="center", border=1)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<html><head><title>IPO Dashboard</title></head><body>")
    f.write(f"<h2>IPO Intention Dashboard - Last Updated: {timestamp}</h2>")
    f.write(html)
    f.write("</body></html>")

# Git auto-commit & push
os.system("git add index.html")
os.system("git commit -m 'Auto update dashboard'")
os.system("git push origin main")
