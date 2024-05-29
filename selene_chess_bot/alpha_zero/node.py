import math
import numpy as np

from typing import TYPE_CHECKING

from pieces.utilites import PieceColor

from game.game import Game

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
        expandable_moves: set[str],
        exploration_weight: float = 1.414,
        state_manager: 'StateManager' = None,
        **kwargs
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

        self.state_manager: StateManager = state_manager
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
        return len(self.expandable_moves) == len(self.explored_moves)

    @property
    def total_parent_visits(self) -> int:
        """
        Get the total number of visits of all parent nodes.

        Returns:
        --------
        int
            The total number of visits of all parent nodes.
        """
        return sum([parent.num_visits for parent in self.parents])

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
            expandable_moves=expandable_moves,
            board_hash=game.current_board_hash,
            exploration_weight=exploration_weight,
            is_game_terminated=game.is_game_terminated,
        )

    @staticmethod
    def get_node_ucb(node: 'GameStateNode') -> float:

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

        q_value = ((node.result / node.num_visits) + 1) / 2
        mul = math.sqrt(
            math.log(node.total_parent_visits) / node.num_visits
        )

        ucb = q_value + node.exploration_weight * mul

        # if ucb == 0:
        #     print('-' * 50)
        #     print('result', node.result)
        #     print('num_visits', node.num_visits)
        #     print('-' * 50)
        #     print('q_value', q_value)
        #     print('mul', mul)
        #     print('-' * 50)

        return ucb

    # ---------------------------- PUBLIC METHODS ----------------------------

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
        if self.num_visits == 0:
            return float("inf")

        return self.get_node_ucb(self)

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

    def update(self, is_game_terminated: bool, result: int):

        self.is_game_terminated = is_game_terminated
        self.result = result

        self.increment_visits()

    def expand(
        self,
        game_instance: 'Game',
        perfom_randomly: bool = False
    ) -> 'GameStateNode | str':
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

        if not self.expandable_moves:
            return False, False

        # move = self._get_move(
        #     random=True,
        # )

        move = self.get_random_move()
        game_instance.move_piece(move)

        # check if the hash is in the state manager
        if self.state_manager:
            game_hash = game_instance.current_board_hash

            if game_hash in self.state_manager:
                state = self.state_manager.get_state(
                    board_hash=game_hash,
                    check_exists=False
                )

                # NOTE: Check that somehow the state when created
                # is not being set as terminated
                # I believe because a node could be a terminal node,
                # or not necessarily
                # Due to the 50 rules, or threefold repetition
                # Check into the implications of this
                state.update(
                    result=game_instance.result,
                    is_game_terminated=game_instance.is_game_terminated,
                )

                return state, move

        new_node = self.create_game_state(
            move=move,
            game=game_instance,
            state_manager=self.state_manager,
            exploration_weight=self.exploration_weight,
        )

        if self.state_manager:
            self.state_manager.add_state(new_node)

        self.add_child(move, new_node)
        self.add_explored_move(new_node)
        new_node.add_parent(self)

        return new_node, move

    def _get_move(self, random: bool = False) -> 'str':
        if random:
            return self.get_random_move()

        best_move = None
        best_ucb = float('-inf')

        for move in self.expandable_moves:

            new_game = Game.parse_fen(self.fen)
            new_game.move_piece(move)

            # if the hash of the new game is not in the state
            # manager, we know that the move has not been explored
            # and we can return it

            if new_game.current_board_hash not in self.state_manager:
                return move

            # if this is in the state manager, then we can check
            # the UCB value of the node

            new_node = self.state_manager.get_state(
                check_exists=False,
                board_hash=new_game.current_board_hash,
            )

            current_ucb = new_node.get_ucb()

            if current_ucb > best_ucb:
                best_ucb = current_ucb
                best_move = move

        return best_move

    def simulate(self, backpropagate: bool = True) -> float:
        """
        Run a random simulation from the current node to the end of the game
        and return the result.

        Returns:
        --------
        float
            The result of the simulation.
        """

        game_instance = Game.parse_fen(self.fen)

        if self.is_game_terminated:
            return self.result

        current_node = self
        while not current_node.is_game_terminated:
            current_node, _ = current_node.expand(
                game_instance=game_instance
            )

            if not current_node:
                return self.result

        if backpropagate:
            current_node.backpropagate()

        game_instance.print_game_state()
        return current_node.result

    def backpropagate(self) -> None:
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
            node.total_value += self.result
            node = next(iter(node.parents), None)  # Move to the parent node
