import unittest
import uuid

from game import GameState

from core.db import config


class TestGameModel(unittest.TestCase):

    def test_create_model(self):

        new_game_state = GameState(
            id=str(uuid.uuid4()),  # Generate a new UUID for the primary key
            player_turn=1,
            is_game_terminated=False,
            white_value=1.0,
            black_value=0.5,
            castling_rights={'K': True, 'Q': True},
            fen='start_position_fen'
        )

        config.session.add(new_game_state)
        config.session.commit()


if __name__ == '__main__':
    unittest.main()
