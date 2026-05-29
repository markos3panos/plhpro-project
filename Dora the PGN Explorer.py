import os
import re
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


def evresi_pgn_arxeion(folder_path):
    pgn_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pgn")]
    return pgn_files


def epilogi_arxeiou(pgn_files):
    if not pgn_files:
        print("Den vrethikan arxeia PGN ston fakelo.")
        return None

    print("\nDiathesima arxeia PGN:")
    for i, file_name in enumerate(pgn_files, start=1):
        print(f"{i}. {file_name}")

    while True:
        try:
            choice = int(input("\nDwse ton arithmo tou arxeiou pou thes na anoixeis: "))
            if 1 <= choice <= len(pgn_files):
                return pgn_files[choice - 1]
            else:
                print("Lathos epilogi. Dokimase xana.")
        except ValueError:
            print("Parakalw dwse enan egkiro arithmo.")


def diavase_pgn_arxeio(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        keimeno = f.read()

    headers = {}
    grammes_kiniseon = []
    se_kiniseis = False

    for grammi in keimeno.splitlines():
        kathari = grammi.strip()

        if not se_kiniseis:
            if kathari.startswith("[") and kathari.endswith("]"):
                esoteriko = kathari[1:-1]
                kena = esoteriko.find(" ")
                if kena > 0:
                    kleidi = esoteriko[:kena]
                    timi_meros = esoteriko[kena + 1:].strip()
                    if timi_meros.startswith('"') and timi_meros.endswith('"'):
                        timi = timi_meros[1:-1]
                    else:
                        timi = timi_meros
                    headers[kleidi] = timi
            elif kathari == "":
                if headers:
                    se_kiniseis = True
            else:
                se_kiniseis = True
                grammes_kiniseon.append(grammi)
        else:
            grammes_kiniseon.append(grammi)

    keimeno_kiniseon = " ".join(grammes_kiniseon)

    keimeno_kiniseon = re.sub(r"\{[^}]*\}", "", keimeno_kiniseon)

    while True:
        neo = re.sub(r"\([^()]*\)", "", keimeno_kiniseon)
        if neo == keimeno_kiniseon:
            break
        keimeno_kiniseon = neo

    keimeno_kiniseon = re.sub(r"\$\d+", "", keimeno_kiniseon)

    apotelesmata = {"1-0", "0-1", "1/2-1/2", "*"}

    imikiniseis = []
    for token in keimeno_kiniseon.split():
        if token in apotelesmata:
            continue

        kathara = re.sub(r"^\d+\.+", "", token)

        if kathara == "":
            continue

        imikiniseis.append(kathara)

    return headers, imikiniseis


def metrise_plies(imikiniseis):
    return len(imikiniseis)


def pare_kiniseis_se_morfi_keimenou(imikiniseis):
    moves_text = ""
    move_number = 1

    for i, kinisi in enumerate(imikiniseis):
        if i % 2 == 0:
            moves_text += f"{move_number}. "
        moves_text += kinisi + " "
        if i % 2 == 1:
            move_number += 1

    return moves_text.strip()


def spase_keimeno(text, max_chars=70):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


def emfanise_stoixeia_partidas(headers, imikiniseis):
    plies = metrise_plies(imikiniseis)

    print("\n----- STOIXEIA PARTIDAS -----\n")
    print(f'[Event "{headers.get("Event", "?")}"]')
    print(f'[Site "{headers.get("Site", "?")}"]')
    print(f'[Date "{headers.get("Date", "?")}"]')
    print(f'[EventDate "{headers.get("EventDate", "?")}"]')
    print(f'[Round "{headers.get("Round", "?")}"]')
    print(f'[Result "{headers.get("Result", "?")}"]')
    print(f'[White "{headers.get("White", "?")}"]')
    print(f'[Black "{headers.get("Black", "?")}"]')
    print(f'[ECO "{headers.get("ECO", "?")}"]')
    print(f'[WhiteElo "{headers.get("WhiteElo", "?")}"]')
    print(f'[BlackElo "{headers.get("BlackElo", "?")}"]')
    print(f'[PlyCount "{plies}"]')

    print("\n----- KINISEIS -----\n")
    moves_text = pare_kiniseis_se_morfi_keimenou(imikiniseis)
    lines = spase_keimeno(moves_text, 70)

    for line in lines:
        print(line)


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


def main():
    folder_path = input("Dwse to path tou fakelou me ta arxeia PGN: ").strip()

    if not os.path.isdir(folder_path):
        print("O fakelos den yparxei.")
        return

    pgn_files = evresi_pgn_arxeion(folder_path)

    selected_file = epilogi_arxeiou(pgn_files)
    if selected_file is None:
        return

    file_path = os.path.join(folder_path, selected_file)

    try:
        headers, imikiniseis = diavase_pgn_arxeio(file_path)

        if not headers and not imikiniseis:
            print("To arxeio den periexei egkiri partida.")
            return

        emfanise_stoixeia_partidas(headers, imikiniseis)

        sxediase_tampla(headers)

    except Exception as e:
        print("Parousiastike sfalma kata tin anagnwsi tou arxeiou.")
        print("Minyma sfalmatos:", e)


if __name__ == "__main__":
    main()
