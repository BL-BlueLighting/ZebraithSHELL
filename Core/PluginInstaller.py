from Framework import *
from Define import *
from PluginManager import *
import requests

rprint = print
print = rich.print

PIVERSION = "1.0.0"
PILOGO = """ __ ___ __  __  _  ____       __  _   _      _   __ ___        _       _   __ ___ __  
 _/(_  / _)/__)/_| //  )__/  /__)/_| / )/__//_| / _(_    /|/| /_| /| )/_| / _(_  /__) 
/__/__/(_)/ ( (  |((  /  /  /   (  |(__/  )(  |(__)/__  /   |(  |/ |/(  |(__)/__/ (   
                                                                                      """

class PluginInstaller:

    def __init__(self, command: dict, plugins:PluginManager):
        self.command = command
        self.source = "https://zebraith.latingtude-studios.icu/"
        self.query_path = "query.php?query="
        self.plugins = plugins
    
    def register_all(self):
        @register_command("zpm", ["action", "more1", "more2", "more3"], self.command)
        def zpm_action(args: CommandAPI):
            rprint(PILOGO)
            print("[cyan]ZEBRAITH[/cyan] Package Manager")
            print("[cyan]Version[/cyan]: [green]{}[/green]".format(PIVERSION))
            print("")

            act = args.GetArg("action", "[default]")
            m1 = args.GetArg("more1", "[default]")
            m2 = args.GetArg("more2", "[default]")
            m3 = args.GetArg("more3", "[default]")

            if act == "help" or act == "":
                print("Zabraith Package Manager Help")
                print("Install plugin:")
                print("    - zpm install <plugin_name>")
                print("    (Once set source) zpm install <plugin_name> src <plugin_source>")
                print("")
                print("More action:")
                print("    - zpm list: List all plugins")
                print("    - zpm remove <plugin_name>: Remove plugin")
                print("    - zpm update: Update all plugins")
                return 0
            
            elif act == "install":
                if m1 == "[default]":
                    print("::  Please enter a plugin name.")
                    return 0
                
                if m2 == "[default]":
                    # normal install
                    print(":: Querying source " + self.source + "...")
                    try:
                        r = requests.get(self.source + self.query_path + m1)
                        r = r.json()
                        results = r["data"]
                        plugin = ""

                        if len(results) > 1:
                            print(f":: Found {len(results)} plugins.\n")
                            print(f":: Choice a plugin to install.")
                            for i in range(len(results)):
                                print(f"    {i + 1}. {results[i]['name']} - {results[i]['version']}")
                            print("")
                            choice = input(":: Choice a plugin: ")
                            choice = int(choice)
                            if choice > len(results) or choice < 1:
                                print(":: Invalid choice.")
                                return 0
                            plugin = results[choice - 1]

                        else:
                            plugin = results[0]
                            print(f":: Found {len(results)} plugin.")
                            print(f":: Plugin {plugin} will be install after you entered.\n")
                        
                        print(":: Begin installation?", end=" ")
                        yn = input("[y/N] ").lower()
                        if yn == "y":
                            print("\n:: Installing...")
                            try:
                                r = requests.get(self.source + plugin)
                                r = r.text
                                with open("." + plugin, "w") as f: # 一般来讲，plugin = plugins/xxx.zshellext
                                    f.write(r)
                                print(f":: Plugin {plugin} installed.")
                                print(f"\n:: Loading {plugin}...")

                                self.plugins.LoadPluginFromFile(plugin, False)
                                print(f":: Plugin {plugin} loaded.")
                            except Exception as e:
                                print(f"\n:: Failed to install plugin {plugin}. Please try again later.")
                                print_exception(e, file=open("./errors.log", "a"))
                                return 0
                        else:
                            print("\n:: Install canceled.")
                            return 0

                    except:
                        print(":: Failed to query source. Please check your network connection.")
                        return 0
                
                elif m2 == "src":
                    if m3 == "[default]":
                        print(":: Please enter a plugin source.")

                    else:
                        print(":: Querying source " + m3 + "...")
                        try:
                            r = requests.get(m3 + self.query_path + m1)
                            r = r.json()
                            results = r["data"]
                            plugin = ""

                            if len(results) > 1:
                                print(f":: Found {len(results)} plugins.")
                                print(f":: Choice a plugin to install.")
                                for i in range(len(results)):
                                    print(f"    {i + 1}. {results[i]['name']} - {results[i]['version']}")
                                print("")
                                choice = input(":: Choice a plugin: ")
                                choice = int(choice)
                                if choice > len(results) or choice < 1:
                                    print(":: Invalid choice.")
                                    return 0
                                plugin = results[choice - 1]
                            else:
                                plugin = results[0]
                                print(f":: Found {len(results)} plugin.")
                                print(f":: Install {plugin['name']} - {plugin['version']}")

                            print(":: Begin installation?")
                            yn = input("[y/N] ").lower()
                            if yn == "y":
                                print(":: Installing...")
                                try:
                                    r = requests.get(m3 + plugin)
                                    r = r.text
                                    with open(plugin, "w") as f: # 一般来讲，plugin = plugins/xxx.zshellext
                                        f.write(r)
                                    print(f":: Plugin {plugin} installed.")
                                except:
                                    print(f":: Failed to install plugin {plugin}. Please try again later.")
                                    return 0
                            else:
                                print(":: Install canceled.")
                                return 0
                        except:
                            print(":: Failed to query source. Please check your network connection or custom source right.")
                            return 0
                        
                
            elif act == "list":
                print(":: Listing plugins local...")
                for i in os.listdir("plugins"):
                    print(f"    - {i}")
            
            elif act == "update":
                print(":: Updating plugins...")
                for i in os.listdir("plugins"):
                    print(f":: Updating {i}...")
                    try:
                        r = requests.get(self.source + i)
                        r = r.text
                        with open("plugins/" + i, "w") as f:
                            f.write(r)
                        print(f":: Plugin {i} updated.")
                    except:
                        print(f":: Failed to update plugin {i}. Please try again later.")
            
            elif act == "remove":
                if m1 == "":
                    print(":: Please enter a plugin name.")

                else:
                    print(":: Removing plugin " + m1 + "...")
                    try:
                        os.remove("plugins/" + m1)
                        print(":: Plugin " + m1 + " removed.")
                    except:
                        print(":: Failed to remove plugin " + m1 + ". Please check your plugin name.")
            
