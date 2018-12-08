import itertools
import operator
from collections import OrderedDict

from pycorenlp import *
import json
import configuration
from data_cleaning import import_reviews

nlp = StanfordCoreNLP("http://localhost:9000/")
word_pairs = {}


def extract_cooccurrence_word(s):
    '''
    to extract info's relations from reviews by openie server
    :param s:
    :return:
    '''
    output = nlp.annotate(s, properties={"annotators": "tokenize,ssplit,pos",
                                         "outputFormat": "json"})
    sentences = output['sentences']
    sentences_tokens = [i['tokens'] for i in sentences]
    nns = []
    for words in sentences_tokens:
        nn = [i['word'] for i in words if
              i['pos'] == 'NN' or i['pos'] == 'NNS' or i['pos'] == 'NNPS' or i['pos'] == 'NNP']
        nns = nns + nn

    nns_pairs = [i for i in itertools.product(nns, nns)]
    return nns_pairs


if __name__ == "__main__":
    config = configuration.get_configs()
    path = config.yelp_dir + config.reviews_filename
    keys = import_reviews.get_keys()
    with open(path, encoding='UTF-8') as f:
        lines = 0
        for x in f.readlines():
            record = json.loads(x)
            if str(record['business_id']) not in keys:
                continue
            s = str(record['text'])
            # s = 'I love this place! My fiance And I go here atleast once a week. The portions are huge! Food is amazing. I love their carne asada. They have great lunch specials... Leticia is super nice and cares about what you think of her restaurant. You have to try their cheese enchiladas too the sauce is different And amazing!!!'
            pairs = extract_cooccurrence_word(s)
            key = ['%s-%s' % (i[0], i[1]) for i in pairs if i[0] != i[1]]
            lines = lines + 1
            for i in key:
                val = 1
                if i in word_pairs:
                    val = word_pairs[i]
                    val = val + 1
                word_pairs[i] = val
            if lines % 10000 == 0:
                sorted_by_value = OrderedDict(sorted(word_pairs.items(), key=lambda t: t[1], reverse=True))
                with open('../data/wordpairs_%s.txt' % str(lines), 'w+', encoding='utf-8') as file_object:
                    for i in sorted_by_value:
                        file_object.write('%s：%s\n' % (i, sorted_by_value.get(i)))
                print('save successful :%s.txt' % lines)
