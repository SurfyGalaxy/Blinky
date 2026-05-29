import requests
import datetime
import json
import os

# Global variables
total_time = 0
names = []
scope = []
new = None
loaded = False
username = None
target = None
start_days = None
days_left = None
delta = None
time_daily = None
percent_done = None
stats = None
file = None
response = None

def load_ysws():
    global stats, file, target, username, start_days, scope, loaded
    looping = True
    while looping:
        file_input = input("Load an existing YSWS profile? (Enter a YSWS name, or press Enter to skip): ")
        
        if file_input == "":
            return False
        
        file = f"{file_input.lower().replace(' ', '_')}_config.json"
        
        if file in os.listdir():
            with open(file, 'r') as f:
                loaded_data = json.load(f)
                username = loaded_data["username"]
                target = loaded_data["target_hours"] * 3600
                start_days = loaded_data["days"]
                scope = loaded_data["projects"]

            response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")
            api_data = response.json()
            stats = api_data["data"]
            loaded = True
            return True
        else:
            print("Invalid YSWS name. Did you save it last time, or misspell it?")
    return False

def init_ysws():
    global stats, loaded, username, target, response
    if not loaded:
        looping = True
        while looping:
            username = input("Who's stats are we using here? ")
            response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")
            if response.status_code == 404:
                print("User not found")
            else:
                looping = False
        target = int(input("How many hours is the YSWS requiring? ")) * 3600
        if response.status_code == 200:
            data = response.json()
            stats = data["data"]

def update_days():
    global stats, days_left, names
    names = []  # Reset names
    for proj in stats["projects"]:
        if proj["total_seconds"] != 0:
            names.append(proj["name"])
    days_left = int(input("How many days left do you have? "))

def edit_projects():
    global scope, names
    looping = True
    while looping:
        available_projects = [proj for proj in names if proj not in scope]
        new = input(f"""Which projects are you adding? Or type 'exit' to proceed, or 'remove' to remove a project added earlier.
        Available projects: {available_projects}, Added projects: {scope} \n""")

        if new not in ["exit", "remove"]:
            if new in names:
                if new not in scope:
                    scope.append(new)
                    print(f"Added {new}! New scope: {scope}")
                else:
                    print(f"Project {new} already in scope! Current scope: {scope}")
            else:
                print(f"{new} doesn't seem to be a project")
        elif new == "exit":
            looping = False
        elif new == "remove":
            remove_item = input(f"Which item would you like removed: {scope}")
            if remove_item in scope:
                scope.remove(remove_item)
                print(f"Removed {remove_item}!")
            else:
                print(f"{remove_item} Doesn't seem to be in scope")

def calculate_stats():
    global stats, target, delta, total_time, percent_done, time_daily, days_left, scope
    total_time = 0
    for proj in stats['projects']:
        if proj["name"] in scope:
            total_time += proj["total_seconds"]
            print(f"Added {proj["name"]}, new total: {total_time} seconds")
    delta = target - total_time
    time_daily = delta / days_left
    percent_done = (total_time / target) * 100

def print_stats():
    global total_time, target, delta, time_daily, percent_done
    print(f"\nBanked time: {datetime.timedelta(seconds=int(total_time))}")
    print(f"Target time: {datetime.timedelta(seconds=int(target))}")
    print(f"Time left: {datetime.timedelta(seconds=int(delta))}")
    print(f"Required Daily code time: {datetime.timedelta(seconds=int(time_daily))}")
    print(f"Percent complete: {round(percent_done)}%")

def save_ysws():
    global file, loaded, days_left, username, target, scope, start_days
    if input("\nDo you want me to save/update these settings? (True/False): ") == "True":
        if not loaded:
            ysws_name = input("\nWhat's the name of this YSWS? ")
            start_days_input = input(f"How many days did you have when starting? (Enter to use {days_left}): ")
            start_days = int(start_days_input) if start_days_input else days_left
            filename = f"{ysws_name.lower().replace(' ', '_')}_config.json"
        else:
            filename = file
        
        save_data = {
            "username": username,
            "target_hours": target // 3600,
            "days": start_days,
            "projects": scope
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"\nSaved as {filename}")

# Main execution
if __name__ == "__main__":
    load_ysws()
    init_ysws()
    update_days()
    edit_projects()
    calculate_stats()
    print_stats()
    save_ysws()