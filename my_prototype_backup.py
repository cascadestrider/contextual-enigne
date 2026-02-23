import os
import requests
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv
import random
import sqlite3
from datetime import date
import time
from datetime import datetime, timedelta
from googlesearch import search

# 1. INITIALIZATION & BRAND PROFILE
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Torque Optics Brand Profile Integration
TORQUE_TECH = {
    "focus": "Perfect Polarized™ and Q Lens™ Technology.",
    "benefit": "Specifically engineered to enhance digital screen visibility and eliminate HUD blackouts.",
    "hook": "Clarity Without Compromise | See Smarter, Not Harder"
}

# 2. THE BRAIN: AI AD GENERATOR
def get_ai_recommendation(title, content_snippet):
    prompt = f"""
    Webpage: {title}
    Discussion: {content_snippet[:1200]}
    
    TASK: This user is struggling to see their device (Phone/HUD/Computer) through sunglasses. 
    Create a 'High-Intent' ad for Torque Optics using these specific assets: {TORQUE_TECH['focus']}.
    
    Format:
    PROBLEM: [Briefly describe the digital friction]
    TORQUE SOLUTION: [How our tech fixes it]
    AD HEADLINE: [Catchy, solution-oriented text]
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 3. THE SCOUT: RESILIENT PAGE ANALYSIS
def scout_and_analyze(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Handle dynamic encoding
        response.encoding = response.apparent_encoding 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Expanded keywords to ensure we find "Hits"
        friction_words = ["phone", "screen", "hud", "display", "black", "dark", "polarized", "glare", "vision"]
        page_text = soup.get_text().lower()
        
        if any(word in page_text for word in friction_words):
            print(f"🎯 CONVERSION OPPORTUNITY: {url}")
            result = get_ai_recommendation(soup.title.string, page_text)
            print(f"\n{result}\n" + "-"*40)
            return True
        return False
    except Exception:
        return False

# 4. THE LANDSCAPE ANALYZER: 2-YEAR PATTERN HUNT
def run_landscape_analyzer():
    # Looking back from Feb 2024 to Feb 2026
    two_years_ago = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    
    print(f"\n📊 --- TORQUE OPTICS: 2-YEAR LANDSCAPE ANALYSIS ---")
    
    # Using 'site:' and 'after:' operators to force higher-quality results
    queries = [
        f"can't see phone screen polarized sunglasses after:{two_years_ago}",
        f"polarized sunglasses blocking car HUD display reddit",
        f"polarized sunglasses laptop screen forum after:{two_years_ago}"
    ]
    
    site_frequency = {}
    hit_count = 0

    for query in queries:
        print(f"🔍 Analyzing Pattern: {query}")
        # Force the generator to list to avoid timeout issues
        results = list(search(query, num_results=5, sleep_interval=2.0))
        
        for url in results:
            domain = url.split('/')[2]
            site_frequency[domain] = site_frequency.get(domain, 0) + 1
            
            if scout_and_analyze(url):
                hit_count += 1
            time.sleep(random.randint(1, 3)) # Avoid Google blocks

    print("\n🔥 HIGH-INTENT AD HOTSPOTS (Target these domains):")
    sorted_sites = sorted(site_frequency.items(), key=lambda x: x[1], reverse=True)
    for site, count in sorted_sites[:5]:
        print(f"📍 {site} ({count} active friction threads)")
    
    if hit_count == 0:
        print("\n⚪ Note: No live ad impressions triggered this time, but hotspots were mapped.")

if __name__ == "__main__":
    run_landscape_analyzer()