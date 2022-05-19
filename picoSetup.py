#!/usr/bin/env python3

######
## Made by Mikbrosim
######

import string
import requests
import os


# apiUrl : https://play.picoctf.org/api/challenges/?event=70&page_size=100
apiURl = ""

# session : [SESSION TOKEN]
session = ""

if baseAPI == "" or session == "":
    print("[!] Please specify apiURl and session")
    exit()

def posixSafeFileName(filename):
    posixAllowed = string.ascii_letters+string.digits+"-._"
    return "".join(c if c in posixAllowed else "_" for c in filename)

data = requests.get(apiURl,cookies={"sessionid":session}).json()["results"]

with open("challengeList.md","wb") as fullList:
    for challenge in data:
        challengeName = challenge["name"]
        challengeCategory = challenge["category"]["name"]
        challengePoints = challenge["event_points"]
        safeName = os.path.join(*map(posixSafeFileName,(challengeCategory,challengeName)))
        if os.path.exists(safeName):
            print(f"[!] Folder for {challengeName} already exists, skipping")
        else:
            os.makedirs(safeName)
            with open(os.path.join(safeName,"README.md"),"wb") as readme:
                for file in (readme,fullList):
                    file.write(f"# {challengeName}\n".encode("utf-8"))
                    file.write(f"**Category:** {challengeCategory}\n\n".encode("utf-8"))
                    file.write(f"**Points:** `{str(challengePoints)}`\n\n".encode("utf-8"))
                    file.write("---\n".encode("utf-8"))
            print(f"[+] Folder for {challengeName} created")
