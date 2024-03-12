import os
import configparser
import inc.helper as helper


class YPD_Config:
    file = './config.ini'
    config = None
    current = {}
    default =   {'MAIN': {'downloads_dir': '.', 'type': 'ask', 'resolution': 'ask', 'skip_existing': 'True'}, 
                'TRANSLATE': {'download':'ask', 'from': 'en', 'to': 'ar'}
                }

    # ----------------------------------------------------------------------------
    def __init__(self):
        main = self.default['MAIN']
        translate = self.default['TRANSLATE']
        # Create config file for first run
        if not os.path.isfile(self.file):
            try:
                f = open(self.file, "a")
                f.write(f'[MAIN]\n')
                f.write(f'downloads_dir = {main['downloads_dir']}\n')
                f.write(f'type = {main['type']}\n')
                f.write(f'skip_existing = {main['skip_existing']}\n')
                f.write(f'resolution = {main['resolution']}\n')
                f.write(f'[TRANSLATE]\n')
                f.write(f'download = {translate['download']}\n')
                f.write(f'from = {translate['from']}\n')
                f.write(f'to =  {translate['to']}\n')
                f.close()
            except Exception as e:
                helper.show_error(e)
                raise Exception("Couldn't create config file!")
        
        self.read()
    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------
    def save_multi(self, section, data):
        for key, value in data.items():
            self.save(section, key, value)
        
    # ----------------------------------------------------------------------------
    def save(self, section, key, value):
        try:
            self.config.set(section=section, option=key, value=value)
            self.config.write(open(self.file, 'w'))
        except Exception:
            raise Exception("Couldn't save settings")
    # ----------------------------------------------------------------------------
    def save_data(self, section, data):
        try:
            for (k, v) in data:
                self.config.set(section=section, option=k, value=v)
                self.current[section][k] = v

            self.config.write(open(self.file, 'w'))

        except Exception as e:
            helper.show_error(e)
            raise Exception("Couldn't save settings")
    # ----------------------------------------------------------------------------
    def get(self, section, key):
        # refresh config data
        self.config.read(self.file)
        
        if section in self.config:
            if key in self.config[section]:
                return self.config[section][key]
            else:
                raise Exception(f"{key} is not exists!")
                # return self.default[section]

            # raise Exception("{key} is not exists!")
    # ----------------------------------------------------------------------------
    def get_section(self, section):
        return self.config[section]
    # ----------------------------------------------------------------------------
    def read(self):
        self.config = configparser.RawConfigParser()
        self.config.read(self.file)
    # ----------------------------------------------------------------------------
        