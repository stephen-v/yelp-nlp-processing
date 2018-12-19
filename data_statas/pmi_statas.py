import math

if __name__ == "__main__":
    word_paris = {}
    word_paris_pmi = {}
    words = {}
    print('start to load data....')
    error_data = 0
    with open('../data/wordpairs_4000.txt', encoding='UTF-8') as f:
        for x in f.readlines():
            try:
                paris, count = x.split('：')
                word1, word2 = paris.split('-')
                word_paris[paris] = count
                if word1 in words:
                    var = words[word1] + 1
                    words[word1] = var
                else:
                    words[word1] = 1

                if word2 in words:
                    var = words[word2] + 1
                    words[word2] = var
                else:
                    words[word2] = 1
                if len(word_paris) % 10000 == 0:
                    print('load %s , but error is %s' % (len(word_paris), error_data))
            except ValueError as e:
                error_data = error_data + 1

    temp = []
    word_paris_len = len(word_paris)
    words_len = len(words)
    processed_data = 0
    print('start to compute pmi...,word_paris_len is %s , words_len is %s' % (word_paris_len, words_len))

    for i in word_paris:
        paris, count = i, word_paris[i]
        word1, word2 = paris.split('-')
        prob_x_y = int(count) / word_paris_len
        prob_x = int(words[word1]) / word_paris_len
        prob_y = int(words[word2]) / word_paris_len
        pmi = math.log(prob_x_y / (prob_x * prob_y))
        with open('../data/wordpairs_pmi.txt', 'a+', encoding='UTF-8') as f:
            f.write('%s:%s|%s' % (paris, pmi, count))
        processed_data = processed_data + 1
        if processed_data % 10000 == 0:
            print('total is %s ,the processed data is %s' % (
                word_paris_len, processed_data))
    print('complete...')
