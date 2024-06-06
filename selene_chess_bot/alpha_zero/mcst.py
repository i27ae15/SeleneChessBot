import numpy as np
import pandas as pd

from alpha_zero.node import GameStateNode
from alpha_zero.state_manager import StateManager

from game.game import Game


class MCST:
    def __init__(
        self,
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

        self.root: GameStateNode = root

        self.initial_fen = initial_fen or self.root.fen
        self.state_manager = state_manager or StateManager()
        self.game: Game = Game.parse_fen(self.initial_fen)

        if not self.root:
            self.root = GameStateNode.create_game_state(
                move=None,
                game=self.game,
                state_manager=self.state_manager,
                exploration_weight=exploration_weight,
            )

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

    def expand(self, node: GameStateNode):
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

        new_node, move = node.expand()
        new_node: GameStateNode
        # this will return a move, such as e4
        if new_node:
            new_node.add_parent(node)
            node.add_child(move, new_node)
            return new_node
        return None

    def run(
        self,
        iterations: int,
        simulation_depth_penalty: float = 1
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

        for i in range(iterations):
            print(f"Running iteration {i+1}/{iterations}...")

            node = self.root

            while node.is_fully_expanded:
                node = node.get_best_child()
                if node.is_game_terminated:
                    break

            if not node.is_game_terminated:
                node = node.expand(Game.parse_fen(node.fen))
                try:
                    value, simulation_depth = node.simulate()
                except Exception as e:
                    print(e)
                    continue
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
        for child in self.root.children.values():
            action_probs[legal_moves.index(child.move)] = child.num_visits

        action_probs /= np.sum(action_probs)
        actions_df = pd.DataFrame(
            {
                "Action": legal_moves,
                "Probability": action_probs,
            }
        ).sort_values("Probability", ascending=False)

        # print children ucb

        print('-'*50)
        for child in self.root.children.values():
            print(child.move, child.get_ucb(), child.num_visits)

        print(actions_df)
        print('-'*50)

        return legal_moves[np.argmax(action_probs)]
