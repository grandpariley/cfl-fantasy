from pkg.model.all_different_teams_less_than_10000 import AllDifferentTeamsAndLessThan10000
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
        'projected': ProjectedPoints(fetcher),
        'average': AveragePoints(fetcher),
        'touchdowns': Touchdowns(fetcher),
        'teamsAnd10000': AllDifferentTeamsAndLessThan10000(fetcher)
    }
