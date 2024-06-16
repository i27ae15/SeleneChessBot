from unittest import TestCase

import tensorflow as tf

from core.testing import print_starting, print_success
from core.printing import __print__ as print

from alpha_zero.alpha_zero import AlphaZero


class AlphaZeroModelTest(TestCase):

    def test_model(self):

        print_starting()

        alpha_zero = AlphaZero(depth_of_search=15)
        model = tf.keras.models.load_model('model_v0_1.keras')

        alpha_zero.self_play(
            model=model,
            num_games=1,
            num_iterations=10,
        )

        print_success()
