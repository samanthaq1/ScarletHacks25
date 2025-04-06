import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from datetime import datetime, timedelta
import google.generativeai as genai
import os
from BackEnd.sample_data import data  # Import the data from sample_data.py

# Configure your Gemini API key
genai.configure(api_key="")

def create_meal_plan(location, budget, duration):

    # Convert sample data to a pandas DataFrame for easier manipulation
    df = pd.DataFrame(data)

    # Convert 'Expiration Date' to datetime objects for date comparisons
    df['Expiration Date'] = pd.to_datetime(df['Expiration Date'])

    # Filter for available items and items that expire within the duration
    end_date = datetime.today().date() + timedelta(days=duration)
    df_filtered = df[(df['Availability'] == 'Available') & (df['Expiration Date'].dt.date <= end_date)]

    # Prepare the prompt for Gemini API
    prompt = f"""
    Create a meal plan for {duration} days, considering a budget of ${budget:.2f}.

    User Location: {location}

    Here are some nearby grocery items with discounted prices and expiration dates:
    {df_filtered.to_string()}

    Please consider these items when creating the meal plan and also include other affordable items available in the user's location. 
    Make sure the meal plan is varied, nutritious, and stays within the given budget.
    Also, please provide the total cost of the meal plan.
    """

    # Generate the meal plan using Gemini API
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    response = model.generate_content(prompt)
    return response.text

# Example usage
location = "Chicago, IL"
budget = 50.00
duration = 3

meal_plan = create_meal_plan(location, budget, duration)
print(meal_plan)