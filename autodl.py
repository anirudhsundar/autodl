import os, sys
import json
import subprocess
import argparse
import re

def print_error_valid(msg):
    print("ERROR: Please provide a valid {0}".format(msg))
    exit(2)

def get_url(user, repo, file_pattern, tag_replace=None, releases='latest'):
    if not user:
        print_error_valid("user")
    if not repo:
        print_error_valid("repo")
    if not file_pattern:
        print_error_valid("file_pattern")

    result_str = ''
    prepare_url = "https://api.github.com/repos/{0}/{1}/releases/{2}".format(user, repo, releases)
    result = subprocess.check_output(["curl", "-s", prepare_url])
    if sys.version_info.major == 3:
        result_str = result.decode('utf-8')
    elif sys.version_info.major == 2:
        result_str = result

    if not result:
        print("ERROR: couldn't access api. please check the url...")
        exit(2)
    # result_str = result.stdout.decode('utf-8')
    val = json.loads(result_str)
    if not val or 'tag_name' not in val:
        print("ERROR: tag_name not found in repo. please check the url...")
        return '', '', ''

    tag_name = val["tag_name"]
    file_tag = tag_name
    if tag_replace:
        file_tag = tag_name.replace(tag_replace[0], tag_replace[1])
    file_pattern = file_pattern.replace("###", file_tag)
    download_url = "https://github.com/{0}/{1}/releases/download/{2}/{3}".format(user, repo, tag_name, file_pattern)
    return download_url, file_tag, file_pattern

def add_arguments():
    parser = argparse.ArgumentParser(description='A simple tool that reads repository information from repo_names.json in the current directory and downloads the latest release versions of the given repos from github')
    parser.add_argument('-o', '--output', help = 'Output directory', default=os.getcwd())
    parser.add_argument('-p', '--paths', help = 'File to append PATHs to', default=os.path.expanduser('~') + '/.autodl_paths.sh')
    parser.add_argument('-n','--dry-run', help = 'Just print the URLs to be downloaded without downloading', action='store_true')
    parser.add_argument('-d', '--download-only', help = 'Download the compressed files', action='store_true')
    parser.add_argument('-b', '--bin-directory', help='Default bin directory to copy the files to', default=os.path.expanduser('~') + '/' + 'bin/')
    parser.add_argument('-i', '--include', help='Comma separated list of tool names (as mentioned in repo_names.json) to download. Cannot be used with --exclude. Eg: clangd,gh,bat')
    parser.add_argument('-e', '--exclude', help='Comma separated list of tool names (as mentioned in repo_names.json) to exclude. Cannot be used with --include. Eg: clangd,gh,bat')
    parser.add_argument('-l', '--list', help='Just list the tools that would be downloaded and exit', action='store_true')
    return parser.parse_args()


def main():

    args = add_arguments()

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
        print('ERROR: Cannot use both "--include" and "--exclude" flags simultaneously. Please remove one of them')

    paths_to_append = []
    urls = []
    files = []

    tool_config = json.load(open('repo_names.json', 'r'))
    for tool in tool_config:
        tool_name = tool['name']
        if include and tool_name not in include:
            continue
        if exclude and tool_name in exclude:
            continue
        if args.list:
            print(tool['name'])
            continue
        else:
            print('Preparing to download',tool['name'])
        user = tool['user']
        repo = tool['repo']
        file_pattern = tool['file_pattern']

        if 'uncompress' in tool and tool['uncompress']:
            uncompress_cmd = tool['uncompress_cmd']
            uncompress_flags = ''
            if 'uncompress_flags' in tool:
                uncompress_flags = tool['uncompress_flags']
                uncompress_flags = re.sub(r'\s+', ' ', uncompress_flags.strip())

        tag_replace = None
        if "tag_replace" in tool:
            tag_replace = tool["tag_replace"]

        remove_v = False
        if "remove_v" in tool:
            remove_v = True
            tag_replace = ['v', '']

        releases = 'latest'
        if 'releases' in tool:
            releases = tool['releases']
        url, tag, filename = get_url(user, repo, file_pattern, tag_replace=tag_replace, releases=releases)
        if not url or not tag or not filename:
            continue
        if dry_run:
            urls.append(url)
            continue

        print('Downloading from... {0}'.format(url))
        full_filename = output + '/' + filename
        subprocess.check_output(['wget', '-q', '-P', output, url])
        if download_only:
            files.append(filename)
            continue

        os.chdir(output)
        if 'uncompress' in tool and tool['uncompress']:
            if uncompress_flags:
                subprocess.check_output([uncompress_cmd, uncompress_flags, full_filename])
            else:
                subprocess.check_output([uncompress_cmd, full_filename])
            subprocess.check_output(['rm', full_filename])
        if 'bin_dir_pattern' in tool:
            bin_path = tool['bin_dir_pattern'].replace('###',tag)
            full_bin_path = output + '/' + bin_path
            if 'copy_to_bin' not in tool:
                paths_to_append.append('export PATH='+full_bin_path+':$PATH')
            else:
                if 'copy_source_name' in tool:
                    output_file_path = bin_directory + '/' + tool_name
                    subprocess.check_output(['cp', full_bin_path + '/' + tool['copy_source_name'], output_file_path])
                    if 'chmod' in tool:
                        subprocess.check_output(['chmod', tool['chmod'], output_file_path])
                else:
                    subprocess.check_output(['cp', full_bin_path + '/' + tool_name, bin_directory])
                    if 'chmod' in tool:
                        subprocess.check_output(['chmod', tool['chmod'], bin_directory])

    if dry_run:
        print('\nDry run completed. The URLs that would be downloaded are listed below:')
        print('\n'.join(urls))
    elif download_only:
        print('\nThe list of files downloaded are printed below:')
        print('\n'.join(files))
    elif not args.list:
        print('All files downloaded and the below statements have been added to '+paths)
        paths_to_append = '\n'.join(paths_to_append)
        paths_to_append = '\n'+paths_to_append
        print(paths_to_append)
        with open(paths, "a") as paths_file:
            paths_file.write(paths_to_append)

if __name__ == '__main__':
    main()
