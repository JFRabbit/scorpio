import yaml


def load_yaml(path):
    with open(path, encoding='utf-8') as f:
        return yaml.load(f)
