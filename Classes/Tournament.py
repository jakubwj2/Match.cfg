from random import shuffle
from itertools import combinations
from Classes.Match import Match


class Tournament:
    def __init__(self, teams):
        shuffle(teams)
        self.teams = teams  # list of all teams in the tournament
        self.groups = []
        self.knockout = 0

    def tournament_format(self):
        """
        Creates a tournament format with groups for small tournaments and a knockout stage for larger tournaments
        """
        num_of_teams = len(self.teams)
        if num_of_teams <= 5:
            self.groups = [self.teams]
        # If tournament consists of 5 or fewer teams create one group
        elif num_of_teams <= 9:
            self.groups = [self.teams[0:num_of_teams//2], self.teams[num_of_teams//2:num_of_teams]]
            self.knockout = 2
        # If tournament consists of 5-9 teams create two groups, two semifinals and a final

    def group_matches(self):
        """
        Creates json match files for every game in the group stage
        """
        group_name = 1
        for group in self.groups:
            matches = [Match(*match) for match in combinations(group, 2)]
            for match in matches:
                match.to_json(f"{match.team1.name}_vs_{match.team2.name}_Group{group_name}")
            group_name += 1
