import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Fixed height for the header
        self.grid_rowconfigure(1, weight=1)  # Allow details to expand

        # === Fonts ===
        header_font = ctk.CTkFont(size=26, weight="bold")
        label_font = ctk.CTkFont(size=14, weight="bold")
        value_font = ctk.CTkFont(size=14)

        # === Header Frame ===
        header_frame = ctk.CTkFrame(self, corner_radius=12)
        header_frame.grid(row=0, column=0, padx=40, pady=(20, 10), sticky="ew")

        profile_label = ctk.CTkLabel(header_frame, text="My Profile", font=header_font)
        profile_label.pack(pady=(15, 5))

        # Optional Divider
        divider = ctk.CTkFrame(header_frame, height=2, fg_color="#CCCCCC")
        divider.pack(fill="x", padx=20, pady=(0, 10))

        # === Details Frame ===
        self.details_frame = ctk.CTkFrame(self, corner_radius=12)
        self.details_frame.grid(row=1, column=0, padx=40, pady=(10, 30), sticky="nsew")

        # 3-column layout: spacer, content, spacer
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=0)
        self.details_frame.grid_columnconfigure(2, weight=1)

        # Set a uniform width for all entries (input boxes)
        input_width = 280  # Adjust this width value as needed for uniformity

        # Username
        username_label = ctk.CTkLabel(self.details_frame, text="Username:", font=label_font)
        username_label.grid(row=0, column=1, padx=(20, 10), pady=(40,8), sticky="w")  # Lowered label
        self.username_value = ctk.CTkLabel(self.details_frame, text="User123", font=value_font)
        self.username_value.grid(row=0, column=2, padx=(10, 20), pady=(40,8), sticky="w")

        # Email
        email_label = ctk.CTkLabel(self.details_frame, text="Email:", font=label_font)
        email_label.grid(row=1, column=1, padx=(20, 10), pady=8, sticky="w")  # Lowered label
        self.email_value = ctk.CTkLabel(self.details_frame, text="user123@example.com", font=value_font)
        self.email_value.grid(row=1, column=2, padx=(10, 20), pady=8, sticky="w")

        # Location
        location_label = ctk.CTkLabel(self.details_frame, text="Location:", font=label_font)
        location_label.grid(row=2, column=1, padx=(20, 10), pady=8, sticky="w")  # Lowered label
        self.location_value = ctk.CTkLabel(self.details_frame, text="Chicago, IL", font=value_font)
        self.location_value.grid(row=2, column=2, padx=(10, 20), pady=8, sticky="w")

        # Edit Button (initial)
        self.edit_button = ctk.CTkButton(self.details_frame, text="Edit Profile", fg_color="#1E88E5", command=self.edit_profile)
        self.edit_button.grid(row=3, column=0, columnspan=3, pady=(20, 10))

        self.editing = False

    def edit_profile(self):
        if not self.editing:
            self.editing = True

            # Save original values
            self.original_username = self.username_value.cget("text")
            self.original_email = self.email_value.cget("text")
            self.original_location = self.location_value.cget("text")

            # Replace labels with entries, and make them all the same width
            self.username_entry = ctk.CTkEntry(self.details_frame, width=280)  # Uniform width
            self.username_entry.insert(0, self.original_username)
            self.username_entry.grid(row=0, column=2, padx=(10, 20), pady=(40,8), sticky="w")
            self.username_value.destroy()

            self.email_entry = ctk.CTkEntry(self.details_frame, width=280)  # Uniform width
            self.email_entry.insert(0, self.original_email)
            self.email_entry.grid(row=1, column=2, padx=(10, 20), pady=8, sticky="w")
            self.email_value.destroy()

            self.location_entry = ctk.CTkEntry(self.details_frame, width=280)  # Uniform width
            self.location_entry.insert(0, self.original_location)
            self.location_entry.grid(row=2, column=2, padx=(10, 20), pady=8, sticky="w")
            self.location_value.destroy()

            # Save Button
            self.save_button = ctk.CTkButton(self.details_frame, text="Save", fg_color="#43A047", command=self.save_profile)
            self.save_button.grid(row=4, column=0, columnspan=3, pady=(10, 5))

            self.edit_button.configure(text="Cancel Edit")

        else:
            self.cancel_edit()

    def cancel_edit(self):
        # Restore original label values
        self.username_value = ctk.CTkLabel(self.details_frame, text=self.original_username)
        self.username_value.grid(row=0, column=2, padx=(10, 20), pady=(40,8), sticky="w")
        self.username_entry.destroy()

        self.email_value = ctk.CTkLabel(self.details_frame, text=self.original_email)
        self.email_value.grid(row=1, column=2, padx=(10, 20), pady=8, sticky="w")
        self.email_entry.destroy()

        self.location_value = ctk.CTkLabel(self.details_frame, text=self.original_location)
        self.location_value.grid(row=2, column=2, padx=(10, 20), pady=8, sticky="w")
        self.location_entry.destroy()

        self.save_button.destroy()
        self.edit_button.configure(text="Edit Profile")
        self.editing = False

    def save_profile(self):
        # Replace entries with new label values
        self.username_value = ctk.CTkLabel(self.details_frame, text=self.username_entry.get())
        self.username_value.grid(row=0, column=2, padx=(10, 20), pady=8, sticky="w")
        self.username_entry.destroy()

        self.email_value = ctk.CTkLabel(self.details_frame, text=self.email_entry.get())
        self.email_value.grid(row=1, column=2, padx=(10, 20), pady=8, sticky="w")
        self.email_entry.destroy()

        self.location_value = ctk.CTkLabel(self.details_frame, text=self.location_entry.get())
        self.location_value.grid(row=2, column=2, padx=(10, 20), pady=8, sticky="w")
        self.location_entry.destroy()

        self.save_button.destroy()
        self.edit_button.configure(text="Edit Profile")
        self.editing = False

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x450")
    profile_page = ProfilePage(app)
    profile_page.pack(fill="both", expand=True)
    app.mainloop()
