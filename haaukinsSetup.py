#!/usr/bin/env python3

######
## Made by Mikbrosim
######

import json
import websocket
import string
import os

# eventUrl : [URLHERE]/challenges
eventUrl = ""

# Session : [JWT-TOKEN]
session = ""

if baseAPI == "" or session == "":
    print("[!] Please specify eventUrl and session")
    exit()

eventUrl = "/".join(eventUrl.split("/")[:3]).replace("http","ws")
ws = websocket.create_connection(f"{eventUrl}/challengesFrontend",
cookie = f"session={session}")
result = ws.recv()
ws.close()

def posixSafeFileName(filename):
    posixAllowed = string.ascii_letters+string.digits+"-._"
    return "".join(c if c in posixAllowed else "_" for c in filename)

# In case of challenge and scoreboard coming along, only save the first
result = "["+result.replace("}\n{","},{")+"]"
data = json.loads(result)[0]["values"]

with open("challengeList.md","wb") as fullList:
    for challenge in data:
        challenge = challenge["challenge"]
        challengeName = challenge["name"]
        challengePoints = challenge["points"]
        challengeDesc = challenge["teamDescription"]
        safeName = posixSafeFileName(challengeName)
        if os.path.exists(safeName):
            print(f"[!] Folder for {challengeName} already exists, skipping")
        else:
            os.makedirs(safeName)
            with open(os.path.join(safeName,"README.md"),"wb") as readme:
                fullList.write(f"# {'['+challengeName+']('+os.path.join(safeName,'README.md')+')'}\n".encode("utf-8"))
                readme.write(f"# {challengeName}\n".encode("utf-8"))
                for file in (readme,fullList):
                    file.write(f"**Points:** `{str(challengePoints)}`\n\n".encode("utf-8"))
                    file.write(f"**Description:** {challengeDesc}\n\n".encode("utf-8"))
                    file.write("---\n".encode("utf-8"))
            print(f"[+] Folder for {challengeName} created")
