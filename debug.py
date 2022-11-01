from colorama import Fore, Back, Style

DEBUG=99 # Debug Level - The higher the number the debug msges


def dprint(msg, d_lvl:int = 1):
    if DEBUG >= d_lvl:
        print(Back.YELLOW + Fore.BLACK + f"DEBUG: {msg}" + Fore.RESET + Back.RESET)

def eprint(msg):
    print(Back.RED + Fore.BLACK + f"DEBUG: {msg}" + Fore.RESET + Back.RESET)
