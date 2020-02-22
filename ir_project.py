# -*- coding: utf-8 -*-
#Information Retreival group project
import math

def cosine(query,YIndex):
    returnList=[0,0,0,0, 0,0,0,0, 0,0]
    max10=[0,0,0,0, 0,0,0,0, 0,0]
    for key in trainDict.keys():
        lyrics=trainDict[key]
        sum2=0
        for wordIndex in query.keys():
            if wordIndex in lyrics.keys():
                sum2=sum2+query[wordIndex]*lyrics[wordIndex]
        cos=sum2/lenOfVectorsX[key]*lenOfVectorsY[YIndex]
        if cos>max10[9]:
            #先找位置
            location=9
            for i in reversed(range(0,10)):
                if cos>=max10[i]:
                    location=i
                else:
                    break
            #下面得出rank结果
            max10.insert(location,cos)
            max10=max10[:10]
            returnList.insert(location,key)
            returnList=returnList[:10]
    return returnList
    

trainFilePath="C:/UW/IR/project/mxm_dataset_train.txt"
testFilePath="C:/UW/IR/project/mxm_dataset_test.txt"
#train和test文件0-16行都是注释，第17行是单词列表，第18行开始是数字

#读入训练数据
trainFile=open(trainFilePath,"r")
trainLines=trainFile.readlines()
trainDict={} #歌词索引
lenOfVectorsX={}
lenOfVectorsY={}

#处理第17行词汇列表
line17=trainLines[17]
wordList=[""]+line17[1:len(line17)-1].split(',')
#wordList是词汇索引
DF=[]
IDF=[0]
for i in range(0,len(wordList)):
    DF.append(0)

N=210519
#处理第18行及其后的数据
for i in range(18,len(trainLines)):
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


#读入训练数据
testFile=open(testFilePath,"r")
testLines=testFile.readlines()
#train和test的词汇表是一样的，不用再处理

testDict={}

#创建输出文件
outputFilePath="C:/UW/IR/project/"
fwrite=open(outputFilePath+"VectorSpaceModelResults.txt", "w")
fwrite.close()
fwrite=open(outputFilePath+"VectorSpaceModelResults.txt", "a")

print("Vector Space Model Test Results:")
print(len(testLines)-18)
#读入并处理18行及其后的测试数据
for i in range(18,30):
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
    print(cosine(query,key))
fwrite.close()