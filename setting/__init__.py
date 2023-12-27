import yaml


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.data = None

    def read(self):
        self.data = yaml.safe_load(open(self.config_file, 'r'))

    def write(self):
        data = {
            "Lock_screen_password": '1324',
            "Password_validity_period": 600,
            "Baidu_Translate_appid": '',
            "Baidu_Translate_appkey": ''

        }

        with open(self.config_file, 'w') as f:
            yaml.dump(data, f)


if __name__ == '__main__':
    config = Config('../config.yaml')
    config.write()
