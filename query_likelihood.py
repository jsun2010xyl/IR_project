# -*- coding: utf-8 -*-
# Information Retreival group project
import math
import time
from util.lyrics_to_bow import lyrics_to_bow
from util.mxm_api import getTrackName, getLyrics


class QueryLikelihoodModal:
    def __init__(self):
        self.prob_dict = {}
        self.smoothing_dict = {}
        self.title_dict = {}
        self.init_prob_dict(["data/mxm_dataset_train.txt",
                             "data/mxm_dataset_test.txt"])
        self.init_title_dict('data/mxm_779k_matches.txt')

    def init_title_dict(self, fname):
        f = open(fname, "r", encoding='utf-8')
        for line in f.readlines():
            if line[0] == '#':
                continue
            tid1, artist1, title1, tid2, artist2, title2 = line.split('<SEP>')
            self.title_dict[tid2] = title2

    def init_prob_dict(self, files):
        for fname in files:
            f = open(fname, "r", encoding='utf-8')
            for line in f.readlines():
                if line[0] == '#':
                    continue
                elif line[0] == '%':
                    wordList = ['']+line[1:len(line)-1].split(',')
                    continue
                stringList = line.split(',')
                key = int(stringList[1])
                tf_dict = {}

                for j in range(2, len(stringList)):
                    index, tf = stringList[j].split(':')
                    tf_dict[wordList[int(index)]] = int(tf)
                self.prob_dict[key] = tf_dict
            f.close()

        # Transform term frequency to probrability
        for song in self.prob_dict.keys():
            word_count = sum(self.prob_dict[song].values())
            vocabulary_size = len(self.prob_dict[song].keys())
            self.prob_dict[song] = {word: self.prob_dict[song][word] /
                                    word_count for word in self.prob_dict[song].keys()}
            self.smoothing_dict[song] = {word: ((self.prob_dict[song][word] + 1) / (word_count + vocabulary_size)) for word in self.prob_dict[song].keys()}

    def get_rank(self, query, k=0, smoothing=True):
        query = lyrics_to_bow(query)
        result = []
        prob_dict = self.smoothing_dict if smoothing else self.prob_dict
        for song in prob_dict.keys():
            prob = 1
            for word in query.keys():
                cur = prob_dict[song][word] if word in prob_dict[song].keys(
                ) else 0
                prob *= cur ** query[word]
            result.append((prob, song))
        result.sort(reverse=True)
        if k == 0:
            return result
        return result[:k]


if __name__ == "__main__":
    print('Using Query-likelihood Model.')

    print('Start initialize the modal')
    start_time = time.time()

    modal = QueryLikelihoodModal()

    print('Finish initialization. (%s seconds)' %
          round(time.time() - start_time, 4))
    while True:
        print('Please enter your query, or enter "exit()" to exit...')
        query = input()
        if query == 'exit()':
            break
        start_time = time.time()
        k = 5
        ranking_result = modal.get_rank(query, k)

        print('Finish ranking. (%s seconds)' %
              round(time.time() - start_time, 4))
        print('Top', k)
        for i, (prob, tid) in enumerate(ranking_result):
            tid = str(tid)
            print('#' + str(i + 1), 'tid: ' + tid, 'prob: ' + str(prob), sep='\t')
            if tid in modal.title_dict:
                print('Title: ' + modal.title_dict[tid])
            else:
                print('!Title not found')
            print(getLyrics(tid))
            print()
        print('-------------------------------------------------')
        print()
