import json
import os
import re
import subprocess
import sys

from autodl import utils
from autodl.url import get_url
from jsonschema import validate, ValidationError


class DownloadOptions:
    def __init__(self, args):
        self.output = args.output.strip()
        self.paths = args.paths.strip()
        self.dry_run = args.dry_run
        self.download_only = args.download_only
        self.bin_directory = args.bin_directory.strip()
        self.include, self.exclude = [], []
        if args.include:
            self.include = args.include.split(",")
        if args.exclude:
            self.exclude = args.exclude.split(",")

        if self.include and self.exclude:
            print(
                'ERROR: Cannot use both "--include" and "--exclude" flags simultaneously. Please remove one of them'
            )


def download_and_setup(args):
    opts = DownloadOptions(args)

    paths_to_append = []
    urls = []
    files = []

    repo_names_path = str(utils.get_config_path())
    tool_config = json.load(open(repo_names_path, "r"))

    schema_path = str(utils.get_schema_path())
    schema = json.load(open(schema_path, "r"))
    try:
        validate(tool_config, schema=schema)
    except ValidationError as err:
        print(
            f"ValidationError: {err.message}. Please check the below instance in repo_names\n {json.dumps(err.instance, indent=2)}"
        )
        sys.exit(2)

    for tool in tool_config:
        tool_name = tool["name"]
        if opts.include and tool_name not in opts.include:
            continue
        if opts.exclude and tool_name in opts.exclude:
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

        releases = "latest"
        if "releases" in tool:
            releases = tool["releases"]
        url, tag, filename = get_url(
            user, repo, file_pattern, tag_replace=tag_replace, releases=releases
        )
        if not url or not tag or not filename:
            continue
        if opts.dry_run:
            urls.append(url)
            continue

        print("Downloading from... {0}".format(url))
        full_filename = opts.output + "/" + filename
        subprocess.check_output(["wget", "-q", "-P", opts.output, url])
        if opts.download_only:
            files.append(filename)
            continue

        os.chdir(opts.output)
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
            full_bin_path = opts.output + "/" + bin_path
            if "copy_to_bin" not in tool:
                paths_to_append.append("export PATH=" + full_bin_path + ":$PATH")
            else:
                if "copy_source_name" in tool:
                    output_file_path = opts.bin_directory + "/" + tool_name
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
                        ["cp", full_bin_path + "/" + tool_name, opts.bin_directory]
                    )
                    if "chmod" in tool:
                        subprocess.check_output(
                            ["chmod", tool["chmod"], opts.bin_directory]
                        )

    if opts.dry_run:
        print(
            "\nDry run completed. The URLs that would be downloaded are listed below:"
        )
        print("\n".join(urls))
    elif opts.download_only:
        print("\nThe list of files downloaded are printed below:")
        print("\n".join(files))
    elif not args.list:
        print(
            "All files downloaded and the below statements have been added to "
            + opts.paths
        )
        paths_to_append = "\n".join(paths_to_append)
        paths_to_append = "\n" + paths_to_append
        print(paths_to_append)
        with open(opts.paths, "a") as paths_file:
            paths_file.write(paths_to_append)
