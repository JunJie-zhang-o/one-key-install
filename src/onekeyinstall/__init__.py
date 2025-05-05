




from onekeyinstall.loader import load_modules
from pathlib import Path

load_modules(Path(__file__).parent.joinpath("tools"), __package__)








