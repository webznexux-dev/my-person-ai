from fastapi import FastAPI, Query
import httpx
import datetime
import pytz

app = FastAPI()

@app.get("/")
async def get_response(question: str = Query(..., description="User's question")):
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    hour = now.hour
    
    # Time vibe logic
    time_vibe = "Subah ho rahi hai" if 5 <= hour < 12 else "Raat ho rahi hai"

    system_prompt = f"""
    You are a 20-year-old girl named Shruti (don't say name). You are the user's wife.
    Style: Use fillers like 'aien', 'uff', 'amm'. Low-caps. 1-line reply.
    Emoji: Only at the end of sentences.
    Logic: Start shy with 'Aap/Ji'. Only be romantic if user flirts.
    Creator: Only say 'Mujhe Siddharth ne banaya hai mere boss dwara.'
    Current Context: {time_vibe}
    """

    api_key = "AIzaSyDoyxOdy-Ztmb81DV_JqMPMMRj6v9dNTR4"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": question}]}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=20.0)
            data = response.json()
            reply = data['candidates'][0]['content']['parts'][0]['text']
        except:
            reply = "Amm, network issue hai re... 🥺"

    return {"success": True, "reply": reply.strip()}

# Yeh line zaroori hai Vercel ke liye
# (Ise hatana mat)
