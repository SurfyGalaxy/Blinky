# 41 (till i use the script)
import requests
import datetime
import json
import os

total_time = 0
names = []
scope = []
new = None
looping = True

while looping == True:
    file = input("Load an existing YSWS profile? (Enter a YSWS name, or press Enter to skip)")
    file = f"{file.lower().replace(' ', '_')}_config.json"
    if file in os.listdir():
        looping = False
        with open(file, 'r') as f:
            data = json.load(f)
        username = data["username"]
        target = data["target_hours"] * 3600
        days = data["days"]
        scope = data["projects"]
        response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")
        data = response.json()
        stats = data["data"]
        new = 0
    elif file == "_config.json":
        looping = False
    else:
        print("Invalid YSWS name. Did you save it last time, or mispell it?")

if new == None:
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
    new = input(f"""Which projects are you adding? Or type 'exit' to proceed, or 'remove' to remove a project added earlier.
     Available projects: {names}, Added projects: {scope} \n""")

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


if input("Do you want me to save these settings as a recallable file, to allow further tracking? (True/False)") == "True":
    ysws_name = input("What's the name of this YSWS? ")
    start_days = input(f"How many days did you have when starting? Or leave blank to use {days_left} days ")
    if not start_days:
        start_days = days_left
    else:
        start_days = int(start_days)
    
    data = {
        "username": username,
        "target_hours": target // 3600,
        "days": start_days,
        "projects": scope
    }
    filename = f"{ysws_name.lower().replace(' ', '_')}_config.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    print("Done!")