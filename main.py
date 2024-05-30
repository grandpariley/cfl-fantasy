from pkg.fetcher import Fetcher


def main():
    f = Fetcher()
    print(f.get_data())


if __name__ == "__main__":
    main()
