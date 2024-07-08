import argparse
import json
from pathlib import Path
import rdkit.Chem as rdkit  # type: ignore
import stk


def main() -> None:
    args = parse_args()
    args.output.mkdir(exist_ok=True, parent=True)
    for cage in args.cage:
        output = args.output / cage.with_suffix(".csv").name
        molecule = rdkit.MolFromMolFile(cage)
        with open(output, "w") as f:
            json.dump({"diameter": diameter}, f)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("cage", type=Path, nargs="+")
    return parser.parse_args()


if __name__ == "__main__":
    main()
