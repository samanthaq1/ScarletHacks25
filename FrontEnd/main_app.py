import customtkinter as ctk
from discover_page import DiscoverPage
from browse_page import BrowsePage
from PIL import Image
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        super().__init__()

        self.title("SellBuy")
        self.geometry("600x900")

        self.page_container = ctk.CTkFrame(self)
        self.page_container.pack(fill="both", expand=True)

        self.pages = {
            "discover": DiscoverPage(self.page_container),
            "browse": BrowsePage(self.page_container)
        }

        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

        # Load icons (always gray)
        self.icons = {
            "discover": ctk.CTkImage(Image.open(file_path + "/assets/discover.png"), size=(24, 24)),
            "browse": ctk.CTkImage(Image.open(file_path + "/assets/browse.png"), size=(24, 24))
        }

        # Bottom nav bar
        nav_bar = ctk.CTkFrame(self, height=60)
        nav_bar.pack(side="bottom", fill="x")

        self.nav_buttons = {}

        # Create nav buttons
        self.nav_buttons["discover"] = self.create_nav_button(nav_bar, "discover", lambda: self.show_page("discover"))
        self.nav_buttons["browse"] = self.create_nav_button(nav_bar, "browse", lambda: self.show_page("browse"))

        self.nav_buttons["discover"].pack(side="left", expand=True, fill="both")
        self.nav_buttons["browse"].pack(side="left", expand=True, fill="both")

        self.active_page = None
        self.show_page("discover")

    def create_nav_button(self, parent, key, command):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        icon = ctk.CTkButton(
            frame,
            text="",
            image=self.icons[key],
            command=command,
            width=40,
            height=40,
            fg_color="transparent",
            hover=False
        )
        label = ctk.CTkLabel(frame, text=key.capitalize(), font=("Segoe UI", 12), text_color="gray")
        icon.pack(pady=(5, 0))
        label.pack()
        frame.icon = icon
        frame.label = label
        return frame

    def show_page(self, name):
        if self.active_page == name:
            return
        self.pages[name].lift()
        self.set_active_nav(name)

    def set_active_nav(self, name):
        for key, frame in self.nav_buttons.items():
            frame.label.configure(text_color="green" if key == name else "gray")
        self.active_page = name


if __name__ == "__main__":
    app = App()
    app.mainloop()
