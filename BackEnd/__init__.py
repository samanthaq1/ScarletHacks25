import google.generativeai as genai

genai.configure(api_key="API key")

model = genai.GenerativeModel('gemini-2.0-flash')

maps_key = "API key"