from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from game.game import Game


class Command(BaseCommand):

    help = 'Create the games from the JSON file accordingly game objects.'

    def add_arguments(self, parser):

        parser.add_argument(
            '--file_name',
            type=str,
            help='Name of the JSON file.',
            default='completed_simulations.json'
        )

    def create_users(self):
        try:
            User.objects.create_superuser(
                username='i27ae15',
                email='andresruse18@gmail.com',
                first_name='Andres',
                last_name='Melendes',
                password='ruse18775',
            )
        except Exception as e:
            print(e)

    def get_data_from_file(self, file_name: str) -> dict:
        import json

        with open(file_name, 'r') as file:
            data: list[dict] = json.load(file)['data']

        return data

    def add_game(self, data: dict):
        game = Game()

        moves: dict = data['moves']
        for index, move_num in enumerate(moves):
            for move in moves[move_num]:
                # print(f"{index + 1} Move: {move}")
                try:
                    game.move_piece(move)
                except Exception as e:
                    print(game.moves)
                    print(f"{index + 1} Move: {move}")

                    print(e)
                    return

    def handle(self, *args, **options):
        self.create_users()
        games = self.get_data_from_file(options['file_name'])

        for index, game in enumerate(games):
            self.add_game(game)
            print(f'Game {index + 1} created successfully.')
