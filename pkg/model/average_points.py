from pkg.model.abstract_model import SimpleModel


class AveragePoints(SimpleModel):
    def key(self, d):
        return float(d['average_points'] if d['average_points'] != '' else 0.0)
