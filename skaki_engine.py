"""
Mikri mihani skakiou: pairnei tis imikiniseis se morfi SAN (opos epistrefei
to pgn_handler) kai paragei tin thesi tis skakieras meta apo kathe imikinisi.

Den xreiazetai kapoia exoteriki vivliothiki (px python-chess).

Dimosia synartisi:
    ola_ta_board_states(imikiniseis) -> list apo katastaseis

Kathe katastasi einai ena dict:
    {
        "board": 8x8 lista (idia morfi me to ARXIKI_THESI),
        "apo":   (grammi, stili) tis afetirias tis teleftaias kinisis i None,
        "pros":  (grammi, stili) tou proorismou tis teleftaias kinisis i None,
        "san":   to keimeno tis kinisis i None (gia tin arxiki thesi),
    }

Symvasi syntetagmenon (idia me to gui_handler):
    board[grammi][stili], grammi 0 = 8i sira (mavra), grammi 7 = 1i sira (lefka),
    stili 0 = stili 'a'. Kefalaia = lefka, peza = mavra, "." = adeio.
"""

import re

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

# Anagnorisi enos SAN token: [kommati][stili-diafor.][grammi-diafor.][x][proorismos][=anavathmisi]
_SAN_RE = re.compile(r"^([KQRBN]?)([a-h]?)([1-8]?)(x?)([a-h][1-8])(=([QRBN]))?$")


def _antigrafo(board):
    return [row[:] for row in board]


def _sq_se_rc(sq):
    """ 'e4' -> (grammi, stili) """
    stili = ord(sq[0]) - ord("a")
    grammi = 8 - int(sq[1])
    return grammi, stili


def _kathari_diadromi(board, sr, sc, dr, dc):
    """ True an ola ta tetragona ANAMESA stin afetiria kai ton proorismo einai adeia. """
    stepr = (dr > sr) - (dr < sr)
    stepc = (dc > sc) - (dc < sc)
    r, c = sr + stepr, sc + stepc
    while (r, c) != (dr, dc):
        if board[r][c] != ".":
            return False
        r += stepr
        c += stepc
    return True


def _mporei_na_paei(board, sr, sc, dr, dc, kommati):
    """ Geometriki dynatotita kinisis (xoris elegxo xromatos proorismou). """
    typos = kommati.upper()
    ddr = dr - sr
    ddc = dc - sc
    if typos == "N":
        return (abs(ddr), abs(ddc)) in ((1, 2), (2, 1))
    if typos == "K":
        return max(abs(ddr), abs(ddc)) == 1
    if typos == "R":
        if ddr != 0 and ddc != 0:
            return False
        return _kathari_diadromi(board, sr, sc, dr, dc)
    if typos == "B":
        if abs(ddr) != abs(ddc):
            return False
        return _kathari_diadromi(board, sr, sc, dr, dc)
    if typos == "Q":
        if ddr == 0 or ddc == 0 or abs(ddr) == abs(ddc):
            return _kathari_diadromi(board, sr, sc, dr, dc)
        return False
    return False


def _apeileitai(board, r, c, apo_lefka):
    """ Apeileitai to tetragono (r,c) apo kommati xromatos apo_lefka? """
    # peza
    if apo_lefka:
        for dc in (-1, 1):
            rr, cc = r + 1, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8 and board[rr][cc] == "P":
                return True
    else:
        for dc in (-1, 1):
            rr, cc = r - 1, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8 and board[rr][cc] == "p":
                return True
    # alogo
    alogo = "N" if apo_lefka else "n"
    for dr, dc in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < 8 and 0 <= cc < 8 and board[rr][cc] == alogo:
            return True
    # vasilias
    vasilias = "K" if apo_lefka else "k"
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8 and board[rr][cc] == vasilias:
                return True
    # pyrgos / vasilissa (orthogonia)
    pyrgos = "R" if apo_lefka else "r"
    aksios = "B" if apo_lefka else "b"
    vasilissa = "Q" if apo_lefka else "q"
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        while 0 <= rr < 8 and 0 <= cc < 8:
            p = board[rr][cc]
            if p != ".":
                if p == pyrgos or p == vasilissa:
                    return True
                break
            rr += dr
            cc += dc
    # aksiomatikos / vasilissa (diagonia)
    for dr, dc in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        rr, cc = r + dr, c + dc
        while 0 <= rr < 8 and 0 <= cc < 8:
            p = board[rr][cc]
            if p != ".":
                if p == aksios or p == vasilissa:
                    return True
                break
            rr += dr
            cc += dc
    return False


def _vasilias_se_sax(board, lefka):
    vasilias = "K" if lefka else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == vasilias:
                return _apeileitai(board, r, c, not lefka)
    return False


def _kastling(board, lefka, kingside):
    r = 7 if lefka else 0
    vasilias = "K" if lefka else "k"
    pyrgos = "R" if lefka else "r"
    board[r][4] = "."
    if kingside:
        board[r][6] = vasilias
        board[r][7] = "."
        board[r][5] = pyrgos
        return board, (r, 4), (r, 6)
    else:
        board[r][2] = vasilias
        board[r][0] = "."
        board[r][3] = pyrgos
        return board, (r, 4), (r, 2)


def efarmose_kinisi(board, san, lefka_paizoun):
    """
    Efarmozei mia imikinisi (SAN) panw se antigrafo tou board.
    Epistrefei (neo_board, afetiria_rc, proorismos_rc).
    Se periptosi pou den anagnoristei i kinisi, epistrefei to board os exei.
    """
    board = _antigrafo(board)
    s = san.strip().rstrip("+#!?")
    s = s.replace("e.p.", "")

    # roke (dexetai kai 0-0)
    xoris_zero = s.replace("0", "O")
    if xoris_zero in ("O-O", "O-O-O"):
        return _kastling(board, lefka_paizoun, xoris_zero == "O-O")

    m = _SAN_RE.match(s)
    if not m:
        return board, None, None

    kommati_gramma, fdis, rdis, _cap, proorismos, _eq, anav = m.groups()
    dr, dc = _sq_se_rc(proorismos)

    # --- kinisi pezou ---
    if kommati_gramma == "":
        pion = "P" if lefka_paizoun else "p"
        if fdis:  # aiximalotismos pezou (peritha pezou pantote dilonei stili)
            sc = ord(fdis) - ord("a")
            sr = dr + 1 if lefka_paizoun else dr - 1
            # en passant: an o proorismos einai adeios
            if board[dr][dc] == ".":
                board[dr + (1 if lefka_paizoun else -1)][dc] = "."
            board[sr][sc] = "."
        else:  # eftheia kinisi
            sc = dc
            r1 = dr + 1 if lefka_paizoun else dr - 1
            if 0 <= r1 < 8 and board[r1][sc] == pion:
                sr = r1
            else:
                sr = dr + 2 if lefka_paizoun else dr - 2
            board[sr][sc] = "."

        if anav:
            board[dr][dc] = anav.upper() if lefka_paizoun else anav.lower()
        else:
            board[dr][dc] = pion
        return board, (sr, sc), (dr, dc)

    # --- kinisi figouras ---
    kommati = kommati_gramma if lefka_paizoun else kommati_gramma.lower()
    ypopsifies = []
    for r in range(8):
        for c in range(8):
            if board[r][c] != kommati:
                continue
            if fdis and c != ord(fdis) - ord("a"):
                continue
            if rdis and r != 8 - int(rdis):
                continue
            if _mporei_na_paei(board, r, c, dr, dc, kommati):
                ypopsifies.append((r, c))

    # an parameinoun perissoteres apo mia, filtrare me vasi to an afinoun ton vasilia se sax
    if len(ypopsifies) > 1:
        nomimes = []
        for (r, c) in ypopsifies:
            dok = _antigrafo(board)
            dok[dr][dc] = dok[r][c]
            dok[r][c] = "."
            if not _vasilias_se_sax(dok, lefka_paizoun):
                nomimes.append((r, c))
        if nomimes:
            ypopsifies = nomimes

    if not ypopsifies:
        return board, None, None

    sr, sc = ypopsifies[0]
    board[dr][dc] = board[sr][sc]
    board[sr][sc] = "."
    return board, (sr, sc), (dr, dc)


def ola_ta_board_states(imikiniseis):
    """
    Pairnei tin lista imikiniseon kai epistrefei tis katastaseis tis skakieras:
    index 0 = arxiki thesi, index i = thesi meta apo i imikiniseis.
    """
    states = [{"board": _antigrafo(ARXIKI_THESI), "apo": None, "pros": None, "san": None}]
    board = _antigrafo(ARXIKI_THESI)
    lefka = True
    for san in imikiniseis:
        try:
            board, apo, pros = efarmose_kinisi(board, san, lefka)
        except Exception:
            apo = pros = None
        states.append({"board": _antigrafo(board), "apo": apo, "pros": pros, "san": san})
        lefka = not lefka
    return states
