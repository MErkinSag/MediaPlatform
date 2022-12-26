from pathlib import Path
import yaml


class Config:
    def __init__(self, config_file: str):
        self.config = self.load_config(file_name=config_file)

    def __call__(self):
        return self.config

    @staticmethod
    def load_config(file_name):

        # Set project path as two levels top
        project_root = Path(__file__).resolve().parents[1]

        config_file = project_root / 'config' / file_name

        if not config_file.exists():
            raise FileNotFoundError(f'{file_name} config file does not exists')

        with open(config_file, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exception:
                raise exception

        return config
