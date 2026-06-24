"""
recipe_details.py  –  No images. Clean layout. Always works.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import database
from utils import *


class RecipeDetailsPage(tk.Frame):
    def __init__(self, master, user_id, username, recipe_id, on_back, **_):
        super().__init__(master, bg=BG_DARK)
        self.user_id   = user_id
        self.username  = username
        self.recipe_id = recipe_id
        self.on_back   = on_back
        self._load_and_build()

    def _load_and_build(self):
        conn = database.get_connection()
        if not conn:
            messagebox.showerror("DB Error", "Cannot connect to database.")
            return
        cur = conn.cursor()

        cur.execute(
            "SELECT recipe_name, cooking_time, difficulty, instructions "
            "FROM recipes WHERE recipe_id=%s", (self.recipe_id,))
        rec = cur.fetchone()
        if not rec:
            messagebox.showerror("Error", "Recipe not found.")
            conn.close()
            return
        rname, ctime, diff, instructions = rec

        cur.execute("""
            SELECT i.ingredient_id, i.ingredient_name, ri.quantity
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
            WHERE ri.recipe_id=%s ORDER BY i.ingredient_name
        """, (self.recipe_id,))
        self.ing_rows = cur.fetchall()

        cur.execute("SELECT ingredient_id FROM pantry WHERE user_id=%s",
                    (self.user_id,))
        pantry_ids = set(r[0] for r in cur.fetchall())
        self.missing = [(i, n, q) for i, n, q in self.ing_rows
                        if i not in pantry_ids]
        conn.close()
        self._build_ui(rname, ctime, diff, instructions, pantry_ids)

    def _build_ui(self, rname, ctime, diff, instructions, pantry_ids):
        # ── Header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=ACCENT, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        emoji = self._recipe_emoji(rname)
        tk.Label(hdr, text=f"{emoji}  {rname}",
                 font=("Segoe UI", 15, "bold"),
                 bg=ACCENT, fg="white").pack(side="left", padx=24, pady=16)
        make_button(hdr, "← Back", self._go_back,
                    bg=ACCENT_DARK, width=12, pady=6).pack(
                        side="right", padx=20, pady=12)

        # ── Body ──────────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # ── LEFT – meta badges + instructions ─────────────────────────────────
        left = tk.Frame(body, bg=BG_CARD,
                        highlightbackground=ACCENT, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Frame(left, bg=ACCENT, height=4).pack(fill="x")

        # Big emoji banner
        banner = tk.Frame(left, bg="#12122a", height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner, text=emoji,
                 font=("Segoe UI", 60),
                 bg="#12122a", fg=ACCENT).place(relx=0.15, rely=0.5,
                                                 anchor="center")
        tk.Label(banner, text=rname,
                 font=("Segoe UI", 18, "bold"),
                 bg="#12122a", fg=TEXT_LIGHT).place(relx=0.55, rely=0.4,
                                                     anchor="center")
        tk.Label(banner, text="Smart Pantry Recipe Recommender",
                 font=("Segoe UI", 9),
                 bg="#12122a", fg=TEXT_DIM).place(relx=0.55, rely=0.72,
                                                   anchor="center")

        # Meta badges row
        badges = tk.Frame(left, bg=BG_CARD)
        badges.pack(fill="x", padx=16, pady=(12, 8))

        for icon, val, col, bg_col in [
            ("⏱️", f"  {ctime} minutes", TEAL,    "#0a2a2e"),
            ("🎯", f"  {diff}",          WARNING,  "#2e2800"),
            ("🧂", f"  {len(self.ing_rows)} ingredients",
                                          ACCENT,   "#1a1030"),
            ("⚠️" if self.missing else "✅",
             f"  {len(self.missing)} missing" if self.missing
             else "  All available",
             DANGER if self.missing else SUCCESS,
             "#2e0a0a" if self.missing else "#0a2e1a"),
        ]:
            b = tk.Frame(badges, bg=bg_col,
                         highlightbackground=col, highlightthickness=1)
            b.pack(side="left", padx=(0, 8), ipadx=8, ipady=5)
            tk.Label(b, text=icon + val,
                     font=("Segoe UI", 10, "bold"),
                     bg=bg_col, fg=col).pack()

        tk.Frame(left, bg="#2a2a44", height=1).pack(fill="x", padx=16, pady=4)

        # Instructions
        tk.Label(left, text="📋  Instructions",
                 font=FONT_SUB, bg=BG_CARD,
                 fg=TEXT_LIGHT).pack(anchor="w", padx=16, pady=(8, 6))

        txt_wrap = tk.Frame(left, bg="#1e1e38",
                            highlightbackground="#3a3a5c",
                            highlightthickness=1)
        txt_wrap.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        txt = tk.Text(txt_wrap, font=("Segoe UI", 11),
                      bg="#1e1e38", fg=TEXT_LIGHT,
                      relief="flat", bd=0, wrap="word",
                      state="normal", pady=12, padx=14,
                      spacing1=4, spacing3=4)
        txt.insert("1.0", instructions or "No instructions provided.")
        txt.config(state="disabled")
        tsb = ttk.Scrollbar(txt_wrap, orient="vertical",
                             command=txt.yview)
        txt.configure(yscrollcommand=tsb.set)
        tsb.pack(side="right", fill="y")
        txt.pack(fill="both", expand=True)

        # ── RIGHT – ingredients + action buttons ──────────────────────────────
        right = tk.Frame(body, bg=BG_CARD,
                         highlightbackground=SUCCESS, highlightthickness=1,
                         width=320)
        right.pack(side="right", fill="both")
        right.pack_propagate(False)
        tk.Frame(right, bg=SUCCESS, height=4).pack(fill="x")

        tk.Label(right, text="🧂  Ingredients",
                 font=FONT_SUB, bg=BG_CARD,
                 fg=TEXT_LIGHT).pack(anchor="w", padx=16, pady=(14, 6))

        # Column header
        ch = tk.Frame(right, bg="#1e3a2e")
        ch.pack(fill="x", padx=16)
        for t, w, a in [("Name", 16, "w"),
                          ("Qty",  9,  "center"),
                          ("✓",    4,  "center")]:
            tk.Label(ch, text=t, font=("Segoe UI", 9, "bold"),
                     bg="#1e3a2e", fg=SUCCESS,
                     width=w, anchor=a).pack(
                         side="left", padx=(6, 0), pady=5)

        # Ingredient rows (scrollable)
        ic = tk.Canvas(right, bg=BG_DARK, highlightthickness=0)
        isb = ttk.Scrollbar(right, orient="vertical", command=ic.yview)
        ic.configure(yscrollcommand=isb.set)
        isb.pack(side="right", fill="y", padx=(0, 4), pady=(0, 4))
        ic.pack(fill="x", padx=(16, 0), pady=(0, 4))

        ifr = tk.Frame(ic, bg=BG_DARK)
        iwin = ic.create_window((0, 0), window=ifr, anchor="nw")
        ifr.bind("<Configure>",
                  lambda e: ic.configure(scrollregion=ic.bbox("all")))
        ic.bind("<Configure>",
                lambda e: ic.itemconfig(iwin, width=e.width))

        for i, (iid, iname, qty) in enumerate(self.ing_rows):
            have   = iid in pantry_ids
            row_bg = BG_CARD if i % 2 == 0 else "#141428"
            r = tk.Frame(ifr, bg=row_bg)
            r.pack(fill="x")
            tk.Label(r, text=f"  {iname}",
                     font=("Segoe UI", 10), bg=row_bg,
                     fg=TEXT_LIGHT, width=16, anchor="w").pack(
                         side="left", pady=6)
            tk.Label(r, text=qty or "—",
                     font=("Segoe UI", 9), bg=row_bg,
                     fg=TEXT_DIM, width=9, anchor="center").pack(side="left")
            tk.Label(r, text="✅" if have else "❌",
                     font=("Segoe UI", 10), bg=row_bg,
                     fg=SUCCESS if have else DANGER,
                     width=4, anchor="center").pack(side="left")

        # ── Pinned action buttons ──────────────────────────────────────────────
        btn_area = tk.Frame(right, bg=BG_CARD)
        btn_area.pack(side="bottom", fill="x", padx=16, pady=(6, 14))
        tk.Frame(btn_area, bg=ACCENT, height=2).pack(fill="x", pady=(0, 10))

        make_button(btn_area, "❤️  Add to Favorites",
                    self._add_favorite, bg=ACCENT2,
                    width=28, pady=11).pack(fill="x", pady=(0, 8))

        if self.missing:
            make_button(btn_area,
                        "🛒  Add Missing to Shopping List",
                        self._add_to_shopping,
                        bg=WARNING, fg=BG_DARK,
                        width=28, pady=11).pack(fill="x", pady=(0, 8))

        make_button(btn_area, "← Back", self._go_back,
                    bg="#252540", width=28, pady=9).pack(fill="x")

    def _recipe_emoji(self, name):
        n = name.lower()
        if "rice"     in n:                                    return "🍚"
        if "egg"      in n or "omelette" in n \
                or "scrambled" in n or "toast" in n:           return "🍳"
        if "chicken"  in n:                                    return "🍗"
        if "pasta"    in n:                                    return "🍝"
        if "noodle"   in n:                                    return "🍜"
        if "soup"     in n:                                    return "🍲"
        if "salad"    in n:                                    return "🥗"
        if "pizza"    in n:                                    return "🍕"
        if "sandwich" in n or "bread" in n:                    return "🥪"
        if "pancake"  in n:                                    return "🥞"
        if "fruit"    in n:                                    return "🍎"
        return "🍽️"

    def _add_favorite(self):
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM favorites WHERE user_id=%s AND recipe_id=%s",
            (self.user_id, self.recipe_id))
        if cur.fetchone():
            messagebox.showinfo("Already Saved ❤️",
                                "This recipe is already in your favorites!")
            conn.close()
            return
        cur.execute(
            "INSERT INTO favorites (user_id, recipe_id) VALUES (%s,%s)",
            (self.user_id, self.recipe_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved! ❤️", "Recipe added to your favorites!")

    def _add_to_shopping(self):
        if not self.missing:
            return
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        added = 0
        for iid, name, qty in self.missing:
            cur.execute(
                "SELECT 1 FROM shopping_list "
                "WHERE ingredient_id=%s AND user_id=%s",
                (iid, self.user_id))
            if cur.fetchone():
                continue
            cur.execute(
                "INSERT INTO shopping_list "
                "(ingredient_id, quantity, user_id) VALUES (%s,%s,%s)",
                (iid, qty, self.user_id))
            added += 1
        conn.commit()
        conn.close()
        if added:
            messagebox.showinfo("Done! 🛒",
                                f"{added} ingredient(s) added to shopping list!")
        else:
            messagebox.showinfo("ℹ️  Info",
                                "Already in your shopping list.")

    def _go_back(self):
        self.pack_forget()
        self.on_back()