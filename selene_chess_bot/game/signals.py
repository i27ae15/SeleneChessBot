# Inside signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from core.utils import INITIAL_FEN

from game.models import GameState
from pieces.utilites import PieceColor
from game.game import Game


@receiver(post_migrate)
def initialize_game_state(sender, **kwargs):
    # Check if the model with the initial board state exists
    exist = GameState.objects.filter(fen=INITIAL_FEN).exists()
    if not exist:

        game = Game(get_game_state=False)
        expandable_moves = game.get_legal_moves(
            color=PieceColor.WHITE,
            show_in_algebraic=True,
            show_as_list=True,
        )

        GameState.objects.create(
            board_hash=game.current_board_hash,
            fen=INITIAL_FEN,
            is_game_terminated=False,
            white_value=0,
            black_value=0,
            player_turn=PieceColor.WHITE.value,
            current_turn=1,
            expandable_moves=expandable_moves
        )

        print('Initial game state created.')
