import customtkinter as ctk
from sample_data import grocery_df

class BrowsePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Browse Page", font=("Segoe UI", 20))
        label.pack(pady=(20, 10))

        self.create_search_bar()
        self.create_store_list()

    # Create stores
    def create_store_list(self):
        # Main frame to hold buttons and details side by side
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Scrollable button list (on left)
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, width=250)
        self.scroll_frame.pack(side="left", fill="y", padx=(0, 10), expand=False)

        # Details (on right)
        self.details_frame = ctk.CTkFrame(self.content_frame)
        self.details_frame.pack(side="left", fill="both", expand=True)

        self.details_label = ctk.CTkLabel(
            self.details_frame, 
            text="", 
            justify="left", 
            anchor="nw", 
            wraplength=300
            )
        self.details_label.pack(pady=(0, 10), padx=10, fill="both", expand=True)

        # Makes store details closable
        self.close_button = ctk.CTkButton(
            self.details_frame, 
            text="Close", 
            command=self.clear_details
            )
        self.close_button.pack(pady=(0, 10))

        # Store the full sorted DataFrame
        self.data = grocery_df

        # Display list
        self.show_store_buttons(self.data)
    
    # Create store buttons
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
    
    def clear_details(self):
        self.details_label.configure(text="")

    # Create searchbar
    def create_search_bar(self):
        # Search bar
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search by food...", width=300)
        self.search_entry.pack(pady=(10, 5), anchor="center")

        # Search button
        search_button = ctk.CTkButton(self, text="Search", command=self.perform_search)
        search_button.pack(pady=(5, 10))

        # Bind Enter key for mobile users
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

    # Search function
    def perform_search(self):
        query = self.search_entry.get().lower()

        # Filter for rows where the food name contains the query and is available
        filtered = self.data[
            self.data["Food"].str.lower().str.contains(query) &
            (self.data["Availability"] == "Available")
        ]

        self.show_store_buttons(filtered)
