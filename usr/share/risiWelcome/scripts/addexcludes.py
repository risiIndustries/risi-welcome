import sys
from configparser import ConfigParser

config = ConfigParser()
config.read(sys.argv[1])

if config.has_option(sys.argv[2], "exclude"):
    exclude = config.get(sys.argv[2], 'exclude')
    exclude = f"{exclude} {sys.argv[3]}"
else:
    exclude = sys.argv[3]

config.set(sys.argv[2], "exclude", exclude)

file = open(sys.argv[1], "w")
config.write(file)
