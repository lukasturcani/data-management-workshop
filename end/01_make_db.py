import sqlite3
from pathlib import Path
import argparse


def main() -> None:
    args = parse_args()
    connection = sqlite3.connect(args.database)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS cages (
            cage_id INTEGER PRIMARY KEY,
            amine TEXT,
            aldehyde TEXT,
            topology TEXT CHECK (topology IN ('FOUR_PLUS_SIX', 'EIGHT_PLUS_TWELVE', 'TWENTY_PLUS_THIRTY')),
            UNIQUE(amine, aldehyde, topology)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS aldehyde_peaks (
            peak_id INTEGER PRIMARY KEY,
            cage_id INTEGER,
            ppm REAL,
            intensity REAL,
            FOREIGN KEY (cage_id) REFERENCES cages(cage_id)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS imine_peaks (
            peak_id INTEGER PRIMARY KEY,
            cage_id INTEGER,
            ppm REAL,
            intensity REAL,
            FOREIGN KEY (cage_id) REFERENCES cages(cage_id)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS cavity_sizes (
            cavity_id INTEGER PRIMARY KEY,
            cage_id INTEGER,
            size REAL,
            UNIQUE(cage_id),
            FOREIGN KEY (cage_id) REFERENCES cages(cage_id)
        )
    """)
    connection.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
