import stk
from pathlib import Path
from itertools import product
from enum import Enum, auto
from typing import assert_never


class Topology(Enum):
    FOUR_PLUS_SIX = auto()
    EIGHT_PLUS_TWELVE = auto()
    TWENTY_PLUS_THIRTY = auto()


def main() -> None:
    amines = [
        stk.BuildingBlock(smiles, stk.PrimaryAminoFactory())
        for smiles in Path("tri_amines.txt").read_text().splitlines()
        if not smiles.isspace()
    ]
    aldehydes = [
        stk.BuildingBlock(smiles, stk.AldehydeFactory())
        for smiles in Path("di_aldehydes.txt").read_text().splitlines()
        if not smiles.isspace()
    ]
    cages = Path("cages")
    cages.mkdir(exist_ok=True, parents=True)
    for amine, aldehyde, topology in product(amines, aldehydes, Topology):
        match topology:
            case Topology.FOUR_PLUS_SIX:
                graph = stk.cage.FourPlusSix([amine, aldehyde])
            case Topology.EIGHT_PLUS_TWELVE:
                graph = stk.cage.EightPlusTwelve([amine, aldehyde])
            case Topology.TWENTY_PLUS_THIRTY:
                graph = stk.cage.TwentyPlusThirty([amine, aldehyde])
            case _ as never:
                assert_never(never)
        cage = stk.ConstructedMolecule(graph)
        cage.write(cages / f"{smiles(amine)}_{smiles(aldehyde)}_{topology.name}.mol")


def smiles(molecule: stk.Molecule) -> str:
    return stk.Smiles().get_key(molecule)


if __name__ == "__main__":
    main()
