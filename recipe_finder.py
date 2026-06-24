"""
recipe_finder.py  –  No images. Clean card layout. Always works.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import database
from utils import *


class RecipeFinderPage(tk.Frame):
    def __init__(self, master, user_id, username, on_back, **_):
        super().__init__(master, bg=BG_DARK)
        self.user_id     = user_id
        self.username    = username
        self.on_back     = on_back
        self._recipe_map = {}
        self._build_ui()
        self._find_recipes()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=SUCCESS_DARK, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🍽️  Recipe Finder",
                 font=("Segoe UI", 16, "bold"),
                 bg=SUCCESS_DARK, fg="white").pack(side="left", padx=24, pady=16)
        make_button(hdr, "← Dashboard", self._go_back,
                    bg="#008c3a", width=16, pady=6).pack(
                        side="right", padx=20, pady=12)

        # Info bar
        info_bar = tk.Frame(self, bg=BG_CARD2)
        info_bar.pack(fill="x")
        self.info_lbl = tk.Label(
            info_bar, text="  🔄  Scanning your pantry…",
            font=("Segoe UI", 10), bg=BG_CARD2, fg=TEXT_DIM)
        self.info_lbl.pack(side="left", padx=20, pady=8)

        legend = tk.Frame(info_bar, bg=BG_CARD2)
        legend.pack(side="right", padx=20)
        for icon, txt, col in [
            ("✅", "Full Match", SUCCESS),
            ("⚠️", "1 Missing",  WARNING),
            ("♻️", "Substitute", ACCENT2),
            ("❌", "Partial",    DANGER),
        ]:
            tk.Label(legend, text=f"{icon} {txt}",
                     font=("Segoe UI", 9),
                     bg=BG_CARD2, fg=col).pack(side="left", padx=10, pady=8)

        # Scrollable card grid
        outer = tk.Frame(self, bg=BG_DARK)
        outer.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(outer, bg=BG_DARK, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical",
                             command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(self.canvas, bg=BG_DARK)
        self._cwin = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind(
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

    def _find_recipes(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self._recipe_map.clear()

        conn = database.get_connection()
        if not conn:
            tk.Label(self.grid_frame,
                     text="❌  Cannot connect to database.",
                     font=FONT_SUB, bg=BG_DARK, fg=DANGER).pack(pady=40)
            return

        cur = conn.cursor()

        cur.execute("SELECT ingredient_id FROM pantry WHERE user_id=%s",
                    (self.user_id,))
        pantry_ids = set(r[0] for r in cur.fetchall())

        if not pantry_ids:
            conn.close()
            self.info_lbl.config(
                text="  🧺  Pantry is empty — go back and add ingredients!")
            tk.Label(self.grid_frame,
                     text="🧺\n\nYour pantry is empty.\nAdd ingredients first.",
                     font=("Segoe UI", 14), bg=BG_DARK,
                     fg=TEXT_DIM, justify="center").pack(pady=60)
            return

        cur.execute("""
            SELECT r.recipe_id, r.recipe_name, r.cooking_time,
                   r.difficulty, ri.ingredient_id
            FROM recipes r
            JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
            ORDER BY r.recipe_id
        """)
        rows = cur.fetchall()

        recipe_info = {}
        recipe_ings = defaultdict(list)
        for rid, rname, ct, diff, iid in rows:
            recipe_info[rid] = (rname, ct, diff)
            recipe_ings[rid].append(iid)

        cur.execute("SELECT ingredient_id, substitute_id "
                    "FROM ingredient_substitutes")
        sub_map = defaultdict(list)
        for iid, sid in cur.fetchall():
            sub_map[iid].append(sid)

        cur.execute("SELECT ingredient_id, ingredient_name FROM ingredients")
        ing_names = {r[0]: r[1] for r in cur.fetchall()}
        conn.close()

        results = []
        for rid, ings in recipe_ings.items():
            total   = len(ings)
            matched = [i for i in ings if i in pantry_ids]
            missing = [i for i in ings if i not in pantry_ids]
            pct     = round(len(matched) * 100 / total)

            if not missing:
                status = "✅  Full Match"
                tag    = "full"
            elif len(missing) == 1:
                m_id = missing[0]
                subs = [s for s in sub_map.get(m_id, []) if s in pantry_ids]
                if subs:
                    status = (f"♻️  {ing_names.get(subs[0],'?')} "
                              f"→ {ing_names.get(m_id,'?')}")
                    tag = "sub"
                    pct = 100
                else:
                    status = f"⚠️  Missing: {ing_names.get(m_id,'?')}"
                    tag    = "one"
            else:
                status = f"❌  {len(missing)} ingredients missing"
                tag    = "partial"

            rname, ct, diff = recipe_info[rid]
            results.append((pct, rid, rname, status, ct, diff, tag, missing))

        results.sort(key=lambda x: -x[0])

        tag_colors = {
            "full":    SUCCESS,
            "one":     WARNING,
            "sub":     ACCENT2,
            "partial": DANGER,
        }

        CARDS_PER_ROW = 3
        for idx, (pct, rid, rname, status, ct, diff, tag, missing) in enumerate(results):
            col   = idx % CARDS_PER_ROW
            row   = idx // CARDS_PER_ROW
            color = tag_colors.get(tag, TEXT_DIM)
            card  = self._make_card(rid, rname, status,
                                     ct, diff, pct, color, missing, tag)
            card.grid(row=row, column=col,
                      padx=10, pady=10, sticky="nsew")

        for c in range(CARDS_PER_ROW):
            self.grid_frame.columnconfigure(c, weight=1, minsize=260)

        cookable = sum(1 for r in results if r[6] in ("full", "sub", "one"))
        self.info_lbl.config(
            text=(f"  🍳  {len(results)} recipes found  •  "
                  f"{cookable} cookable with your pantry  •  "
                  f"Click a card to open"))

    def _make_card(self, rid, rname, status,
                   ct, diff, pct, color, missing, tag):

        card = tk.Frame(self.grid_frame, bg=BG_CARD,
                        highlightbackground=color,
                        highlightthickness=2,
                        cursor="hand2",
                        width=280, height=210)
        card.pack_propagate(False)

        # Coloured top bar
        tk.Frame(card, bg=color, height=5).pack(fill="x")

        # Emoji + recipe name header
        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x", padx=12, pady=(10, 4))

        emoji = self._recipe_emoji(rname)
        tk.Label(top, text=emoji,
                 font=("Segoe UI", 28),
                 bg=BG_CARD, fg=color).pack(side="left", anchor="n")

        tk.Label(top, text=rname,
                 font=("Segoe UI", 12, "bold"),
                 bg=BG_CARD, fg=TEXT_LIGHT,
                 wraplength=200, justify="left",
                 anchor="nw").pack(side="left", padx=(10, 0), anchor="n")

        # Status badge
        badge = tk.Frame(card, bg=BG_DARK,
                         highlightbackground=color, highlightthickness=1)
        badge.pack(anchor="w", padx=12, pady=(2, 0))
        tk.Label(badge, text=f" {status} ",
                 font=("Segoe UI", 8, "bold"),
                 bg=BG_DARK, fg=color).pack(padx=2, pady=2)

        # Meta row
        meta = tk.Frame(card, bg=BG_CARD)
        meta.pack(fill="x", padx=12, pady=(6, 0))
        tk.Label(meta, text=f"⏱  {ct} min",
                 font=("Segoe UI", 9),
                 bg=BG_CARD, fg=TEAL).pack(side="left")
        tk.Label(meta, text=f"   🎯 {diff}",
                 font=("Segoe UI", 9),
                 bg=BG_CARD, fg=WARNING).pack(side="left")
        tk.Label(meta, text=f"   {pct}%",
                 font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=color).pack(side="left")

        # View button
        fg_btn = BG_DARK if color in (SUCCESS, WARNING) else TEXT_LIGHT
        make_button(
            card, "📖  View Recipe",
            lambda r=rid, m=missing, t=tag: self._open_recipe(r, m, t),
            bg=color, fg=fg_btn,
            width=26, pady=8).pack(fill="x", padx=12, pady=(10, 10))

        # Whole card is clickable
        def _click(e, r=rid, m=missing, t=tag):
            self._open_recipe(r, m, t)
        for w in [card, top, meta]:
            w.bind("<Button-1>", _click)

        return card

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

    def _open_recipe(self, rid, missing, tag):
        if len(missing) == 1 and tag == "one":
            conn = database.get_connection()
            cur  = conn.cursor()
            cur.execute(
                "SELECT ingredient_name FROM ingredients "
                "WHERE ingredient_id=%s", (missing[0],))
            row    = cur.fetchone()
            conn.close()
            m_name = row[0] if row else "Unknown"
            if not messagebox.askyesno(
                "⚠️  One Ingredient Missing",
                f"This recipe needs '{m_name}' which is not in your pantry.\n\n"
                f"Do you have '{m_name}' at home?"
            ):
                return

        from recipe_details import RecipeDetailsPage
        self.pack_forget()
        RecipeDetailsPage(
            self.master,
            user_id=self.user_id,
            username=self.username,
            recipe_id=rid,
            on_back=self._show_self
        ).pack(fill="both", expand=True)

    def _show_self(self):
        self.pack(fill="both", expand=True)

    def _go_back(self):
        self.pack_forget()
        self.on_back()