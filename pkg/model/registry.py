from pkg.model.projected_points import ProjectedPoints


def init_models(fetcher):
    return {
        'ProjectedPoints': ProjectedPoints(fetcher)
    }
