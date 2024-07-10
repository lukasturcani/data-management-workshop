import stk
import argparse
from pathlib import Path
from itertools import product
from enum import Enum, auto
from typing import assert_never
import atomlite


class Topology(Enum):
    FOUR_PLUS_SIX = auto()
    EIGHT_PLUS_TWELVE = auto()
    TWENTY_PLUS_THIRTY = auto()


AMINES = [
    "Nc1nc(N)nc(N)n1",
    "Cc1c(CN)c(C)c(CN)c(C)c1CN",
    "NCCN(CCN)CCN",
    "CCc1c(CN)c(CC)c(CN)c(CC)c1CN",
    "NCCCN(CCCN)CCCN",
]

ALDEHYDES = [
    "O=Cc1cccc(C=O)c1",
    "CC(C)(C)c1cc(C=O)c(O)c(C=O)c1",
    "O=Cc1cc2sc(C=O)cc2s1",
    "O=Cc1ccc(C=O)cc1",
    "O=Cc1c(F)c(F)c(C=O)c(F)c1F",
]


def main() -> None:
    args = parse_args()
    db = atomlite.Database(args.database)
    amines = [stk.BuildingBlock(smiles, stk.PrimaryAminoFactory()) for smiles in AMINES]
    aldehydes = [
        stk.BuildingBlock(smiles, stk.AldehydeFactory()) for smiles in ALDEHYDES
    ]
    for amine, aldehyde, topology in product(amines, aldehydes, Topology):
        graph: stk.TopologyGraph
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
        cursor = db.connection.execute(
            """
            INSERT INTO cages(amine, aldehyde, topology)
            VALUES (?,?,?)
            """,
            (smiles(amine), smiles(aldehyde), topology.name),
        )
        db.add_entries(
            atomlite.Entry.from_rdkit(
                key=str(cursor.lastrowid),
                molecule=cage.to_rdkit_mol(),
            ),
            commit=False,
        )
    db.connection.commit()


def smiles(molecule: stk.Molecule) -> str:
    return stk.Smiles().get_key(molecule)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
