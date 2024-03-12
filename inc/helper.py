from pytube.exceptions import PytubeError

# import subprocess
from pathvalidate import sanitize_filename
import emoji
from icecream import ic

import traceback
import os
import re

class AgeRestrictionError(PytubeError):
    def __init__(message):
        super().__init__(message)

class UnavailableError(PytubeError):
    def __init__(message):
        super().__init__(message)

def dump(obj, i=1):
    s = "-" * i
    i = i + 1
    for attr in dir(obj):
        print(f"{s} obj.%s = %r" % (attr, getattr(obj, attr)))
        # print(type(obj), type(object))
        if type(obj) is object:
            dump(obj, i)


# for more: https://stackoverflow.com/a/59672132/2269902
def slugify(filepath, no_emoji=True):
    filepath = str(filepath.replace('  ', ''))
    
    clean_filepath = sanitize_filename(filepath)
    if no_emoji:
        return deEmojify(clean_filepath)
    return clean_filepath


def deEmojify(text):
    return emoji.replace_emoji(text, replace='')

    
# https://stackoverflow.com/a/49986645/2269902
# https://gist.github.com/n1n9-jp/5857d7725f3b14cbc8ec3e878e4307ce
def __deEmojify(text):
    
    emoji_pattern = re.compile("["
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # chinese char       
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"        
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"                
        u"\u2640-\u2642"
        u"\u2600-\u2B55"        
            "]+", flags = re.UNICODE)

    return emoji_pattern.sub(r'', text)
# ----------------------------------------------------------------------------


def show_error(e):
    # traceback.print_exc()
    file = traceback.extract_tb(e.__traceback__)[-1].filename
    line_number = traceback.extract_tb(e.__traceback__)[-1].lineno
    code = traceback.extract_tb(e.__traceback__)[-1].line
    col_no = traceback.extract_tb(e.__traceback__)[-1].colno
    func = traceback.extract_tb(e.__traceback__)[-1].name
    print(f"Exception occurred on {file}:{line_number}")
    print(f"Col Number: {col_no}")
    print(f"Code: {code}")
    print(f"Function: {func}")
    print('--------------------')
    print(repr(e))
    ic(traceback.extract_tb(e.__traceback__))
    ic(e)
    # Messagebox.ok(str(e), title="Error", alert=True, padding=(25, 25))
    # dump(traceback.extract_tb(e.__traceback__)[-1])


# ----------------------------------------------------------------------------
def close_process(window_title):
    cmd = f'TASKKILL /F /FI "WINDOWTITLE eq {window_title}" /IM explorer.exe"'
    subprocess.Popen(cmd)

# ----------------------------------------------------------------------------
def close_window(path, is_file=False):
    # parent_path = get_parent_path(path)
    # window_title = get_dir_name(parent_path)
    if is_file:
        window_title = path.split("/")[-2]
    else:
        window_title = path.split("/")[-1]
    # print('window_title:', window_title)
    close_process(window_title)
# ----------------------------------------------------------------------------
def explore_file(path):
    if os.path.isfile(path):
        close_window(path, True)
        cmd = f'explorer.exe /select,"%s"'
        path = os.path.realpath(path)
        subprocess.Popen(cmd % path)
    else:
        raise Exception(f"File '{path}' is not exist")
# ----------------------------------------------------------------------------
def explore_folder(path):
    cmd = f'explorer.exe "%s"'
    
    if os.path.isdir(path):
        close_window(path)
        path = os.path.realpath(path)
        subprocess.Popen(cmd % path)
    else:
        raise Exception(f"Directory '{path}' is not exist")

# path = self.config.get('MAIN', 'downloads_dir')
# ----------------------------------------------------------------------------
def bool(string: str):
    if str(string).lower() == 'true':
        return True
    
    return False
# ----------------------------------------------------------------------------    
def list_middle(input_list):
    middle = float(len(input_list))/2
    if middle % 2 != 0:
        return input_list[int(middle - .5)]
    else:
        return (input_list[int(middle)], input_list[int(middle-1)])

# ----------------------------------------------------------------------------            
