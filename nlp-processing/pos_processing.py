from pycorenlp import *
import db_factory

nlp = StanfordCoreNLP("http://localhost:9000/")
conn = db_factory.create_conn()


def save_triples(triples):
    c1 = conn.cursor()
    try:
        c1.executemany('insert into triples(review_id,subject,relation,object) values(%s,%s,%s,%s)', triples)
        conn.commit()
    except Exception as e:
        print(e)


def extract_info(s, review_id):
    '''
    to extract info's relations from reviews by openie server
    :param s:
    :return:
    '''
    output = nlp.annotate(s, properties={"annotators": "tokenize,ssplit,pos,depparse,natlog,openie",
                                         "outputFormat": "json", "openie.triple.strict": "true"})
    sentences = output['sentences']
    triples = [sentence['openie'] for sentence in sentences]
    infos = []
    for i in triples:
        for rel in i:
            relationSent = review_id, rel['subject'], rel['relation'], rel['object']
            infos.append(relationSent)
    return infos


if __name__ == "__main__":
    c2 = conn.cursor()
    limit = 1001
    while True:
        c2.execute('select review_id,text from restaurant_reviews limit %s' % limit)
        reviews = c2.fetchall()
        for i in reviews:
            triples = extract_info(i['text'], i['review_id'])
            save_triples(triples)
        print('processed %s' % limit)
        limit = limit + 1000
        if len(reviews) < 1000:
            break
