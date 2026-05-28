import requests
import datetime

total_time = 0

username = "SurfyGalaxy"
target = 35*3600
days_left = 40
response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")

if response.status_code == 200:
    data = response.json()
    stats = data["data"]

    print(f"Languages: {stats["languages"]}")
    print(f"Projects: {stats["projects"]}")

# datetime.timedelta(time=seconds)
for proj in stats['projects']:
    total_time += proj["total_seconds"]

delta = target-total_time
print(datetime.timedelta(seconds=delta))

time_daily = delta/days_left
print(datetime.timedelta(seconds=time_daily))

