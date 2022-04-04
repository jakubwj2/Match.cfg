import json


class Match:
    def __init__(self, team1, team2, num_maps=1):
        self.team1 = team1
        self.team2 = team2
        self.match_id = f"{team1.name} vs {team2.name}"
        self.num_maps = num_maps

    def to_json(self, name):
        with open("match_cfg_template.json", "r") as match_template, \
             open(f"Group_Matches\\{name}.json", "w") as match_cfg:
            match_json = json.load(match_template)

            match_json["team1"]["name"] = self.team1.name
            match_json.update({"matchid": self.match_id,
                               "num_maps": self.num_maps,
                               "team1": self.team1.team,
                               "team2": self.team2.team})
            match_cfg.write(json.dumps(match_json, indent=4, sort_keys=True))
