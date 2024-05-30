from pkg.model.average_points import AveragePoints
from pkg.model.projected_points import ProjectedPoints
from pkg.model.touchdowns import Touchdowns


def init_models(fetcher):
    """
    Add your new models here. They must implement the abstract Model
    :param fetcher: a Fetcher for the CFL fantasy data
    :return: a registry of models to run
    """
    return {
        'projected points': ProjectedPoints(fetcher),
        'average points': AveragePoints(fetcher),
        'touchdowns': Touchdowns(fetcher),
    }
