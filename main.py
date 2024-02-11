import os
import time
import sqlite3
import traceback
from utils import *
main_ver=(1,0,0)
print("""

  _                _                  _                    _  ____ _     ___    
 | |    ___   ___ | | ___   _ _ __   | |    ___   ___ __ _| |/ ___| |   |_ _|   
 | |   / _ \ / _ \| |/ / | | | '_ \  | |   / _ \ / __/ _` | | |   | |    | |    
 | |__| (_) | (_) |   <| |_| | |_) | | |__| (_) | (_| (_| | | |___| |___ | |    
 |_____\___/ \___/|_|\_\\\\__,_| .__/  |_____\___/ \___\__,_|_|\____|_____|___|   
                             |_|                                                

Ver. 1.0.0 By @0x24a
                                       
""")
if os.path.exists("repo.txt"):
    with open("repo.txt","r") as f:
        repo_url=f.read().strip()
else:
    print("fatal: repo.txt not found.")
    exit()

if not os.path.exists("database.db"):
    print("Checking database...")
    print("Database not found, downloading...")
    stream_download(repo_url,"database.db")
    print("Database downloaded!")

print("\nDatabase Status Report:")
print(f"\tDatabase Size: {os.path.getsize('database.db')/1024/1024:.2f} MB")
print(f"\tDatabase Downloaded At: {time.ctime(os.path.getmtime('database.db'))}")
connection=sqlite3.connect("database.db")
cursor=connection.cursor()
print(f"\tDatabase Message Count: {cursor.execute('SELECT id from chat;').fetchall()[-1][0]+1}")
connection.close()

print("\nIniting database connection... ",end="",flush=True)
connection=sqlite3.connect("database.db")
print("Connected!")
print("Loading actions...")
plugins={}
registereds=[]
for module in os.listdir("plugins"):
    if module.endswith(".py") and os.path.isfile(f"plugins/{module}") and module != "__init__.py":
        try:
            m=__import__("plugins."+module[:-3]).__dict__[module[:-3]]
            if m.plugin['name'] in plugins:
                print(f"Plugin {module[:-3]} already registered! Skipping...")
            if m.plugin['required_version'] > main_ver:
                print(f"Plugin '{module[:-3]}' requires a newer version of the main program{m.plugin['required_version']}! Skipping...")
            else:
                plugins[m.plugin['name']]=m.plugin
                registereds.append(module[:-3])
        except Exception as e:
            print(f"Error loading plugin '{module[:-3]}': {e}, Skipping...")
print(f"Loaded {len(plugins)} actions: {', '.join(registereds)}")

print()
print("Type 'help' for information of commands.")
print()
while True:
    try:
        command=input("lookup> ")
        command_name=command.split(" ")[0]
        args=" ".join(command.split(" ")[1:])
        if command_name == "update":
            connection.close()
            print("Updating database...")
            stream_download(repo_url,"database.db")
            print("Database updated, reloading connection...")
            connection=sqlite3.connect("database.db")
            print()
        elif command_name == "help":
            result="Available commands:\n"
            result+=f"help\t-\tShows this message\nupdate\t-\tUpdates the database\nexit\t-\tExits the program\n"
            for plugin in plugins.values():
                result+=f"{plugin['name']}\t-\t{plugin['info']}\n"
            print(result)
        elif command_name == "exit":
            print("Cleaning up")
            connection.close()
            break
        elif command_name in plugins:
            plugins[command_name]["main"](connection,args)
        else:
            print("Invalid command!")
    except KeyboardInterrupt:
        print("Exiting...")
        connection.close()
        break
    except Exception as e:
        print(f"Error when executing command: ")
        traceback.print_exc()
        print()