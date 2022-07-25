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

#### repo_names.json documentation

There is a simple [Markdown documentation](docs/markdown/repo_names_documentation.md)

or if you prefer an [interactive HTML version](https://htmlpreview.github.io/?https://github.com/anirudhsundar/autodl/blob/main/docs/html/repo_names_documentation.html)
