import pandas as pd
from steam_id_tools import to_numeric_string
from Classes.Player import Player
from Classes.Team import Team
from Classes.Match import Match
from Classes.Tournament import Tournament


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
registration_information.loc[:, "Steam_Id"] = registration_information.Steam_Id.apply(to_numeric_string)
teams_df = registration_information.groupby("Team")
# Rearrange registration information to a usable format.

teams = []
for team_name, team in teams_df:
    teams.append(Team(team_name,
                      [Player(player["Firstname"].strip() + " " + player["Lastname"].strip(),
                              player["Steam_Id"])
                       for index, player in team.iterrows()]))
# Create a list of team objs from registration details

match = Match(teams[1], teams[4])
match.to_json("match")

tournament = Tournament(teams)
tournament.tournament_format()
tournament.group_matches()
