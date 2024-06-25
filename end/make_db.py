import sqlite3
from pathlib import Path
import argparse
from dataclasses import dataclass
import csv
from collections.abc import Iterator, Iterable


@dataclass(frozen=True, slots=True)
class Peak:
    ppm: float
    intensity: float


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
            FOREIGN KEY (cage_id) REFERENCES cages(id)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS imine_peaks (
            peak_id INTEGER PRIMARY KEY,
            cage_id INTEGER,
            ppm REAL,
            intensity REAL,
            FOREIGN KEY (cage_id) REFERENCES cages(id)
        )
    """)

    with open(args.csv) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row["imine_peaks"]:
                row["imine_peaks"] = "[]"
            if not row["imine_amplitudes"]:
                row["imine_amplitudes"] = "[]"
            if not row["aldehyde_peaks"]:
                row["aldehyde_peaks"] = "[]"
            if not row["aldehyde_amplitudes"]:
                row["aldehyde_amplitudes"] = "[]"
            cage_id = connection.execute(
                "INSERT INTO cages(amine, aldehyde, topology) VALUES (?,?,?)",
                (row["amine"], row["aldehyde"], row["topology"]),
            ).lastrowid
            for peak in get_peaks(
                eval(row["imine_peaks"]), eval(row["imine_amplitudes"])
            ):
                connection.execute(
                    "INSERT INTO imine_peaks(cage_id, ppm, intensity) VALUES (?,?,?)",
                    (cage_id, peak.ppm, peak.intensity),
                )
            for peak in get_peaks(
                eval(row["aldehyde_peaks"]), eval(row["aldehyde_amplitudes"])
            ):
                connection.execute(
                    "INSERT INTO aldehyde_peaks(cage_id, ppm, intensity) VALUES (?,?,?)",
                    (cage_id, peak.ppm, peak.intensity),
                )
    connection.commit()


def get_peaks(ppms: Iterable[float], intensities: Iterable[float]) -> Iterator[Peak]:
    for ppm, intensity in zip(ppms, intensities, strict=True):
        yield Peak(ppm, intensity)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
