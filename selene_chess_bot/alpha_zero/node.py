import math
import numpy as np

from pieces.utilites import PieceColor

from game.game import Game


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
        result: int,
        board_hash: bytes,
        player_turn: PieceColor,
        is_game_terminated: bool,
        expandable_moves: set[str],
        exploration_weight: float = 1.414
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
        self.parents: set['GameStateNode'] = set()
        self.children: dict[bytes, 'GameStateNode'] = {}
        self.board_hash: bytes = board_hash
        self.is_game_terminated: bool = is_game_terminated

        self.result: int = result
        self.fen: str = fen

        self.player_turn: PieceColor = player_turn
        self.num_visits: int = 0
        self.total_value: float = 0.0

        self.expandable_moves: set['GameStateNode'] = expandable_moves
        self.explored_moves: set['GameStateNode'] = set()

        self.policy: dict[bytes, float] = {}
        self.exploration_weight: float = exploration_weight

    @property
    def is_fully_expanded(self) -> bool:
        """
        Check if the node is fully expanded (no more moves to explore).

        Returns:
        --------
        bool
            True if the node is fully expanded, False otherwise.
        """
        return len(self.expandable_moves) == len(self.explored_moves)

    def add_explored_move(self, game_state: 'GameStateNode') -> None:
        """
        Add a move to the set of explored moves.

        Parameters:
        -----------
        game_state : GameStateNode
            The game state node corresponding to the explored move.
        """
        self.explored_moves.add(game_state)

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
        self.parents.add(parent)
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

    def select(self) -> 'GameStateNode':
        """
        Select the child node with the highest UCB value.

        Returns:
        --------
        GameStateNode
            The child node with the highest UCB value.
        """
        best_child = None
        best_ucb = float('-inf')

        for child in self.children.values():
            ucb = self.get_ucb(child, self.player_turn)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child

    def get_ucb(self, child: 'GameStateNode', side: PieceColor) -> float:
        """
        Calculate the UCB value for the given child node.

        Parameters:
        -----------
        child : GameStateNode
            The child node for which to calculate the UCB value.
        side : PieceColor
            The color of the player whose turn it is.

        Returns:
        --------
        float
            The UCB value of the child node.
        """
        if self.num_visits == 0:
            return float("inf")

        q_value = ((self.result / self.num_visits) + 1) / 2
        ucb = q_value + self.exploration_weight * math.sqrt(
            math.log(self.num_visits) / child.num_visits
        )

        return ucb

    def get_untried_move(self) -> str:
        """
        Get a move that has not been tried yet.

        Returns:
        --------
        str
            A move that has not been tried yet, or False if all moves have
            been tried.
        """
        for move in self.expandable_moves:
            if move not in self.explored_moves:
                return move
        return False

    def get_random_move(self) -> str:
        """
        Get a random move from the set of expandable moves.

        Returns:
        --------
        str
            A random move from the set of expandable moves.
        """
        return np.random.choice(list(self.expandable_moves))

    def expand(self) -> 'GameStateNode | str':
        """
        Expand the current node by creating a new child node.

        Parameters:
        -----------
        game_instance : Game
            The game instance used to generate the new game state.

        Returns:
        --------
        GameStateNode or str
            The new game state node and the move leading to it.
        """
        game_instance = Game.parse_fen(self.fen)

        move: str = self.get_random_move()

        game_instance.move_piece(move)
        new_node = self.create_game_state(game_instance)
        self.add_child(move, new_node)
        self.add_explored_move(new_node)

        return new_node, move

    def simulate(self) -> float:
        """
        Run a random simulation from the current node to the end of the game
        and return the result.

        Returns:
        --------
        float
            The result of the simulation.
        """
        game_instance = Game.parse_fen(self.fen)
        current_game_state: GameStateNode = self.create_game_state(
            game_instance
        )

        if self.is_game_terminated:
            return self.result

        while not game_instance.is_game_terminated:
            valid_moves = current_game_state.expandable_moves
            move = np.random.choice(list(valid_moves))
            game_instance.move_piece(move)

            if game_instance.is_game_terminated:
                return game_instance.result

            current_game_state = self.create_game_state(game_instance)

    def tt(self):

        game_instance = Game.parse_fen(self.fen)
        if self.is_game_terminated:
            return self.result

        while not game_instance.is_game_terminated:
            valid_moves = game_instance.get_legal_moves(
                color=game_instance.player_turn,
                show_in_algebraic=True,
                show_as_list=True
            )
            move = np.random.choice(valid_moves)
            game_instance.move_piece(move)

        return game_instance.result

    def backpropagate(self, result: float) -> None:
        """
        Backpropagate the simulation result up the tree, updating values and
        visit counts.

        Parameters:
        -----------
        result : float
            The result of the simulation to be propagated.
        """
        node = self
        while node is not None:
            node.increment_visits()
            node.total_value += result
            node = next(iter(node.parents), None)  # Move to the parent node

    @staticmethod
    def create_game_state(game: 'Game') -> 'GameStateNode':
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
            fen=game.current_fen,
            result=game.result,
            board_hash=game.current_board_hash,
            player_turn=game.player_turn,
            is_game_terminated=game.is_game_terminated,
            expandable_moves=expandable_moves
        )
