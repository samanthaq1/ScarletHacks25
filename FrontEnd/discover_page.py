import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from BackEnd.sample_data import grocery_df 

class DiscoverPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)

        # App bar
        self.app_bar = ctk.CTkFrame(self, corner_radius=0, fg_color="#3F7D58")
        self.app_bar.grid(row=0, column=0, sticky="ew")
        self.app_bar.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.app_bar, text="Discover Stores Near You!", font=("Segoe UI", 20, "bold"), anchor="w", text_color="white")
        self.title_label.grid(row=0, column=0, pady=20, padx=10, sticky="w")


        self.trending_label = ctk.CTkLabel(self, text="Trending Stores", font=("Segoe UI", 16, "bold"))
        self.trending_label.grid(row=1, column=0, pady=(10, 5))

        trending_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        trending_scroll_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.trending_frame = trending_scroll_frame

        self.store_label = ctk.CTkLabel(self, text="Recommendations Based On Your History", font=("Segoe UI", 16, "bold"))
        self.store_label.grid(row=3, column=0, pady=(10, 5))

        store_scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        store_scroll_frame.grid(row=4, column=0, padx=10, sticky="ew")
        self.store_frame = store_scroll_frame

        # Store button references
        self.store_buttons = {}

        # Default load
        self.populate_trending_stores()
        self.populate_rec_stores()

    def populate_trending_stores(self):
        for widget in self.trending_frame.winfo_children():
            widget.destroy()

        # Get top 5 stores by click count
        trending_data = (
            grocery_df.groupby(["Store", "Location"])["Click Count"]
            .sum()
            .reset_index()
            .sort_values(by="Click Count", ascending=False)
            .head(5)
        )

        for _, row in trending_data.iterrows():
            card = ctk.CTkFrame(self.trending_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            btn = ctk.CTkButton(
                card,
                text=row["Store"],
                command=lambda s=row["Store"]: self.show_store_dialog(s)
            )
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(
                card,
                text=row["Location"],
                wraplength=140,
                font=("Segoe UI", 10),
                text_color="gray"
            )
            label.pack(pady=(0, 10))

    def populate_rec_stores(self):
        for widget in self.store_frame.winfo_children():
            widget.destroy()

        grouped = grocery_df .groupby(["Store", "Location"]).first().reset_index()
        for _, row in grouped.iterrows():
            card = ctk.CTkFrame(self.store_frame, width=150)
            card.pack(side="left", padx=10, pady=10)

            btn = ctk.CTkButton(card, text=row["Store"], command=lambda s=row["Store"]: self.show_store_items(s))
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(card, text=row["Location"], wraplength=140, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))

    
    def show_store_dialog(self, store_name):
        items = grocery_df[grocery_df["Store"] == store_name]

        if items.empty:
            ctk.CTkMessagebox(title="Info", message="No items available.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title(f"{store_name} - Items")
        popup.geometry("400x400")
        popup.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(popup, text=f"Items at {store_name}", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        frame = ctk.CTkScrollableFrame(popup)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        for _, row in items.iterrows():
            item_text = (
                f"Food: {row['Food']}\n"
                f"Original Price: ${row['Original Price']:.2f}\n"
                f"Final Price: ${row['Final Price']:.2f}\n"
                f"Expiration Date: {row['Expiration Date']}\n"
                f"Availability: {row['Availability']}"
            )
            label = ctk.CTkLabel(frame, text=item_text, justify="left", anchor="w")
            label.pack(anchor="w", pady=5)