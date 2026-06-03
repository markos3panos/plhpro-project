import tkinter as tk
from tkinter import font as tkfont


PIECES_UNICODE = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟",
}

ARXIKI_THESI = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


def sxediase_tampla(headers):
    aspros = headers.get("White", "?")
    mavros = headers.get("Black", "?")

    root = tk.Tk()
    root.title(f"Skakiera - {aspros} vs {mavros}")
    root.configure(bg="#312e2b")
    root.resizable(False, False)

    MEGETHOS = 64
    PERITHORIO = 28
    DIASTASI = MEGETHOS * 8

    XROMA_ANOIXTO = "#f0d9b5"
    XROMA_SKOURO = "#b58863"

    canvas = tk.Canvas(
        root,
        width=DIASTASI + 2 * PERITHORIO,
        height=DIASTASI + 2 * PERITHORIO,
        bg="#312e2b",
        highlightthickness=0,
    )
    canvas.pack(padx=10, pady=10)

    for grammi in range(8):
        for stili in range(8):
            x1 = PERITHORIO + stili * MEGETHOS
            y1 = PERITHORIO + grammi * MEGETHOS
            x2 = x1 + MEGETHOS
            y2 = y1 + MEGETHOS
            xroma = XROMA_ANOIXTO if (grammi + stili) % 2 == 0 else XROMA_SKOURO
            canvas.create_rectangle(x1, y1, x2, y2, fill=xroma, outline=xroma)

    etiketa_font = ("Arial", 11, "bold")
    for i in range(8):
        canvas.create_text(
            PERITHORIO / 2,
            PERITHORIO + i * MEGETHOS + MEGETHOS / 2,
            text=str(8 - i),
            fill="#e8e6e3",
            font=etiketa_font,
        )
        canvas.create_text(
            PERITHORIO + i * MEGETHOS + MEGETHOS / 2,
            DIASTASI + PERITHORIO + PERITHORIO / 2,
            text=chr(ord("a") + i),
            fill="#e8e6e3",
            font=etiketa_font,
        )

    diathesimes = set(tkfont.families())
    for ypopsifia in ("Segoe UI Symbol", "DejaVu Sans", "Arial Unicode MS", "Arial"):
        if ypopsifia in diathesimes:
            piece_font = (ypopsifia, 40)
            break
    else:
        piece_font = ("Arial", 40)

    for grammi in range(8):
        for stili in range(8):
            pioni = ARXIKI_THESI[grammi][stili]
            if pioni == ".":
                continue
            x = PERITHORIO + stili * MEGETHOS + MEGETHOS / 2
            y = PERITHORIO + grammi * MEGETHOS + MEGETHOS / 2
            symvolo = PIECES_UNICODE[pioni]
            skia_xroma = "#000000" if pioni.isupper() else "#3a3a3a"
            kyrio_xroma = "#ffffff" if pioni.isupper() else "#1a1a1a"
            canvas.create_text(x + 1, y + 1, text=symvolo, font=piece_font, fill=skia_xroma)
            canvas.create_text(x, y, text=symvolo, font=piece_font, fill=kyrio_xroma)

    info = tk.Label(
        root,
        text=f"{aspros}  (lefka)   vs   {mavros}  (mavra)",
        bg="#312e2b",
        fg="#e8e6e3",
        font=("Arial", 11, "bold"),
        pady=6,
    )
    info.pack(side="bottom")

    root.mainloop()
