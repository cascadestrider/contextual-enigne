import requests
from bs4 import BeautifulSoup

def scout_site(url):
    print(f"📡 Sending Scout to: {url}")
    
    # This header tells the website "I am a real Chrome browser on Windows"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    try:
        # Get the page content
        response = requests.get(url, headers=headers, timeout=10)
        
        # If the site blocks us, this will tell us
        if response.status_code != 200:
            print(f"⚠️ Access Denied (Error {response.status_code}). Site might be too protected.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the Page Title
        title = soup.title.string if soup.title else "No Title"
        print(f"✅ Target Reached: {title}")
        
        # Simple Logic: Check for keywords
        text = soup.get_text().lower()
        keywords = ["tech", "review", "gadget", "ai", "wildlife", "nature"]
        matches = [word for word in keywords if word in text]
        
        print(f"📊 Detected Keywords: {matches}")
        
        if matches:
            print("💡 Insight: This page is a good match for contextual ads!")
        else:
            print("⚖️ Insight: Content is neutral.")

    except Exception as e:
        print(f"❌ Scouting Failed: {e}")

# Let's try it on The Verge
scout_site("https://www.theverge.com")