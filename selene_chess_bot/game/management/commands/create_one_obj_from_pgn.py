
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from pgn.pgn import PGN
from game.models import GameState
from core.utils import INITIAL_FEN


class Command(BaseCommand):
    help = 'Create 15404 GameState Objects from MacKenzie.txt PGN file.'

    def add_arguments(self, parser):
        # Optional: add any command line arguments here
        pass

    def extract_pgn_to_variables(self, file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            games = file.read().strip().split('\n\n')

        return games

    def handle(self, *args, **options):

        self.create_game_states()

    def create_game_states(self):
        # Eliminate all the game states but the initial one
        GameState.objects.exclude(fen=INITIAL_FEN).delete()

        try:
            User.objects.create_superuser(
                username='i27ae15',
                email='andresruse18@gmail.com',
                first_name='Andres',
                last_name='Ruse',
                password='ruse18775',
            )
        except Exception as _:
            print('User already exists.')

        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[4].replace('\n', ' ')

        print('game', game)
        PGN(game)
