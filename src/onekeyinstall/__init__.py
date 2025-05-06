




from onekeyinstall.loader import load_modules
from pathlib import Path

load_modules(Path(__file__).parent.joinpath("tools"), __package__)




import fire



class Cli:
    
    def __init__(self):
        pass



def main():
    fire.Fire(Cli)