'''
该模块是为了给搜索系统提供接口，让搜索系统接收到程序返回的结果
资料库中的数据存储格式如下

id productTitle productDescription

'''

import pandas as pd
import numpy as np

#form InterfaceForSearchSystem import *

class DatabaseLoader:
    #database 读取的文件
    def loadDatabase(self):
        import os.path

        databaseAbsPath = "./ModelSystem/ProcessedData/Database.csv"
        #数据库找不到就报错
        databasePath = os.path.abspath(databaseAbsPath)
        print(databasePath)
        exists = os.path.exists(databasePath)
        if(exists==False):    
            raise Exception("未找到资料库" + databasePath)
        
        
        #加载文件
        self.database =  pd.read_csv(databasePath)

class SubResult:
    weights=  [0.2,0.2,0.6]
    grades = [3.5,4.0,3.6]

class InterfaceForSearchSystem:
    #databaseLoader = null
    __isInit=False
    __databaseLoader = None
      

    def init(self):
        '''
        该方式是为了让modelSystem加载资料库和模型
        '''
        self.__isInit = True
        #加载数据库
        self.__databaseLoader = DatabaseLoader()
        self.__databaseLoader.loadDatabase()
        #print(databaseLoader.database)

        pass
    
    def getSearchResult(self,keyWord):
        '''
        keyWord是用户搜索的关键词，类型为string
        返回排序好的搜索结果（前50个结果）：ids,relevances

        ids[i]为排名第i的产品在资料库中的id
        relevances[i]为第i个产品的相关度评分 


        ids: list ,dtype =int32
        relevance:list , dtype = float32

        '''

        if(self.__isInit == False):
            raise Exception("未初始化")

        #model work
        ids = [ i for i in range (50)]
        relevances = []
        results = []
        for  i in range(50):
            relevances.append((50-i)/50 *4)
            results.append(SubResult())
        
        #print(ids)
        #print(relevances)

        return ids,relevances,results

    def getDatabase(self):
        '''
        返回数据库
        '''
    
        if(self.__isInit == False):
            raise Exception("未初始化")

        return self.__databaseLoader.database.copy()
    
    def getCandidateWords(self):
        if(self.__isInit == False):
            raise Exception("未初始化")

        words = list((self.__databaseLoader.database)["query"])

        candidateWords = dict()

        for word in words:
            
            if word in candidateWords.keys():
                candidateWords[word] += 1
            else:
                candidateWords[word] = 1
        
        return candidateWords
            


'''
前端的使用方法

实例化
interface = InterfaceForSearchSystem()

初始化
interface.init()

ids,relevances = interface.getSearchResult("Zhangluoxi")

查看相关度排名第一的产品在资料库中的id
print(ids[0])

查看相关度排名第一的产品的相关度评分
print(relevances[0])

获取相关度排名第一的产品的title
index = ids[0]
database=getDatabase()
print( database['product_title'][index] )

获取产品的 description
将上文的 product_title 替换为 product_description

'''

#以下部分为测试
if __name__ == "__main__":
    a = InterfaceForSearchSystem()
    a.init()

    ids,relevances,results = a.getSearchResult('as')

    #输出排名第一的产品title
    index = ids[0]
    database=a.getDatabase()
    

    candidateWords = a.getCandidateWords()
    for key in candidateWords.keys():
        print( key , ", ",candidateWords[key])

    pass