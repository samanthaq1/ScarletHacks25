from sample_data import grocery_df

def get_trending_items(df, top_n=3):
    """
    Calculates and prints the top trending grocery items based on click counts, without index.

    Args:
        df (pd.DataFrame): The grocery data DataFrame.
        top_n (int): The number of top trending items to print.
    """

    if "Click Count" not in df.columns:
        print("Click Count column not found in DataFrame.")
        return

    trending_items = df.sort_values(by="Click Count", ascending=False).head(top_n)
    print("Trending Items:")
    print(trending_items.to_string(index=False))  # Print without index

# Example usage
get_trending_items(grocery_df)
get_trending_items(grocery_df.drop("Click Count", axis = 1))