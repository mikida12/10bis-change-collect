import yaml


def get_configurations():
    config = {}
    with open("configurations.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            print(config)
        except yaml.YAMLError as exc:
            print(f"error parsing configurations file - {exc}")
    return config


def validate_configurations(cofig_data):
    return True
