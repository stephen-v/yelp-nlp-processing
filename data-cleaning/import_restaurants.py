"""
import all restaurant from yelp_business.json
author:stephen
"""
import json
import pymysql
import configuration
import db_factory


def parse_dataset(path):
    """
    parse data from json
    :param path:
    :return:
    """
    with open(path, encoding='UTF-8') as f:
        business_list = []
        for x in f.readlines():
            record = json.loads(x)
            if str(record['categories']).find('Restaurants') == -1:
                continue
            item = ((str(record['business_id'])), (str(record['name'])), (str(record['categories'])),
                    (int(record['review_count'])))
            business_list.append(item)

    return business_list


def save_db(data, db_config):
    """
    save to db
    :param data:
    :param db_config:
    :return:
    """
    conn = db_factory.create_conn()
    c1 = conn.cursor()
    failed_data, processed_data = (0, 0)
    for i in data:
        try:
            c1.execute('insert into Restaurants(business_id ,name,categories,review_count) values (%s,%s,%s,%s)', i)
            conn.commit()
            processed_data = processed_data + 1
        except Exception as Argument:
            print(Argument, i)
            failed_data = failed_data + 1
            continue
        if processed_data % 1000 == 0:
            print('processed data %d' % processed_data)
    print('insert Restaurant success!  %d records but failed %d' % (len(data), failed_data))


if __name__ == "__main__":
    config = configuration.get_configs()
    data = parse_dataset(config.yelp_dir + config.business_filename)
    save_db(data, config)
