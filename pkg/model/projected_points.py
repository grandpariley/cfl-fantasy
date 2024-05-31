from pkg.model.abstract_model import Model


class ProjectedPoints(Model):
    def score(self, d):
        return float(d['projected_points'])
