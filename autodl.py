import os, sys
import json
import subprocess
import argparse

def print_error_valid(msg):
    print("ERROR: Please provide a valid {0}".format(msg))
    exit(2)

def get_url(user, repo, file_pattern, remove_v=False):
    if not user:
        print_error_valid("user")
    if not repo:
        print_error_valid("repo")
    if not file_pattern:
        print_error_valid("file_pattern")

    result_str = ''
    if sys.version_info.major == 3:
        result = subprocess.check_output(["curl", "https://api.github.com/repos/{0}/{1}/releases/latest".format(user, repo)])
        result_str = result.decode('utf-8')
    elif sys.version_info.major == 2:
        result = subprocess.check_output(["curl", "https://api.github.com/repos/{0}/{1}/releases/latest".format(user, repo)])
        result_str = result

    if not result:
        print("ERROR: couldn't access api. please check the url...")
        exit(2)
    # result_str = result.stdout.decode('utf-8')
    val = json.loads(result_str)
    if not val:
        print("ERROR: tag_name not found in repo. please check the url...")
        exit(2)

    tag_name = val["tag_name"]
    file_tag = tag_name
    if remove_v:
        file_tag = tag_name.replace('v', '')
    file_pattern = file_pattern.replace("###", file_tag)
    download_url = "https://github.com/{0}/{1}/releases/download/{2}/{3}".format(user, repo, tag_name, file_pattern)
    return download_url, file_tag, file_pattern

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help = 'Output directory')
    parser.add_argument('-p', '--paths', help = 'File to append PATHs to')
    parser.add_argument('-n','--dry-run', help = 'Just print the URLs to be downloaded without downloading', action='store_true')
    parser.add_argument('-d', '--download-only', help = 'Download the compressed files', action='store_true')
    args = parser.parse_args()
    dotfiles_dir = os.getcwd()

    output = os.getcwd()
    if args.output:
        output = args.output

    paths = os.path.expanduser('~')+'/.local_paths'
    if args.paths:
        paths = args.paths

    download_only = args.download_only
    dry_run = args.dry_run

    paths_to_append = []

    tool_config = json.load(open('repo_names.json', 'r'))
    for tool in tool_config:
        user = tool['user']
        repo = tool['repo']
        file_pattern = tool['file_pattern']
        uncompress_cmd = tool['uncompress_cmd']
        uncompress_flags = ''
        if 'uncompress_flags' in tool:
            uncompress_flags = tool['uncompress_flags']
        remove_v = False
        if "remove_v" in tool:
            remove_v = True

        url, tag, filename = get_url(user, repo, file_pattern, remove_v=remove_v)
        if dry_run:
            print (url)
            continue

        full_filename = output + '/' + filename
        subprocess.check_output(['wget', '-P', output, url])
        if download_only:
            continue

        os.chdir(output)
        if 'uncompress' in tool:
            if uncompress_flags:
                subprocess.check_output([uncompress_cmd, uncompress_flags, full_filename])
            else:
                subprocess.check_output([uncompress_cmd, full_filename])
        if 'bin_dir_pattern' in tool:
            bin_path = tool['bin_dir_pattern'].replace('###',tag)
            bin_path = output + '/' + bin_path
            if 'copy_to_bin' not in tool:
                paths_to_append.append('export PATH='+bin_path+':$PATH')
            else:
                subprocess.check_output(['cp',bin_path+'/'+tool['name'],os.path.expanduser('~') + '/' + 'bin'])

    print('All files downloaded... Add below paths to PATH')
    with open(paths, "a") as paths_file:
        paths_file.write('\n'.join(paths_to_append))

if __name__ == '__main__':
    main()
