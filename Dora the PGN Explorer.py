import os
import tkinter as tk
from tkinter import font as tkfont
import chess.pgn


# Unicode symvola gia ta pionia tou skakiou
PIECES_UNICODE = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟",
}

# Arxiki diataxi - kefalaia=lefka, peza=mavra, telia=adeio tetragono
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


# Sinartisi pou vriskει ola ta arxeia .pgn mesa se enan fakelo
def evresi_pgn_arxeion(folder_path):
    pgn_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pgn")]
    return pgn_files


# Sinartisi pou deixnei ti lista ton arxeion kai zita epilogi
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


# Sinartisi pou metraei to plithos twn plies (half-moves)
def metrise_plies(game):
    count = 0
    node = game

    while node.variations:
        node = node.variation(0)
        count += 1

    return count


# Sinartisi pou metatrepei tis kiniseis se morfi SAN
def pare_kiniseis_se_morfi_keimenou(game):
    board = game.board()
    moves_text = ""
    move_number = 1

    for move in game.mainline_moves():
        if board.turn:  # aspros paizei
            moves_text += f"{move_number}. "
        moves_text += board.san(move) + " "
        if not board.turn:  # molis epaikse o mavros, pame se epomeno arithmo kinisis
            move_number += 1
        board.push(move)

    return moves_text.strip()


# Sinartisi pou spaei ena keimeno se grammes me megisto mikos
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


# Sinartisi pou emfanizei ta stoixeia tis partitδας opws sto screenshot
def emfanise_stoixeia_partidas(game):
    headers = game.headers
    plies = metrise_plies(game)

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
    moves_text = pare_kiniseis_se_morfi_keimenou(game)
    lines = spase_keimeno(moves_text, 70)

    for line in lines:
        print(line)


# Sinartisi pou sxediazei to tampla tou skakiou se tkinter parathiro
# kai topothetei ta pionia stin arxiki tous thesi (Erotima iii)
def sxediase_tampla(game):
    headers = game.headers
    aspros = headers.get("White", "?")
    mavros = headers.get("Black", "?")

    root = tk.Tk()
    root.title(f"Skakiera - {aspros} vs {mavros}")
    root.configure(bg="#312e2b")
    root.resizable(False, False)

    MEGETHOS = 64               # megethos kathenos tetragonou se pixel
    PERITHORIO = 28             # peritorio gia tis etiketes a-h kai 1-8
    DIASTASI = MEGETHOS * 8

    XROMA_ANOIXTO = "#f0d9b5"   # anoixto tetragono
    XROMA_SKOURO = "#b58863"    # skouro tetragono

    canvas = tk.Canvas(
        root,
        width=DIASTASI + 2 * PERITHORIO,
        height=DIASTASI + 2 * PERITHORIO,
        bg="#312e2b",
        highlightthickness=0,
    )
    canvas.pack(padx=10, pady=10)

    # Sxediasi twn 64 tetragonon
    for grammi in range(8):
        for stili in range(8):
            x1 = PERITHORIO + stili * MEGETHOS
            y1 = PERITHORIO + grammi * MEGETHOS
            x2 = x1 + MEGETHOS
            y2 = y1 + MEGETHOS
            xroma = XROMA_ANOIXTO if (grammi + stili) % 2 == 0 else XROMA_SKOURO
            canvas.create_rectangle(x1, y1, x2, y2, fill=xroma, outline=xroma)

    # Etiketes: arithmoi 1-8 aristera kai grammata a-h kato
    etiketa_font = ("Arial", 11, "bold")
    for i in range(8):
        # arithmos grammis (8 panw, 1 kato)
        canvas.create_text(
            PERITHORIO / 2,
            PERITHORIO + i * MEGETHOS + MEGETHOS / 2,
            text=str(8 - i),
            fill="#e8e6e3",
            font=etiketa_font,
        )
        # gramma stilis (a aristera, h dexia)
        canvas.create_text(
            PERITHORIO + i * MEGETHOS + MEGETHOS / 2,
            DIASTASI + PERITHORIO + PERITHORIO / 2,
            text=chr(ord("a") + i),
            fill="#e8e6e3",
            font=etiketa_font,
        )

    # Epilogi katallilis grammatoseiras gia ta symvola tou skakiou
    diathesimes = set(tkfont.families())
    for ypopsifia in ("Segoe UI Symbol", "DejaVu Sans", "Arial Unicode MS", "Arial"):
        if ypopsifia in diathesimes:
            piece_font = (ypopsifia, 40)
            break
    else:
        piece_font = ("Arial", 40)

    # Topothetisi pionion stin arxiki tous thesi
    for grammi in range(8):
        for stili in range(8):
            pioni = ARXIKI_THESI[grammi][stili]
            if pioni == ".":
                continue
            x = PERITHORIO + stili * MEGETHOS + MEGETHOS / 2
            y = PERITHORIO + grammi * MEGETHOS + MEGETHOS / 2
            symvolo = PIECES_UNICODE[pioni]
            # Skia gia kalitero contrast kai meta to kyrio symvolo
            skia_xroma = "#000000" if pioni.isupper() else "#3a3a3a"
            kyrio_xroma = "#ffffff" if pioni.isupper() else "#1a1a1a"
            canvas.create_text(x + 1, y + 1, text=symvolo, font=piece_font, fill=skia_xroma)
            canvas.create_text(x, y, text=symvolo, font=piece_font, fill=kyrio_xroma)

    # Pliroforiaki etiketa stin koryfi me tous paiktes
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
    # O xristis dinei to path tou fakelou
    folder_path = input("Dwse to path tou fakelou me ta arxeia PGN: ").strip()

    if not os.path.isdir(folder_path):
        print("O fakelos den yparxei.")
        return

    # Vriskei ta pgn arxeia
    pgn_files = evresi_pgn_arxeion(folder_path)

    # O xristis epilegei ena arxeio
    selected_file = epilogi_arxeiou(pgn_files)
    if selected_file is None:
        return

    file_path = os.path.join(folder_path, selected_file)

    try:
        with open(file_path, "r", encoding="utf-8") as pgn_file:
            # Diavazoume tin proti partita apo to arxeio
            game = chess.pgn.read_game(pgn_file)

            if game is None:
                print("To arxeio den periexei egkiri partida.")
                return

            # Emfanisi stoixeiwn (Erotima ii)
            emfanise_stoixeia_partidas(game)

            # Anoigma grafikis skakieras me ta pionia stin arxiki thesi (Erotima iii)
            sxediase_tampla(game)

    except Exception as e:
        print("Parousiastike sfalma kata tin anagnwsi tou arxeiou.")
        print("Minyma sfalmatos:", e)


if __name__ == "__main__":
    main()
