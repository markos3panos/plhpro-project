import os
import chess.pgn


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

            # Emfanisi stoixeiwn
            emfanise_stoixeia_partidas(game)

    except Exception as e:
        print("Parousiastike sfalma kata tin anagnwsi tou arxeiou.")
        print("Minyma sfalmatos:", e)


if __name__ == "__main__":
    main()
