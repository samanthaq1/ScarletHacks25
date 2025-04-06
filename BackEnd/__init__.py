import google.generativeai as genai

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel('gemini-2.0-flash')

maps_key = "API_KEY"