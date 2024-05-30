from pkg.model.model import Model


class ProjectedPoints(Model):
    def sort(self):
        return sorted(self.data, key=lambda d: d['projected_points'])
