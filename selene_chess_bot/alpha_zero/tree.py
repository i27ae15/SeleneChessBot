import networkx as nx

from selene_chess_bot.alpha_zero.node import GameStateNode


def create_tree_representation(
    parent: 'GameStateNode',
    visited: set = None,
    count_nodes: bool = False,
    nx_graph: nx.DiGraph = None,
) -> nx.DiGraph:
    """
    Create the nx.Diagraph tree code representation with a DFS on the tree.
    """

    if nx_graph is None:
        nx_graph = nx.DiGraph()

    if visited is None:
        visited = set()

    # Check if the current node has already been visited
    if str(parent.board_hash) in visited:
        return nx_graph

    # Mark the current node as visited
    visited.add(str(parent.board_hash))

    if len(parent.children) == 0:
        return nx_graph

    for child in parent.children:
        child: GameStateNode
        nx_graph.add_edge(str(parent.board_hash), str(child.board_hash))
        create_tree_representation(
            parent=child,
            visited=visited,
            nx_graph=nx_graph,
            count_nodes=count_nodes,
        )

    return nx_graph
