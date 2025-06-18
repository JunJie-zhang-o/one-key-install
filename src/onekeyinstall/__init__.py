




from onekeyinstall.loader import load_modules
from pathlib import Path


load_modules(Path(__file__).parent.joinpath("tools"), __package__)



_version = "0.0.1"


class Cli:
    
    def __init__(self):
        pass




