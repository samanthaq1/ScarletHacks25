import google.generativeai as genai

genai.configure(api_key="AIzaSyAjAILDTv3M41p64ywtAoX3wCYBAzQvEIc")

model = genai.GenerativeModel('gemini-2.0-flash')

maps_key = "MY_API_KEY"