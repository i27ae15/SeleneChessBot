from django.test import TestCase
from alpha_zero.alpha_zero import AlphaZero
from alpha_zero.tree import TreeRepresentation
from alpha_zero.checkpoint import Checkpoint


class AlphaZeroTest(TestCase):

    def test_alpha_zero(self):

        alpha_zero = AlphaZero(
            depth_of_search=10,
        )
        alpha_zero.play_game()

    def test_nodes(self):

        alpha_zero = AlphaZero(
            depth_of_search=1,
            mcst_exploration_weight=2.0
        )
        best_move, root = alpha_zero.play_game()
        # print(f'best_move ucb: {best_move.get_ucb()}')
        # print(f'root children: {root.children}')

        print('-' * 50)

        # for move, child in root.children.items():
        #     print(f'{move} ucb: {child.get_ucb()}, num visits: {child.num_visits}')

        tree = TreeRepresentation(root_node=root, view_tree=False)

        nx_diagraph = tree.create_tree_representation(
            parent=root,
        )

        Checkpoint.save_checkpoint(flatten=True, root=root)
        checkpoint = Checkpoint().load_checkpoint()

        nx_diagraph_loaded = tree.create_tree_representation(
            parent=checkpoint,
        )

        self.assertEqual(
            nx_diagraph.number_of_nodes(),
            nx_diagraph_loaded.number_of_nodes()
        )

        print('loading tree from checkpoint...')
        TreeRepresentation(root_node=checkpoint)
