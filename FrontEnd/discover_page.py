import customtkinter as ctk
from sample_data import grocery_df
from maps import searchArea

class DiscoverPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)

        # App bar
        self.app_bar = ctk.CTkFrame(self, corner_radius=0)
        self.app_bar.grid(row=0, column=0, sticky="ew")
        self.app_bar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.app_bar, text="Discover Stores Near You", font=("Segoe UI", 20, "bold"), anchor="w")
        self.title_label.grid(row=0, column=0, pady=20, padx=10, sticky="w")

        # Location entry included in App Bar
        self.location_entry = ctk.CTkEntry(self.app_bar, placeholder_text="Enter your location")
        self.location_entry.grid(row=0, column=1, pady=20, padx=10, sticky="e")

        # Radius dropdown
        self.radius_var = ctk.StringVar(value="5")
        self.radius_label = ctk.CTkLabel(self.app_bar, text="within", font=("Segoe UI", 10), anchor="e")
        self.radius_label.grid(row=0, column=2, pady=20, padx=5, sticky="e")
        self.radius_menu = ctk.CTkOptionMenu(
            self.app_bar,
            values=["5 miles", "10", "15", "20", "25"],
            variable=self.radius_var,
            command=self.update_store_list
        )
        self.radius_menu.grid(row=0, column=3, pady=20, padx=10, sticky="e")

        self.trending_label = ctk.CTkLabel(self, text="Trending Stores Around Your Area", font=("Segoe UI", 16, "bold"))
        self.trending_label.grid(row=1, column=0, pady=(10, 5))

        trending_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        trending_scroll_frame.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.trending_frame = trending_scroll_frame

        self.store_label = ctk.CTkLabel(self, text="Recommendations based on your history", font=("Segoe UI", 16, "bold"))
        self.store_label.grid(row=3, column=0, pady=(10, 5))

        store_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        store_scroll_frame.grid(row=4, column=0, padx=10, sticky="ew")
        self.store_frame = store_scroll_frame

        # Store button references
        self.store_buttons = {}

        # Default load
        # self.update_store_list()
        self.populate_trending_stores()
        self.populate_all_stores()

    def populate_trending_stores(self):
        for widget in self.trending_frame.winfo_children():
            widget.destroy()

        trending_data = grocery_df.groupby(["Store", "Location"])["Click Count"].sum().reset_index()
        trending_data = trending_data.sort_values(by="Click Count", ascending=False)

        for _, row in trending_data.iterrows():
            card = ctk.CTkFrame(self.trending_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            btn = ctk.CTkButton(card, text=row["Store"], command=lambda s=row["Store"]: self.show_store_items(s))
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(card, text=row["Location"], wraplength=140, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))

    def populate_all_stores(self):
        for widget in self.store_frame.winfo_children():
            widget.destroy()

        grouped = grocery_df.groupby(["Store", "Location"]).first().reset_index()
        for _, row in grouped.iterrows():
            card = ctk.CTkFrame(self.store_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            btn = ctk.CTkButton(card, text=row["Store"], command=lambda s=row["Store"]: self.show_store_items(s))
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(card, text=row["Location"], wraplength=140, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))


    def update_store_list(self, *args):
        for widget in self.store_frame.winfo_children():
            widget.destroy()

        user_location = self.location_entry.get().strip()
        if not user_location:
            user_location = "2323 S Leavitt St"  # fallback

        max_radius = float(self.radius_var.get())
        
        try:
            nearby_stores = searchArea(user_location, max_radius)
        except Exception as e:
            print(f"Map error: {e}")
            ctk.CTkLabel(self.store_frame, text="Error finding stores.").pack(pady=10)
            return

        # Filter stores in grocery_df that match nearby Google results
        df_stores = grocery_df[["Store", "Location"]].drop_duplicates()
        matched = []

        for store, loc in nearby_stores:
            for _, row in df_stores.iterrows():
                if store.lower() in row["Store"].lower() or row["Store"].lower() in store.lower():
                    matched.append((row["Store"], row["Location"]))
                    break

        if not matched:
            ctk.CTkLabel(self.store_frame, text="No matching stores found.").pack(pady=10)
            return

        self.store_buttons.clear()

        for store, location in matched:
            btn = ctk.CTkButton(self.store_frame, text=store, command=lambda s=store: self.show_store_items(s))
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(self.store_frame, text=location, wraplength=150, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))

            self.store_buttons[store] = btn


    def show_store_items(self, store_name):
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        filtered = grocery_df[grocery_df["Store"] == store_name]

        if filtered.empty:
            ctk.CTkLabel(self.info_frame, text="No items available.").pack(pady=10)
            return

        for _, row in filtered.iterrows():
            item_text = f"""
                        Food: {row['Food']}
                        Original Price: ${row['Original Price']:.2f}
                        Final Price: ${row['Final Price']:.2f}
                        Expiration Date: {row['Expiration Date']}
                        Availability: {row['Availability']}
                        """
            label = ctk.CTkLabel(self.info_frame, text=item_text.strip(), justify="left", anchor="w")
            label.pack(fill="x", pady=5, padx=5)
