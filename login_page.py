"""
login_page.py  –  Beautiful login screen
"""
import tkinter as tk
from tkinter import messagebox
import database
from utils import *


class LoginPage(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.on_login_success = on_login_success
        self._build_ui()

    def _build_ui(self):
        # ── Left decorative panel ─────────────────────────────────────────────
        left = tk.Frame(self, bg=BG_CARD2, width=420)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="🍳", font=("Segoe UI", 72),
                 bg=BG_CARD2, fg=ACCENT).place(relx=0.5, rely=0.30, anchor="center")
        tk.Label(left, text="PANTRIX", font=("Segoe UI", 32, "bold"),
                 bg=BG_CARD2, fg=TEXT_LIGHT).place(relx=0.5, rely=0.46, anchor="center")
        tk.Label(left, text="Smart Pantry Recipe Recommender",
                 font=("Segoe UI", 11), bg=BG_CARD2, fg=TEXT_DIM).place(
                     relx=0.5, rely=0.53, anchor="center")

        # decorative dots
        for i, (x, y, col) in enumerate([
            (0.2, 0.72, ACCENT), (0.5, 0.76, ACCENT2),
            (0.8, 0.72, TEAL),   (0.35, 0.80, GOLD),
            (0.65, 0.79, SUCCESS)
        ]):
            tk.Label(left, text="●", font=("Segoe UI", 18),
                     bg=BG_CARD2, fg=col).place(relx=x, rely=y, anchor="center")

        tk.Label(left, text="Cook smarter. Waste less. Eat better.",
                 font=("Segoe UI", 9, "italic"),
                 bg=BG_CARD2, fg=TEXT_DIM).place(relx=0.5, rely=0.88, anchor="center")

        # ── Right login form ──────────────────────────────────────────────────
        right = tk.Frame(self, bg=BG_DARK)
        right.pack(side="right", fill="both", expand=True)

        card = tk.Frame(right, bg=BG_CARD,
                        highlightbackground=ACCENT, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400)

        # Title bar strip
        strip = tk.Frame(card, bg=ACCENT, height=6)
        strip.pack(fill="x")

        tk.Label(card, text="Welcome Back 👋", font=("Segoe UI", 20, "bold"),
                 bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=(28, 2))
        tk.Label(card, text="Sign in to your account",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack(pady=(0, 24))

        def field(lbl, show=""):
            tk.Label(card, text=lbl, font=("Segoe UI", 10, "bold"),
                     bg=BG_CARD, fg=TEXT_DIM, anchor="w").pack(
                         fill="x", padx=36, pady=(0, 3))
            e = tk.Entry(card, font=FONT_BODY, bg="#252540",
                         fg=TEXT_LIGHT, insertbackground=ACCENT,
                         relief="flat", bd=8, show=show,
                         highlightthickness=1,
                         highlightbackground="#3a3a5c",
                         highlightcolor=ACCENT)
            e.pack(fill="x", padx=36, pady=(0, 16))
            return e

        self.entry_user = field("👤  Username")
        self.entry_pass = field("🔒  Password", show="●")

        make_button(card, "LOGIN  →", self._login,
                    bg=ACCENT, width=30, pady=12).pack(padx=36, pady=(4, 12))

        sep = tk.Frame(card, bg="#2a2a44", height=1)
        sep.pack(fill="x", padx=36, pady=4)

        tk.Label(card, text="New to PANTRIX?",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack(pady=(8, 4))
        make_button(card, "CREATE ACCOUNT", self._open_signup,
                    bg="#252540", width=30, pady=10).pack(padx=36, pady=(0, 32))

    def _login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        conn = database.get_connection()
        if not conn:
            messagebox.showerror("DB Error", "Cannot connect to database.")
            return
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            self.on_login_success(row[0], row[1])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def _open_signup(self):
        from signup_page import SignupPage
        self.pack_forget()
        SignupPage(self.master,
                   on_back=self._show_self,
                   on_signup_success=self.on_login_success).pack(
                       fill="both", expand=True)

    def _show_self(self):
        self.pack(fill="both", expand=True)