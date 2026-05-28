import requests
import datetime
import json
import os

total_time = 0
names = []
scope = []
new = None
looping = True
loaded = False

while looping == True:
    file_input = input("Load an existing YSWS profile? (Enter a YSWS name, or press Enter to skip): ")
    
    if file_input == "":
        looping = False
        break
    
    file = f"{file_input.lower().replace(' ', '_')}_config.json"
    
    if file in os.listdir():
        looping = False
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
    elif file == "_config.json":
        looping = False
    else:
        print("Invalid YSWS name. Did you save it last time, or mispell it?")

if loaded == False:
    looping = True
    while looping == True:
        username = input("Who's stats are we using here? ")
        response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")
        if response.status_code == 404:
            print("User not found")
        else:
            looping = False
    target = int(input("How many hours is the YSWS requiring? "))*3600
    if response.status_code == 200:
        data = response.json()
        stats = data["data"]

for proj in stats["projects"]:
    if proj["total_seconds"] != 0:
        names.append(proj["name"])
days_left = int(input("How many days left do you have? "))

looping = True
while looping == True:
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
    if new == "exit":
        looping = False
    elif new == "remove":
        new = input (f"Which item would you like removed: {scope}")
        if new in scope:
            scope.remove(new)
            print(f"Removed {new}!")
        else:
            print(f"{new} Doesn't seem to be in scope")
        

for proj in stats['projects']:
    if proj["name"] in scope:
        total_time += proj["total_seconds"]

delta = target-total_time

print(f"Banked time: {datetime.timedelta(seconds=total_time)}")
print(f"Target time: {datetime.timedelta(seconds=target)}")
print(f"Time left: {datetime.timedelta(seconds=delta)}")

time_daily = delta/days_left
print(f"Required Daily code time: {datetime.timedelta(seconds=time_daily)}")

percent_done = (total_time/target)*100
print(f"Percent complete: {round(float(percent_done))}%")


if input("Do you want me to save/update these settings as a recallable file, to allow further tracking? (True/False) ") == "True":
    if loaded == False:
        ysws_name = input("What's the name of this YSWS? ")
        start_days_input = input(f"How many days did you have when starting? Or leave blank to use {days_left} days ")
        if not start_days_input:
            start_days = days_left
        else:
            start_days = int(start_days_input)
        filename = f"{ysws_name.lower().replace(' ', '_')}_config.json"
    else:
        filename = file
    
    save_data = {
        "username": username,
        "target_hours": target // 3600,
        "days": start_days,
        "projects": scope
    }
    
    if os.path.exists(filename) and loaded == True:
        os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(save_data, f)
    print("Done!")