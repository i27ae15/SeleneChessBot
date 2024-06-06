from django.test import TestCase
from alpha_zero.alpha_zero import AlphaZero
from alpha_zero.tree import TreeRepresentation
from alpha_zero.checkpoint import Checkpoint


class AlphaZeroTest(TestCase):

    def test_nodes(self):

        alpha_zero = AlphaZero(
            depth_of_search=15,
            # mcst_exploration_weight=2.0
        )
        root = alpha_zero.play_game()

        print('-' * 50)
        # tree = TreeRepresentation(root_node=root, view_tree=False)

        # nx_diagraph = tree.create_tree_representation(
        #     parent=root,
        # )

        # Checkpoint.save_checkpoint(flatten=True, root=root)
        # checkpoint = Checkpoint().load_checkpoint()

        # nx_diagraph_loaded = tree.create_tree_representation(
        #     parent=root,
        # )

        # self.assertEqual(
        #     nx_diagraph.number_of_nodes(),
        #     nx_diagraph_loaded.number_of_nodes()
        # )

        # print('nx_diagraph nodes:', nx_diagraph.number_of_nodes())

        # print('loading tree from checkpoint...')
        # TreeRepresentation(root_node=root)
