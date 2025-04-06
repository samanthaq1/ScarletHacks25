def get_trending_items(df, top_n=5):
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
    return trending_items
