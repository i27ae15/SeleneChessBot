def dfs_on_(
    self,
    parent: GameState,
    save_games: list[GameState] = None
):

    if save_games is not None:
        save_games.append(parent)

    if parent.children.all().count() == 0:
        return

    # go for the children with the most visits

    children = parent.children.all().order_by('-num_visits')
    child = children.first()
    self.dfs_on_visits(child, save_games)
