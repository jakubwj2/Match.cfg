class Match:
    def __init__(self, team1, team2, num_maps=1):
        self.team1 = team1
        self.team2 = team2
        self.match_id = f"{team1.name} vs {team2.name}"
        self.num_maps = num_maps
