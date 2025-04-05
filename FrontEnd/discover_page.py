from BackEnd.sample_data import grocery_df
import customtkinter as ctk



class DiscoverPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.store_frame = ctk.CTkFrame(self)
        self.store_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.info_frame = ctk.CTkScrollableFrame(self)
        self.info_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.store_buttons = {}
        self.create_store_buttons()

    def create_store_buttons(self):
        # Get unique stores and their locations
        stores = grocery_df[["Store", "Location"]].drop_duplicates()

        for _, row in stores.iterrows():
            store_name = row["Store"]
            location = row["Location"]

            btn = ctk.CTkButton(self.store_frame, text=store_name, command=lambda s=store_name: self.show_store_items(s))
            btn.pack(pady=(5, 0), fill="x")

            label = ctk.CTkLabel(self.store_frame, text=location, wraplength=150, font=("Segoe UI", 10), text_color="gray")
            label.pack(pady=(0, 10))

            self.store_buttons[store_name] = btn

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

