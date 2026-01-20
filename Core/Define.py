import rich, time
from typing import Any
from exceptiongroup import (print_exception)
import platform, os

class BreakException(Exception):
    pass

def slowprint(text: str):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

def error(exception: Exception | Any, content: str):
    rich.print(f"[bold red][ ERROR ][/bold red]", end = "")
    rich.print(" Failed to execute command. \n          For more information, please see informations under.")
    if type(exception) == Any:
        rich.print(f"    {content}")
    else:
        print_exception(exception, file=open("./errors.log", "r+"))

def hard_clear():
    """强制执行系统级清屏命令"""
    # Windows
    if platform.system() == "Windows":
        os.system('cls')
    # Linux / macOS
    else:
        os.system('clear')