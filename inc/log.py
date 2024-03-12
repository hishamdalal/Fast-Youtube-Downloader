
def line(title, message):
    print(f'{str(title)+":":20}{str(message)}')
# ----------------------------------------------------------------------------
def separator(char="=", size=60):
    chr = char * size
    print(chr + "\n")
# ----------------------------------------------------------------------------            
def text_separator(text='', char="=", size=50):
    chr = char * size
    print(f'{str(text)+":":20}{chr}\n')
# ----------------------------------------------------------------------------            
def msg(message):
    print(f'{str(message)}')

# ----------------------------------------------------------------------------            