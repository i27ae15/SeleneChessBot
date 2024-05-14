import os
import django

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.contrib.auth.models import User

from pgn.pgn import PGN


class Command(BaseCommand):
    help = 'Create 15404 GameState Objects from MacKenzie.txt PGN file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--games_to_create',
            type=int,
            help='Number of games to create.'
        )

    def extract_pgn_to_variables(self, file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            games = file.read().strip().split('\n\n')

        return games

    def handle(self, *args, **options):

        # Setting up the Django environment
        os.environ.setdefault(
            'DJANGO_SETTINGS_MODULE',
            'selene_chess_bot.settings'
        )
        django.setup()

        # Calling the migrate command
        call_command('migrate')

        games_to_create = options.get('games_to_create', float('inf'))
        self.create_game_states(games_to_create=games_to_create)

    def create_game_states(self, games_to_create: int):

        User.objects.create_superuser(
            username='i27ae15',
            email='andresruse18@gmail.com',
            first_name='Andres',
            last_name='Ruse',
            password='ruse18775',
        )

        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)

        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            PGN(g)

            if games_to_create is None:
                continue

            if index == games_to_create - 1:
                break
