import argparse
import json
from pathlib import Path
import stk


def main() -> None:
    args = parse_args()
    args.output.mkdir(exist_ok=True, parents=True)
    for cage in args.cage:
        output = args.output / cage.with_suffix(".json").name
        molecule = stk.BuildingBlock.init_from_file(cage)
        with open(output, "w") as f:
            json.dump({"diameter": molecule.get_maximum_diameter()}, f)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("cage", type=Path, nargs="+")
    return parser.parse_args()


if __name__ == "__main__":
    main()
