# Inside signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from core.utils import INITIAL_BOARD_HASH, INITIAL_FEN

from game.models import GameState


@receiver(post_migrate)
def initialize_game_state(sender, **kwargs):
    # Check if the model with the initial board state exists
    exist = GameState.objects.filter(board_hash=INITIAL_BOARD_HASH).exists()
    if not exist:
        # Create the initial board state
        GameState.objects.create(
            board_hash=INITIAL_BOARD_HASH,
            fen=INITIAL_FEN,
            is_game_terminated=False,
            white_value=0,
            black_value=0,
        )

        print('initial game state created')
