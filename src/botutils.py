import re

def CheckCarrierIDPattern(string):
    return re.match(r'^\w{3}-\w{3}$', string)