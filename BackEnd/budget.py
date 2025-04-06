import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from datetime import datetime, timedelta
import google.generativeai as genai
import os
from BackEnd.sample_data import grocery_df  # Import the data from sample_data.py
from FrontEnd.browse_page import user_location

# Configure your Gemini API key
genai.configure(api_key="AIzaSyAjAILDTv3M41p64ywtAoX3wCYBAzQvEIc")

def create_meal_plan(budget, duration):


    # Convert 'Expiration Date' to datetime objects for date comparisons
    grocery_df['Expiration Date'] = pd.to_datetime(grocery_df['Expiration Date'])

    # Filter for available items and items that expire within the duration
    end_date = datetime.today().date() + timedelta(days=duration)
    df_filtered = grocery_df[(grocery_df['Availability'] == 'Available') & (grocery_df['Expiration Date'].dt.date <= end_date)]

    # Prepare the prompt for Gemini API
    prompt = f"""
    Create a meal plan for {duration} days, considering a budget of ${budget:.2f}.

    User Location: {user_location}

    Here are some nearby grocery items with discounted prices and expiration dates:
    {df_filtered.to_string()}

    Please consider these items when creating the meal plan and also include other affordable items available in the user's location. 
    Make sure the meal plan is varied, nutritious, and stays within the given budget.
    Also, please provide the total cost of the meal plan. No need to overexplain anything. Keep each line of text to at most 5 words to allow for easy readibility.
    """

    # Generate the meal plan using Gemini API
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

# Example usage
location = "Chicago, IL"
budget = 50.00
duration = 3

meal_plan = create_meal_plan(budget, duration)
print(meal_plan)