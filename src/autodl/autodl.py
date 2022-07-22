"""
This is a short script to automatically download the
latest releases of certain tools (which are listed in repo_names.json).
"""

import json
import os
import re
import subprocess
import sys

from autodl import utils
from autodl.url import get_url
from autodl.argument_parser import parse_arguments


def main():

    args = parse_arguments()

    output = args.output.strip()
    paths = args.paths.strip()
    dry_run = args.dry_run
    download_only = args.download_only
    bin_directory = args.bin_directory.strip()
    include, exclude = [], []
    if args.include:
        include = args.include.split(",")
    if args.exclude:
        exclude = args.exclude.split(",")

    if include and exclude:
        print(
            'ERROR: Cannot use both "--include" and "--exclude" flags simultaneously. Please remove one of them'
        )

    paths_to_append = []
    urls = []
    files = []

    repo_names_path = str(utils.get_config_path())
    tool_config = json.load(open(repo_names_path, "r"))
    for tool in tool_config:
        tool_name = tool["name"]
        if include and tool_name not in include:
            continue
        if exclude and tool_name in exclude:
            continue
        if args.list:
            print(tool["name"])
            continue
        else:
            print("Preparing to download", tool["name"])
        user = tool["user"]
        repo = tool["repo"]
        file_pattern = tool["file_pattern"]

        if "uncompress" in tool and tool["uncompress"]:
            uncompress_cmd = tool["uncompress_cmd"]
            uncompress_flags = ""
            if "uncompress_flags" in tool:
                uncompress_flags = tool["uncompress_flags"]
                uncompress_flags = re.sub(r"\s+", " ", uncompress_flags.strip())

        tag_replace = None
        if "tag_replace" in tool:
            tag_replace = tool["tag_replace"]

        remove_v = False
        if "remove_v" in tool:
            remove_v = True
            tag_replace = ["v", ""]

        releases = "latest"
        if "releases" in tool:
            releases = tool["releases"]
        url, tag, filename = get_url(
            user, repo, file_pattern, tag_replace=tag_replace, releases=releases
        )
        if not url or not tag or not filename:
            continue
        if dry_run:
            urls.append(url)
            continue

        print("Downloading from... {0}".format(url))
        full_filename = output + "/" + filename
        subprocess.check_output(["wget", "-q", "-P", output, url])
        if download_only:
            files.append(filename)
            continue

        os.chdir(output)
        if "uncompress" in tool and tool["uncompress"]:
            if uncompress_flags:
                subprocess.check_output(
                    [uncompress_cmd, uncompress_flags, full_filename]
                )
            else:
                subprocess.check_output([uncompress_cmd, full_filename])
            subprocess.check_output(["rm", full_filename])
        if "bin_dir_pattern" in tool:
            bin_path = tool["bin_dir_pattern"].replace("###", tag)
            full_bin_path = output + "/" + bin_path
            if "copy_to_bin" not in tool:
                paths_to_append.append("export PATH=" + full_bin_path + ":$PATH")
            else:
                if "copy_source_name" in tool:
                    output_file_path = bin_directory + "/" + tool_name
                    subprocess.check_output(
                        [
                            "cp",
                            full_bin_path + "/" + tool["copy_source_name"],
                            output_file_path,
                        ]
                    )
                    if "chmod" in tool:
                        subprocess.check_output(
                            ["chmod", tool["chmod"], output_file_path]
                        )
                else:
                    subprocess.check_output(
                        ["cp", full_bin_path + "/" + tool_name, bin_directory]
                    )
                    if "chmod" in tool:
                        subprocess.check_output(["chmod", tool["chmod"], bin_directory])

    if dry_run:
        print(
            "\nDry run completed. The URLs that would be downloaded are listed below:"
        )
        print("\n".join(urls))
    elif download_only:
        print("\nThe list of files downloaded are printed below:")
        print("\n".join(files))
    elif not args.list:
        print(
            "All files downloaded and the below statements have been added to " + paths
        )
        paths_to_append = "\n".join(paths_to_append)
        paths_to_append = "\n" + paths_to_append
        print(paths_to_append)
        with open(paths, "a") as paths_file:
            paths_file.write(paths_to_append)


if __name__ == "__main__":
    main()
