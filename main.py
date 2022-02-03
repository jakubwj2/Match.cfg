import pandas as pd
import json
import re


def to_steamID(steamID):
    id_str = str(steamID)

    if id_str.isnumeric() and not len(id_str) == 17:
        id_str = f"[U:1:{id_str}]"

    if re.search("^STEAM_", id_str): # Already a steamID
        return id_str

    elif re.search("^\[.*\]$", id_str): # If passed steamID3

        id_split = id_str.split(":") # Split string into 'Universe', Account type, and Account number
        account_id3 = int(id_split[2][:-1]) # Remove ] from end of steamID3

        if account_id3 % 2 == 0:
            account_type = 0
        else:
            account_type = 1

        account_id = (account_id3 - account_type) // 2
        return "STEAM_0:" + str(account_type) + ":" + str(account_id)

    elif id_str.isnumeric(): # Passed steamID64

        id64_base = 76561197960265728 # steamID64 are all offset from this value
        offset_id = int(id_str) - id64_base

        # Get the account type and id
        if offset_id % 2 == 0:
            account_type = 0
        else:
            account_type = 1

        account_id = ((offset_id - account_type) // 2)

        return "STEAM_0:" + str(account_type) + ":" + str(account_id)
    else:
        raise ValueError(f"Wrong steam_id format: {id_str}")


def to_numeric_string(steam_id):
    if (isinstance(steam_id, float) or steam_id.isnumeric()):
        return str(int(steam_id))
    return str(steam_id)


class Player:
    def __init__(self, name, steam_id):
        self.name = name
        self.steam_id = to_steamID(steam_id)


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def get_team(self):
        return {"name": self.name,
                "tag": self.name,
                "players": [to_steamID(player.steam_id) for player in self.players],
                "flag":"CZ"
                }
    team = property(get_team)


class Match:
    def __init__(self, team1, team2, num_maps=1):
        self.team1 = team1
        self.team2 = team2
        self.match_id = f"{team1.name} vs {team2.name}"
        self.num_maps = num_maps


sheet_id = "1IsO2CVtWUKuaFGSX_F_tuoaNpO-g0h4esTuck-4wxiM"
registration_information = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv",
                                       usecols=["Jméno", "Příjmení", "Název týmu (pokud máš)", "Steam kód uživatele"])
# Get a cvs file with necessary details of applicants.

registration_information.rename(columns={"Jméno": "Firstname",
                                         "Příjmení": "Lastname",
                                         "Název týmu (pokud máš)": "Team",
                                         "Steam kód uživatele": "Steam_Id"},
                                inplace=True)
registration_information.drop(range(34, len(registration_information)), inplace=True)
registration_information.loc[:,"Steam_Id"] = registration_information.Steam_Id.apply(to_numeric_string)
teams_df = registration_information.groupby("Team")
# Rearrange registration information to a usable format.

teams = []
for team_name, team in teams_df:
    teams.append(Team(team_name,
                      [Player(player["Firstname"].strip() + " " + player["Lastname"].strip(),
                              player["Steam_Id"])
                       for index, player in team.iterrows()]))
# Create a list of team objs from registration details

match = Match(teams[2], teams[4])

with open("match_cfg_template.json", "r") as match_template, open("match.json", "w") as match_cfg:
    match_json = json.load(match_template)

    match_json["team1"]["name"] = match.team1.name
    match_json.update({"matchid":match.match_id,
                       "num_maps":match.num_maps,
                       "team1": match.team1.team,
                       "team2": match.team2.team})
    match_cfg.write(json.dumps(match_json, indent=4, sort_keys=True))
# print([[player.name, player.steam_id] for player in teams[4].players])
