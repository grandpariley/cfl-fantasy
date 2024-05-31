from pkg.model.abstract_model import Model

picked_teams = []


class AllDifferentTeamsAndLessThan10000(Model):
    def score(self, d):
        if d['team'] in picked_teams or int(d['price']) > 10000:
            return 0
        return float(d['projected_points'])

    def re_score(self, d, picks, last_picked, budget):
        if last_picked:
            picked_teams.append(last_picked['team'])
        return self.score(d)
