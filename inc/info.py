import os

import inc.helper as helper

class Info:
    
    data = {}
    file = ''
    # downloads_dir = ''
    # download_type = ''
    # download_quality = ''
    # download_resolution = ''
    
    # playlist_title = ''
    # playlist_count = 0
    # playlist_details = ''
    # playlist_url = ''
    
    # obj._playlist_id
    # obj._video_url
    # obj._input_url
    # obj.count
    
    # https://pytube.io/en/latest/api.html#playlist-object
    def __init__(self):
        pass
    # ----------------------------------------------------------------------------
    def set_path(self, path):
        self.file = path.strip()
    # ----------------------------------------------------------------------------
    def set(self, key, value):
        self.data[key] = helper.slugify(str(value)).strip()
    # ----------------------------------------------------------------------------
    def get(self, key):
        if key in self.data:
            return self.data[key]
    # ----------------------------------------------------------------------------
    def save(self):
        # print('---> ', self.file)
        if not os.path.isfile(self.file):
            try:
                f = open(self.file, mode="w+", encoding='utf-8', newline="\r\n")
                for key, value in self.data.items():
                    f.write(key +":\t"+value)
                f.close()
            except Exception as e:
                helper.show_error(e)
                raise Exception(f"Couldn't create info file '{self.file}'")
        # else:
        #     print(f'File "{self.file}" is already exists')
    # ----------------------------------------------------------------------------
