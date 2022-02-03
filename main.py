import pandas as pd
import json


class Player:
    def __init__(self, name, steam_id):
        self.name = name
        self.steam_id = steam_id


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players


class Match:
    def __init__(self, team1, team2, match_id, num_maps=1):
        self.team1 = team1
        self.team2 = team2
        self.match_id = match_id
        self.num_match = num_maps


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
teams_df = registration_information.groupby("Team")
# Rearrange registration information to a usable format.

teams = []
for team_name, team in teams_df:
    teams.append(Team(team_name,
                      [Player(player["Firstname"].strip() + " " + player["Lastname"].strip(),
                              player["Steam_Id"])
                       for index, player in team.iterrows()]))
# Create a list of team objs from registration details

with open("match.cfg") as match_cfg:
    match_json = json.load(match_cfg)
    print(match_json)

print(str(teams))
