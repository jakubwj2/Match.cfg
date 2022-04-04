from steam_id_tools import to_steamID


class Team:
    def __init__(self, name, players):
        self.name = name.replace(" ", "_")
        self.players = players

    def get_team(self):
        return {"name": self.name,
                "tag": self.name,
                "players": [to_steamID(player.steam_id) for player in self.players],
                "flag": "CZ"
                }
    team = property(get_team)
