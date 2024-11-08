#!/usr/bin/env python3
import requests
import subprocess
import itertools
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

#!/usr/bin/env python3
import re
import sys
import itertools

# args: str vx.x.x
def needToUpdate(one, two):
    cleanedValue = re.sub(r'[a-zA-Z]',"",one.strip())
    split=cleanedValue.split(".")
    cleanedValueTwo = re.sub(r'[a-zA-Z]',"",two.strip())
    splitTwo=cleanedValueTwo.split(".")
    
    try:
        numericOne=list(map(int,split))
        numericTwo=list(map(int,splitTwo))
    except ValueError:
        return False
    currentResult=False
    for i in list(itertools.zip_longest(numericOne, numericTwo)):
        a, b=i
        if a != None and b != None:
            if a < b:
                print(f"version {one} is lower than {two}")
                currentResult=True
                break
    return currentResult


#a=needToUpdate("v2.0.0","v3")
#b=needToUpdate("v4.0.0","v3")
#c=needToUpdate("v3.0.0","v3")
#d=needToUpdate("v2.3.5","v3.0.0")
#e=needToUpdate("abc","v3.0.0")
#print(f"a = {a}")
#print(f"b = {b}")
#print(f"c = {c}")
#print(f"d = {d}")
#print(f"e = {e}")



if(os.path.exists(".github") == True):
    #print("Exiats")
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
        #print(f"{j.file} => {j.value}")
        #print(f"{j.currentVersion} ({j.justVersionNumber}) -> {j.owner} -> {j.repo}")
        #print(f"{j.versionBits}")
        url=f"https://api.github.com/repos/{j.owner}/{j.repo}/releases"
        response = requests.get(url, headers=headers)
        newerVersion=response.json()[0]["name"]
        #print(f"Newer value is: {newerVersion}")
        #update=needToUpdate()
        #print(re.sub(r'[a-zA-Z]',"",response.json()[0]["name"]))
        update=needToUpdate(j.currentVersion,newerVersion)
        if update == True:
            print(f"{j.value} in  file: {j.file} can be updated to {newerVersion}")
        #print(f"{j.value} ---> {update}")
else:
    print("Nope Exiats")
    sys.exit(1)


# Bitrise would be
# - [a-zA-Z-]*\@[0-9\.]*:
