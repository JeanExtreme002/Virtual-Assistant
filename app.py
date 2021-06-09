from src import Application
import sys

__author__ = "Jean Loui Bernard Silva de Jesus"

application = Application("Virtual Assistant", sys.argv)
sys.exit(application.exec_())
