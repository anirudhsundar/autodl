import json
import subprocess
import sys


def print_error_valid(msg):
    print("ERROR: Please provide a valid {0}".format(msg))
    sys.exit(2)


def get_url(user, repo, file_pattern, tag_replace=None, releases="latest"):
    if not user:
        print_error_valid("user")
    if not repo:
        print_error_valid("repo")
    if not file_pattern:
        print_error_valid("file_pattern")

    result_str = ""
    prepare_url = "https://api.github.com/repos/{0}/{1}/releases/{2}".format(
        user, repo, releases
    )
    result = subprocess.check_output(["curl", "-s", prepare_url])
    if sys.version_info.major == 3:
        result_str = result.decode("utf-8")
    elif sys.version_info.major == 2:
        result_str = result

    if not result:
        print("ERROR: couldn't access api. please check the url...")
        sys.exit(2)
    # result_str = result.stdout.decode('utf-8')
    val = json.loads(result_str)
    if not val or "tag_name" not in val:
        print("ERROR: tag_name not found in repo. please check the url...")
        return "", "", ""

    tag_name = val["tag_name"]
    file_tag = tag_name
    if tag_replace:
        file_tag = tag_name.replace(tag_replace[0], tag_replace[1])
    file_pattern = file_pattern.replace("###", file_tag)
    download_url = "https://github.com/{0}/{1}/releases/download/{2}/{3}".format(
        user, repo, tag_name, file_pattern
    )
    return download_url, file_tag, file_pattern
