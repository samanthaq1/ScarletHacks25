import pandas as pd
import customtkinter as ctk

class BrowsePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Browse Page", font=("Segoe UI", 20))
        label.pack(pady=(20, 10))
        self.create_search_bar()

    def create_store_list(self):
        d=3

    def create_search_bar(self):
        # Search bar
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search...")
        self.search_entry.pack(pady=(10, 5), padx=20, fill="x")

        # Search button
        search_button = ctk.CTkButton(self, text="Search", command=self.perform_search)
        search_button.pack(pady=5)

        # Bind Enter key for mobile
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

    def perform_search(self):
        query = self.search_entry.get()
        print(f"Searching for: {query}")
