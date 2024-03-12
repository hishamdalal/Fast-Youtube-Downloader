import winreg
import os
from pathlib import Path

# ----------------------------------------------------------------------------
# https://stackoverflow.com/a/75807211/2269902
def get_downloads_path():
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")

    downloads_path = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]

    winreg.CloseKey(reg_key)

    return(downloads_path)

# ----------------------------------------------------------------------------
def is_valid_path(path, is_dir=False):
    # print('path:::', path, is_dir)
    if path:
        if is_dir and Path(path).is_dir():
            return True
        elif Path(path).is_file():
            return True
    else:
        return False
# ----------------------------------------------------------------------------
