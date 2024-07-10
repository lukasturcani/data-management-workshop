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
        molecule = stk.BuildingBlock.init_from_rdkit_mol(entry.to_rdkit())
        connection.execute(
            "INSERT INTO cavity_sizes(cage_id, size) VALUES (?,?)",
            (
                molecule.get_maximum_diameter(),
                entry.properties["cage_id"],
            ),
        )

    connection.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
