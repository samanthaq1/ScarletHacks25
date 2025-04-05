from sample_data import grocery_df

def search_food(food_name, grocery_df, sort_by=None):
    food_name_lower = food_name.lower()
    matching_items = grocery_df[grocery_df['Food'].str.lower().str.contains(food_name_lower)]

    if matching_items.empty:
        print("\nNo matching food items found.")
        return

    results = matching_items.to_dict(orient="records")

    if sort_by:
        try:
            results = sorted(results, key=lambda x: x[sort_by])
            print(f"\nSorted by: {sort_by}") #Print the sorting information
        except KeyError:
            print("\nInvalid sort_by parameter.")
            return
    else:
      print("\nUnsorted Results:")

    for item in results:
        print(item)

# Example usage
search_term = "Milk"
search_food(search_term, grocery_df, sort_by="Final Price")

search_term = "Bananas"
search_food(search_term, grocery_df, sort_by="Expiration Date")

search_term = "Milk"
search_food(search_term, grocery_df, sort_by="Store")

search_term = "Milk"
search_food(search_term, grocery_df, sort_by="not a valid sort")

search_term = "Milk"
search_food(search_term, grocery_df)