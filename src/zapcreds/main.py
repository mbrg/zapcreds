import argparse

import requests

from zapcreds.harvest import authenticate_session, get_credentials


def parse_arguments(args=None):
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--email", type=str, required=True, help="Zapier user email")
    parser.add_argument("-p", "--password", type=str, required=True, help="Zapier user password")
    parser.add_argument("-o", "--out", type=str, default="creds.csv", help="Relative path to output file")
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"),
        help="Logging level",
    )

    args = parser.parse_args(args)

    # make sure out path has a .csv file ending
    if not args.out.endswith(".csv"):
        args.out += ".csv"

    return args


def main():
    args = parse_arguments()

    session = requests.Session()
    authenticate_session(session, args.email, args.password)

    creds = get_credentials(session)

    creds.to_csv(args.out)


if __name__ == "__main__":
    main()
