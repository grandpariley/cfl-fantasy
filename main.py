from pkg.fetcher import Fetcher
from pkg.model.projected_points import ProjectedPoints


def main():
    f = Fetcher()
    projected_points = ProjectedPoints('ProjectedPoints', f.get_data())
    projected_points.pick()
    projected_points.present()


if __name__ == "__main__":
    main()
