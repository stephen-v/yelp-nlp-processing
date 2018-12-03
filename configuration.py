import configparser
from collections import namedtuple
import os


def get_configs():
    """
    get configs
    :return:
    """
    conf = configparser.ConfigParser()
    file_path = os.path.split(os.path.realpath(__file__))[0] + '/config.ini'
    conf.read(file_path)
    host = conf.get('mysql', 'host')
    port = conf.get('mysql', 'port')
    user = conf.get('mysql', 'user')
    pwd = conf.get('mysql', 'pwd')
    db = conf.get('mysql', 'db')
    yelp_dir = conf.get('yelp_path', 'yelp_dir')
    business_filename = conf.get('yelp_path', 'business_filename')
    Config = namedtuple('Config', 'host port user pwd yelp_dir business_filename db')
    config = Config(host, port, user, pwd, yelp_dir, business_filename, db)
    return config
