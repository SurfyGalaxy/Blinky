import requests

username = "SurfyGalaxy"
response = requests.get(f"https://hackatime.hackclub.com/api/v1/users/{username}/stats?features=projects,languages")

if response.status_code == 200:
    data = response.json()
    stats = data["data"]

    print(f"Languages: {stats["languages"]}")
    print(f"Projects: {stats["projects"]}")