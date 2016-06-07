import os

try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    # python27
    # Refer to the older SafeConfigParser as ConfigParser
    from ConfigParser import SafeConfigParser as ConfigParser

config = ConfigParser()

# get the path to config.ini
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

# check if the path is to a valid file
if not os.path.isfile(config_path):
    raise IOError  # not a standard python exception

config.read(config_path)
