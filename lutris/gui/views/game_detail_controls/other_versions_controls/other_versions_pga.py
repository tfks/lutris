

def get_other_versions(
    game,
    name_filter=None,
    filter_installed=False,
    filter_runner=None,
    select=None,
    show_installed_first=False
):
    if game is None:
        return None

    # Select config files from game id's directory
    # ~/.cache/lutris/other-versions/game-slug/uid?.yaml
