# -*- coding: utf-8 -*-
#Information Retreival group project
import math
from util.lyrics_to_bow import lyrics_to_bow

def get_ids_called(title):
    ids = []
    f = open('C:/UW/IR/project/mxm_779k_matches.txt', "r", encoding='utf-8')
    for line in f.readlines():
        line = line.rstrip('\n')
        if line[0] == '#':
            continue
        tid1, artist1, title1, tid2, artist2, title2 = line.split('<SEP>')
        if title2.lower() == title.lower():
            ids.append(int(tid2))
    return ids


def cosine(query,YIndex):
    searchNum=20
    returnList=[0 for i in range(0,searchNum)]
    max20=[0 for i in range(0,searchNum)]
    for key in trainDict.keys():
        lyrics=trainDict[key]
        sum2=0
        for wordIndex in query.keys():
            if wordIndex in lyrics.keys():
                sum2=sum2+query[wordIndex]*lyrics[wordIndex]
        cos=sum2/lenOfVectorsX[key]*lenOfVectorsY[YIndex]
        if cos>max20[searchNum-1]:
            #先找位置
            location=searchNum-1
            for i in reversed(range(0,searchNum)):
                if cos>=max20[i]:
                    location=i
                else:
                    break
            #下面得出rank结果
            max20.insert(location,cos)
            max20=max20[:searchNum]
            returnList.insert(location,key)
            returnList=returnList[:searchNum]
    return returnList
    

trainFilePath="C:/UW/IR/project/mxm_dataset_train.txt"
testFilePath="C:/UW/IR/project/mxm_dataset_test.txt"
#train和test文件0-16行都是注释，第17行是单词列表，第18行开始是数字

#读入训练数据
trainFile=open(trainFilePath,"r")
trainLines=trainFile.readlines()
testFile=open(testFilePath,"r")
testLines=testFile.readlines()

trainDict={} #歌词索引
lenOfVectorsX={}
lenOfVectorsY={}

#处理第17行词汇列表
line17=trainLines[17]
wordList=[""]+line17[1:len(line17)-1].split(',')
#wordList是词汇索引
DF=[0 for i in range(0,len(wordList))]
IDF=[0]



#combine all training data
trainLines=trainLines[18:]+testLines[18:]

N=len(trainLines)
#处理第18行及其后的数据
for i in range(0,len(trainLines)):
    stringList=trainLines[i].split(',')
    key=int(stringList[1])
    newDict={}
    
    for j in range(2,len(stringList)):
        twoNum=stringList[j].split(':')
        index=int(twoNum[0])
        freq=int(twoNum[1])
        newDict[index]=freq
        DF[index]=DF[index]+1
    
    trainDict[key]=newDict
    
for i in range(1,len(wordList)):
    IDF.append(math.log10(N/DF[i]))

for key in trainDict.keys():
    innerDict=trainDict[key]
    mySum=0
    for index in innerDict.keys():
        innerDict[index]=innerDict[index]*IDF[index]
        mySum=mySum+innerDict[index]*innerDict[index]
    lenOfVectorsX[key]=math.sqrt(mySum)

testDict={}
#read queries from file
queryFilePath="C:/UW/IR/project/query.txt"
queryFile=open(queryFilePath,"r")
queryLines=queryFile.readlines()

#创建输出文件
outputFilePath="C:/UW/IR/project/"
fwrite=open(outputFilePath+"VectorSpaceModelResults.txt", "w")
fwrite.close()
fwrite=open(outputFilePath+"VectorSpaceModelResults.txt", "a")


print("Vector Space Model Test Results:")
for i in range(0,len(queryLines)):
    line=queryLines[i][:len(queryLines[i])-1]
    line=line.lower()
    tempDict=lyrics_to_bow(line)
    #tempDict和query都用来存放查询数据，格式不一样
    query={}
    sum1=0
    
    for key in tempDict.keys():
        if key in wordList:
            for k in range(1,len(wordList)):
                if wordList[k]==key:
                    index=k
                    break
            query[index]=freq*IDF[index]
            sum1=sum1+query[index]*query[index]
    
    testDict[i]=query
    lenOfVectorsY[i]=math.sqrt(sum1)
    #print(cosine(query,i))
    searchResultList=cosine(query,i)
    compareList=get_ids_called(line)
    
    '''print("x")
    print(searchResultList)
    print(compareList)'''
    
    flag=False
    for song in searchResultList:
        if song in compareList:
            flag=True
            break
    if flag:
        print("yes")
    else:
        print("no")

'''for i in range(18,30):
    stringList=testLines[i].split(',')
    key=int(stringList[1])
    query={}
    sum1=0
    for j in range(2,len(stringList)):
        twoNum=stringList[j].split(':')
        index=int(twoNum[0])
        freq=int(twoNum[1])
        query[index]=freq*IDF[index]
        sum1=sum1+query[index]*query[index]
    testDict[key]=query
    lenOfVectorsY[key]=math.sqrt(sum1)
    #下面计算cosine
    print(cosine(query,key))'''
fwrite.close()