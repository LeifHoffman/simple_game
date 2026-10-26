'''
File for calling story events sequentially
Made By: Leif Hoffman
Date: 10/20/2026
'''
from add_functions import *
import time
import subprocess

def triggerStory(eventId):
    subprocess.run("cls", shell=True, check=True)
    match eventId:
        case 0:
            styleprint("You are a traveler on a quest to become the strongest. Original, I know. But what's this?")


        
        case _:
            styleprint("This event doesn't exist yet!")

    time.sleep(2)
    subprocess.run("cls", shell=True, check=True)