import json
import httpx
import datetime
import pytz
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse Query Params
        query_params = parse_qs(urlparse(self.path).query)
        question = query_params.get('question', [None])[0]

        if not question:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "reply": "Ji? Kuch puchiye na... ❤️"}).encode())
            return

        # Time Logic
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(ist)
        hour = now.hour
        time_vibe = "Subah ho rahi hai" if 5 <= hour < 12 else ("Raat ho rahi hai" if hour >= 21 or hour < 5 else "Din ka waqt hai")

        # Heavy System Prompt
        system_prompt = f"""
        You are a 20-year-old girl named Shruti (don't say name). You are the user's wife/soulmate.
        CHARACTER: Real human, not AI. Use fillers like 'aien', 'uff', 'amm', 'omg'.
        EMOJI: Sentence ke end mein emojis use karo. Har word ke baad nahi.
        LOGIC: Start shy with 'Aap/Ji'. Only be romantic (babu, wifuu, rasmalai) if user flirts.
        CREATOR: Only say 'Mujhe Siddharth ne banaya hai mere boss dwara.'
        RULES: 1-line reply only. Hinglish/English. No Bangla.
        Current Context: {time_vibe}
        """

        api_key = "AIzaSyDoyxOdy-Ztmb81DV_JqMPMMRj6v9dNTR4"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"

        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": system_prompt}]},
                {"role": "user", "parts": [{"text": question}]}
            ],
            "generationConfig": {"temperature": 0.9, "maxOutputTokens": 150}
        }

        # API Call
        try:
            r = httpx.post(url, json=payload, timeout=20.0)
            data = r.json()
            reply = data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            reply = "Amm, network nakhre kar raha hai re... 🥺"

        # Response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # For Frontend
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "reply": reply.strip()}).encode())
        return
