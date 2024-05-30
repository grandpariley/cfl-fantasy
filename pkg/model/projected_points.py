from pkg.model.abstract_model import Model


class ProjectedPoints(Model):
    def sort(self, data):
        return sorted(data, key=lambda d: d['projected_points'])
