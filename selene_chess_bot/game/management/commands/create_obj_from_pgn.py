
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from pgn.pgn import PGN


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

        self.test_from_real_games()

    def test_from_real_games(self):

        User.objects.create_user(
            username='i27ae15',
            email='andresruse18@gmail.com',
            first_name='Andres',
            last_name='Ruse',
            password='ruse18775'
        )

        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)

        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            PGN(g)
