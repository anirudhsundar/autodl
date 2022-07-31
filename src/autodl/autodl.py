from autodl.argument_parser import parse_arguments
from autodl.downloader import download_and_setup


def main():
    args = parse_arguments()
    download_and_setup(args)

if __name__ == "__main__":
    main()
