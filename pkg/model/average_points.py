from pkg.model.abstract_model import Model


class AveragePoints(Model):
    def score(self, d):
        return float(d['average_points'] if d['average_points'] != '' else 0.0)
