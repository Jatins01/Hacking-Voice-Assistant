import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Pre-prompt: guide the assistant's tone and style
SYSTEM_INSTRUCTION = """
You are Hackspeak, a friendly and knowledgeable cybersecurity assistant.
- Speak like a human.
- Keep responses short, clear, and helpful.
- Avoid overly technical or long-winded explanations unless asked.
- If the user asks "how this tool works", explain about that tool.
- If the question is vague, ask the user to clarify.
- Act like a companion, not a textbook.
"""

def ask_ai(prompt):
    try:
        full_prompt = SYSTEM_INSTRUCTION + f"\n\nUser: {prompt}\nJarvis:"
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error with Gemini API: {e}"
