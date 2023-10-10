from bin import application
from bin.init import installer
import sys


if __name__ == "__main__":
    installer.install()
    g = application.Application()
    g.run()
    sys.exit()
