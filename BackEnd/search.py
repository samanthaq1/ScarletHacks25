def search_food(food_name, grocery_df, sort_by=None):
    food_name_lower = food_name.lower()
    matching_items = grocery_df[grocery_df['Food'].str.lower().str.contains(food_name_lower)]

    if matching_items.empty:
        return "No matching food items found."

    results = matching_items.to_dict(orient="records") #convert to list of dictionaries.

    if sort_by:
        try:
            results = sorted(results, key=lambda x: x[sort_by])
        except KeyError:
            return "Invalid sort_by parameter."

    return results

# Example usage
search_term = "Milk"
search_results = search_food(search_term, grocery_df, sort_by="Final Price")
print("Sorted by Final Price:")
print(search_results)

search_term = "Bananas"
search_results = search_food(search_term, grocery_df, sort_by="Expiration Date")
print("\nSorted by Expiration Date:")
print(search_results)

search_term = "Milk"
search_results = search_food(search_term, grocery_df, sort_by="Store")
print("\nSorted by Store:")
print(search_results)

search_term = "Milk"
search_results = search_food(search_term, grocery_df, sort_by="not a valid sort")
print("\nInvalid sort:")
print(search_results)
