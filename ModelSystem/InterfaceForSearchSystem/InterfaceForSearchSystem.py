'''
该模块是为了给搜索系统提供接口，让搜索系统接收到程序返回的结果
资料库中的数据存储格式如下

id productTitle productDescription

'''

import pandas as pd

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
        返回排序好的搜索结果，其结构为

        sample = [id,relevance,otherInformation] ,id为该产品在资料库中的id
        返回值= 多个sample构成的list 

        id:int32
        relevance:float32
        otherInformation:待定

        '''

        if(self.__isInit == False):
            raise Exception("未初始化")

        #model work
        sample1 = [0,3.8]
        sample2 = [1,3.2]
        return [sample1,sample2]

    def getDatabase(self):
        '''
        返回数据库
        '''
        
        if(self.__isInit == False):
            raise Exception("未初始化")

        return self.__databaseLoader.database.copy()
        

'''
前端的使用方法

实例化
interface = InterfaceForSearchSystem()

初始化
interface.init()

searchResult - interface.getSearchResult("Zhangluoxi")

查看相关度排名第一的产品在资料库中的id
print(searchResult[0][0])

查看相关度排名第一的产品的相关度评分
print(searchResult[0][1])

'''

#以下部分为测试
if __name__ == "__main__":
    a = InterfaceForSearchSystem()
    a.init()
    print(a.getDatabase())
    pass