# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app

import pandas as pd
import sys
import re
import os
import random
import json
import pulp
import subprocess
import hashlib

initialize_app()
IN_FILE_NAME = "input.xlsx"
OUT_FILE_NAME = "output.json"
HASH_FILE = "hash_list"
SEP1 = "$1$\n"
SEP2 = "$2$\n"
MAX_FILE_SIZE = 2 << 22 # 4MB

@https_fn.on_request(
        cors=options.CorsOptions( #security is annoying sometimes
        cors_origins=["*"],
        cors_methods=["get", "post"],
    )
)
def calculate(req: https_fn.Request) -> https_fn.Response:
    if req.method != "POST":
        return "not POST"

    #parse args from https post
    tmp_file = req.files['file']
    tmp_file.save(IN_FILE_NAME) #save to disk

    hours = float(req.form["hours"])
    tableValues = json.loads(req.form["tableValues"])
    gain3 = float(req.form["gain3"])
    gain4 = float(req.form["gain4"])

    #compute input hash
    with open(IN_FILE_NAME, "rb") as file:
        excel_string = file.read()
        hash = hashlib.md5(str((excel_string, hours, tableValues, gain3, gain4)).encode()) 

    #find if hash already exists
    json_str = ""
    if os.path.isfile(HASH_FILE):
        with open(HASH_FILE, "r") as file:
            content = file.read()
            ndx = content.find(hash.digest().hex())
            if ndx != -1:
                json_str = content[content.find(SEP1 ,ndx)+len(SEP1):content.find(SEP2, ndx)]
                #found in hash file
        #evict if too big
        if os.path.getsize(HASH_FILE) > MAX_FILE_SIZE:
            os.remove(HASH_FILE)
    
    if json_str == "":
        #not found in hash file
        #run algorithm
        cmd = f"python3.11 maximize_productivity.py {IN_FILE_NAME} {tableValues[0][3]} {tableValues[0][2]} {tableValues[0][1]} {tableValues[0][0]} {tableValues[1][3]} {tableValues[1][2]} {tableValues[1][1]} {tableValues[1][0]} {hours} {gain3} {gain4}"
        proc = subprocess.run(args=cmd, shell=True, capture_output=True)
        #for debug
        #print("stdout: ", proc.stdout) 
        #print("stderr: ", proc.stderr)
        #read output from file
        with open(OUT_FILE_NAME, "r") as json_output:
            json_str = json_output.read()
        #update hash file
        with open(HASH_FILE, "a+") as file:
            file.write(f"{hash.digest().hex()}{SEP1}{json_str}{SEP2}")


    #prepare response
    res = https_fn.Response()
    res.access_control_allow_credentials = True #to avoid cors problems
    res.content_type = "application/json"
    res.data = json_str
    return res