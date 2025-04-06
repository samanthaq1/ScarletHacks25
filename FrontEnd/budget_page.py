import customtkinter as ctk
# Configure your Gemini API key
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from BackEnd.budget import create_meal_plan
# Hardcoded location


class BudgetPage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Title Label
        title_label = ctk.CTkLabel(self, text="Budget Meal Planner", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Input Frame
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # Budget input
        budget_label = ctk.CTkLabel(input_frame, text="Budget ($):", font=ctk.CTkFont(size=14))
        budget_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.budget_entry = ctk.CTkEntry(input_frame, width=250)
        self.budget_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Duration input
        duration_label = ctk.CTkLabel(input_frame, text="Duration (days):", font=ctk.CTkFont(size=14))
        duration_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = ctk.CTkEntry(input_frame, width=250)
        self.duration_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Generate Meal Plan Button
        self.generate_button = ctk.CTkButton(input_frame, text="Generate Meal Plan", command=self.generate_meal_plan)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Overlay Frame for meal plan
        self.overlay_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("white", "gray38"), width=500, height=300)
        self.overlay_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.overlay_frame.grid_forget()  # Hide overlay by default

        # Exit Button for overlay
        self.exit_button = ctk.CTkButton(self.overlay_frame, text="X", command=self.close_overlay, width=20, height=20)
        self.exit_button.place(x=479, y=-1)

        # Scrollable Frame to hold the meal plan content
        self.scrollable_frame = ctk.CTkScrollableFrame(self.overlay_frame, width=458, height=230)
        self.scrollable_frame.place(x=10, y=30)

        # Label to show the meal plan text
        self.meal_plan_label = ctk.CTkLabel(self.scrollable_frame, text="Meal Plan will appear here.", font=ctk.CTkFont(size=14))
        self.meal_plan_label.pack(pady=10)

    def generate_meal_plan(self):
        # Get the user inputs
        try:
            budget = float(self.budget_entry.get())
            duration = int(self.duration_entry.get())
        except ValueError:
            self.show_overlay("Error", "Please enter valid values for budget and duration.")
            return

        # Generate the meal plan using the function
        meal_plan = create_meal_plan(budget, duration)

        # Show the generated meal plan in the overlay
        self.show_overlay(meal_plan)

    def show_overlay(self, message):
        # Set the title and message in the overlay
        self.meal_plan_label.configure(text=message)

        # Position overlay in the center of the window using fixed size (500x300)
        overlay_width = 500
        overlay_height = 300
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Calculate the center position of the overlay
        x_position = (window_width - overlay_width) // 2
        y_position = (window_height - overlay_height) // 2

        # Set the position for the overlay frame
        self.overlay_frame.place(x=x_position, y=y_position)

        # Show overlay
        self.overlay_frame.lift()  # Bring overlay to the top

    def close_overlay(self):
        # Hide the overlay when the exit button is pressed
        self.overlay_frame.place_forget()

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("600x450")
    budget_page = BudgetPage(app)
    budget_page.pack(fill="both", expand=True)
    app.mainloop()
