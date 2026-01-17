import rich
from rich.console import Console
from Define import *
from Framework import *
from PluginManager import *
from exceptiongroup import (print_exception)

"""
Zebraith SHELL.

A plugin-based shell.
VER. 1

>>> ./zebraith.bat
"""

#region VARS

console = Console()
print = console.print
plugins = PluginManager()
nowDirectory = "~"
cparser = CommandParser()

VERSION = "1.0.0"

#endregion

#region MAIN LOGIC
print("Zebraith SHELL.")
slowprint("VERSION, " + VERSION)
slowprint("Initializing...\n")

slowprint("    + Loading base plugins...")
slowprint("        - Plugin 'BaseCommands', Author 'BL.BlueLighting' Loaded.")
slowprint("        - Plugin 'DebuggingCommands', Author 'BL.BlueLighting' Loaded.")
slowprint("    + Base plugins load finished.")

print("")

slowprint("    + Loading custom plugins...")
plugins.load_all_plugins()
slowprint("    + Custom plugins load finished.")

print("")

print("Welcome to Zebraith SHELL.")
time.sleep(0.5)

open("./errors.log", "w").write("")

console.clear()

print("Zebraith SHELL, Version " + VERSION)
print(f"    - Loaded {len(plugins.loaded_plugins) + 2} plugins.")
if len(plugins.failed_plugins_file_list) > 0:
    print(f"        \\ Failed to load {len(plugins.failed_plugins_file_list)} plugins. \n        \\ Use 'plugin list failed' to list all failed plugins.")

print("")

while True:
    try:
        command: str = input(f"user@zebraith:{nowDirectory}$ ")
        cparser.parse(command).Eval(Commands)
    except KeyboardInterrupt:
        print("\n    Goodbye.")
        break
    except Exception as e:
        print(f'[bold red][ ERROR ][/bold red] Failed to run command {command}') #type: ignore
        print(f"[bold red][ ERROR ][/bold red] 'Cause an unexcepted exception occur.") #type: ignore
        print(f"[bold red][ ERROR ][/bold red] ")
        print(f"[bold red][ ERROR ][/bold red] This exception has been record in ./errors.log.")
        print(f"[bold red][ ERROR ][/bold red] Please contact to plugin developer.")
        print_exception(e, file=open("./errors.log", "r+"))


#endregion