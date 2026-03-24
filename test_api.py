import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print(f"Testing API Key: {api_key[:10]}...{api_key[-4:]}")
print(f"Key length: {len(api_key)}")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-flash-lite-latest")
    response = model.generate_content("Say 'Hello'")
    print("✅ SUCCESS! API Key is valid!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
