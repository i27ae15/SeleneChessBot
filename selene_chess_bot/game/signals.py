# Inside signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from core.utils import INITIAL_FEN
from core.testing import BColors

from game.models import GameState
from game.game import Game


@receiver(post_migrate)
def initialize_game_state(sender, **kwargs):
    return
    # Check if the model with the initial board state exists
    exist = GameState.objects.filter(fen=INITIAL_FEN).exists()
    if not exist:
        g = Game()
        g.current_game_state.num_visits = 0
        g.current_game_state.save()

        # Create the initial game state
        # Within the game class, everythin is set up to create the inital
        # GameState object, we just need to set the num_visits to 0 since they
        # are initialized to 1

        print(f'{BColors.OKGREEN}-{BColors.ENDC}' * 50)
        print(f'{BColors.OKGREEN}Initial game state created.{BColors.ENDC}')
        print(f'{BColors.OKGREEN}-{BColors.ENDC}' * 50)
