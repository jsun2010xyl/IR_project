# -*- coding: utf-8 -*-
# Information Retreival group project
import math
import time
from util.lyrics_to_bow import lyrics_to_bow
from util.mxm_api import getTrackName, getLyrics

trainFilePath = "data/mxm_dataset_train.txt"
testFilePath = "data/mxm_dataset_test.txt"

print('Using Query-likelyhood Model.')
print('Making necessary preparation. Please be patient.')
start_time = time.time()
# 读入训练数据
trainFile = open(trainFilePath, "r", encoding='utf-8')
trainLines = trainFile.readlines()
prob_dict = {}

# Load word list in 17 line
line17 = trainLines[17]
wordList = [""]+line17[1:len(line17)-1].split(',')

# Load lyrics term frequency
for i in range(18, len(trainLines)):
    stringList = trainLines[i].split(',')
    key = int(stringList[1])
    tf_dict = {}

    for j in range(2, len(stringList)):
        index, tf = stringList[j].split(':')
        tf_dict[wordList[int(index)]] = int(tf)
    prob_dict[key] = tf_dict
trainFile.close()

testFile = open(testFilePath, "r", encoding='utf-8')
testLines = testFile.readlines()
for i in range(18, len(testLines)):
    stringList = testLines[i].split(',')
    key = int(stringList[1])
    tf_dict = {}

    for j in range(2, len(stringList)):
        index, tf = stringList[j].split(':')
        tf_dict[wordList[int(index)]] = int(tf)
    prob_dict[key] = tf_dict
testFile.close()


print('Finish reading data. (%s seconds)' % round(time.time() - start_time, 4))

start_time = time.time()
for song in prob_dict.keys():
    word_count = sum(prob_dict[song].values())
    prob_dict[song] = {word: prob_dict[song][word] /
                       word_count for word in prob_dict[song].keys()}
print('Finish preprocess. (%s seconds)' % round(time.time() - start_time, 4))

while True:
    print('Please enter your query, or enter "exit()" to exit...')
    query = input()
    if query == 'exit()':
        break
    query = lyrics_to_bow(query)
    start_time = time.time()
    ranking_result = []
    for song in prob_dict.keys():
        prob = 1
        for word in query.keys():
            cur = prob_dict[song][word] if word in prob_dict[song].keys() else 0
            prob *= cur ** query[word]
        ranking_result.append((prob, song))
    ranking_result.sort(reverse=True)
    print('Finish ranking. (%s seconds)' % round(time.time() - start_time, 4))
    print('Top 5')
    for i, (prob, tid) in enumerate(ranking_result[:5]):
        print('-------------------------------------------------')
        print('#' + str(i + 1), 'tid: ' + str(tid), 'probrability: ' + str(round(prob, 5)), sep='\t')
        print('Title: ' + getTrackName(tid))
        print(getLyrics(tid))
        print()
    print('-------------------------------------------------')
    print()