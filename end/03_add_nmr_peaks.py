from pathlib import Path
from collections.abc import Iterator, Iterable
import sqlite3
import argparse
import csv
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Peak:
    ppm: float
    intensity: float


def main() -> None:
    args = parse_args()
    connection = sqlite3.connect(args.database)
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
                "SELECT cage_id FROM cages WHERE amine=? AND aldehyde=? AND topology=?",
                (row["amine"], row["aldehyde"], row["topology"]),
            ).fetchone()[0]
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
