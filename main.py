"""
main.py
Entry point for PANTRIX – Smart Pantry Recipe Recommender.
Run this file in PyCharm to start the application.
"""

import tkinter as tk
from login_page import LoginPage
from dashboard import DashboardPage


class PantrixApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PANTRIX - Smart Pantry Recipe Recommender")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#1e1e2e")

        # Center on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1200) // 2
        y = (self.root.winfo_screenheight() - 700)  // 2
        self.root.geometry(f"1200x700+{x}+{y}")

        self._show_login()
        self.root.mainloop()

    # ── Screen transitions ────────────────────────────────────────────────────
    def _clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _show_login(self):
        self._clear()
        login = LoginPage(self.root, on_login_success=self._show_dashboard)
        login.pack(fill="both", expand=True)

    def _show_dashboard(self, user_id, username):
        self._clear()
        dash = DashboardPage(
            self.root,
            user_id=user_id,
            username=username,
            on_logout=self._show_login
        )
        dash.pack(fill="both", expand=True)


if __name__ == "__main__":
    PantrixApp()