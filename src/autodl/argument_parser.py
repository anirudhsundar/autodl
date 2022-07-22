import argparse
import os


def add_arguments():
    parser = argparse.ArgumentParser(
        description="A simple tool that reads repository information from repo_names.json in the current directory and downloads the latest release versions of the given repos from github"
    )
    parser.add_argument("-o", "--output", help="Output directory", default=os.getcwd())
    parser.add_argument(
        "-p",
        "--paths",
        help="File to append PATHs to",
        default=os.path.expanduser("~") + "/.autodl_paths.sh",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        help="Just print the URLs to be downloaded without downloading",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--download-only",
        help="Download the compressed files",
        action="store_true",
    )
    parser.add_argument(
        "-b",
        "--bin-directory",
        help="Default bin directory to copy the files to",
        default=os.path.expanduser("~") + "/" + "bin/",
    )
    parser.add_argument(
        "-i",
        "--include",
        help="Comma separated list of tool names (as mentioned in repo_names.json) to download. Cannot be used with --exclude. Eg: clangd,gh,bat",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        help="Comma separated list of tool names (as mentioned in repo_names.json) to exclude. Cannot be used with --include. Eg: clangd,gh,bat",
    )
    parser.add_argument(
        "-l",
        "--list",
        help="Just list the tools that would be downloaded and exit",
        action="store_true",
    )
    return parser.parse_args()
