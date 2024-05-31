from pkg.model.abstract_model import Model


class Touchdowns(Model):
    def score(self, d):
        return sum([int(d['pass_tds']), int(d['receiving_tds']), int(d['rush_tds'])])
