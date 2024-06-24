import argparse
from pathlib import Path
import csv


def main() -> None:
    args = parse_args()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("peaks", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
