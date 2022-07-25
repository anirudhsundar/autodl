## Automatically download latest github releases

This is a short script to automatically download the latest releases of certain tools (which are listed in repo_names.json).

### Quickstart guide

**Requirements**
- python3+

Installation is as simple as
`pip install -U git+https://github.com/anirudhsundar/autodl.git`

Just run `python -m autodl.autodl` inside the autodl directory to download the files into the current directory. It also extracts the files and adds the `export` commands for the `PATH` to the `~/.local_paths` file. So, just add `source ~/.local_paths` to your bashrc/zshrc/cshrc

For a list of the different options try `python autodl.py -h` to the help.

### How it works
The `autodl.py` script automatically fetches the tag of the latest release for the repos listed in `repo_names.json` and then downloads the linux-x86/64 version of the release.

#### repo_names.json format

This json file just contains a list of json objects/dictionaries where each object is of the format:

```javascript
    {
        "name": "gh", // Name of the final binary
        "user": "cli", // The user/organization part of github url
        "repo": "cli", // The repository part of github url
        "file_pattern": "gh_###_linux_amd64.tar.gz", // The filename to be downloaded with ### replacing the version
        "tag_replace": ["v",""], // if the version tag contains a v, but the filename does not, this should be true
        "bin_dir_pattern": "gh_###_linux_amd64/bin", // the directory structure to bin, created after uncompressing
        "uncompress_cmd": "tar", // uncompression command to be used based on the file type
        "uncompress_flags": "zxf", // Any extra uncompression flags to be used
        "uncompress": true // decided if uncompression should be done
    }
```
