import os
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def getPath():
    path = input("path to folder of CSVs to import: ")
    try: os.chdir(path)
    except:
        print("path does not lead to folder or folder does not exist")
        path = getPath()
    return path

flow = InstalledAppFlow.from_client_secrets_file(
    "C:/Users/Lance/Desktop/client.json",
    scopes=["https://www.googleapis.com/auth/youtube"]
)
flow.run_local_server()
service = build('youtube', 'v3', credentials=flow.credentials)

path = getPath()

for name in os.listdir(path):
    if not os.path.isfile(os.path.join(path, name)) or name.find("-videos.csv") == -1: continue
    playlist = service.playlists().insert(part="snippet,status,id", body=dict(
        snippet=dict(title = name[:-11]), 
        status=dict(privacyStatus = "private")
    )).execute()
    with open(os.path.join(path, name), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                service.playlistItems().insert(part="snippet", body=dict(
                    snippet=dict(
                        playlistId=playlist["id"],
                        resourceId=dict(
                            kind="youtube#video",
                            videoId=row["Video ID"]
                        )
                    )
                )).execute()
            except: continue

service.close()