import pandas as pd
import json
from steam_id_tools import to_steamID, to_numeric_string
from Player import Player
from Team import Team
from Match import Match


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
