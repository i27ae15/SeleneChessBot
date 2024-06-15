import numpy as np
import pandas as pd

from alpha_zero.node import GameStateNode
from alpha_zero.state_manager import StateManager

from core.printing import __print__ as pprint
from core.utils import INITIAL_FEN

from game import Game
from game.checkmate_detector import CheckmateDetector

from pieces.utilites import PLAYER_VALUES

# TODO:
# Check if possibel to Add the checkmate routes to the MCST to choose those
# moves instead of calculating them again


class MCST:
    def __init__(
        self,
        model=None,
        initial_fen: str = None,
        root: GameStateNode = None,
        exploration_weight: float = 1.414,
        state_manager: StateManager = None,
    ):
        """
        Initialize the Monte Carlo Search Tree with the initial game state.

        Parameters:
        -----------
        initial_fen : str
            The initial FEN (Forsyth-Edwards Notation) string representing the
            starting position of the game.
        """

        self.model = model
        self.root: GameStateNode = root

        self.initial_fen = None
        self.__initialize_fen(initial_fen, root)
        self.state_manager = state_manager or StateManager()
        self.game: Game = Game.parse_fen(self.initial_fen)

        if not self.root:
            self.root = GameStateNode.create_game_state(
                move=None,
                game=self.game,
                state_manager=self.state_manager,
                exploration_weight=exploration_weight,
            )

    def __initialize_fen(
        self,
        initial_fen: str = None,
        root: GameStateNode = None,
    ) -> None:

        if self.initial_fen:
            return

        if root:
            self.initial_fen = root.fen
            return

        if initial_fen:
            self.initial_fen = initial_fen
            return

        self.initial_fen = INITIAL_FEN

    def select(self, node: GameStateNode):
        """
        Traverse the tree from the given node to a leaf node using a selection
        policy.

        The selection policy typically follows the Upper Confidence Bound (UCB)
        algorithm to balance exploration and exploitation.

        Parameters:
        -----------
        node : GameStateNode
            The starting node for selection.

        Returns:
        --------
        GameStateNode
            The leaf node reached by the selection policy.
        """
        while node.is_fully_expanded and node.children:
            node = node.get_best_child()
        return node

    def expand(self, node: GameStateNode = None):
        """
        Expand the given node by adding one or more child nodes if it is not
        fully expanded.

        This method generates a new game state from the given node and creates
        a new child node for the tree.

        Parameters:
        -----------
        node : GameStateNode
            The node to be expanded.

        Returns:
        --------
        GameStateNode or None
            The newly expanded child node, or None if expansion is not
            possible.
        """

        if node is None:
            node = self.root

        return node.expand(model=self.model)

    def run(
        self,
        iterations: int = None,
        print_iterations: bool = True,
        simulation_depth_penalty: float = 0.01
    ) -> GameStateNode:
        """
        Run the Monte Carlo Tree Search for a specified number of iterations.

        This method performs the following steps:
        1. Select: Traverse the tree from the root to a leaf node using a tree
            policy.

        2. Expand: Expand the leaf node if it is not fully expanded.

        3. Simulate: Simulate a random playout from the expanded node to
            obtain a result.

        4. Backpropagate: Backpropagate the simulation result up the tree to
            update the node statistics.

        5. Reset: Reset the game state to the initial position after each
            simulation.

        Parameters:
        -----------
        iterations : int
            The number of simulations (games) to be performed from the current
            state.

        simulation_depth_penalty : float
            The penalty for depth of simulation.

        Returns:
        --------
        Node
            The child node of the root with the highest number of visits.

        Details:
        --------
        The method iterates through the following main steps for a specified
        number of iterations:

        1. **Selection**: The `select` method is used to navigate from the
            root node to a leaf node by following a tree policy, typically
            based on the Upper Confidence Bound (UCB) algorithm.

        2. **Expansion**: The `expand` method is called on the selected node.
            If the node is not fully expanded, this method will expand the
            node by adding one or more child nodes.

        3. **Simulation**: The `simulate` method is called on the newly
            expanded node. This method runs a random playout (simulation) from
            the current state to the end of the game to get a result
            (e.g., win, loss, draw).

        4. **Backpropagation**: The `backpropagate` method is used to
            propagate the result of the simulation up the tree, updating the
            statistics (e.g., visit count, win count) of the nodes involved.

        5. **Reset Game State**: After each simulation, the game state is
            reset to the initial position using the
            `Game.parse_fen(self.initial_fen)` method to ensure that each
            simulation starts from the same initial state.

        Example:
        --------
        >>> mcst = MCST()
        >>> best_move = mcst.run(1000)
        >>> print("Best move after 1000 iterations:", best_move)
        """

        if not iterations:
            # then, the number of iterations is going to be the number of
            # legal moves for the current position multiplied by 3
            iterations = len(self.game.get_legal_moves(
                show_as_list=True,
                show_in_algebraic=True,
            )) * 3
            pprint(f"Number of iterations: {iterations}")

        for i in range(iterations):
            if print_iterations:
                pprint(
                    f"Running iteration {i+1}/{iterations}...",
                    print_lines=False
                )

            node = self.root

            while node.is_fully_expanded:
                node = node.get_best_child()

                if node.is_game_terminated:
                    break

            if not node.is_game_terminated:

                # before expanding, we need to check if there is a
                # force checkmate on the position

                value = self._manage_checkmate(node)

                if not value:
                    node = node.expand(
                        model=self.model,
                        game_instance=Game.parse_fen(node.fen),
                    )
                    try:
                        value, simulation_depth = node.simulate()
                    except Exception as e:
                        pprint(e)
                        continue
                else:
                    simulation_depth = 0

            else:
                value = node.result
                simulation_depth = 0

            node.backpropagate(
                value=value,
                simulation_depth=simulation_depth,
                depth_penalty=simulation_depth_penalty
            )

        legal_moves = self.game.get_legal_moves(
            show_as_list=True,
            show_in_algebraic=True,
            color=self.game.player_turn,
        )
        action_probs = np.zeros(len(legal_moves))
        self.create_actions_df(legal_moves, action_probs)

        # get the children of the root node with the best move

        best_move = legal_moves[np.argmax(action_probs)]

        for child in self.root.children.values():
            if child.move == best_move:
                return child

        pprint('best_move', best_move)
        raise ValueError("No best move in the children of the root node.")

    def create_actions_df(self, legal_moves: list, action_probs: np.array):
        visits = np.zeros(len(legal_moves))
        ucb = np.zeros(len(legal_moves))

        for child in self.root.children.values():
            action_probs[legal_moves.index(child.move)] = child.num_visits
            visits[legal_moves.index(child.move)] = child.num_visits
            ucb[legal_moves.index(child.move)] = child.get_ucb()

        action_probs /= np.sum(action_probs)
        self.actions_df = pd.DataFrame(
            {
                "Action": legal_moves,
                "Probability": action_probs,
                "Visits": visits,
                "UCB": ucb,
            }
        ).sort_values("Probability", ascending=True)

    def _manage_checkmate(
        self,
        node: GameStateNode
    ) -> int:

        checkmate_detector = CheckmateDetector(
            fen=node.fen,
            detecting_mate_for=node.player_turn
        )
        checkmate_detector.find_force_checkmate()

        player_mate: int = 0

        if checkmate_detector.is_checkmate:
            pprint(f"Checkmate detected for {node.player_turn}!")
            pprint(checkmate_detector.get_routes_to_checkmates())
            player_mate = PLAYER_VALUES[node.player_turn]

            # take the routes of the checkmate and create the children
            # of the node

            for move_dict in checkmate_detector.get_routes_to_checkmates():
                for move in move_dict:

                    if move == 'best_depth':
                        continue

                    new_node = GameStateNode.create_game_state(
                        move=move,
                        game=Game.parse_fen(node.fen),
                        exploration_weight=node.exploration_weight,
                    )
                    new_node.backpropagate(
                        value=float('inf') * player_mate,
                        simulation_depth=0,
                        depth_penalty=0
                    )

                    new_node.add_parent(node)
                    new_node.result = player_mate
                    new_node.is_game_terminated = True

                    node.add_child(move, new_node)

            node.is_game_terminated = True

        return player_mate
