import numpy as np
import math

from game import Game


class Node:
    """
    A node in the Monte Carlo Tree Search (MCTS) representing a game state.

    Attributes:
        game: A reference to the game being played which provides methods like
        get_valid_moves, get_next_state, etc.
        args: A dictionary of additional arguments or parameters such as the
        exploration constant.
        state: The current state of the game at this node.
        parent: The node's parent node. None if this is the root node.
        action_taken: The action that led to this state from the parent node.
        children: A list of child nodes that branch from this node.
        expandable_moves: Tracks which moves are valid and unexplored from
        this state.
        visit_count: The number of times this node has been visited during the
        search.
        value_sum: The sum of values backpropagated up through this node.
    """

    def __init__(
        self,
        game: Game,
        c_value: float,
        state: int,
        parent: 'Node | None' = None,
        action_taken=None
    ):
        """
        Initializes a new node with the given game state and optional parent
        and action.

        Parameters:
            game: The game being played.
            args: Configuration arguments for MCTS, like exploration constant.
            state: The current game state this node represents.
            parent: The parent Node of this node (None if root).
            action_taken: The action taken to reach this node from the parent
            node.
        """
        self.game: Game = game
        self.c_value: float = c_value
        self.state: int = state
        self.parent: Node | None = parent
        self.action_taken = action_taken

        self.children: list[Node] = []
        self.expandable_moves: list[str] = game.get_legal_moves(
            color=game.player_turn
        )

        self.visit_count: int = 0
        self.value_sum: int = 0

    def is_fully_expanded(self):
        """
        Checks if the node is fully expanded, i.e., all possible moves have
        been explored.

        Returns:
            A boolean indicating whether all expandable moves have been
            explored.
        """
        return np.sum(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self):
        """
        Selects a child node to explore next using the Upper Confidence Bound
        (UCB) algorithm.

        Returns:
            The child node with the highest UCB value.
        """
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        """
        Calculates the Upper Confidence Bound (UCB) value for a given child
        node.

        Parameters:
            child: The child node for which to calculate the UCB value.

        Returns:
            The UCB value of the given child node.
        """
        q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.c_value * math.sqrt(
            math.log(self.visit_count) / child.visit_count
        )

    def expand(self):
        """
        Expands the node by creating a new child node from an unexplored move.

        Returns:
            The newly created child node.
        """
        action = np.random.choice(np.where(self.expandable_moves == 1)[0])
        self.expandable_moves[action] = 0

        child_state = self.state
        child_state = self.game.get_next_state(child_state, action, 1)
        child_state = self.game.change_perspective(child_state, player=-1)

        child = Node(
            game=self.game,
            c_value=self.c_value,
            state=child_state,
            parent=self,
            action_taken=action
        )
        self.children.append(child)
        return child

    def simulate(self):
        """
        Simulates a random playthrough from the current state until a terminal
        state is reached.

        Returns:
            The value of the terminal state reached during the simulation.
        """
        value, is_terminal = self.game.get_value_and_terminated(
            self.state,
            self.action_taken
        )
        value = self.game.get_opponent_value(value)

        if is_terminal:
            return value

        rollout_state = self.state.copy()
        rollout_player = 1
        while True:
            valid_moves = self.game.get_valid_moves(rollout_state)
            action = np.random.choice(
                np.where(valid_moves == 1)[0]
            )
            rollout_state = self.game.get_next_state(
                rollout_state, action, rollout_player
            )
            value, is_terminal = self.game.get_value_and_terminated(
                rollout_state, action
            )
            if is_terminal:
                if rollout_player == -1:
                    value = self.game.get_opponent_value(value)
                return value

            rollout_player = self.game.get_opponent(rollout_player)

    def backpropagate(self, value):
        """
        Backpropagates the value from a simulation up through the tree,
        updating this node and its ancestors.

        Parameters:
            value: The value to backpropagate, typically the result of a
            simulation.
        """
        self.value_sum += value
        self.visit_count += 1

        value = self.game.get_opponent_value(value)
        if self.parent is not None:
            self.parent.backpropagate(value)


class MCTS:
    """
    Implements the Monte Carlo Tree Search algorithm for decision-making in
    game environments.

    Attributes:
        game: A reference to the game being played which provides necessary
        methods like get_valid_moves, get_next_state, etc.
        args: A dictionary of configuration arguments for MCTS, including the
        number of searches and the exploration constant.
    """

    def __init__(
        self,
        game: Game,
        num_searches: int = 100,
        c_value: float = 1.0
    ) -> None:
        """
        Initializes the MCTS with the specified game and configuration
        arguments.

        Parameters:
            game: The game being played, expected to provide necessary methods
            for MCTS.
            args: Configuration arguments for MCTS, including number of
            searches and exploration constant.
        """
        self.game: Game = game
        self.num_searches: int = num_searches
        self.c_value: float = c_value

    def search(self, state: int):
        """
        Performs a Monte Carlo Tree Search from the given game state.

        This method carries out a number of search iterations
        (as specified in args['num_searches']), each consisting of four
        phases: Selection, Expansion, Simulation, and Backpropagation.

        Parameters:
            state: The current state of the game from which to start the MCTS.

        Returns:
            A numpy array representing the probabilities of taking each action
            from the root state.
            The probabilities are proportional to the visit counts of each
            action's corresponding node.
        """
        # define root
        root = Node(
            game=self.game,
            c_value=self.c_value,
            state=state
        )

        # selection
        for _ in range(self.num_searches):
            # we want to go down as the node is fully expanded
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = self.game.get_value_and_terminated(
                node.state, node.action_taken
            )
            value = self.game.get_opponent_value(value)

            # check if the node is terminated and backpropagate

            if not is_terminal:
                # expansion
                node = node.expand()
                # simulation
                # Perform random actions to create this simulation
                value = node.simulate()

            # backpropagation
            node.backpropagate(value)

            # return visit_counts
            action_probs = np.zeros(self.game.action_size)
            for child in root.children:
                action_probs[child.action_taken] = child.visit_count
            action_probs /= np.sum(action_probs)
            return action_probs
