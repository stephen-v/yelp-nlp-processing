import configuration
import pymysql


def create_conn():
    config = configuration.get_configs()
    conn = pymysql.connect(host=config.host,
                           user=config.user,
                           password=config.pwd,
                           db=config.db,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor,
                           port=int(config.port)
                           )
    return conn
