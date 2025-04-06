import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from BackEnd.recs import recommendations
from BackEnd.trending import get_trending_items
from BackEnd.sample_data import grocery_df 

class DiscoverPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)

        # App bar
        self.app_bar = ctk.CTkFrame(self, corner_radius=0, fg_color="#3F7D58")
        self.app_bar.grid(row=0, column=0, sticky="ew")
        self.app_bar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.app_bar, text="Discover Stores For You!", font=("Segoe UI", 20, "bold"), anchor="w", text_color="white")
        self.title_label.grid(row=0, column=0, pady=20, padx=10, sticky="w")

        # Trending with Frame of Stores
        self.trending_label = ctk.CTkLabel(self, text="Trending Stores", font=("Segoe UI", 16, "bold"))
        self.trending_label.grid(row=1, column=0, pady=(10, 5))

        trending_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        trending_scroll_frame.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.trending_frame = trending_scroll_frame

        # Recommendations with Frame of Stores
        self.store_label = ctk.CTkLabel(self, text="Recommendations Based On Your History", font=("Segoe UI", 16, "bold"))
        self.store_label.grid(row=4, column=0, pady=(10, 5))

        store_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        store_scroll_frame.grid(row=5, column=0, padx=10, sticky="ew")
        self.store_frame = store_scroll_frame

        # Default load
        self.populate_trending_stores()
        self.populate_rec_stores()

    def populate_trending_stores(self):
        for widget in self.trending_frame.winfo_children():
            widget.destroy()

        # Loads the top 5 stores based on click count
        trending_data = get_trending_items(grocery_df)

        for _, row in trending_data.iterrows():
            card = ctk.CTkFrame(self.trending_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            store_button = ctk.CTkButton(card, text=row["Store"], command=lambda s=row["Store"], r=3: self.show_store_items(s, r))
            store_button.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(card, text=row["Location"], wraplength=140, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))

    def populate_rec_stores(self):
        for widget in self.store_frame.winfo_children():
            widget.destroy()

        if not recommendations:
            grouped = grocery_df.groupby(["Store", "Location"]).first().reset_index()
        else:
            rec_foods = [rec["Food"] for rec in recommendations]
            rec_data = grocery_df[grocery_df["Food"].isin(rec_foods)]
            grouped = rec_data.groupby(["Store", "Location"]).first().reset_index()

        for _, row in grouped.iterrows():
            card = ctk.CTkFrame(self.store_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            btn = ctk.CTkButton(card, text=row["Store"], command=lambda s=row["Store"], r=6: self.show_store_items(s, r))
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(card, text=row["Location"], wraplength=140, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))
    
    def show_store_items(self, store_name, row_num):
        # Remove existing info frame if present
        if hasattr(self, "info_frame") and self.info_frame.winfo_exists():
            self.info_frame.destroy()

        items = grocery_df[grocery_df["Store"] == store_name]

        if items.empty:
            return

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=row_num, column=0, padx=10, pady=10, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self.info_frame, text=f"Items at {store_name}", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        close_button = ctk.CTkButton(self.info_frame, text="X", command=self.info_frame.destroy, fg_color="gray", width=20, height=20)
        close_button.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="e")

        scroll_frame = ctk.CTkScrollableFrame(self.info_frame)
        scroll_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        for _, row in items.iterrows():
            availability = row['Availability']
            color = "green" if availability.lower() == "available" else "red"

            item_frame = ctk.CTkFrame(scroll_frame)
            item_frame.pack(fill="x", padx=5, pady=5)

            food_label = ctk.CTkLabel(item_frame, text=f"Food: {row['Food']}  ({availability})", font=("Segoe UI", 18, "bold"), text_color=color)
            food_label.pack(anchor="w")

            price_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            price_frame.pack(anchor="w")
            orig_price_label = ctk.CTkLabel(price_frame, text=f"Original: ${row['Original Price']:.2f} ", font=("Segoe UI", 15), text_color="gray")
            orig_price_label.pack(side="left")
            final_price_label = ctk.CTkLabel(price_frame, text=f"Now: ${row['Final Price']:.2f}", font=("Segoe UI", 15, "bold"), text_color=color)
            final_price_label.pack(side="left")

            exp_label = ctk.CTkLabel(item_frame, text=f"Expiration Date: {row['Expiration Date']}", font=("Segoe UI", 15), text_color=color)
            exp_label.pack(anchor="w")


