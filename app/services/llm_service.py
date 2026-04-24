import json
import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def _clean_json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"):
        text = text.replace("```json", "", 1).strip()
    if text.startswith("```"):
        text = text.replace("```", "", 1).strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    return text

def call_gemini_json(prompt: str) -> dict:
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    text = _clean_json_text(response.text)
    return json.loads(text)

def call_gemini_text(prompt: str) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()