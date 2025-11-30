import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    # Try looking one directory up
    load_dotenv(dotenv_path="../.env")
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: Could not find GOOGLE_API_KEY in .env file.")
else:
    print(f"✅ Key found: {api_key[:5]}...")
    genai.configure(api_key=api_key)

    print("\n🔎 Listing available models for your account:")
    print("---------------------------------------------")
    try:
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"• {m.name}")
                count += 1
        
        if count == 0:
            print("⚠️ No models found. Your API key might not have access to GenAI yet.")
    except Exception as e:
        print(f"❌ Error listing models: {e}")