from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
just_fix_windows_console()


def line(title, message):
    custom(title, message, Fore.CYAN, Fore.WHITE)
# ----------------------------------------------------------------------------
def error(message):
    custom('Error', message, Fore.RED, Fore.MAGENTA)
# ----------------------------------------------------------------------------
def info(message):
    custom('Info', message, Fore.YELLOW, Fore.CYAN)
# ----------------------------------------------------------------------------
def custom(title, message, title_color=Fore.YELLOW, message_color=Fore.WHITE):
    print(f'{Fore.YELLOW}{title+":":20}{message_color}{str(message)}')
    Fore.RESET
# ----------------------------------------------------------------------------
def separator(char="=", size=70):
    print(Fore.MAGENTA)
    chr = char * size
    # print(chr + "\n")
    print(chr, Fore.RESET)
# ----------------------------------------------------------------------------            
def text_separator(text='', char="=", size=50):
    chr = char * size
    print(f'{Fore.YELLOW}{str(text)+":":20}{Fore.BLUE}{chr}\n')
    Fore.RESET
# ----------------------------------------------------------------------------            
def msg(message, color=Fore.GREEN):
    print(f'{color}{str(message)}')
    Fore.RESET
# ----------------------------------------------------------------------------            
