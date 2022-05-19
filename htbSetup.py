#!/usr/bin/env python3

######
## Made by Mikbrosim
######

import json
import string
import os

# catsLocation : "./cate.json"
catsLocation = ""

# chalLocation : "./chal.json"
chalLocation = ""

if catsLocation == "" or chalLocation == "":
    print("[!] Please specify location to the JSON file of 'categories' and 'challenges'")
    exit()

cats = json.load(open(catsLocation,"r"))
chal = json.load(open(chalLocation,"r"))

cats = {cat["id"]:cat["name"] for cat in cats}

def posixSafeFileName(filename):
    posixAllowed = string.ascii_letters+string.digits+"-._"
    return "".join(c if c in posixAllowed else "_" for c in filename)

with open("challengeList.md","wb") as fullList:
    for challenge in chal["challenges"]:
        challengeName = challenge["name"]
        challengeCategory = cats[challenge["challenge_category_id"]]
        challengeDifficulty = challenge["difficulty"]
        challengeDescription = challenge["description"]

        safeName = os.path.join(*map(posixSafeFileName,(challengeCategory,challengeName)))
        if os.path.exists(safeName):
            print(f"[!] Folder for {challengeName} already exists, skipping")
        else:
            os.makedirs(safeName)
            with open(os.path.join(safeName,"README.md"),"wb") as readme:
                for file in (readme,fullList):
                    file.write(f"# {challengeName}\n".encode("utf-8"))
                    file.write(f"**Category:** {challengeCategory}\n\n".encode("utf-8"))
                    file.write(f"**Difficulty:** `{challengeDifficulty}`\n\n".encode("utf-8"))
                    file.write(f"**Description:** {challengeDescription}\n\n".encode("utf-8"))
                    file.write("---\n".encode("utf-8"))
            print(f"[+] Folder for {challengeName} created")
