import tkinter as tk
from tkinter import font as tkfont

from skaki_engine import ola_ta_board_states


PIECES_UNICODE = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟",
}


def sxediase_tampla(headers, imikiniseis):
    aspros = headers.get("White", "?")
    mavros = headers.get("Black", "?")

    # states[0] = arxiki thesi, states[i] = thesi meta apo i imikiniseis.
    states = ola_ta_board_states(imikiniseis)
    katastasi = {"ply": 0}

    MEGETHOS = 64
    PERITHORIO = 28
    DIASTASI = MEGETHOS * 8
    XROMA_ANOIXTO = "#f0d9b5"
    XROMA_SKOURO = "#b58863"

    root = tk.Tk()
    root.title(f"Skakiera - {aspros} vs {mavros}")
    root.configure(bg="#312e2b")
    root.resizable(False, False)

    canvas = tk.Canvas(
        root,
        width=DIASTASI + 2 * PERITHORIO,
        height=DIASTASI + 2 * PERITHORIO,
        bg="#312e2b",
        highlightthickness=0,
    )
    canvas.pack(padx=10, pady=10)

    etiketa_font = ("Arial", 11, "bold")
    diathesimes = set(tkfont.families())
    for ypopsifia in ("Segoe UI Symbol", "DejaVu Sans", "Arial Unicode MS", "Arial"):
        if ypopsifia in diathesimes:
            piece_font = (ypopsifia, 40)
            break
    else:
        piece_font = ("Arial", 40)

    def sxediase():
        canvas.delete("all")
        board = states[katastasi["ply"]]["board"]

        for grammi in range(8):
            for stili in range(8):
                x1 = PERITHORIO + stili * MEGETHOS
                y1 = PERITHORIO + grammi * MEGETHOS
                xroma = XROMA_ANOIXTO if (grammi + stili) % 2 == 0 else XROMA_SKOURO
                canvas.create_rectangle(x1, y1, x1 + MEGETHOS, y1 + MEGETHOS, fill=xroma, outline=xroma)

                pioni = board[grammi][stili]
                if pioni != ".":
                    canvas.create_text(
                        x1 + MEGETHOS / 2, y1 + MEGETHOS / 2,
                        text=PIECES_UNICODE[pioni], font=piece_font,
                        fill="#ffffff" if pioni.isupper() else "#1a1a1a",
                    )

        for i in range(8):
            canvas.create_text(PERITHORIO / 2, PERITHORIO + i * MEGETHOS + MEGETHOS / 2,
                               text=str(8 - i), fill="#e8e6e3", font=etiketa_font)
            canvas.create_text(PERITHORIO + i * MEGETHOS + MEGETHOS / 2,
                               DIASTASI + PERITHORIO + PERITHORIO / 2,
                               text=chr(ord("a") + i), fill="#e8e6e3", font=etiketa_font)

        # enimerosi etiketas kai koumpion
        ply = katastasi["ply"]
        synolo = len(states) - 1
        if ply == 0:
            status_label.config(text=f"{ply} / {synolo}  (arxiki thesi)")
        else:
            status_label.config(text=f"{ply} / {synolo}:  {states[ply]['san']}")
        previous_move_button.config(state="normal" if ply > 0 else "disabled")
        next_move_button.config(state="normal" if ply < synolo else "disabled")

    def next_move():
        if katastasi["ply"] < len(states) - 1:
            katastasi["ply"] += 1
            sxediase()

    def previous_move():
        if katastasi["ply"] > 0:
            katastasi["ply"] -= 1
            sxediase()

    status_label = tk.Label(root, text="", bg="#312e2b", fg="#f7ec74", font=("Arial", 12, "bold"))
    status_label.pack()

    button_frame = tk.Frame(root, bg="#312e2b")
    button_frame.pack(pady=10)

    previous_move_button = tk.Button(button_frame, text="Previous move", command=previous_move, width=12)
    previous_move_button.pack(side="left", padx=5)

    next_move_button = tk.Button(button_frame, text="Next move", command=next_move, width=12)
    next_move_button.pack(side="left", padx=5)

    sxediase()
    root.mainloop()
