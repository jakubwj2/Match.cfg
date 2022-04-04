from steam_id_tools import to_steamID


class Player:
    def __init__(self, name, steam_id):
        self.name = name
        self.steam_id = to_steamID(steam_id)
