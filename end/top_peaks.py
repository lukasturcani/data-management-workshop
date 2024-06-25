import sqlite3
import argparse
import polars as pl
from pathlib import Path


def main() -> None:
    args = parse_args()
    connection = sqlite3.connect(args.database)
    cages = pl.read_database("SELECT * FROM cages", connection)
    imine_peaks = pl.read_database("SELECT * FROM imine_peaks", connection)
    imine_peaks = cages.join(imine_peaks, on="cage_id")
    top_peaks = (
        (
            imine_peaks.group_by("cage_id").agg(
                pl.col("peak_id").top_k_by("intensity", 2)
            )
        )
        .explode("peak_id")
        .join(imine_peaks, on="peak_id")
    )

    print(top_peaks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
