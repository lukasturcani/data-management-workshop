import argparse
import stk
from pathlib import Path
import sqlite3
import atomlite


def main() -> None:
    args = parse_args()
    db = atomlite.Database(args.database)
    connection = sqlite3.connect(args.database)
    for entry in db.get_entries():
        molecule = stk.BuildingBlock.init_from_rdkit_mol(
            atomlite.json_to_rdkit(entry.molecule)
        )
        connection.execute(
            "INSERT INTO cavity_sizes(cage_id, size) VALUES (?,?)",
            (
                int(entry.key),
                molecule.get_maximum_diameter(),
            ),
        )

    connection.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
