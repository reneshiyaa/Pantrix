"""
favorites_page.py  –  Beautiful favorites screen
"""
import tkinter as tk
from tkinter import ttk, messagebox
import database
from utils import *


class FavoritesPage(tk.Frame):
    def __init__(self, master, user_id, username, on_back, **_):
        super().__init__(master, bg=BG_DARK)
        self.user_id  = user_id
        self.username = username
        self.on_back  = on_back
        self._fav_map = {}
        self._build_ui()
        self._load()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT2, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="❤️  Favorite Recipes",
                 font=("Segoe UI", 16, "bold"),
                 bg=ACCENT2, fg="white").pack(side="left", padx=24, pady=16)
        make_button(hdr, "← Dashboard", self._go_back,
                    bg="#aa00cc", width=16, pady=6).pack(
                        side="right", padx=20, pady=12)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=14)

        # Table
        tbl = tk.Frame(body, bg=BG_CARD,
                       highlightbackground=ACCENT2, highlightthickness=1)
        tbl.pack(side="left", fill="both", expand=True)
        tk.Frame(tbl, bg=ACCENT2, height=4).pack(fill="x")

        cols = ("  Recipe Name", "Cook Time", "Difficulty")
        self.tree = ttk.Treeview(tbl, columns=cols,
                                  show="headings", height=26)
        for c, w, a in zip(cols, [420, 140, 130], ["w", "center", "center"]):
            self.tree.heading(c, text=c.strip())
            self.tree.column(c, width=w, anchor=a)

        style = ttk.Style()
        style.configure("Treeview",
                         background=BG_CARD, foreground=TEXT_LIGHT,
                         fieldbackground=BG_CARD, rowheight=32,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                         background=ACCENT2, foreground="white",
                         font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", ACCENT)])

        vsb = ttk.Scrollbar(tbl, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=0)
        self.tree.bind("<Double-1>", lambda _: self._view_recipe())

        # Side panel
        side = tk.Frame(body, bg=BG_CARD,
                        highlightbackground=ACCENT2, highlightthickness=1,
                        width=200)
        side.pack(side="right", fill="y", padx=(14, 0))
        side.pack_propagate(False)

        tk.Frame(side, bg=ACCENT2, height=4).pack(fill="x")
        tk.Label(side, text="Actions", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=(16, 12))

        make_button(side, "📖  View Recipe",
                    self._view_recipe, bg=ACCENT,
                    width=18, pady=11).pack(padx=12, pady=6)
        make_button(side, "🗑️  Remove",
                    self._remove, bg=DANGER,
                    width=18, pady=11).pack(padx=12, pady=6)

        tk.Frame(side, bg="#2a2a44", height=1).pack(
            fill="x", padx=12, pady=10)
        tk.Label(side,
                 text="💡 Tip:\nDouble-click\nto view recipe",
                 font=("Segoe UI", 9), bg=BG_CARD,
                 fg=TEXT_DIM, justify="center").pack(pady=8)

    def _load(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self._fav_map.clear()

        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            """
            SELECT f.favorite_id, r.recipe_id, r.recipe_name,
                   r.cooking_time, r.difficulty
            FROM favorites f
            JOIN recipes r ON f.recipe_id = r.recipe_id
            WHERE f.user_id=%s ORDER BY r.recipe_name
            """, (self.user_id,))
        for fid, rid, rname, ct, diff in cur.fetchall():
            iid = self.tree.insert(
                "", "end", iid=fid,
                values=(f"  {rname}", f"{ct} min", diff))
            self._fav_map[iid] = rid
        conn.close()

    def _view_recipe(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a recipe first.")
            return
        rid = self._fav_map.get(sel[0])
        if not rid:
            return
        from recipe_details import RecipeDetailsPage
        self.pack_forget()
        RecipeDetailsPage(self.master,
                          user_id=self.user_id,
                          username=self.username,
                          recipe_id=rid,
                          on_back=self._show_self).pack(
                              fill="both", expand=True)

    def _show_self(self):
        self.pack(fill="both", expand=True)
        self._load()

    def _remove(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select",
                                "Please select a favorite to remove.")
            return
        if not messagebox.askyesno("Confirm",
                                    "Remove this recipe from favorites?"):
            return
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        for fid in sel:
            cur.execute("DELETE FROM favorites WHERE favorite_id=%s",
                        (int(fid),))
        conn.commit()
        conn.close()
        self._load()

    def _go_back(self):
        self.pack_forget()
        self.on_back()