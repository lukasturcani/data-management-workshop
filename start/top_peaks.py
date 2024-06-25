import argparse
from pathlib import Path
import csv
from dataclasses import dataclass
from collections.abc import Iterator, Iterable


@dataclass(frozen=True, slots=True)
class Peak:
    ppm: float
    intensity: float


def main() -> None:
    args = parse_args()
    with open(args.peaks) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row["amine"], row["aldehyde"], row["topology"])
            if not row["imine_peaks"]:
                row["imine_peaks"] = "[]"
            if not row["imine_amplitudes"]:
                row["imine_amplitudes"] = "[]"
            if not row["aldehyde_peaks"]:
                row["aldehyde_peaks"] = "[]"
            if not row["aldehyde_amplitudes"]:
                row["aldehyde_amplitudes"] = "[]"
            imine_peaks = sorted(
                get_peaks(eval(row["imine_peaks"]), eval(row["imine_amplitudes"])),
                key=lambda peak: peak.intensity,
                reverse=True,
            )
            print("imine", imine_peaks[:2])
            aldehyde_peaks = sorted(
                get_peaks(
                    eval(row["aldehyde_peaks"]), eval(row["aldehyde_amplitudes"])
                ),
                key=lambda peak: peak.intensity,
                reverse=True,
            )
            print("aldehyde", aldehyde_peaks[:2])
            print()


def get_peaks(ppms: Iterable[float], intensities: Iterable[float]) -> Iterator[Peak]:
    for ppm, intensity in zip(ppms, intensities, strict=True):
        yield Peak(ppm, intensity)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("peaks", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
