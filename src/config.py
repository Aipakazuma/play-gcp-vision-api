import yaml

config = None
with open('./config.yml', 'r') as f:
    config = yaml.load(f)

assert config is not None, 'Create yaml file.'
