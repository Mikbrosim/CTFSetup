#!/usr/bin/env python3

######
## Made by Mikbrosim
######

import requests
import json
import string
import os

def posixSafeFileName(filename):
    posixAllowed = string.ascii_letters+string.digits+"-_"
    return "".join(c if c in posixAllowed else "_" for c in filename)

# EXAMPLE BASEAPI : https://[URL]/api/v1/challenges
baseAPI = ""

# SESSION ID : b1cab1ad1ce51B51a51.ce51Bce51B
session = ""

if baseAPI == "" or session == "":
    print("[!] Please specify baseAPI and session")
    exit()

r = requests.get(baseAPI,cookies={"session":session})

challenges = json.loads(r.text)["data"]

if "message" in challenges and "ikke startet" in challenges["message"]:
    print("[-] Event hasn't started yet")
    exit()

with open("challengeList.md","wb") as fullList:
    for challenge in challenges:
        id = challenge["id"]
        r = requests.get(baseAPI+"/"+str(id),cookies={"session":session})
        challenge = json.loads(r.text)["data"]

        # from my haaukinsSetup.py
        challengeName = challenge["name"]
        challengePoints = challenge["value"]
        challengeDesc = challenge["description"]
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
