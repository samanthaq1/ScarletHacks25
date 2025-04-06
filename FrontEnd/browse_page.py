import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.map import get_link
import webbrowser
import customtkinter as ctk
from BackEnd.sample_data import grocery_df
from PIL import Image

user_location = "3101 S Wabash Ave, Chicago, IL 60616"  # Hardcoded data for kacek as user location   
class BrowsePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Browse Page", font=("Segoe UI", 20))
        label.pack(pady=(20, 10))

        # Get full path to the image in the 'assets' folder and load into image to icon
        icon_path = os.path.dirname(os.path.realpath(__file__))
        self.store_icon = ctk.CTkImage(light_image=Image.open(icon_path + "/assets/destination.png"), size=(24, 24))

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
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row_frame.pack(pady=5, padx=10, fill="x")

            # Image button (icon only)
            icon_button = ctk.CTkButton(
                row_frame,
                image=self.store_icon,
                text="",
                width=32,
                height=32,
                command=lambda addr=location: self.open_store_directions(addr)
            )
            icon_button.pack(side="left", padx=(0, 8))

            # Store name button
            store_button = ctk.CTkButton(
                row_frame,
                text=store,
                width=200,
                anchor="w",
                command=lambda g=group, s=store, l=location: self.show_store_details(s, l, g)
            )
            store_button.pack(side="left", fill="x", expand=True)


    def show_store_details(self, store, location, store_df):
        # Close the existing frame if it exists
        if hasattr(self, 'details_popup') and self.details_popup.winfo_ismapped():
            self.details_popup.destroy()

        # Create a new frame that acts as a popup
        self.details_popup = ctk.CTkFrame(self)
        
        # Center the frame in the middle of the window
        self.details_popup.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.6)


        # Details label inside the popup
        label = ctk.CTkLabel(
            self.details_popup,
            text="",
            justify="left",
            anchor="nw",
            wraplength=320
        )
        label.pack(pady=(10, 10), padx=10, fill="both", expand=True)

        # Close button inside the popup
        close_button = ctk.CTkButton(
            self.details_popup,
            text="Close",
            command=self.details_popup.destroy
        )
        close_button.pack(pady=(0, 10))

        # Prepare the details text
        available = store_df[store_df["Availability"] == "Available"]
        if available.empty:
            text = f"🏬 {store}\n📍 {location}\n\n⚠️ No available food items."
        else:
            text = f"🏬 {store}\n📍 {location}\n\n🛒 Available Items:\n"
            for _, row in available.iterrows():
                text += f"• {row['Food']} - ${row['Final Price']:.2f} (exp: {row['Expiration Date']})\n"

        # Update label with the store details
        label.configure(text=text)
    
    def clear_details(self):
        self.details_label.configure(text="")

    # Opening link
    def open_store_directions(self, store_address):
        
        link = get_link(user_location, store_address)
        webbrowser.open(link)

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

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x700")
    browser= BrowsePage(app)
    browser.pack(fill="both", expand=True)
    app.mainloop()
