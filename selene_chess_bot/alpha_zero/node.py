import math
import numpy as np

from typing import TYPE_CHECKING

from core.printing import __print__ as pprint

from pieces.utilites import PieceColor

from game import Game

from board.types import BoardStates

if TYPE_CHECKING:
    from alpha_zero.state_manager import StateManager


class GameStateNode:
    """
    GameStateNode class representing a node in the Monte Carlo Search Tree.

    Attributes:
    -----------
    fen : str
        The FEN (Forsyth-Edwards Notation) string representing the game state.

    result : int
        The result of the game from this node's perspective
        (e.g., win, loss, draw).

    board_hash : bytes
        A hash representing the current board position.

    player_turn : PieceColor
        The color of the player whose turn it is to move.

    is_game_terminated : bool
        A flag indicating whether the game has ended.

    expandable_moves : set[str]
        A set of legal moves that can be made from this position.

    exploration_weight : float
        The weight used in the UCB calculation for balancing exploration and
        exploitation.

    Methods:
    --------
    __init__(
        fen: str,
        result: int,
        board_hash: bytes,
        player_turn: PieceColor,
        is_game_terminated: bool,
        expandable_moves: set[str],
        exploration_weight: float = 1.414
    ):
        Initialize the GameStateNode with the given game state parameters.

    is_fully_expanded() -> bool:
        Check if the node is fully expanded (no more moves to explore).

    add_explored_move(game_state: 'GameStateNode') -> None:
        Add a move to the set of explored moves.

    add_parent(parent: 'GameStateNode') -> bool:
        Add a parent node to the current node.

    add_child(move: str, child: 'GameStateNode') -> bool:
        Add a child node to the current node for a given move.

    increment_visits() -> None:
        Increment the visit count for the node.

    select() -> 'GameStateNode':
        Select the child node with the highest UCB value.

    get_ucb(child: 'GameStateNode', side: PieceColor) -> float:
        Calculate the UCB value for the given child node.

    get_untried_move() -> str:
        Get a move that has not been tried yet.

    get_random_move() -> str:
        Get a random move from the set of expandable moves.

    expand(game_instance: 'Game') -> 'GameStateNode | str':
        Expand the current node by creating a new child node.

    simulate() -> float:
        Run a random simulation from the current node to the end of the game
        and return the result.

    backpropagate(result: float) -> None:
        Backpropagate the simulation result up the tree, updating values and
        visit counts.

    create_game_state(game: 'Game') -> 'GameStateNode':
        Create a new game state node from the given game instance.
    """

    def __init__(
        self,
        fen: str,
        move: str,
        result: int,
        board_hash: bytes,
        player_turn: PieceColor,
        is_game_terminated: bool,
        board_states: BoardStates,
        expandable_moves: set[str],
        exploration_weight: float = 1.414,
        state_manager: 'StateManager' = None,
        **kwargs  # why am I using this ?
    ) -> None:
        """
        Initialize the GameStateNode with the given game state parameters.

        Parameters:
        -----------
        fen : str
            The FEN (Forsyth-Edwards Notation) string representing the game
            state.

        result : int
            The result of the game from this node's perspective
            (e.g., win, loss, draw).

        board_hash : bytes
            A hash representing the current board position.

        player_turn : PieceColor
            The color of the player whose turn it is to move.

        is_game_terminated : bool
            A flag indicating whether the game has ended.

        expandable_moves : set[str]
            A set of legal moves that can be made from this position.

        exploration_weight : float, optional
            The weight used in the UCB calculation for balancing exploration
            and exploitation (default is 1.414).
        """
        self.parent: GameStateNode = None
        self.children: dict[bytes, 'GameStateNode'] = {}
        self.board_hash: bytes = board_hash
        self.is_game_terminated: bool = is_game_terminated

        self.result: int = result
        self.fen: str = fen

        # The board states are used to keep track of the Threefold repetition
        self.board_states: BoardStates = board_states

        self.player_turn: PieceColor = player_turn
        self.num_visits: int = 0
        self.total_value: float = 0.0

        self.expandable_moves: set['GameStateNode'] = expandable_moves
        self.untried_moves: set['GameStateNode'] = expandable_moves.copy()

        self.policy: dict[bytes, float] = {}
        self.exploration_weight: float = exploration_weight

        self.state_manager: StateManager = state_manager

        self.depth: int = self.parent.depth + 1 if self.parent else 0

        # NOTE: This is momentarily, we have to set the move to be
        # a hash of the board position not a string
        self.move: str = move

    #  ---------------------------- PROPERTIES ----------------------------

    @property
    def move_number(self) -> int:
        """
        Get the move number of the current node.

        Returns:
        --------
        int
            The move number of the current node.
        """
        return self.fen.split(' ')[5]

    @property
    def is_fully_expanded(self) -> bool:
        """
        Check if the node is fully expanded (no more moves to explore).

        Returns:
        --------
        bool
            True if the node is fully expanded, False otherwise.
        """
        return len(self.expandable_moves) == len(self.children)

    #  ---------------------------- STATIC METHODS ----------------------------

    @staticmethod
    def create_game_state(
        move: str,
        game: 'Game',
        exploration_weight: float = 1.414,
        state_manager: 'StateManager' = None
    ) -> 'GameStateNode':
        """
        Create a new game state node from the given game instance.

        Parameters:
        -----------
        game : Game
            The game instance from which to create the game state node.

        Returns:
        --------
        GameStateNode
            The created game state node.
        """
        game.create_current_fen()
        expandable_moves = game.get_legal_moves(
            color=game.player_turn,
            show_in_algebraic=True,
            show_as_list=True
        )

        return GameStateNode(
            move=move,
            result=game.result,
            fen=game.current_fen,
            state_manager=state_manager,
            player_turn=game.player_turn,
            board_states=game.board_states,
            expandable_moves=expandable_moves,
            board_hash=game.current_board_hash,
            exploration_weight=exploration_weight,
            is_game_terminated=game.is_game_terminated,
        )

    @staticmethod
    def get_node_ucb(
        node: 'GameStateNode',
        depth_penalty: float = 0.01
    ) -> float:

        """
        Calculate the UCB value for the given node.

        Parameters:
        -----------

        node : GameStateNode
            The node for which to calculate the UCB value.

        Returns:
        --------
        float
            The UCB value of the given node.
        """
        if node.num_visits == 0:
            return float("inf")

        # Calculate the exploitation term (average value)
        exploitation_term = node.total_value / node.num_visits

        # Calculate the exploration term (UCB)
        exploration_term = node.exploration_weight * math.sqrt(
            math.log(node.parent.num_visits) / node.num_visits
        )

        # Depth penalty term (penalize deeper nodes)
        depth_penalty_term = depth_penalty * node.depth

        # UCB value with depth penalty
        return exploitation_term + exploration_term - depth_penalty_term

    # ---------------------------- PUBLIC METHODS ----------------------------

    def add_parent(self, parent: 'GameStateNode') -> bool:
        """
        Add a parent node to the current node.

        Parameters:
        -----------
        parent : GameStateNode
            The parent node to be added.

        Returns:
        --------
        bool
            True if the parent was added successfully, False otherwise.
        """
        if parent is None:
            return False
        self.parent = parent
        self.depth = parent.depth + 1
        return True

    def add_child(self, move: str, child: 'GameStateNode') -> bool:
        """
        Add a child node to the current node for a given move.

        Parameters:
        -----------
        move : str
            The move leading to the child node.
        child : GameStateNode
            The child node to be added.

        Returns:
        --------
        bool
            True if the child was added successfully, False otherwise.
        """
        self.children[move] = child
        return True

    def increment_visits(self) -> None:
        """
        Increment the visit count for the node.
        """
        self.num_visits += 1

    def get_best_child(self) -> 'GameStateNode':
        """
        Select the child node with the highest UCB value.

        Returns:
        --------
        GameStateNode
            The child node with the highest UCB value.
        """
        best_child: GameStateNode = None
        best_ucb = float('-inf')

        for child in self.children.values():
            ucb = child.get_ucb()

            if ucb == float("inf"):
                return child

            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child

    def get_ucb(self) -> float:
        """
        Calculate the UCB value for the current node.

        float
            The UCB value of the current node.
        """
        return self.get_node_ucb(self)

    def get_random_move(self) -> str:
        """
        Get a random move from the set of expandable moves.

        Returns:
        --------
        str
            A random move from the set of expandable moves.
        """
        return np.random.choice(list(self.expandable_moves))

    def retrieve_move_from_untried_moves(self) -> str:
        """
        Get a move that has not been tried yet and remove it from the
        set of untried moves

        Returns:
        --------
        str
            A move that has not been tried yet.
        """
        # BUG: Sometimes the untried moves set is empty
        random_move = np.random.choice(list(self.untried_moves))
        self.untried_moves.remove(random_move)
        return random_move

    def expand(
        self,
        game_instance: 'Game',
        model=None
    ) -> 'GameStateNode':

        """
        Expand the current node by creating a new child node using the neural
        network.

        Parameters:
        -----------
        game_instance : Game
            The current game instance.

        model : tf.keras.Model
            The neural network model to predict policy and value.

        Returns:
        --------
        GameStateNode or None
            The newly expanded child node, or None if expansion is not
            possible.

        NOTE:
            This methods works as a manager to choose between `__model_expand`
            which uses a neural network to predict the best move and
            `__no_model_expand` which uses a random move.
        """

        if model:
            return self.__model_expand(game_instance, model)
        elif not model:
            return self.__no_model_expand(game_instance)

    def backpropagate(
        self,
        value: int,
        simulation_depth: int,
        depth_penalty: float = 0.01
    ) -> None:
        """
        Backpropagate the simulation result up the tree, updating values and
        visit counts.

        Parameters:
        -----------
        result : float
            The result of the simulation to be propagated.
        """

        self.increment_visits()
        depth_penalty_term = depth_penalty * (simulation_depth - self.depth)
        self.total_value += value - depth_penalty_term

        if self.parent:
            self.parent.backpropagate(
                value=value,
                simulation_depth=simulation_depth,
                depth_penalty=depth_penalty
            )

    def simulate(self) -> tuple[float, int]:

        game_instance = Game.parse_fen(self.fen)
        game_instance.board_states = self.board_states
        value: float = game_instance.result

        value = game_instance.get_opponent_value(value=value)

        if self.is_game_terminated:
            return value, 0

        player_values: dict[PieceColor, float] = {
            PieceColor.WHITE: -1,
            PieceColor.BLACK: 1
        }

        simulation_depth = self.depth

        while not game_instance.is_game_terminated:
            moves = game_instance.get_legal_moves(
                game_instance.player_turn,
                show_in_algebraic=True,
                show_as_list=True
            )
            try:
                move = np.random.choice(moves)
            except Exception as e:
                print('error:', e)
                print('moves:', moves)
                raise e

            game_instance.move_piece(move)
            simulation_depth += 1

        value = player_values[game_instance.player_turn]
        return value, simulation_depth

    # ---------------------------- PRIVATE METHODS ----------------------------

    def __model_expand(
        self,
        game_instance: 'Game',
        model
    ) -> 'GameStateNode':

        if self.is_fully_expanded:
            return None

        # encode the board state to use as input to the neural network
        encoded_board = game_instance.board.get_encoded_board()

        # predict policy and value using the neural network
        policy, _ = model.predict(encoded_board.reshape(1, 8, 8, 12))
        policy = policy.flatten()

        # Create a list of untried moves paired with their policy values
        untried_move_policy_pairs = [
            (move, policy[self.untried_moves.index(move)])
            for move in self.untried_moves
        ]

        # sort untruied moves based on the policy values
        untried_move_policy_pairs.sort(key=lambda x: x[1], reverse=True)

        move, _ = untried_move_policy_pairs[0]
        self.untried_moves.remove(move)
        game_instance.move_piece(move)

        new_node = self.create_game_state(
            move=move,
            game=game_instance,
            state_manager=self.state_manager,
            exploration_weight=self.exploration_weight,
        )

        self.add_child(move, new_node)
        new_node.add_parent(self)

        return new_node

    def __no_model_expand(
        self,
        game_instance: 'Game',
    ) -> 'GameStateNode':

        """
        Expand the current node by creating a new child node.
        """

        if self.is_fully_expanded:
            return None

        move = self.retrieve_move_from_untried_moves()
        game_instance.move_piece(move)

        new_node = self.create_game_state(
            move=move,
            game=game_instance,
            state_manager=self.state_manager,
            exploration_weight=self.exploration_weight,
        )
        self.add_child(move, new_node)
        new_node.add_parent(self)

        return new_node
