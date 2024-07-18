import os
from pathlib import Path

#get the current working directory
def cwd():
    return Path(__file__).resolve().parent
