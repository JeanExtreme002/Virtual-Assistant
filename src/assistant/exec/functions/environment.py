import os

HOME = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]

paths = HOME + ";"
paths += os.path.join(HOME, "desktop") + ";"
paths += os.path.join(os.environ["PUBLIC"], "desktop") + ";"
paths += os.environ["PATH"]
