import os


def evresi_pgn_arxeion(folder_path):
    pgn_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pgn")]
    return pgn_files


def epilogi_arxeiou(pgn_files):
    if not pgn_files:
        print("Den vrethikan arxeia PGN ston fakelo.")
        input("Press Enter to close...")
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
