import re

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
