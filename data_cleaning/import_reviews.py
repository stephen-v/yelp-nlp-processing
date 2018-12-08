import json
import pymysql
import configuration
import db_factory
import configuration


def get_keys():
    """
    get restaurant business_id
    :return:
    """
    conn = db_factory.create_conn()
    c1 = conn.cursor()
    c1.execute('select business_id from restaurants')
    id_list = [row['business_id'] for row in c1.fetchall()]
    return id_list


def parse_data(keys, path):
    """

    :param keys:
    :param path:
    :return:
    """
    conn = db_factory.create_conn()
    c1 = conn.cursor()
    with open(path, encoding='UTF-8') as f:
        review_list = []
        processed_data = 0
        for x in f.readlines():
            record = json.loads(x)
            if str(record['business_id']) not in keys:
                continue
            item = ((str(record['business_id'])), (str(record['review_id'])), (str(record['stars'])),
                    (str(record['text'])))
            review_list.append(item)
            if len(review_list) == 1000:
                try:
                    c1.executemany('insert into restaurant_reviews(business_id,review_id,star,text) value(%s,%s,%s,%s)',
                                   review_list)
                    conn.commit()
                    review_list.clear()
                    processed_data = processed_data + 1000
                    print('processed data %d' % processed_data)
                except Exception as e:
                    print(e)
                    continue
        print('reviews completed .')


if __name__ == "__main__":
    keys = get_keys()
    config = configuration.get_configs()
    parse_data(keys, config.yelp_dir + config.reviews_filename)
