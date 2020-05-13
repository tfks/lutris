

class Steam:
    NAME = "Steam"
    ICON = "steam"
    SLUG = "steam"
    STORE = "steam"
    EXCLUDED_APPIDS = [
        "228980",  # Steamworks Common Redistributables
        "1070560",  # Steam Linux Runtime
    ]
    STEAM_API_HEADER_IMAGE_URL = "https://steamcdn-a.akamaihd.net/steam/apps/%s/header.jpg"


class Gog:
    NAME = "GOG"
    ICON = "gog"
    EMBED_URL = "https://embed.gog.com"
    API_URL = "https://api.gog.com"
    REDIRECT_URI = "https://embed.gog.com/on_login_success?origin=client"
    LOGIN_SUCCESS_URL = "https://www.gog.com/on_login_success"
    CLIENT_ID = "46899977096215655"
    CLIENT_SECRET = "9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9"
    COOKIE_AUTH = ".gog.auth"
    COOKIE_TOKEN = ".gog.token"
    FILENAME_JSON_LIBRARY = "gog-library.json"


class GameDetailsView:
    BACKGROUND_OPACITY = 0.2

