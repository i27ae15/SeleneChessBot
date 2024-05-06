import math
import uuid
import numpy as np

from typing import Any

from django.db import models

from pieces.utilites import PieceColor


C_VALUE = 1.414


class GameState(models.Model):

    """
    This also should act as the node in the AlphaZero tree.

    The Json for the expandable_moves and explored_moves would be in the following format:

    {
        'moves': ['Pe4', 'Pe5', 'Pd4', 'Pd5']
    }

    """

    parent: 'GameState' = models.ForeignKey(
        'GameState',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        default=None,
        blank=True
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    board_hash = models.BinaryField()

    is_game_terminated: bool = models.BooleanField()

    white_value: float = models.FloatField()
    black_value: float = models.FloatField()

    fen: str = models.CharField(max_length=255)

    player_turn: int = models.IntegerField(
        choices=PieceColor.choices
    )
    current_turn: int = models.IntegerField()

    num_visits: int = models.IntegerField(default=1)
    expandable_moves: list = models.JSONField()
    explored_moves: list = models.JSONField(default=list)

    move_taken: str = models.CharField(max_length=255)

    @property
    def player_turn_obj(self) -> PieceColor:
        return PieceColor(self.player_turn)

    def add_explored_move(self, move: str) -> None:
        self.explored_moves.append(move)
        self.save()

    def increment_visits(self):
        self.num_visits += 1
        self.save()

    def is_fully_expanded(self) -> bool:
        return len(self.expandable_moves) == len(self.children.all())

    def select(self) -> 'GameState':
        """
        Selects the child with the highest UCB1 value.
        """
        best_child = None
        best_ucb = float('-inf')

        for child in self.children.all():
            ucb = self.get_ucb(child, self.player_turn_obj)
            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child

    def get_ucb(self, child: 'GameState', side: PieceColor) -> float:
        """
        Calculates the UCB1 value for the node.
        """

        values = {
            PieceColor.WHITE: self.white_value,
            PieceColor.BLACK: self.black_value
        }

        value = values[side]

        q_value = ((value / self.num_visits) + 1) / 2
        ucb = q_value + C_VALUE * math.sqrt(
            math.log(self.num_visits) / child.num_visits
        )

        return ucb

    def get_untried_move(self) -> str:
        """
        Returns a move that has not been tried yet.
        """

        move = np.random.choice(self.expandable_moves)
        self.expandable_moves.remove(move)
        self.add_explored_move(move)

        return move

    def expand(self, game_instance: Any) -> 'GameState | bool':
        """
        Expands the current node by creating a new child.
        """

        if self.is_fully_expanded():
            raise False  # No more moves to expand

        move: str = self.get_untried_move()

        print(f"Taken: {move}")

        game_instance.move_piece(move)
        return game_instance.current_game_state

    def simulate(self, game: Any):

        """
        Game would be the pointer to the game object.
        """
        game_instance = game.parse_fen(self.fen)
        current_game_state: GameState = game_instance.current_game_state

        if self.is_game_terminated:
            return self.game_values

        while True:
            try:
                valid_moves = current_game_state.expandable_moves
                move = np.random.choice(valid_moves)

                print('-' * 50)
                print('Selected move:', move)

                game_instance.move_piece(move)
                game_instance.board.print_board()
                print('-' * 50)

                if game_instance.is_game_terminated:

                    game_instance.print_game_state()

                    print('-' * 50)

                    wlm = game_instance.get_legal_moves(
                        color=PieceColor.BLACK,
                        show_in_algebraic=True,
                        show_as_list=True
                    )

                    print('white moves:', wlm)

                    print('-' * 50)

                    blm = game_instance.get_legal_moves(
                        color=PieceColor.WHITE,
                        show_in_algebraic=True,
                        show_as_list=True
                    )

                    print('black moves:', blm)

                    return game_instance.game_values[game_instance.player_turn]
            except Exception as e:
                print('-' * 50)
                print('error occurred')
                print(e)
                print('-' * 50)

                game_instance.print_game_state()

                print('-' * 50)

                wlm = game_instance.get_legal_moves(
                    color=PieceColor.BLACK,
                    show_in_algebraic=True,
                    show_as_list=True
                )

                print('white moves:', wlm)

                print('-' * 50)

                blm = game_instance.get_legal_moves(
                    color=PieceColor.WHITE,
                    show_in_algebraic=True,
                    show_as_list=True
                )

                print('black moves:', blm)

            current_game_state = game_instance.current_game_state

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)
