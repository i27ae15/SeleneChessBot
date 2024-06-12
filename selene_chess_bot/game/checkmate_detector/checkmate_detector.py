from game import Game
from game.checkmate_detector.check_detector import CheckDetector

from pieces.utilites import PieceColor

from .node import MoveNode


class CheckmateDetector:

    def __init__(
        self,
        fen: str,
        detecting_mate_for: PieceColor,
        maximum_depth: int = 5
    ):

        """
        A class to detect checkmate in a given position.

        self.check_mates is a list because a position could have more than
        one forced checkmate.

        NOTE:
            Although the class is aim to get a forced checkmate in a given
            position, the given position must have a check on it, so the
            CheckDetecor can detect it.

        """
        self.initial_fen: str = fen
        self.detecting_mate_for: str = detecting_mate_for
        self.game: Game = Game.parse_fen(fen)

        self.roots: list[MoveNode] = []
        self.check_mates: list[MoveNode] = []

        self.maximum_depth: int = maximum_depth

        self._routes_to_checkmates: list[dict] = []

    @property
    def is_checkmate(self) -> bool:
        """
        Returns True if there is a checkmate in the given position.
        """
        return bool(self.check_mates)

    def get_routes_to_checkmates(
        self,
        get_shortest_mate: bool = True
    ) -> list[dict]:

        """
        Retrieves the routes to checkmates from the current game state.

        Parameters:
        -----------
        get_shortest_mate : bool, optional
            If True, only the shortest routes to checkmate are returned.
            Default is True.

        Returns:
        --------
        list[dict]
            A list of dictionaries where each dictionary represents a route to
            checkmate.

        Notes:
        ------
        - This method caches the results in `self._routes_to_checkmates` to
            avoid redundant calculations.

        - It calls the `_get_routes_to_checkmates` method to perform the
            actual computation.

        Example:
        --------
        ```
        node = MoveNode()
        routes = node.get_routes_to_checkmates()
        ```
        """

        if not self._routes_to_checkmates:
            self._routes_to_checkmates = self._get_routes_to_checkmates(
                get_shortest_mate=get_shortest_mate
            )
        return self._routes_to_checkmates

    def _get_routes_to_checkmates(
        self,
        get_shortest_mate: bool = True
    ) -> list[dict]:

        """
        Computes the routes to checkmates from the current game state.

        Parameters:
        -----------
        get_shortest_mate : bool, optional
            If True, only the shortest routes to checkmate are returned.
            Default is True.

        Returns:
        --------
        list[dict]
            A list of dictionaries where each dictionary represents a route to
            checkmate.

        Notes:
        ------

        - This method traverses the `check_mates` attribute, which is a list
            of `MoveNode` instances.

        - It collects the routes to checkmate and optionally filters them to
            include only the shortest routes.

        Example:
        --------
        ```
        node = MoveNode()
        routes = node._get_routes_to_checkmates()
        ```
        """

        list_of_routes = []

        best_depth = float('inf')
        for move in self.check_mates:
            route = move.get_route_to_checkmate()
            route_depth = route['best_depth']
            list_of_routes.append(route)

            if get_shortest_mate:
                # If we are looking for the shortest route, update best_depth
                # and remove longer routes
                if best_depth >= route_depth:
                    best_depth = route_depth
                else:
                    # Remove the longer route
                    list_of_routes.remove(route)

        # traverse the parent nodes to find the
        # best route to the checkmate
        if get_shortest_mate:
            # Traverse the list of routes to keep only the best routes
            # to checkmate
            best_lines = []
            for route in list_of_routes:
                if route['best_depth'] == best_depth:
                    best_lines.append(route)
        else:
            # If not filtering, all routes are considered best
            best_lines = list_of_routes

        return best_lines

    def find_force_checkmate(self) -> bool:

        """
        Identifies forced checkmate sequences from the initial FEN position
        and stores the results.

        Notes:
        ------
        - This method initializes a `CheckDetector` to find all checks in the
            given position.

        - For each check, it creates a new game state, initializes a
            `MoveNode`, and checks for forced checkmate sequences.

        - If a forced checkmate is found, the root node of the sequence is
            added to `self.check_mates`.

        Example:
        --------
        ```
        move_tree = MoveTree(initial_fen)
        move_tree.find_force_checkmate()
        forced_mates = move_tree.check_mates
        ```

        Steps:
        ------
        1. Initialize a `CheckDetector` with the initial FEN position.
        2. Iterate over all checks found by the `CheckDetector`.
        3. For each check:
        a. Parse the FEN and create a `Game` object.
        b. Initialize a `MoveNode` for the check.
        c. Add the node to the roots.
        d. Make the move in the game.
        e. Call `_find_force_checkmate` to recursively check for forced mates.
        f. If a forced checkmate is found, add the node to `self.check_mates`.
        """

        check_detector = CheckDetector(fen=self.initial_fen)
        found_forced_mate = False

        # Iterate over all checks found by the CheckDetector
        for check in check_detector.checks_on_position:
            # Parse the FEN and create a Game object
            game: Game = Game.parse_fen(self.initial_fen)

            # Initialize a MoveNode for the checks
            current_node = MoveNode(
                move=check,
                parent=None,
                player_turn=game.player_turn,
                seeking_mate_for=self.detecting_mate_for,
            )
            self.roots.append(current_node)

            game.move_piece(check)

            is_mate = self._find_force_checkmate(
                depth=1,
                game=game,
                parent=current_node,
                fen=game.create_current_fen(),
            )
            if is_mate:
                found_forced_mate = True
                self.check_mates.append(current_node)

        return found_forced_mate

    def _find_force_checkmate(
        self,
        fen: str,
        game: Game,
        depth: int = 0,
        parent: MoveNode = None
    ) -> bool:

        """
        Recursively searches for forced checkmate sequences from the given
        game state.

        Parameters:
        -----------
        fen : str
            The FEN string representing the current game state.

        game : Game
            The current game object.

        depth : int, optional
            The current depth of the search in the move tree. Default is 0.

        parent : MoveNode, optional
            The parent node in the move tree. Default is None.

        Returns:
        --------
        bool
            True if a forced checkmate is found, False otherwise.

        Notes:
        ------

        - This method checks if the current game state leads to a forced
            checkmate.

        - It recursively simulates moves and builds the move tree, marking
            nodes that lead to checkmate.

        - If the depth exceeds `self.maximum_depth`, the search terminates and
            returns False.

        Example:
        --------
        ```
        move_tree = MoveTree(initial_fen)
        game = Game.parse_fen(initial_fen)
        is_mate = move_tree._find_force_checkmate(fen=initial_fen, game=game)
        ```
        """

        if depth > self.maximum_depth:
            return False

        # Check if the game is terminated and not drawn, indicating a checkmate
        if game.is_game_terminated and not game.is_game_drawn:
            if game.game_values[self.detecting_mate_for] > 0:
                parent.is_checkmate = True
                return True

        # Get the list of possible moves for the current game state
        moves = self._get_moves_for_simulation(fen=fen, game=game)

        if not moves and game.player_turn == self.detecting_mate_for:
            return False

        for move in moves:
            game: Game = Game.parse_fen(fen)
            current_node = MoveNode(
                move=move,
                depth=depth,
                parent=parent,
                player_turn=game.player_turn,
                seeking_mate_for=self.detecting_mate_for,
            )

            game.move_piece(move)

            if parent:
                parent.add_child(current_node)

            # Recursively search for forced checkmate from the new game state
            self._find_force_checkmate(
                game=game,
                depth=depth + 1,
                parent=current_node,
                fen=game.create_current_fen(),
            )

        # Return whether all children nodes lead to a forced checkmate
        return parent.children_forced_checkmate()

    def _get_moves_for_simulation(
        self,
        fen: str,
        game: Game,
    ) -> list[str]:
        """
        Retrieves the list of possible moves for the current game state.
        A helper method for the _find_force_checkmate method.

        Parameters:
        -----------
        fen : str
            The FEN string representing the current game state.

        game : Game
            The current game object.

        Returns:
        --------
        list[str]
            A list of possible moves in algebraic notation.

        Notes:
        ------
        - If it is the detecting player's turn, the method returns moves that
            put the opponent in check.
        - Otherwise, it returns all legal moves for the current player.

        Example:
        --------
        ```
        move_tree = MoveTree(initial_fen)
        game = Game.parse_fen(initial_fen)
        moves = move_tree._get_moves_for_simulation(fen=initial_fen, game=game)
        ```
        """

        moves: list[str] = []

        # If it is the detecting player's turn, get moves that put the
        # opponent in check
        if game.player_turn == self.detecting_mate_for:
            check_detector = CheckDetector(fen=fen)
            moves = check_detector.checks_on_position
        else:
            # Otherwise, get all legal moves for the current player
            moves = game.get_legal_moves(
                show_as_list=True,
                show_in_algebraic=True,
            )

        return moves
