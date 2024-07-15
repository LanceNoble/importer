import sys
import os
import csv
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    "C:/Users/Lance/Desktop/client.json",
    scopes=["https://www.googleapis.com/auth/youtube"]
)
flow.run_local_server()
service = build('youtube', 'v3', credentials=flow.credentials)

parser = argparse.ArgumentParser(
    prog="YouTubeImporter",
    description="Import exported YouTube data",
    epilog="Text at the bottom of help"
)
parser.add_argument("path", type=str, action="store", default="")

def noop(path: str):
    pass

def importPlaylists(path: str):
    pass
    # print("Importing playlists...")
    # playlistsPath = os.path.join(path, "playlists")
    # if os.path.exists(playlistsPath) == False:
    #     print("ERROR: non-existent path")
    #     return
    # for item in os.listdir(playlistsPath):
    #     if item.find("-videos.csv") == -1: continue
    #     playlist = service.playlists().insert(part="snippet,status,id", body=dict(
    #         snippet=dict(title=item[:-11]),
    #         status=dict(privacyStatus="private")
    #     )).execute()

parser.add_argument("-p", action="store_const", const=importPlaylists, default=noop)

# add subs to the user's yt account from a csv file specified by the path
# generate a csv file listing subs that couldn't be added
def importSubscriptions(path: str):
    print("Importing subscriptions...")
    subscriptionsPath = os.path.join(path, "subscriptions", "subscriptions.csv")
    if os.path.exists(subscriptionsPath) == False:
        print("ERROR: non-existent path")
        return
    with open(subscriptionsPath, newline='', encoding="utf-8") as inp, open(os.path.join(path, "subscriptions", "modsubs.csv"), 'w', newline='', encoding="utf-8") as out:
        reader = csv.reader(inp)
        header = reader.__next__()
        if len(header) != 3 or header[0] != "Channel Id" and header[1] != "Channel Url" and header[2] != "Channel Title":
            print("ERROR: invalid format")
            return
        writer = csv.writer(out)
        for row in reader:
            if len(row) != 3 or row[0][0] != 'U' and row[0][1] != 'C':
                continue
            try:
                service.subscriptions().insert(part="snippet", body=dict(
                    snippet=dict(
                        resourceId=dict(
                            kind="youtube#subscription",
                            channelId=row[0]
                        )
                    )
                )).execute()
            except:
                writer.writerow([row[0], row[1], row[2]])

parser.add_argument("-s", action="store_const", const=importSubscriptions, default=noop)

args = parser.parse_args()
args.p(args.path)
args.s(args.path)

# for item in os.listdir(path):
#     if item.find("-videos.csv") == -1: continue
#     playlist = service.playlists().insert(part="snippet,status,id", body=dict(
#         snippet=dict(title = item[:-11]), 
#         status=dict(privacyStatus = "private")
#     )).execute()
#     with open(os.path.join(path, item), newline='') as inp, open(os.path.join(path, item[:-11]), 'w', newline='') as out:
#         reader = csv.reader(inp)
#         writer = csv.writer(out)
#         writer.writerow(["Video ID", "Playlist Video Creation Timestamp"])
#         for row in reader:
#             try:
#                 service.playlistItems().insert(part="snippet", body=dict(
#                     snippet=dict(
#                         playlistId=playlist["id"],
#                         resourceId=dict(
#                             kind="youtube#video",
#                             videoId=row[0]
#                         )
#                     )
#                 )).execute()
#             except:
#                 writer.writerow([row[0], row[1]])

service.close()