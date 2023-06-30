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

initialize_app()
IN_FILE_NAME = "input.xlsx"
OUT_FILE_NAME = "output.json"

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
    file = req.files['file']
    file.save(IN_FILE_NAME) #save to disk

    hours = float(req.form["hours"])
    tableValues = json.loads(req.form["tableValues"])
    gain3 = float(req.form["gain3"])
    gain4 = float(req.form["gain4"])

    #run algorithm
    cmd = f"python3.11 maximize_productivity.py {IN_FILE_NAME} {tableValues[0][3]} {tableValues[0][2]} {tableValues[0][1]} {tableValues[0][0]} {tableValues[1][3]} {tableValues[1][2]} {tableValues[1][1]} {tableValues[1][0]} {hours} {gain3} {gain4}"
    proc = subprocess.run(args=cmd, shell=True, capture_output=True)

    #for debug
    #print("stdout: ", proc.stdout) 
    #print("stderr: ", proc.stderr)

    #prepare response
    with open(OUT_FILE_NAME, "r") as json_output:
        json_str = json_output.read()
    res = https_fn.Response()
    res.access_control_allow_credentials = True #to avoid cors problems
    res.content_type = "application/json"
    res.data = json_str
    return res