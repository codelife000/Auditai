from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
from collections import Counter

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_with_ai(scan_data):
    # Extract keywords from page text
    keywords = []
    if "paragraph_count" in scan_data and scan_data["paragraph_count"] > 0:
        # Dummy keywords from headings
        keywords = re.findall(r'\b\w+\b', scan_data.get("title",""))[:10]

    prompt = f"""
You are a website audit expert.
Analyze this website scan data and return:
1) issues
2) suggestions
3) top keywords (list)
4) heading counts

Respond ONLY in JSON with keys:
- issues (list)
- suggestions (list)
- keywords (list)
- headings_count (dict)
Scan Data:
{json.dumps(scan_data, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a website audit expert"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        content = response.choices[0].message.content
        ai_report = json.loads(content)
        # fallback for missing keys
        ai_report.setdefault("keywords", keywords)
        ai_report.setdefault("headings_count", scan_data.get("headings_count", {}))
        return ai_report
    except Exception:
        return {
            "issues": [
                f"H1 tags found: {scan_data.get('h1_count', 0)}",
                f"Images without ALT: {scan_data.get('images_without_alt', 0)}",
                f"Page load time: {scan_data.get('load_time', 0)}s"
            ],
            "suggestions": [
                "Add missing meta description",
                "Optimize images and include ALT text",
                "Improve page speed"
            ],
            "keywords": keywords,
            "headings_count": scan_data.get("headings_count", {})
        }
