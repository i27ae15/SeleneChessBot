from alpha_zero.node import GameStateNode
from game.game import Game


class MCST:
    def __init__(
        self,
        initial_fen: str,
    ):
        """
        Initialize the Monte Carlo Search Tree with the initial game state.

        Parameters:
        -----------
        initial_fen : str
            The initial FEN (Forsyth-Edwards Notation) string representing the
            starting position of the game.
        """
        self.initial_fen = initial_fen
        self.game: Game = Game.parse_fen(initial_fen)
        self.root = GameStateNode.create_game_state(game=self.game)

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
            node = node.select()
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

    def simulate(self, node: GameStateNode):
        """
        Run a random simulation (playout) from the given node to the end of
        the game and return the result.

        Parameters:
        -----------
        node : GameStateNode
            The node from which to start the simulation.

        Returns:
        --------
        int
            The result of the simulation (e.g., win, loss, draw).
        """
        return node.simulate()

    def backpropagate(self, node: GameStateNode, result: int):
        """
        Backpropagate the result of a simulation up the tree to update the
        statistics of the nodes involved.

        Parameters:
        -----------
        node : GameStateNode
            The node from which to start the backpropagation.
        result : int
            The result of the simulation to be propagated.
        """
        node.backpropagate(result)

    def run(self, iterations: int):
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
            node = self.select(self.root)

            if not node.is_fully_expanded:
                expanded_node = self.expand(node)

                if expanded_node:
                    result = self.simulate(expanded_node)
                    self.backpropagate(expanded_node, result)
                    # Creating a new game to reset the state to the initial
                    # position

        return max(self.root.children.values(), key=lambda n: n.num_visits)
