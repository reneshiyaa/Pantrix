"""
signup_page.py  –  Beautiful signup screen
"""
import tkinter as tk
from tkinter import messagebox
import database
from utils import *


class SignupPage(tk.Frame):
    def __init__(self, master, on_back, on_signup_success):
        super().__init__(master, bg=BG_DARK)
        self.on_back = on_back
        self.on_signup_success = on_signup_success
        self._build_ui()

    def _build_ui(self):
        # Left decorative panel
        left = tk.Frame(self, bg=BG_CARD2, width=420)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="🥗", font=("Segoe UI", 72),
                 bg=BG_CARD2, fg=SUCCESS).place(relx=0.5, rely=0.28, anchor="center")
        tk.Label(left, text="Join PANTRIX", font=("Segoe UI", 26, "bold"),
                 bg=BG_CARD2, fg=TEXT_LIGHT).place(relx=0.5, rely=0.44, anchor="center")
        tk.Label(left, text="Your kitchen. Your recipes. Your way.",
                 font=("Segoe UI", 10), bg=BG_CARD2, fg=TEXT_DIM).place(
                     relx=0.5, rely=0.51, anchor="center")

        features = ["✅  Track pantry ingredients",
                    "🍽️  Find matching recipes",
                    "❤️  Save your favorites",
                    "🛒  Auto shopping list"]
        for i, f in enumerate(features):
            tk.Label(left, text=f, font=("Segoe UI", 10),
                     bg=BG_CARD2, fg=TEXT_DIM).place(
                         relx=0.15, rely=0.62 + i * 0.07, anchor="w")

        # Right form
        right = tk.Frame(self, bg=BG_DARK)
        right.pack(side="right", fill="both", expand=True)

        card = tk.Frame(right, bg=BG_CARD,
                        highlightbackground=SUCCESS, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400)

        tk.Frame(card, bg=SUCCESS, height=6).pack(fill="x")

        tk.Label(card, text="Create Account ✨",
                 font=("Segoe UI", 20, "bold"),
                 bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=(28, 2))
        tk.Label(card, text="It's free and takes 10 seconds",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack(pady=(0, 22))

        def field(lbl, show=""):
            tk.Label(card, text=lbl, font=("Segoe UI", 10, "bold"),
                     bg=BG_CARD, fg=TEXT_DIM, anchor="w").pack(
                         fill="x", padx=36, pady=(0, 3))
            e = tk.Entry(card, font=FONT_BODY, bg="#252540",
                         fg=TEXT_LIGHT, insertbackground=SUCCESS,
                         relief="flat", bd=8, show=show,
                         highlightthickness=1,
                         highlightbackground="#3a3a5c",
                         highlightcolor=SUCCESS)
            e.pack(fill="x", padx=36, pady=(0, 14))
            return e

        self.entry_user  = field("👤  Username")
        self.entry_email = field("📧  Email")
        self.entry_pass  = field("🔒  Password", show="●")

        make_button(card, "SIGN UP  →", self._signup,
                    bg=SUCCESS, fg=BG_DARK,
                    width=30, pady=12).pack(padx=36, pady=(6, 12))

        tk.Frame(card, bg="#2a2a44", height=1).pack(fill="x", padx=36, pady=4)

        make_button(card, "← Back to Login", self._go_back,
                    bg="#252540", width=30, pady=10).pack(
                        padx=36, pady=(8, 32))

    def _signup(self):
        username = self.entry_user.get().strip()
        email    = self.entry_email.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not email or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        conn = database.get_connection()
        if not conn:
            messagebox.showerror("DB Error", "Cannot connect to database.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                (username, email, password)
            )
            conn.commit()
            uid = cursor.lastrowid
            conn.close()
            messagebox.showinfo("Welcome! 🎉",
                                f"Account created! Welcome to PANTRIX, {username}!")
            self.on_signup_success(uid, username)
        except Exception as ex:
            conn.close()
            messagebox.showerror("Error", f"Signup failed:\n{ex}")

    def _go_back(self):
        self.pack_forget()
        self.on_back()