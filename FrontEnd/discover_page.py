import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from BackEnd.recs import recommendations
from BackEnd.trending import get_trending_items
from BackEnd.sample_data import grocery_df 
from BackEnd.map import distance
from BackEnd.user import ProfileData
from PIL import Image

user_location = "3101 S Wabash Ave, Chicago, IL 60616"  # Hardcoded data for kacek as user location  

class DiscoverPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # Init Icons
        file_path = os.path.dirname(os.path.realpath(__file__))
        self.store_icon = ctk.CTkImage(Image.open(file_path + "/assets/grocery.png"), size=(50, 50))
        # self.pf = ProfileData()
        # fName = self.pf.get_username()
        self.grid_columnconfigure(0, weight=1)

        # App bar
        self.app_bar = ctk.CTkFrame(self, corner_radius=0, fg_color="#3F7D58")
        self.app_bar.grid(row=0, column=0, sticky="ew")
        self.app_bar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.app_bar, text="Welcome, Discover Groceries For You!", font=("Segoe UI", 24, "bold"), anchor="w", text_color="white")
        self.title_label.grid(row=0, column=0, pady=20, padx=10, sticky="w")

        # Trending with Frame of Stores
        self.trending_label = ctk.CTkLabel(self, text="Trending Stores", font=("Segoe UI", 20, "bold"))
        self.trending_label.grid(row=1, column=0, pady=(10, 5))

        trending_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        trending_scroll_frame.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.trending_frame = trending_scroll_frame

        # Recommendations with Frame of Stores
        self.store_label = ctk.CTkLabel(self, text="Recommendations Based On Your History", font=("Segoe UI", 20, "bold"))
        self.store_label.grid(row=4, column=0, pady=(45, 5))

        store_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", height = 50)
        store_scroll_frame.grid(row=5, column=0, padx=10, sticky="ew")
        self.store_frame = store_scroll_frame

        # Default load
        self.populate_trending_stores()
        self.populate_rec_foods()

    def populate_trending_stores(self):
        for widget in self.trending_frame.winfo_children():
            widget.destroy()

        # Loads the top 5 stores based on click count
        trending_data = get_trending_items(grocery_df)

        for _, row in trending_data.iterrows():
            card = ctk.CTkFrame(self.trending_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            store_button = ctk.CTkButton(
                card,
                text=row["Store"],
                image=self.store_icon,
                compound="top",
                # command=lambda s=row["Store"]: self.show_store_items(s, 3)
                command=lambda s=row["Store"]: self.show_list(3, store_name=s)
            )
            store_button.pack(pady=(5, 0), fill="x")
                

            dist = distance(user_location, row["Location"])
            location_text = f"{row['Location']} ({dist})"

            label = ctk.CTkLabel(card, text=location_text, wraplength=140, font=("Segoe UI", 12), text_color="gray")
            label.pack(pady=(0, 10))

    def populate_rec_foods(self):
        for widget in self.store_frame.winfo_children():
            widget.destroy()

        if not recommendations:
            grouped = grocery_df["Food"].unique()
        else:
            rec_foods = [rec["Store"] for rec in recommendations]
            rec_data = grocery_df[grocery_df["Store"].isin(rec_foods)]
            grouped = rec_data.groupby(["Food"]).first().reset_index()

        for _, row in grouped.iterrows():
            card = ctk.CTkFrame(self.store_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            food_button = ctk.CTkButton(
                card,
                text=row["Food"],
                compound="top",
                command=lambda f=row["Food"]: self.show_list(6, food_name=f)
            )
            food_button.pack(pady=(5, 0), fill="x")
    
    def show_list(self, row_num, store_name=None, food_name = None):
        # Remove existing info frame if present
        if hasattr(self, "info_frame") and self.info_frame.winfo_exists():
            self.info_frame.destroy()

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=row_num, column=0, padx=10, pady=10, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)

        if (store_name != None):
            items = grocery_df[grocery_df["Store"] == store_name]

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

                food_label = ctk.CTkLabel(item_frame, text=f"{row['Food']} ({availability})", font=("Segoe UI", 18, "bold"), text_color=color)
                food_label.pack(anchor="w")

                price_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                price_frame.pack(anchor="w")
                orig_price_label = ctk.CTkLabel(price_frame, text=f"Original: ${row['Original Price']:.2f} ", font=("Segoe UI", 15), text_color="gray")
                orig_price_label.pack(side="left")
                final_price_label = ctk.CTkLabel(price_frame, text=f"Now: ${row['Final Price']:.2f}", font=("Segoe UI", 15, "bold"), text_color=color)
                final_price_label.pack(side="left")

                exp_label = ctk.CTkLabel(item_frame, text=f"Expires: {row['Expiration Date']}", font=("Segoe UI", 15), text_color=color)
                exp_label.pack(anchor="w")

        elif (food_name != None): 
            items = grocery_df[grocery_df["Food"] == food_name]
            title = ctk.CTkLabel(self.info_frame, text=f"Where to buy: {food_name}", font=("Segoe UI", 16, "bold"))
            title.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

            close_button = ctk.CTkButton(self.info_frame, text="X", command=self.info_frame.destroy, fg_color="gray", width=20, height=20)
            close_button.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="e")

            scroll_frame = ctk.CTkScrollableFrame(self.info_frame)
            scroll_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

            for _, row in items.iterrows():
                availability = row['Availability']
                if (availability.lower() == "available"):
                    dist = distance(user_location, row["Location"])

                    item_frame = ctk.CTkFrame(scroll_frame)
                    item_frame.pack(fill="x", padx=5, pady=5)

                    store_label = ctk.CTkLabel(item_frame, text=f"{row['Store']}", font=("Segoe UI", 18, "bold"))
                    store_label.pack(anchor="w")

                    price_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                    price_frame.pack(anchor="w")
                    orig_price_label = ctk.CTkLabel(price_frame, text=f"Original: ${row['Original Price']:.2f} ", font=("Segoe UI", 15), text_color="gray")
                    orig_price_label.pack(side="left")
                    final_price_label = ctk.CTkLabel(price_frame, text=f"Now: ${row['Final Price']:.2f}", font=("Segoe UI", 15, "bold"), text_color="green")
                    final_price_label.pack(side="left")

                    exp_label = ctk.CTkLabel(item_frame, text=f"Expires: {row['Expiration Date']}", font=("Segoe UI", 14), text_color="green")
                    exp_label.pack(anchor="w")

