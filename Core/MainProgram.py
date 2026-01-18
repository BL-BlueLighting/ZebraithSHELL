import rich
from rich.console import Console
from Define import *
from Framework import *
from PluginManager import *
from exceptiongroup import (print_exception)
import Core.PluginInstaller as pi

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

if not (os.path.exists("./skipload")):

    print(open("./logo.txt", "r").read())
    slowprint("VERSION, " + VERSION)
    slowprint("Initializing...\n")

    slowprint("    + Loading base plugins...")
    slowprint("        - Plugin 'BaseCommands', Author 'BL.BlueLighting' Loaded.")
    slowprint("        - Plugin 'Zebraith Package Manager', Author 'BL.BlueLighting' Loaded.")
    slowprint("    + Base plugins load finished.")

    print("")

    slowprint("    + Loading custom plugins...")
    plugins.load_all_plugins()
    slowprint("    + Custom plugins load finished.")

    print("")

    print("Welcome to Zebraith SHELL.")
    time.sleep(0.5)

else:
    plugins.load_all_plugins(skipload=True)

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

@register_command("version", [])
def version():
    print(open("./logo.txt", "r").read())
    slowprint("VERSION " + VERSION)
    slowprint("Made by BL.BlueLighting with ❤️")

@register_command("logostyle", ["style"])
def logostyle(style: CommandAPI):
    style = style.GetArg('style')
    if style in ["1", "2", "3", "4", "5", "6"]:
        open("./logo.txt", "w").write(open(f"./logos/logo_style{style}.txt").read())
        print(f"Logo style has been changed to {style}.")
    else:
        print(f"Logo style {style} is not found.")

@register_command("clear", [])
def clear(api):
    hard_clear()

@register_command("clearAgain", [])
def clearAgain(api):
    hard_clear()
    print(open("./logo.txt", "r").read())
    print("VERSION " + VERSION + "\n")
    print(f"    - Loaded {len(plugins.loaded_plugins) + 2} plugins.")
    if len(plugins.failed_plugins_file_list) > 0:
        print(f"        \\ Failed to load {len(plugins.failed_plugins_file_list)} plugins. \n        \\ Use 'plugin list failed' to list all failed plugins.")

@register_command("reboot", [])
def reboot(api):
    print("Rebooting...")
    time.sleep(0.5)
    hard_clear()
    os.system("python MainProgram.py")
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