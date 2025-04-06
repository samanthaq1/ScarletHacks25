import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel('gemini-2.0-flash')

maps_key = "MY_API_KEY"