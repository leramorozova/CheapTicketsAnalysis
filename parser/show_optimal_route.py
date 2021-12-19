import argparse
from path_finder import PathFinder


CURRENT_DATASET = '../data/data.csv'
CURRENT_DATASET_ENCODING = 'cp1251'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--origin",
        "-o",
        type=str,
        help="Origin city",
    )
    parser.add_argument(
        "--destination",
        "-d",
        type=str,
        help="Destination city",
    )

    args = parser.parse_args()
    path_finder = PathFinder(CURRENT_DATASET, CURRENT_DATASET_ENCODING)
    path = path_finder.find_path(args.origin, args.destination)
    if path:
        print(path)
    else:
        print(f"No path was found from '{args.origin}' "
              f"to '{args.destination}'. "
              f"Please check name correctness.")
    return 0


if __name__ == "__main__":
    main()
