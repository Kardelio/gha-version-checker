#!/usr/bin/env python3
import requests
import subprocess
import json
import re
import sys
import os
import base64

class Entry:
    def __init__(self, file, value):
        self.file = file
        self.value = value
        splitedValue = value.split("@")
        self.currentVersion = splitedValue[1].strip()
        self.justVersionNumber = re.sub(r'[a-zA-Z]',"",splitedValue[1].strip())
        self.splitVers=self.justVersionNumber.split(".")
        self.versionBits=len(self.splitVers)
        self.owner = splitedValue[0].split("/")[0].strip()
        self.repo = splitedValue[0].split("/")[1].strip()

if(os.path.exists(".github") == True):
    print("Exiats")
    USER=os.environ["GITHUB_USERNAME"]
    KEY=os.environ["GITHUB_API_KEY"]
    b64Key=base64.b64encode((USER+":"+KEY).encode("ascii")).decode("ascii")

    headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Basic {b64Key}"
            }


    res = subprocess.run(['/usr/bin/grep','-nr','uses','.github'], capture_output=True, text=True)
    lines=res.stdout.splitlines()
    out=[]

    for i in lines:
        file=i.split(":")[0]
        value=i.split("uses:")[1]
        out.append(Entry(file.replace("\"","").strip(),value.replace("\"","").strip()))

    for j in out:
        print(f"{j.file} => {j.value}")
        print(f"{j.currentVersion} ({j.justVersionNumber}) -> {j.owner} -> {j.repo}")
        print(f"{j.versionBits}")
        url=f"https://api.github.com/repos/{j.owner}/{j.repo}/releases"
        response = requests.get(url, headers=headers)
        print(response.json()[0]["name"])
        print(re.sub(r'[a-zA-Z]',"",response.json()[0]["name"]))
else:
    print("Nope Exiats")
    sys.exit(1)
