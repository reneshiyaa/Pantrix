"""
shopping_list_page.py  –  Beautiful shopping list page
"""
import tkinter as tk
from tkinter import ttk, messagebox
import database
from utils import *


class ShoppingListPage(tk.Frame):
    def __init__(self, master, user_id, username, on_back, **_):
        super().__init__(master, bg=BG_DARK)
        self.user_id  = user_id
        self.username = username
        self.on_back  = on_back
        self._build_ui()
        self._load()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=WARNING_DARK, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🛒  Shopping List",
                 font=("Segoe UI", 16, "bold"),
                 bg=WARNING_DARK, fg=BG_DARK).pack(
                     side="left", padx=24, pady=16)
        make_button(hdr, "← Dashboard", self._go_back,
                    bg="#c47f00", fg=BG_DARK,
                    width=16, pady=6).pack(
                        side="right", padx=20, pady=12)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=14)

        # Table
        tbl = tk.Frame(body, bg=BG_CARD,
                       highlightbackground=WARNING, highlightthickness=1)
        tbl.pack(side="left", fill="both", expand=True)
        tk.Frame(tbl, bg=WARNING, height=4).pack(fill="x")

        cols = ("  Ingredient", "Quantity")
        self.tree = ttk.Treeview(tbl, columns=cols,
                                  show="headings", height=26)
        for c, w, a in zip(cols, [500, 220], ["w", "center"]):
            self.tree.heading(c, text=c.strip())
            self.tree.column(c, width=w, anchor=a)

        style = ttk.Style()
        style.configure("Treeview",
                         background=BG_CARD, foreground=TEXT_LIGHT,
                         fieldbackground=BG_CARD, rowheight=32,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                         background=WARNING_DARK, foreground=BG_DARK,
                         font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", ACCENT)])

        vsb = ttk.Scrollbar(tbl, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Side panel
        side = tk.Frame(body, bg=BG_CARD,
                        highlightbackground=WARNING, highlightthickness=1,
                        width=200)
        side.pack(side="right", fill="y", padx=(14, 0))
        side.pack_propagate(False)

        tk.Frame(side, bg=WARNING, height=4).pack(fill="x")
        tk.Label(side, text="Actions", font=FONT_SUB,
                 bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=(16, 12))

        make_button(side, "🗑️  Delete Item",
                    self._delete, bg=DANGER,
                    width=18, pady=11).pack(padx=12, pady=6)
        make_button(side, "🗑️  Clear All",
                    self._delete_all, bg=DANGER,
                    width=18, pady=11).pack(padx=12, pady=6)

        tk.Frame(side, bg="#2a2a44", height=1).pack(
            fill="x", padx=12, pady=10)
        tk.Label(side,
                 text="💡 Tip:\nItems are added\nautomatically\nfrom recipes",
                 font=("Segoe UI", 9), bg=BG_CARD,
                 fg=TEXT_DIM, justify="center").pack(pady=8)

    def _load(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute(
            """
            SELECT s.shopping_id, i.ingredient_name, s.quantity
            FROM shopping_list s
            JOIN ingredients i ON s.ingredient_id = i.ingredient_id
            WHERE s.user_id=%s ORDER BY i.ingredient_name
            """, (self.user_id,))
        for sid, name, qty in cur.fetchall():
            self.tree.insert("", "end", iid=sid,
                             values=(f"  {name}", qty or "—"))
        conn.close()

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select an item to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected item(s)?"):
            return
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        for sid in sel:
            cur.execute("DELETE FROM shopping_list WHERE shopping_id=%s",
                        (int(sid),))
        conn.commit()
        conn.close()
        self._load()

    def _delete_all(self):
        if not messagebox.askyesno("Confirm",
                                    "Clear your entire shopping list?"):
            return
        conn = database.get_connection()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("DELETE FROM shopping_list WHERE user_id=%s",
                    (self.user_id,))
        conn.commit()
        conn.close()
        self._load()

    def _go_back(self):
        self.pack_forget()
        self.on_back()