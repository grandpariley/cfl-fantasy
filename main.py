import sys

from pkg.fetcher import Fetcher
from pkg.model.registry import init_models


def main():
    f = Fetcher()
    registry = init_models(f)
    for m in registry:
        if len(sys.argv) > 1 and m not in sys.argv:
            continue
        registry[m].pick()
        print(m + ' suggests you pick: ')
        registry[m].present()


if __name__ == "__main__":
    main()
