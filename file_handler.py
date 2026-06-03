import os


BASE_DIR = os.getcwd()
DEFAULT_PATH = os.path.join(BASE_DIR, "pgn_files")


def evresi_pgn_arxeion(folder_path):
    pgn_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pgn")]
    return pgn_files


def epilogi_arxeiou(pgn_files):
    if not pgn_files:
        raise ValueError("No valid PGN files were found in the provided directory.")

    print("\nDiathesima arxeia PGN:")
    for i, file_name in enumerate(pgn_files, start=1):
        print(f"{i}. {file_name}")

    while True:
        choice = int(input("\nDwse ton arithmo tou arxeiou pou thes na anoixeis: "))
        if 1 <= choice <= len(pgn_files):
            return pgn_files[choice - 1]
        else:
            print("Lathos epilogi. Dokimase xana.")


def get_folder_path():
    folder_path = input("Dwse to path tou fakelou me ta arxeia PGN: ").strip()

    if not os.path.isdir(folder_path):
        print("O fakelos den yparxei.")
        print("Attempting to load from default path './pgn_files'.")

        if not os.path.isdir(DEFAULT_PATH):
            print("Default path './pgn_files' was not found.")
            raise ValueError("No valid path was found.")

        return DEFAULT_PATH

    return folder_path


def resolve_pgn_folder():
    try:
        folder_path = get_folder_path()

        pgn_files = evresi_pgn_arxeion(folder_path)

        selected_file = epilogi_arxeiou(pgn_files)
        if not selected_file:
            raise ValueError("Error opening selected file.")

        return os.path.join(folder_path, selected_file)

    except Exception as ex:
        raise ex
