"""
pantry_page.py  –  Fixed: Search for Recipes button always visible,
                   pinned at the very bottom of the right panel.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import database
from utils import *


class PantryPage(tk.Frame):
    def __init__(self, master, user_id, username, on_back, **_):
        super().__init__(master, bg=BG_DARK)
        self.user_id  = user_id
        self.username = username
        self.on_back  = on_back
        self.all_ingredients = []
        self._build_ui()
        self._load_ingredients()
        self._load_pantry()

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=ACCENT, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🥦  Pantry Manager",
                 font=("Segoe UI", 16, "bold"),
                 bg=ACCENT, fg="white").pack(side="left", padx=24, pady=16)
        make_button(hdr, "← Dashboard", self._go_back,
                    bg=ACCENT_DARK, width=16, pady=6).pack(
                        side="right", padx=20, pady=12)

        # ── Body (left + right side by side) ──────────────────────────────────
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=24, pady=16)

        # ════════════════════════════════════════════════════════════
        # LEFT – ingredient search & listbox
        # ════════════════════════════════════════════════════════════
        left = tk.Frame(body, bg=BG_CARD,
                        highlightbackground=ACCENT, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))

        tk.Frame(left, bg=ACCENT, height=4).pack(fill="x")

        tk.Label(left, text="🔍  Search & Select Ingredients",
                 font=FONT_SUB, bg=BG_CARD, fg=TEXT_LIGHT).pack(
                     anchor="w", padx=16, pady=(14, 6))

        # Search box
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter)
        sw = tk.Frame(left, bg="#252540",
                      highlightbackground=ACCENT, highlightthickness=1)
        sw.pack(fill="x", padx=16, pady=(0, 6))
        tk.Label(sw, text="🔍", font=("Segoe UI", 11),
                 bg="#252540", fg=TEXT_DIM).pack(side="left", padx=(8, 0))
        tk.Entry(sw, textvariable=self.search_var,
                 font=FONT_BODY, bg="#252540", fg=TEXT_LIGHT,
                 insertbackground=ACCENT, relief="flat", bd=6,
                 highlightthickness=0).pack(
                     side="left", fill="x", expand=True)

        tk.Label(left, text="Hold Ctrl to select multiple ingredients",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack(
                     anchor="w", padx=16, pady=(0, 6))

        lb_frame = tk.Frame(left, bg=BG_CARD)
        lb_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.listbox = tk.Listbox(
            lb_frame, selectmode="extended",
            bg="#1e1e38", fg=TEXT_LIGHT, font=FONT_BODY,
            relief="flat", selectbackground=ACCENT,
            selectforeground="white", activestyle="none",
            bd=0, highlightthickness=0)
        lsb = ttk.Scrollbar(lb_frame, orient="vertical",
                             command=self.listbox.yview)
        self.listbox.config(yscrollcommand=lsb.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        lsb.pack(side="left", fill="y")

        # ════════════════════════════════════════════════════════════
        # RIGHT – expiry + add button + pantry list + SEARCH RECIPES
        # ════════════════════════════════════════════════════════════
        right = tk.Frame(body, bg=BG_CARD,
                         highlightbackground=SUCCESS, highlightthickness=1,
                         width=390)
        right.pack(side="right", fill="both")
        right.pack_propagate(False)

        tk.Frame(right, bg=SUCCESS, height=4).pack(fill="x")

        # ── Expiry date field ─────────────────────────────────────────────────
        tk.Label(right, text="📅  Expiry Date  (YYYY-MM-DD)",
                 font=("Segoe UI", 10, "bold"),
                 bg=BG_CARD, fg=TEXT_DIM).pack(
                     anchor="w", padx=16, pady=(14, 4))

        ew = tk.Frame(right, bg="#252540",
                      highlightbackground=SUCCESS, highlightthickness=1)
        ew.pack(fill="x", padx=16, pady=(0, 10))
        self.expiry_var = tk.StringVar()
        tk.Entry(ew, textvariable=self.expiry_var,
                 font=FONT_BODY, bg="#252540", fg=TEXT_LIGHT,
                 insertbackground=SUCCESS, relief="flat", bd=8,
                 highlightthickness=0).pack(fill="x")

        # ── Add button ────────────────────────────────────────────────────────
        make_button(right, "➕  Add Selected to Pantry",
                    self._add_to_pantry, bg=ACCENT,
                    width=32, pady=11).pack(padx=16, pady=(0, 12))

        tk.Frame(right, bg="#2a2a44", height=1).pack(fill="x", padx=16)

        # ── Pantry label ──────────────────────────────────────────────────────
        tk.Label(right, text="🧺  Your Current Pantry",
                 font=FONT_SUB, bg=BG_CARD, fg=TEXT_LIGHT).pack(
                     anchor="w", padx=16, pady=(10, 6))

        # Column header strip
        ch = tk.Frame(right, bg=ACCENT)
        ch.pack(fill="x", padx=16)
        for txt, w, anc in [("Ingredient", 18, "w"),
                              ("Expiry",     12, "center"),
                              ("",           10, "center")]:
            tk.Label(ch, text=txt, font=("Segoe UI", 9, "bold"),
                     bg=ACCENT, fg="white", width=w,
                     anchor=anc).pack(side="left",
                                      padx=(6, 0), pady=6)

        # ── Scrollable pantry rows  (expands to fill available space) ─────────
        scroll_area = tk.Frame(right, bg=BG_DARK)
        scroll_area.pack(fill="both", expand=True, padx=16, pady=(0, 0))

        self.canvas = tk.Canvas(scroll_area, bg=BG_DARK,
                                highlightthickness=0)
        vsb = ttk.Scrollbar(scroll_area, orient="vertical",
                             command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.rows_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self._cwin = self.canvas.create_window(
            (0, 0), window=self.rows_frame, anchor="nw")

        self.rows_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self._cwin, width=e.width))
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(
                -1 * (e.delta // 120), "units"))

        # ── PINNED BOTTOM SECTION – always visible ────────────────────────────
        bottom = tk.Frame(right, bg=BG_CARD)
        bottom.pack(side="bottom", fill="x", padx=16, pady=(0, 14))

        tk.Frame(bottom, bg=ACCENT, height=2).pack(fill="x", pady=(6, 10))

        make_button(bottom, "🍽️  Search for Recipes",
                    self._search_recipes, bg=SUCCESS,
                    fg=BG_DARK, width=32, pady=13).pack(fill="x")

    # ── Ingredient list ───────────────────────────────────────────────────────
    def _load_ingredients(self):
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            "SELECT ingredient_id, ingredient_name "
            "FROM ingredients ORDER BY ingredient_name")
        self.all_ingredients = cur.fetchall()
        conn.close()
        self._populate_listbox(self.all_ingredients)

    def _populate_listbox(self, items):
        self.listbox.delete(0, "end")
        for _, name in items:
            self.listbox.insert("end", f"  {name}")

    def _filter(self, *_):
        term = self.search_var.get().lower()
        self._filt = [(i, n) for i, n in self.all_ingredients
                      if term in n.lower()]
        self._populate_listbox(self._filt)

    @property
    def _filtered(self):
        return getattr(self, "_filt", self.all_ingredients)

    # ── Add to pantry ─────────────────────────────────────────────────────────
    def _add_to_pantry(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning(
                "Nothing Selected",
                "Please select at least one ingredient from the list.")
            return
        expiry = self.expiry_var.get().strip() or None
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        added = 0
        for idx in sel:
            iid, _ = self._filtered[idx]
            cur.execute(
                "SELECT 1 FROM pantry WHERE user_id=%s AND ingredient_id=%s",
                (self.user_id, iid))
            if cur.fetchone():
                continue
            cur.execute(
                "INSERT INTO pantry (user_id, ingredient_id, expiry_date) "
                "VALUES (%s, %s, %s)",
                (self.user_id, iid, expiry))
            added += 1
        conn.commit()
        conn.close()
        if added:
            messagebox.showinfo("✅  Added",
                                f"{added} ingredient(s) added to pantry!")
        else:
            messagebox.showinfo("ℹ️  Info",
                                "All selected ingredients are already in pantry.")
        self._load_pantry()

    # ── Pantry rows with inline ✕ Remove ─────────────────────────────────────
    def _load_pantry(self):
        for w in self.rows_frame.winfo_children():
            w.destroy()

        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.pantry_id, i.ingredient_name, p.expiry_date
            FROM pantry p
            JOIN ingredients i ON p.ingredient_id = i.ingredient_id
            WHERE p.user_id = %s
            ORDER BY i.ingredient_name
            """,
            (self.user_id,))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            tk.Label(
                self.rows_frame,
                text="🧺  Your pantry is empty\n\nSelect ingredients on the\nleft and click Add.",
                font=("Segoe UI", 10), bg=BG_DARK,
                fg=TEXT_DIM, justify="center").pack(pady=24)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return

        for i, (pid, name, expiry) in enumerate(rows):
            row_bg = BG_CARD if i % 2 == 0 else "#141428"
            row = tk.Frame(self.rows_frame, bg=row_bg)
            row.pack(fill="x")

            tk.Label(row, text=f"  {name}",
                     font=FONT_BODY, bg=row_bg, fg=TEXT_LIGHT,
                     width=18, anchor="w").pack(side="left", pady=7)

            exp_col = DANGER if expiry else TEXT_DIM
            tk.Label(row,
                     text=str(expiry) if expiry else "—",
                     font=("Segoe UI", 9), bg=row_bg,
                     fg=exp_col, width=12,
                     anchor="center").pack(side="left", pady=7)

            tk.Button(
                row, text="✕ Remove",
                font=("Segoe UI", 8, "bold"),
                bg=DANGER, fg="white",
                activebackground=DANGER_DARK, activeforeground="white",
                relief="flat", bd=0, cursor="hand2",
                padx=8, pady=3,
                command=lambda p=pid, n=name: self._remove_row(p, n)
            ).pack(side="left", padx=8, pady=5)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _remove_row(self, pantry_id, name):
        if not messagebox.askyesno("Confirm",
                                   f"Remove '{name}' from pantry?"):
            return
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("DELETE FROM pantry WHERE pantry_id=%s", (pantry_id,))
        conn.commit()
        conn.close()
        self._load_pantry()

    # ── Search for Recipes ────────────────────────────────────────────────────
    def _search_recipes(self):
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM pantry WHERE user_id=%s", (self.user_id,))
        count = cur.fetchone()[0]
        conn.close()

        if count == 0:
            messagebox.showwarning(
                "Empty Pantry",
                "Your pantry is empty!\nPlease add at least one ingredient first.")
            return

        from recipe_finder import RecipeFinderPage
        self.pack_forget()
        RecipeFinderPage(
            self.master,
            user_id=self.user_id,
            username=self.username,
            on_back=self._show_self
        ).pack(fill="both", expand=True)

    def _show_self(self):
        self.pack(fill="both", expand=True)
        self._load_pantry()

    def _go_back(self):
        self.pack_forget()
        self.on_back()