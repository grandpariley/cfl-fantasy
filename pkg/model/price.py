from pkg.model.abstract_model import SimpleModel


class Price(SimpleModel):
    def key(self, d):
        return int(d['price'])
