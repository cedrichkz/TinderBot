import subprocess
from osax import *

applescript = """
display dialog "Some message goes here..." ¬
with title "This is a pop-up window" ¬
buttons {"CANCEL","OK"}
"""


subprocess.call("osascript -e '{}'".format(applescript), shell=True)
