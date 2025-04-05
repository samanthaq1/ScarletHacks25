import pandas as pd
from BackEnd.sample_data import grocery_df


# Hardcoded previous searches
search_data = {"search_term": ["Milk", "Chicken", "Bananas"]}
search_df = pd.DataFrame(search_data)

# Recommendation logic
search_terms = search_df["search_term"].str.lower().tolist() #Get the search items from the dataframe.
matching_items = grocery_df[grocery_df['Food'].str.lower().apply(lambda food: any(term in food for term in search_terms))]

if not matching_items.empty:
    sorted_items = matching_items.sort_values(by=['Final Price', 'Expiration Date'])
    initial_recommendations = sorted_items.to_dict('records')[:6] #Double the amount for gemini.

    prompt = f"""Given these initial grocery recommendations: {initial_recommendations}, and previous search terms: {search_terms}, provide the top 3 most relevant recommendations. Focus on items that are on sale and expiring soon, and are most likely to be of interest based on the previous searches. Only return the list of the 3 dictionaries. Do not return any other text."""

    response = model.generate_content(prompt)

    try:
        refined_recommendations = eval(response.text)
        if isinstance(refined_recommendations, list):
            for item in refined_recommendations:
                for key, value in item.items():
                    if isinstance(value, np.str_):
                        item[key] = str(value)
            recommendations = refined_recommendations[:3]
    except (SyntaxError, NameError, TypeError):
        print("Gemini recommendation processing failed. Returning initial recommendations.")
        recommendations = initial_recommendations[:3]
else:
  recommendations = []

# Print the recommendations
for item in recommendations:
    converted_item = {}
    for key, value in item.items():
        if isinstance(value, np.str_):
            converted_item[key] = str(value)
        else:
            converted_item[key] = value
    print(converted_item)