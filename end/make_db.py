import sqlite3
from pathlib import Path
import argparse


def main() -> None:
    args = parse_args()
    connection = sqlite3.connect(args.database)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS cages (
            id INTEGER PRIMARY KEY,
            amine TEXT,
            aldehyde TEXT,
            topology TEXT CHECK (topology IN ('FOUR_PLUS_SIX', 'EIGHT_PLUS_TWELVE', 'TWENTY_PLUS_THIRTY')),
            UNIQUE(amine, aldehyde, topology),
        );
        CREATE TABLE IF NOT EXISTS aldehyde_peaks (
            id INTEGER PRIMARY KEY,
            cage_id INTEGER,
            ppm REAL,
            intensity REAL,
            FOREIGN KEY (cage_id) REFERENCES cages(id)
        );
        CREATE TABLE IF NOT EXISTS imine_peaks (
            id INTEGER PRIMARY KEY,
            cage_id INTEGER,
            ppm REAL,
            intensity REAL,
            FOREIGN KEY (cage_id) REFERENCES cages(id)
        );
    """)

    # for row in rows(args.csv):
    #     connection.execute("INSERT INTO cages VALUES ()")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
