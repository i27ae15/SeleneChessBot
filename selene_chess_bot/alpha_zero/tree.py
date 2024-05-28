import networkx as nx

from shiny import App, ui
from pyvis.network import Network

from alpha_zero.node import GameStateNode


class TreeRepresentation:

    def __init__(
        self,
        root_node: GameStateNode,
        view_game: bool = True,
        count_nodes: bool = True,
    ) -> None:

        self.root_node = root_node

        if view_game:
            self.view_game(
                count_nodes=count_nodes
            )

    def create_tree_representation(
        self,
        parent: 'GameStateNode',
        visited: set = None,
        count_nodes: bool = False,
        nx_graph: nx.DiGraph = None,
    ) -> nx.DiGraph:
        """
        Create the nx.Diagraph tree code representation with a DFS on the tree.
        """

        # print(parent.children)

        if nx_graph is None:
            nx_graph = nx.DiGraph()

        if visited is None:
            visited = set()

        # Check if the current node has already been visited
        if str(parent.board_hash) in visited:
            return nx_graph

        # Mark the current node as visited
        visited.add(str(parent.board_hash))

        if len(parent.children) == 0:
            return nx_graph

        for _, child in parent.children.items():

            child: GameStateNode
            nx_graph.add_edge(str(parent.board_hash), str(child.board_hash))
            self.create_tree_representation(
                parent=child,
                visited=visited,
                nx_graph=nx_graph,
                count_nodes=count_nodes,
            )

        return nx_graph

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

    def view_game(self, count_nodes: bool = True):
        nx_diagraph = self.create_tree_representation(
            parent=self.root_node,
            count_nodes=count_nodes
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
