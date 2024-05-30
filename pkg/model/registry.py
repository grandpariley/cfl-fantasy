from pkg.model.projected_points import ProjectedPoints


def init_models(fetcher):
    """
    Add your new models here. They must implement the abstract Model
    :param fetcher: a Fetcher for the CFL fantasy data
    :return: a registry of models to run
    """
    return {
        'projected points': ProjectedPoints(fetcher)
    }
