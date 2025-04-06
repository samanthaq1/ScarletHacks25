import customtkinter as ctk
from sample_data import grocery_df

class BrowsePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Browse Page", font=("Segoe UI", 20))
        label.pack(pady=(20, 10))

        self.create_search_bar()
        self.create_store_list()

    def create_store_list(self):
        # Main frame to hold buttons and details side by side
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Scrollable button list (LEFT)
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, width=250)
        self.scroll_frame.pack(side="left", fill="y", padx=(0, 10), expand=False)

        # Details (RIGHT)
        self.details_label = ctk.CTkLabel(self.content_frame, text="", justify="left", anchor="nw", width=250)
        self.details_label.pack(side="left", fill="both", expand=True)

        # Store the full sorted DataFrame
        self.data = grocery_df

        # Display list
        self.show_store_buttons(self.data)
    
    def show_store_buttons(self, df):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        store_groups = df.groupby(["Store", "Location"])

        for (store, location), group in store_groups:
            button = ctk.CTkButton(
                self.scroll_frame,
                text=store,
                width=200,
                command=lambda g=group, s=store, l=location: self.show_store_details(s, l, g)
            )
            button.pack(pady=5, padx=10, anchor="w")

    def show_store_details(self, store, location, store_df):
        # Filter for available items only
        available = store_df[store_df["Availability"] == "Available"]

        if available.empty:
            text = f"🏬 {store}\n📍 {location}\n\n⚠️ No available food items."
        else:
            text = f"🏬 {store}\n📍 {location}\n\n🛒 Available Items:\n"
            for _, row in available.iterrows():
                text += f"• {row['Food']} - ${row['Final Price']:.2f} (exp: {row['Expiration Date']})\n"

        self.details_label.configure(text=text)

    def create_search_bar(self):
        # Search bar
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search by food or store...")
        self.search_entry.pack(pady=(10, 5), padx=20, fill="x")

        # Search button
        search_button = ctk.CTkButton(self, text="Search", command=self.perform_search)
        search_button.pack(pady=(5, 10))

        # Bind Enter key for mobile
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

    def perform_search(self):
        query = self.search_entry.get().lower()

        # Search in 'Store'
        filtered = self.data[self.data["Store"].str.lower().str.contains(query)]
        self.show_store_buttons(filtered)
