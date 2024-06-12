from dataclasses import dataclass

from typing import TypedDict, Optional


class TreeRepresentation(TypedDict):

    """
    A dictionary intended to representation a tree structure.

    {
        'Node_0_ID': {
            'children': ['Node_1_ID', 'Node_2_ID']
        },
        'Node_1_ID': {
            'children': ['Node_3_ID', 'Node_4_ID']
        }
        ...

        Have in mind that a gs can have multiple children and multiple
        parents.

        'Node_5_ID': {
            'children': ['Node_1_ID', 'Node_2_ID']
        }

        ...

        Plus at the end of the nodes, we can add the nx.DiGraph representation

        'nx.DiGraph

    }
    """
    node_id: dict[str, dict[str, list[str]]]


@dataclass
class FENInfo:
    board: list[list[str]]
    active_color: str
    castling_rights: dict[str, dict[str, bool]]
    en_passant_target: Optional[str]
    halfmove_clock: int
    fullmove_number: int
