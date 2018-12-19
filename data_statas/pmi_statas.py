import math

if __name__ == "__main__":
    word_paris_pmi = {}
    word_paris_len = 810000 - 14456
    words = {}
    print('start to load data....')
    error_data = 0
    processed_data = 0
    with open('../data/words_statas.txt', encoding='UTF-8') as f:
        for x in f.readlines():
            try:
                word, count = x.split(':')
                words[word] = count
            except ValueError as e:
                print(e)
    print('words list load successful...')
    temp = []
    with open('../data/wordpairs_4000.txt', encoding='UTF-8') as f:
        for x in f.readlines():
            try:
                word_pair, count = x.split('：')
                word1, word2 = word_pair.split('-')
                if word1 in words and word2 in words:
                    prob_x_y = int(count) / word_paris_len
                    prob_x = int(words[word1]) / word_paris_len
                    prob_y = int(words[word2]) / word_paris_len
                    pmi =math.log(prob_x_y / (prob_x * prob_y))
                    temp.append('%s:%s|%s' % (word_pair, pmi, count))
                    processed_data = processed_data + 1
                if processed_data % 10000 == 0:
                    with open('../data/pmi_statas.txt', 'a+', encoding='UTF-8') as f1:
                        f1.writelines(temp)
                    print('process data %s , but error is %s' % (processed_data, error_data))
            except ValueError or KeyError as e:
                error_data = error_data + 1
        print('complete...')
