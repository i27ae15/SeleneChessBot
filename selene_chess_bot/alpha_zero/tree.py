import networkx as nx

from shiny import App, ui
from pyvis.network import Network

from alpha_zero.node import GameStateNode


class TreeRepresentation:

    """
        A class to represent and visualize a game state tree.

        Attributes:
        ----------
        root_node : GameStateNode
            The root node of the game state tree.
        view_tree : bool
            A flag to indicate whether to visualize the tree on initialization.

        Methods:
        -------

        create_tree_representation(
            parent,
            visited=None,
            nx_graph=None,
            use_string_hash=False
        ):
            Creates a NetworkX DiGraph representation of the game state tree.

        get_html_representation_of_tree(
            nx_diagraph,
            height="1200px",
            width="100%"
        ):
            Generates an HTML representation of the tree using pyvis.

        create_app(network_html, title='Si el momento se dio, aprovechalo'):
            Creates a Shiny App to display the tree visualization.

        view_tree():
            Initiates the visualization process for the game state tree.
    """

    def __init__(
        self,
        root_node: GameStateNode,
        view_tree: bool = True,
        tree_title: str = None,
    ) -> None:

        """
        Initializes the TreeRepresentation class with a root node and an
        optional flag to visualize the tree.

        Parameters:
        ----------

        root_node : GameStateNode
            The root node of the game state tree.

        view_tree : bool, optional
            If True, automatically visualizes the tree upon initialization
            (default is True).
        """

        self.root_node = root_node
        self.tree_title = tree_title

        if view_tree:
            if self.tree_title is None:
                self.tree_title = 'Si el momento se dio, aprovechalo'

            self.view_tree(title=self.tree_title)

    @staticmethod
    def create_tree_representation(
        parent: 'GameStateNode',
        visited: set = None,
        nx_graph: nx.DiGraph = None,
        use_string_hash: bool = False,
    ) -> nx.DiGraph:
        """
        Creates a NetworkX DiGraph representation of the game state tree using
        a depth-first search (DFS) traversal.

        Parameters:
        ----------

        parent : GameStateNode
            The current node being processed in the game state tree.

        visited : set, optional
            A set of visited nodes to prevent cycles (default is None).

        nx_graph : nx.DiGraph, optional
            The NetworkX DiGraph being constructed (default is None).

        use_string_hash : bool, optional
            If True, uses string hashes of nodes for edge creation
            (default is False).

        Returns:
        -------
        nx.DiGraph
            The constructed NetworkX DiGraph representing the game state tree.
        """

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

            edg1 = str(parent.board_hash) if use_string_hash else parent
            edg2 = str(child.board_hash) if use_string_hash else child

            child: GameStateNode
            nx_graph.add_edge(edg1, edg2)
            TreeRepresentation.create_tree_representation(
                parent=child,
                visited=visited,
                nx_graph=nx_graph,
                use_string_hash=use_string_hash
            )

        return nx_graph

    def get_html_representation_of_tree(
        self,
        nx_diagraph,
        height="1200px",
        width="100%"
    ) -> str:

        """
        Generates an HTML representation of the tree using pyvis.

        Parameters:
        ----------

        nx_diagraph : nx.DiGraph
            The NetworkX DiGraph representing the game state tree.

        height : str, optional
            The height of the HTML canvas for the tree visualization
            (default is "1200px").

        width : str, optional
            The width of the HTML canvas for the tree visualization
            (default is "100%").

        Returns:
        -------
        str
            The HTML string for visualizing the tree.
        """

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

        return net.generate_html()

    def view_tree(
        self,
        title: str = 'Si el momento se dio, aprovechalo'
    ):
        """
        Initiates the visualization process for the game state tree.
        """

        nx_diagraph = self.create_tree_representation(
            use_string_hash=True,
            parent=self.root_node,
        )

        html_representation = self.get_html_representation_of_tree(
            nx_diagraph=nx_diagraph
        )

        app = self._create_app(
            title=title,
            network_html=html_representation,
        )

        app.run()

    def _create_app(
        self,
        network_html: str,
        title: str = 'Si el momento se dio, aprovechalo'
    ) -> App:

        """
        Creates a Shiny App to display the tree visualization.

        Parameters:
        ----------

        network_html : str
            The HTML string for visualizing the tree.

        title : str, optional
            The title of the Shiny App
            (default is 'Si el momento se dio, aprovechalo').

        Returns:
        -------
        App
            The Shiny App instance for displaying the tree visualization.
        """

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
