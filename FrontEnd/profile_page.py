import customtkinter as ctk

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Profile Header
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        profile_label = ctk.CTkLabel(header_frame, text="My Profile", font=ctk.CTkFont(size=24, weight="bold"))
        profile_label.pack(pady=10)

        # Profile Details Frame
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # Configure 3 columns: spacer, content, spacer
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=0)
        self.details_frame.grid_columnconfigure(2, weight=1)

        # Username
        username_label = ctk.CTkLabel(self.details_frame, text="Username:", font=ctk.CTkFont(size=14, weight="bold"))
        username_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.username_value = ctk.CTkLabel(self.details_frame, text="User123")
        self.username_value.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Email
        email_label = ctk.CTkLabel(self.details_frame, text="Email:", font=ctk.CTkFont(size=14, weight="bold"))
        email_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.email_value = ctk.CTkLabel(self.details_frame, text="user123@example.com")
        self.email_value.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Location
        location_label = ctk.CTkLabel(self.details_frame, text="Location:", font=ctk.CTkFont(size=14, weight="bold"))
        location_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.location_value = ctk.CTkLabel(self.details_frame, text="Chicago, IL")
        self.location_value.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Edit Button (initial)
        self.edit_button = ctk.CTkButton(self.details_frame, text="Edit Profile", command=self.edit_profile)
        self.edit_button.grid(row=3, column=0, columnspan=3, pady=(15, 0))  # centered

        self.editing = False

    def edit_profile(self):
        if not self.editing:
            self.editing = True

            # Save original values
            self.original_username = self.username_value.cget("text")
            self.original_email = self.email_value.cget("text")
            self.original_location = self.location_value.cget("text")

            # Replace labels with entries
            self.username_entry = ctk.CTkEntry(self.details_frame)
            self.username_entry.insert(0, self.original_username)
            self.username_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")
            self.username_value.destroy()

            self.email_entry = ctk.CTkEntry(self.details_frame)
            self.email_entry.insert(0, self.original_email)
            self.email_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")
            self.email_value.destroy()

            self.location_entry = ctk.CTkEntry(self.details_frame)
            self.location_entry.insert(0, self.original_location)
            self.location_entry.grid(row=2, column=2, padx=10, pady=5, sticky="w")
            self.location_value.destroy()

            # Save button
            self.save_button = ctk.CTkButton(self.details_frame, text="Save", command=self.save_profile)
            self.save_button.grid(row=4, column=0, columnspan=3, pady=10)  # centered

            self.edit_button.configure(text="Cancel Edit")

        else:
            self.cancel_edit()

    def cancel_edit(self):
        # Restore original label values
        self.username_value = ctk.CTkLabel(self.details_frame, text=self.original_username)
        self.username_value.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.username_entry.destroy()

        self.email_value = ctk.CTkLabel(self.details_frame, text=self.original_email)
        self.email_value.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.email_entry.destroy()

        self.location_value = ctk.CTkLabel(self.details_frame, text=self.original_location)
        self.location_value.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.location_entry.destroy()

        self.save_button.destroy()
        self.edit_button.configure(text="Edit Profile")
        self.editing = False

    def save_profile(self):
        # Replace entries with new label values
        self.username_value = ctk.CTkLabel(self.details_frame, text=self.username_entry.get())
        self.username_value.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.username_entry.destroy()

        self.email_value = ctk.CTkLabel(self.details_frame, text=self.email_entry.get())
        self.email_value.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.email_entry.destroy()

        self.location_value = ctk.CTkLabel(self.details_frame, text=self.location_entry.get())
        self.location_value.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.location_entry.destroy()

        self.save_button.destroy()
        self.edit_button.configure(text="Edit Profile")
        self.editing = False

# if __name__ == "__main__":
#     app = ctk.CTk()
#     app.geometry("600x400")
#     profile_page = ProfilePage(app)
#     profile_page.pack(fill="both", expand=True)
#     app.mainloop()
