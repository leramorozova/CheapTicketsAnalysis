import argparse
from data_processor import get_tickets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_airports",
        "-n",
        type=int,
        default=1000,
        required=False,
        help="Amount of airports",
    )
    parser.add_argument(
        "--airports_sizes",
        "-s",
        type=list,
        default=["M", "S"],
        required=False,
        help="Sizes of airports, L | M | S",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=".",
        required=False,
        help="Output dir",
    )
    parser.add_argument(
        "--verbose", 
        dest="verbose", 
        action="store_true",
        help="Write logs to output"
    )
    parser.add_argument(
        "--silent", 
        dest="verbose", 
        action="store_false",
        help="Do not write logs to output"
    )
    parser.set_defaults(verbose=True)
    args = parser.parse_args()
    get_tickets(args.num_airports, args.airports_sizes, args.output, args.verbose)
    return 1


if __name__ == "__main__":
    main()
