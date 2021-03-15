import json
from utils import resource_path

HAO_I = 'haoi'
TWO_CAPTCHA = '2captcha'
NONE = 'none'


def load_config():
    config = None
    try:
        with open(resource_path('config.json')) as f:
            config_json = json.load(f)
            config = Config(config_json)
    except Exception as e:
        config = Config({})
        write_config(config)
    return config


def write_config(config):
    config_json = json.dumps(config.__dict__)
    with open(resource_path("config.json"), 'w') as f:
        f.write(config_json)


class Config:
    def __init__(self, config={}):
        self.screenSize = config.get('screenSize', [470, 850])
        self.method = config.get('method', NONE)
        self.haoiUser = config.get('haoiUser', None)
        self.haoiRebate = config.get('haoiRebate', None)
        self.twocaptchaKey = config.get('twocaptchaKey', None)



global_config = Config()
