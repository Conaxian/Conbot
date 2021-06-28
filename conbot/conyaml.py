### Imports

# Dependencies
from ruamel.yaml import YAML

# Conbot Modules
import const
from cbcollections import AttrDict

### Initialization

# Create a YAML parser
yaml = YAML(typ="safe")
yaml.default_flow_style = False

### Function Definitions

# Load YAML
def load_yaml(filename: str) -> dict:
    """
    Loads YAML data from a file.
    """
    data = cache.get(filename, None)
    if data == None:
        with open(filename, "a+", encoding=const.encoding) as file:
            file.seek(0)
            data = yaml.load(file) or {}
            cache[filename] = data
    return data

# Save YAML
def save_yaml(filename: str, data: dict):
    """
    Saves YAML data to a file.
    """
    cache[filename] = data
    with open(filename, "w", encoding=const.encoding) as file:
        yaml.dump(data, file)

# Load Conbot data
def read_data(path: str):
    """
    Reads Conbot data from the specified path in the
    YAML file defined in `const.data_file`.
    """
    data = load_yaml(const.data_file)
    for node in path.split("/"):
        data = data.get(node, {})
    if isinstance(data, dict):
        data = {str(key):value for key, value in data.items()}
        return AttrDict(**data)
    else: return data

# Save Conbot data
def write_data(path: str, new):
    """
    Writes Conbot data to the specified path in the
    YAML file defined in `const.data_file`.
    """
    data = load_yaml(const.data_file)
    original_data = data
    nodes = path.split("/")
    if isinstance(new, AttrDict): new = dict(iter(new))
    for node in nodes:
        if node != nodes[-1]:
            try:
                data = data[node]
            except KeyError:
                data[node] = {}
                data = data[node]
        else:
            data[node] = new
    save_yaml(const.data_file, original_data)

### Initialization

# Cache all loaded files
cache = {}
