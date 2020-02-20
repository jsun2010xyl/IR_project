# -*- coding: utf-8 -*-
#Information Retreival group project
import math


trainFilePath="C:/UW/IR/project/mxm_dataset_train.txt"
testFilePath="C:/UW/IR/project/mxm_dataset_test.txt"
#train和test文件0-16行都是注释，第17行是单词列表，第18行开始是数字

#读入训练数据
trainFile=open(trainFilePath,"r")
trainLines=trainFile.readlines()
trainDict={} #歌词索引
lenOfVectors={}

#处理第17行单词列表
line17=trainLines[17]
wordList=[""]+line17[1:len(line17)-1].split(',')
#wordList是词汇索引


#处理第18行及其后的数据
for i in range(18,len(trainLines)):
    stringList=trainLines[i].split(',')
    key=int(stringList[1])
    newDict={}
    
    for j in range(2,len(stringList)):
        twoNum=stringList[j].split(':')
        secondNum=int(twoNum[1])
        newDict[int(twoNum[0])]=secondNum
        
    
    trainDict[key]=newDict
    
    
#读入训练数据
testFile=open(testFilePath,"r")
testLines=testFile.readlines()