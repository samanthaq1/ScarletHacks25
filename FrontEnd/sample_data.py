# Hardcoded sample grocery data
from datetime import datetime, timedelta
import pandas as pd

data = [
    {"Food": "Milk", "Store": "SuperMart", "Location": "2323 S Leavitt St", "Original Price": 3.50, "Final Price": 2.80, "Expiration Date": (datetime.today().date() + timedelta(days=2)).strftime('%Y-%m-%d'), "Availability": "Available"},
    {"Food": "Bread", "Store": "FreshCo", "Location": "1400 W Monroe St", "Original Price": 2.00, "Final Price": 1.00, "Expiration Date": (datetime.today().date() + timedelta(days=1)).strftime('%Y-%m-%d'), "Availability": "Available"},
    {"Food": "Chicken Breast", "Store": "ValueFoods", "Location": "110 E Lockwood Ave", "Original Price": 8.00, "Final Price": 6.00, "Expiration Date": (datetime.today().date() + timedelta(days=3)).strftime('%Y-%m-%d'), "Availability": "Available"},
    {"Food": "Bananas", "Store": "GreenGrocers", "Location": "2857 S Kedvale Ave", "Original Price": 1.50, "Final Price": 1.50, "Expiration Date": (datetime.today().date() + timedelta(days=5)).strftime('%Y-%m-%d'), "Availability": "Available"},
    {"Food": "Yogurt", "Store": "MegaMarket", "Location": "2430 S St Louis Ave", "Original Price": 4.00, "Final Price": 3.20, "Expiration Date": (datetime.today().date() + timedelta(days=2)).strftime('%Y-%m-%d'), "Availability": "Sold Out"},
    {"Food": "Milk", "Store": "MegaMarket", "Location": "2635 S Drake Ave", "Original Price": 2.94, "Final Price": 1.91, "Expiration Date": (datetime.today().date() + timedelta(days=6)).strftime('%Y-%m-%d'), "Availability": "Available"},
    {"Food": "Milk", "Store": "GreenGrocers", "Location": "3128 S Millard Ave", "Original Price": 2.46, "Final Price": 2.46, "Expiration Date": (datetime.today().date() + timedelta(days=12)).strftime('%Y-%m-%d'), "Availability": "Available"},
    {"Food": "Bananas", "Store": "SuperMart", "Location": "2818 W 26th St", "Original Price": 2.97, "Final Price": 2.97, "Expiration Date": (datetime.today().date() + timedelta(days=15)).strftime('%Y-%m-%d'), "Availability": "Available"}
]

grocery_df = pd.DataFrame(data)
