import gui_handler
import file_handler
import pgn_handler


def main():

    try:
        file_path = file_handler.resolve_pgn_folder()
        headers, imikiniseis = pgn_handler.diavase_pgn_arxeio(file_path)

        if not headers and not imikiniseis:
            print("To arxeio den periexei egkiri partida.")
            return

        pgn_handler.emfanise_stoixeia_partidas(headers, imikiniseis)

        gui_handler.sxediase_tampla(headers)

    except Exception as e:
        print("Parousiastike sfalma kata tin anagnwsi tou arxeiou.")
        print("Minyma sfalmatos: ", e)
        input("Press Enter to close...")


if __name__ == "__main__":
    main()
