from pkg.model.abstract_model import SimpleModel


class ProjectedPoints(SimpleModel):
    def key(self, d):
        return d['projected_points']
