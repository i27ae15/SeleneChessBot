
from django.core.management.base import BaseCommand

from shiny import App, ui
from pyvis.network import Network

from core.utils import INITIAL_FEN

from game.models import GameState


class Command(BaseCommand):
    help = 'Create dashboard view for the Tree.'

    def handle(self, *args, **options):

        self.view_game()

    def get_html_representation_of_tree(
        self,
        nx_diagraph,
        height="1200px",
        width="100%"
    ) -> str:
        net = Network(height=height, width=width, directed=True)
        root_node = [n for n, d in nx_diagraph.in_degree() if d == 0][0]

        net.from_nx(nx_graph=nx_diagraph)

        for node in net.nodes:
            if node["id"] == root_node:
                node["color"] = "red"

        # Set hierarchical layout and add custom interaction with JavaScript
        net.set_options(
            """
            {
                "layout": {
                    "hierarchical": {
                    "enabled": true,
                    "levelSeparation": 150,
                    "nodeSpacing": 100,
                    "treeSpacing": 200,
                    "direction": "UD",
                    "sortMethod": "directed"
                    }
                },
                "physics": {
                    "enabled": false
                },
                "interaction": { "hover": true },
                "manipulation": {
                    "enabled": true,
                    "initiallyActive": true,
                    "addNode": false,
                    "addEdge": false,
                    "editEdge": false,
                    "deleteNode": false,
                    "deleteEdge": false,
                    "controlNodeStyle": {
                        "borderWidth": 2,
                        "borderWidthSelected": 2,
                        "color": "red"
                    }
                },
                "edges": {
                    "smooth": {
                    "type": "dynamic"
                    }
                }
            }
            """
        )

        # Custom JS to highlight nodes and edges on selection
        # net.show("network.html", notebook=False)
        # net.set_edge_smooth('dynamic')
        return net.generate_html()

    def create_app(
        self,
        network_html: str,
        title: str = 'Si el momento se dio, aprovechalo'
    ) -> App:

        def server(input, output, session):
            pass

        app_ui = ui.page_fluid(
            ui.panel_title(title=title),
            ui.panel_main(
                ui.panel_well(
                    ui.HTML(network_html)
                )
            )
        )

        return App(app_ui, server)

    def view_game(self):
        parent = GameState.objects.get(fen=INITIAL_FEN)
        nx_diagraph = GameState.create_tree_representation(
            parent,
            count_nodes=True
        )

        print('-' * 50)
        print('Number of nodes:', nx_diagraph.number_of_nodes())
        print('-' * 50)

        html_representation = self.get_html_representation_of_tree(
            nx_diagraph=nx_diagraph
        )

        app = self.create_app(
            html_representation,
            title="Si el momento se dio, aprovechalo."
        )

        app.run()
