import os
import pathlib

from src.core.utils.constants import Constants

def build_home_directory():
    home = str(pathlib.Path.home())
    return str(os.path.sep.join((home, Constants.APP_NAME)))
