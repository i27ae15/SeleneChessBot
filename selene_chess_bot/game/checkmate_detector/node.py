from typing import Generator

from pieces.utilites import PieceColor


class MoveNode:

    def __init__(
        self,
        move: str,
        parent: 'MoveNode',
        player_turn: PieceColor,
        seeking_mate_for: PieceColor,
        depth: int = 0,
        is_checkmate: bool = False
    ) -> None:

        self.parent: MoveNode = parent
        self.children: list[MoveNode] = list()

        self.move: str = move
        self.depth: int = depth

        self.player_turn: PieceColor = player_turn
        self.seeking_mate_for: PieceColor = seeking_mate_for
        self.is_checkmate: bool = is_checkmate

    def add_child(self, child: 'MoveNode') -> None:
        self.children.append(child)

    def children_forced_checkmate(self) -> bool:

        """
        Determines whether the current position forces a checkmate by
        evaluating the children nodes.

        Returns:
        --------
        bool
            True if the current position forces a checkmate, False otherwise.

        Notes:
        ------
        - This function checks the `is_checkmate` attribute of the children
            nodes.

        - The result is stored in the `is_checkmate` attribute of the current
            node.

        - If `self.seeking_mate_for` is equal to `self.player_turn`, the
        function checks if all children nodes are checkmate nodes.

        - If `self.seeking_mate_for` is not equal to `self.player_turn`, the
        function checks if any child node is a checkmate node.

        Example:
        --------
        ```
        node = MoveNode()
        is_forced_mate = node.children_forced_checkmate()
        ```
        """

        if self.seeking_mate_for == self.player_turn:
            # If the current node is the one that is looking for the
            # checkmate then, we need to check for -ALL- of the children to be
            # a checkmate node.

            self.is_checkmate = all(
                [child.is_checkmate for child in self.children]
            )
            return self.is_checkmate

        if self.seeking_mate_for != self.player_turn:
            # If the current node is not the one that is looking for the
            # checkmate then, we need to check if -ANY- of the children is a
            # checkmate node.

            self.is_checkmate = any(
                [child.is_checkmate for child in self.children]
            )
            return self.is_checkmate

    def next_moves_to_checkmate(self) -> Generator['MoveNode', None, None]:

        for child in self.children:
            if child.is_checkmate:
                yield child

    def get_route_to_checkmate(
        self,
    ) -> dict[str]:

        if not self.is_checkmate:
            raise Exception('The current node is not a checkmate node.')

        dict_result = dict()
        dict_result[self.move] = dict()

        dict_result['best_depth'] = self._get_route_to_checkmate(
            depth=1,
            dict_result=dict_result[self.move],
        )
        return dict_result

    def _get_route_to_checkmate(
        self,
        depth: int,
        dict_result: dict['MoveNode'],
        get_only_best_lines: bool = True
    ) -> int:

        """
        Recursively determines the route to checkmate from the current
        game state and populates a dictionary with the path and depths of
        the best moves.

        Parameters:
        -----------
        depth : int
            The current depth in the move tree.

        dict_result : dict
            A dictionary to store the results of the search, including
            depths and moves.

        get_only_best_lines : bool, optional
            If True, only the best lines (shortest path to checkmate) are
            kept in the dictionary. Default is True.

        Returns:
        --------
        int
            The depth of the shortest path to checkmate from the current
            node.

        Notes:
        ------
        - The function updates `dict_result` in place, adding information
            about the move tree and depths.

        - If `get_only_best_lines` is True, the function prunes less
            optimal moves from `dict_result`.

        - BCD stands for Best Child Depth

        Example:
        --------
        ```
        move_tree = MoveNode()
        result_dict = {}
        depth = move_tree._get_route_to_checkmate(0, result_dict)
        ```
        """

        # Add the current depth to the node child
        # son then, we can compare the depth of the children
        dict_result['depth'] = depth

        # We need to check this here because altho self.children could be empty
        # the current node may not be a checkmate node. could be a stalemate
        # for instance
        if not self.children and self.is_checkmate:
            dict_result['is_checkmate'] = True
            dict_result['best_child_depth'] = depth
            return depth

        # prepare to compare the depth of the children to get the best
        # depth, or the shortest path to the checkmate for the given move
        best_child_depth = float('inf')
        for child in self.next_moves_to_checkmate():

            # add the move to the dict
            dict_result[child.move] = dict()

            # call the function recursively to get to the end of the tree
            child_depth = child._get_route_to_checkmate(
                depth=depth + 1,
                dict_result=dict_result[child.move],
            )

            # perform the comparation
            # but note that even if this is false, the child is being added
            # to the dictionary
            if best_child_depth >= child_depth:
                best_child_depth = child_depth
            else:
                # delete the child from the dict
                # since we now that we have better line(s)
                if get_only_best_lines:
                    dict_result.pop(child.move)

        # set the best depth to the dict
        dict_result['best_child_depth'] = best_child_depth

        # delete the children which line is bigger than the best line
        if get_only_best_lines:
            for child in self.next_moves_to_checkmate():
                if child.move not in dict_result:
                    continue

                d_bcd = dict_result[child.move]['best_child_depth']
                if d_bcd > best_child_depth:
                    dict_result.pop(child.move)

        return best_child_depth

    def __str__(self) -> str:
        return f"Move: {self.move}"

    def __repr__(self) -> str:
        return f"Move: {self.move}"
