# Made by DariXmain
# Email : DariXMain9gmail.com || ariyanminecraft@gmail.com
# Name : DMO (DariX-MiniORM)
# Build Date : 5/1/2026 (11/2/1405)

import os

from typing import Optional
from datetime import datetime

DIRECTORY = "SqlLog"

# Code

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)

def Log(log : str, type: str = "startup", format : Optional[str] = "txt", rewriting : bool = False):

    """ args

        log : Message of log
        type : Log file name
        format : Log save format
        rewriting : if file exits Delete and make a new
        
    """


    if not log or log == "":
        raise ValueError("Your log content is empty.")

    message = f"[{datetime.today().date()}][{datetime.now().time().strftime("%H:%M:%S")}]: {log} !"

    if os.path.exists(f"{DIRECTORY}/{type}.{format}") and rewriting:
        os.remove(f"{DIRECTORY}/{type}.{format}")

    with open(f"{DIRECTORY}/{type}.{format}", "a", encoding="utf-8") as buffer:
        buffer.write(f"{message}\n")

    print(message)
