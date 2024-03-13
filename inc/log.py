from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
just_fix_windows_console()


def line(title, message):
    print(f'{Fore.CYAN}{str(title)+":":20}{Fore.WHITE}{str(message)}{Fore.RESET}')
# ----------------------------------------------------------------------------
def separator(char="=", size=60):
    chr = char * size
    print(chr + "\n")
# ----------------------------------------------------------------------------            
def text_separator(text='', char="=", size=50):
    chr = char * size
    print(f'{Fore.YELLOW}{str(text)+":":20}{Fore.MAGENTA}{chr}\n')
# ----------------------------------------------------------------------------            
def msg(message):
    print(f'{Fore.GREEN}{str(message)}')

# ----------------------------------------------------------------------------            
