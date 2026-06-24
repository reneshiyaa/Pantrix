"""
utils.py  –  PANTRIX design system (v2 – rich visual theme)
"""
import tkinter as tk

# ── Palette ──────────────────────────────────────────────────────────────────
BG_DARK      = "#0f0f1a"
BG_CARD      = "#1a1a2e"
BG_CARD2     = "#16213e"
ACCENT       = "#7c6af7"
ACCENT_DARK  = "#5a4fcf"
ACCENT2      = "#e040fb"
TEXT_LIGHT   = "#f0f0ff"
TEXT_DIM     = "#8888aa"
SUCCESS      = "#00e676"
SUCCESS_DARK = "#00c853"
DANGER       = "#ff5370"
DANGER_DARK  = "#c62828"
WARNING      = "#ffd740"
WARNING_DARK = "#f9a825"
GOLD         = "#ffc107"
TEAL         = "#00bcd4"

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_TITLE  = ("Segoe UI", 26, "bold")
FONT_SUB    = ("Segoe UI", 14, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 11, "bold")
FONT_HERO   = ("Segoe UI", 36, "bold")

# ── Reusable button ───────────────────────────────────────────────────────────
def make_button(parent, text, command, bg=None, fg=TEXT_LIGHT,
                width=22, pady=10, font=None):
    bg   = bg or ACCENT
    font = font or FONT_BTN
    # darken helper
    def darken(color):
        mapping = {
            ACCENT: ACCENT_DARK, SUCCESS: SUCCESS_DARK,
            DANGER: DANGER_DARK, WARNING: WARNING_DARK,
            GOLD: "#e6a800", TEAL: "#0097a7",
        }
        return mapping.get(color, "#333355")

    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg,
        activebackground=darken(bg), activeforeground=fg,
        relief="flat", font=font, cursor="hand2",
        width=width, pady=pady, bd=0,
        highlightthickness=0
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=darken(bg)))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def card_frame(parent, **kw):
    """A rounded-looking card frame."""
    return tk.Frame(parent, bg=BG_CARD,
                    highlightbackground=ACCENT,
                    highlightthickness=1, **kw)


def section_label(parent, text, fg=TEXT_LIGHT):
    tk.Label(parent, text=text, font=FONT_SUB,
             bg=BG_CARD, fg=fg).pack(anchor="w", padx=16, pady=(14, 4))


def divider(parent, bg=ACCENT):
    tk.Frame(parent, bg=bg, height=2).pack(fill="x", padx=16, pady=4)