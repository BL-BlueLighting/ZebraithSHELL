import rich
from rich.console import Console
from Define import *
from Framework import *
from PluginManager import *
from exceptiongroup import (print_exception)
import PluginInstaller as pi

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

VERSION = "1.3.0"

#endregion

#region MAIN LOGIC

hard_clear()

if not (os.path.exists("./skipload")):

    print(open("./logo.txt", "r").read())
    slowprint("Version " + VERSION)
    slowprint("Initializing...\n")

    slowprint("    + Loading base plugins...")
    slowprint("        :: Plugin 'BaseCommands', Author 'BL.BlueLighting' Loaded.")
    slowprint("        :: Plugin 'Zebraith Package Manager', Author 'BL.BlueLighting' Loaded.")
    slowprint("    + Base plugins load finished.")

    print("")

    slowprint("    + Loading custom plugins...")
    plugins.LoadAllPlugins()
    slowprint("    + Custom plugins load finished.")

    print("")

    print("Welcome to Zebraith SHELL.")
    time.sleep(0.5)

else:
    plugins.LoadAllPlugins(skipload=True)

open("./errors.log", "w").write("")

hard_clear()

print(open("./logo.txt", "r").read())
print("VERSION " + VERSION + "\n")
print(f"    - Loaded {len(plugins.loaded_plugins) + 2} plugins.")
if len(plugins.failed_plugins_file_list) > 0:
    print(f"        \\ Failed to load {len(plugins.failed_plugins_file_list)} plugins. \n        \\ Use 'plugin list failed' to list all failed plugins.")

# initialize pi
zpm = pi.PluginInstaller(Commands, plugins)
zpm.register_all()

@RegisterCommand("version", [])
def version():
    print(open("./logo.txt", "r").read())
    slowprint("VERSION " + VERSION)
    slowprint("Made by BL.BlueLighting with ❤️")

@RegisterCommand("logostyle", ["style"])
def logostyle(style: CommandAPI):
    style = style.GetArg('style')
    if style in ["1", "2", "3", "4", "5", "6"]:
        open("./logo.txt", "w").write(open(f"./logos/logo_style{style}.txt").read())
        print(f"Logo style has been changed to {style}.")
    else:
        print(f"Logo style {style} is not found.")

@RegisterCommand("clear", [])
def clear(api):
    hard_clear()

@RegisterCommand("clearAgain", [])
def clearAgain(api):
    hard_clear()
    print(open("./logo.txt", "r").read())
    print("VERSION " + VERSION + "\n")
    print(f"    - Loaded {len(plugins.loaded_plugins) + 2} plugins.")
    if len(plugins.failed_plugins_file_list) > 0:
        print(f"        \\ Failed to load {len(plugins.failed_plugins_file_list)} plugins. \n        \\ Use 'plugin list failed' to list all failed plugins.")

@RegisterCommand("reboot", [])
def reboot(api):
    print("Rebooting...")
    time.sleep(0.5)
    hard_clear()
    is3 = ""
    if platform.system() != "Windows":
        is3 = "3"
    os.system(f"python{is3} ./Core/MainProgram.py") # 对 linux 添加 python -> python3
    exit()

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