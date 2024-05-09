# Inside signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from core.utils import INITIAL_FEN
from core.testing import BColors

from game.models import GameState
from game.game import Game


@receiver(post_migrate)
def initialize_game_state(sender, **kwargs):
    # Check if the model with the initial board state exists
    exist = GameState.objects.filter(fen=INITIAL_FEN).exists()
    if not exist:

        Game()
        # Create the initial game state
        # Within the game class, everythin is set up to create the inital
        # GameState object

        print(f'{BColors.OKGREEN}Initial game state created.{BColors.ENDC}')
