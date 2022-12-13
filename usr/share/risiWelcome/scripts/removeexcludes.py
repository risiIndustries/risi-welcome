import sys
from configparser import ConfigParser

config = ConfigParser()
config.read(sys.argv[1])

section = sys.argv[2]

if config.has_option(section, "exclude"):
    exclude = config.get(section, 'exclude')
    exclude_list = exclude.split()
    if sys.argv[3] in exclude_list:
        exclude_list.remove(sys.argv[3])
        exclude = " ".join(exclude_list)
        config.set(section, "exclude", exclude)

file = open(sys.argv[1], "w")
config.write(file)
