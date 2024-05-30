from pkg.fetcher import Fetcher
from pkg.model.registry import init_models


def main():
    f = Fetcher()
    registry = init_models(f)
    for m in registry:
        registry[m].pick()
        print(m + ' suggests you pick: ')
        registry[m].present()


if __name__ == "__main__":
    main()
