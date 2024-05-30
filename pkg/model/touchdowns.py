from pkg.model.abstract_model import SimpleModel


class Touchdowns(SimpleModel):
    def key(self, d):
        return sum([int(d['pass_tds']), int(d['receiving_tds']), int(d['rush_tds'])])
