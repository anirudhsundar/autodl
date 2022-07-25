from pathlib import Path

def get_root_dir():
    return Path(__file__).parent

def get_config_path():
    ROOT_DIR = get_root_dir()
    return Path(Path(ROOT_DIR)/'repo_names.json')

def get_schema_path():
    ROOT_DIR = get_root_dir()
    return Path(Path(ROOT_DIR)/'repo_names.schema.json')
