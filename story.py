'''
File for calling story events sequentially
Made By: Leif Hoffman
Date: 10/20/2026
'''
from add_functions import *
import time
import subprocess

def storyStart():
    subprocess.run("cls", shell=True, check=True)
    styleprint("You are a traveler on a quest to become the strongest. Original, I know. But what's this?")
    time.sleep(2)