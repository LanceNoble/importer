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
    "C:\Users\Lance\Desktop\client.json",
    scopes=["https://www.googleapis.com/auth/youtube"]
)
flow.run_local_server()
service = build('youtube', 'v3', credentials=flow.credentials)

# print("getting your playlists...")
# userPlaylists = service.playlists().list(part="id,snippet", mine=True).execute()["items"]
# discography = dict()
# count = 0
# print("here are the playlists you've created: ")

# for playlist in userPlaylists:
#     count += 1
#     print("% i. % s" % (count, playlist["snippet"]["title"]))
#     videos = service.playlistItems().list(part="contentDetails", playlistId=playlist["id"]).execute()["items"]
#     discography[playlist["snippet"]["title"]] = videos

path = getPath()

files = []
for name in os.listdir(path):
    if not os.path.isfile(os.path.join(path, name)) or name.find("-videos.csv") == -1: continue
    playlistProperties = dict(
        snippet = dict(title = name[:-11]), 
        status = dict(privacyStatus = "private")
    )
    service.playlists().insert(part="id", body=playlistProperties).execute()
    # if name[:-11] not in discography:
    #     playlistProperties = dict(
    #         snippet = dict(title = name[:-11]), 
    #         status = dict(privacyStatus = "private")
    #     )
    #     service.playlists().insert(part="snippet,status", body=playlistProperties).execute()
    files.append(name)

userPlaylists = service.playlists().list(part="id,snippet", mine=True).execute()["items"]
discography = dict()
count = 0
for playlist in userPlaylists:
    videos = service.playlistItems().list(part="contentDetails", playlistId=playlist["id"]).execute()["items"]
    discography[playlist["snippet"]["title"]] = videos

for file in files:
    with open(os.path.join(path, file), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            # insert or update
            #service.playlistItems().update(part="contentDetails,id,snippet,status")
            print("update playlist")
            print(row)

service.close()