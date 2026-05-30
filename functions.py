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
days_left = None  # Added this
delta = None
time_daily = None
percent_done = None
stats = None
file = None
response = None

def set_days_left(days):
    global days_left
    days_left = int(days)

def load_ysws(file_input):
    global stats, file, target, start_days, scope, loaded
    file = f"{file_input.lower().replace(' ', '_')}.json"
    
    if file in os.listdir():
        with open(file, 'r') as f:
            loaded_data = json.load(f)
            username = loaded_data["username"]
            target = loaded_data["target_hours"] * 3600
            start_days = loaded_data["days"]
            scope = loaded_data["projects"]
            print("Loaded")

        response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")
        print(response)
        if response.status_code == 200:
            api_data = response.json()
            stats = api_data["data"]
            print(f"stats: {stats}")
            loaded = True
            init_project_list()
            return True
    return False

def init_ysws(username, target_hours):
    global stats, loaded, response, target, scope, global_username
    global_username = username
    response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")
    if response.status_code == 404:
        return False
    
    data = response.json()
    stats = data["data"]
    target = int(target_hours) * 3600
    scope = []
    return True

def init_project_list():
    global stats, names
    names = []
    if stats and "projects" in stats:
        for proj in stats["projects"]:
            if proj["total_seconds"] != 0:
                names.append(proj["name"])

def calculate_stats(days_left, days_ago, start_days):
    global stats, target, delta, total_time, percent_done, time_daily, scope, average_rate

    if days_left == "":
        days_left = 1
    else:
        days_left = int(days_left)
    
    if days_ago == "":
        try:
            start_days = int(start_days)
        except ValueError:
            return False
        days_ago = start_days - days_left
    
    if start_days == "":
        try:
            start_days = int(start_days)
        except ValueError:
            return False
        start_days = days_ago + days_left

    total_time = 0
    for proj in stats['projects']:
        if proj["name"] in scope:
            total_time += proj["total_seconds"]
    
    delta = target - total_time
    print(days_left)
    if days_left and days_left > 0:
        time_daily = delta / days_left
    else:
        time_daily = 0
    percent_done = (total_time / target) * 100 if target > 0 else 0
    average_rate = total_time / start_days

def save_ysws(start_days, ysws_name):
    global file, loaded, global_username, target, scope
    if loaded: # Updating a profile that already exists
        os.remove(file)
        print("Here")
    else:
        file = ysws_name.replace(" ", "_")
        file = file.lower()
        file = file + ".json"
        print(file)
    
    save_data = {
        "username": global_username,
        "target_hours": target // 3600,
        "days": int(start_days),
        "projects": scope
    }
    
    with open(file, 'w') as f:
        json.dump(save_data, f, indent=2)
    return True