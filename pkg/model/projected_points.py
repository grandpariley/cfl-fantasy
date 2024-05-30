from pkg.model.abstract_model import Model


class ProjectedPoints(Model):
    def sort(self):
        return sorted(self.data, key=lambda d: d['projected_points'])
