"""
dashboard.py  –  Fixed card layout, wider cards, no text cutoff
"""
import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
import database
from utils import *


class DashboardPage(tk.Frame):
    def __init__(self, master, user_id, username, on_logout):
        super().__init__(master, bg=BG_DARK)
        self.user_id   = user_id
        self.username  = username
        self.on_logout = on_logout
        self._build_ui()
        self.after(500, self._check_expiry)

    def _build_ui(self):
        # ── Top navbar ────────────────────────────────────────────────────────
        nav = tk.Frame(self, bg=BG_CARD2, height=64)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        tk.Label(nav, text="🍳  PANTRIX",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG_CARD2, fg=ACCENT).pack(side="left", padx=30, pady=14)

        user_pill = tk.Frame(nav, bg=ACCENT, padx=14, pady=5)
        user_pill.pack(side="right", padx=20, pady=14)
        tk.Label(user_pill, text=f"👤  {self.username}",
                 font=("Segoe UI", 10, "bold"),
                 bg=ACCENT, fg="white").pack()

        # ── Hero ──────────────────────────────────────────────────────────────
        hero = tk.Frame(self, bg=BG_DARK)
        hero.pack(fill="x", padx=50, pady=(28, 6))

        tk.Label(hero, text=f"Hello, {self.username}! 👋",
                 font=("Segoe UI", 28, "bold"),
                 bg=BG_DARK, fg=TEXT_LIGHT).pack(anchor="w")
        tk.Label(hero, text="What would you like to cook today?",
                 font=("Segoe UI", 12),
                 bg=BG_DARK, fg=TEXT_DIM).pack(anchor="w")

        tk.Frame(self, bg=ACCENT, height=2).pack(
            fill="x", padx=50, pady=(8, 20))

        # ── Cards grid – centred, wider cards ─────────────────────────────────
        grid_wrap = tk.Frame(self, bg=BG_DARK)
        grid_wrap.pack(expand=True)

        cards = [
            ("🥦", "Add Pantry Ingredients",
             "Manage what's in your kitchen",    ACCENT,   self._open_pantry),
            ("🍽️", "Find Recipes",
             "Match recipes to your pantry",     SUCCESS,  self._open_finder),
            ("❤️", "Favorites",
             "Your saved recipe collection",     ACCENT2,  self._open_favs),
            ("🛒", "Shopping List",
             "Ingredients you need to buy",      WARNING,  self._open_shop),
        ]

        for i, (icon, title, desc, color, cmd) in enumerate(cards):
            col = i % 2
            row = i // 2
            self._make_card(
                grid_wrap, icon, title, desc, color, cmd
            ).grid(row=row, column=col, padx=20, pady=12, sticky="nsew")

        grid_wrap.columnconfigure(0, weight=1, minsize=320)
        grid_wrap.columnconfigure(1, weight=1, minsize=320)

        # ── Logout ────────────────────────────────────────────────────────────
        make_button(self, "🚪  Logout", self._logout,
                    bg=DANGER, width=20, pady=10).pack(pady=(14, 28))

    # ── Card factory ──────────────────────────────────────────────────────────
    def _make_card(self, parent, icon, title, desc, color, cmd):
        card = tk.Frame(parent, bg=BG_CARD,
                        highlightbackground=color,
                        highlightthickness=2,
                        cursor="hand2",
                        width=300, height=150)
        card.pack_propagate(False)

        # Coloured top bar
        tk.Frame(card, bg=color, height=6).pack(fill="x")

        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="both", expand=True, padx=20, pady=12)

        # Icon + title on same row — icon fixed size, title wraps
        top = tk.Frame(inner, bg=BG_CARD)
        top.pack(fill="x")

        tk.Label(top, text=icon,
                 font=("Segoe UI", 26),
                 bg=BG_CARD, fg=color,
                 width=2).pack(side="left", anchor="n")

        tk.Label(top, text=title,
                 font=("Segoe UI", 13, "bold"),
                 bg=BG_CARD, fg=TEXT_LIGHT,
                 justify="left", wraplength=200,
                 anchor="nw").pack(side="left", padx=(10, 0), anchor="n")

        tk.Label(inner, text=desc,
                 font=("Segoe UI", 9),
                 bg=BG_CARD, fg=TEXT_DIM,
                 justify="left").pack(anchor="w", pady=(8, 0))

        # Hover effect
        def _set_bg(widget, bg):
            try:
                widget.config(bg=bg)
                for child in widget.winfo_children():
                    _set_bg(child, bg)
            except Exception:
                pass

        def on_enter(_):
            _set_bg(card, color)
        def on_leave(_):
            _set_bg(card, BG_CARD)

        for w in [card] + self._all_children(card):
            w.bind("<Button-1>", lambda e, c=cmd: c())
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)

        return card

    def _all_children(self, widget):
        result = []
        for child in widget.winfo_children():
            result.append(child)
            result.extend(self._all_children(child))
        return result

    # ── Navigation ────────────────────────────────────────────────────────────
    def _switch(self, PageClass):
        self.pack_forget()
        PageClass(self.master,
                  user_id=self.user_id,
                  username=self.username,
                  on_back=self._show_self).pack(fill="both", expand=True)

    def _show_self(self):
        self.pack(fill="both", expand=True)

    def _open_pantry(self):
        from pantry_page import PantryPage
        self._switch(PantryPage)

    def _open_finder(self):
        from recipe_finder import RecipeFinderPage
        self._switch(RecipeFinderPage)

    def _open_favs(self):
        from favorites_page import FavoritesPage
        self._switch(FavoritesPage)

    def _open_shop(self):
        from shopping_list_page import ShoppingListPage
        self._switch(ShoppingListPage)

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.pack_forget()
            self.on_logout()

    # ── Expiry alert ──────────────────────────────────────────────────────────
    def _check_expiry(self):
        conn = database.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        threshold = date.today() + timedelta(days=3)
        cursor.execute(
            """
            SELECT i.ingredient_name, p.expiry_date
            FROM pantry p
            JOIN ingredients i ON p.ingredient_id = i.ingredient_id
            WHERE p.user_id=%s AND p.expiry_date IS NOT NULL
              AND p.expiry_date <= %s
            ORDER BY p.expiry_date
            """,
            (self.user_id, threshold)
        )
        rows = cursor.fetchall()
        conn.close()
        if rows:
            lines = "\n".join(
                f"  • {r[0]}  (expires {r[1]})" for r in rows)
            messagebox.showwarning(
                "⚠️  Expiry Alert",
                "The following ingredients expire within 3 days:\n\n" + lines
            )