import os
import gui_handler
import file_handler
import pgn_handler

def main():
    folder_path = input("Dwse to path tou fakelou me ta arxeia PGN: ").strip()

    if not os.path.isdir(folder_path):
        print("O fakelos den yparxei.")
        input("Press Enter to close...")
        return

    pgn_files = file_handler.evresi_pgn_arxeion(folder_path)

    selected_file = file_handler.epilogi_arxeiou(pgn_files)
    if selected_file is None:
        return

    file_path = os.path.join(folder_path, selected_file)

    try:
        headers, imikiniseis = pgn_handler.diavase_pgn_arxeio(file_path)

        if not headers and not imikiniseis:
            print("To arxeio den periexei egkiri partida.")
            return

        pgn_handler.emfanise_stoixeia_partidas(headers, imikiniseis)

        gui_handler.sxediase_tampla(headers)

    except Exception as e:
        print("Parousiastike sfalma kata tin anagnwsi tou arxeiou.")
        print("Minyma sfalmatos:", e)


if __name__ == "__main__":
    main()
