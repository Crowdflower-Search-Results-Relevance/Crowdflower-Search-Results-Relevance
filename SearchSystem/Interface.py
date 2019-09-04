
import pickle
import pandas as pd



class Interface():
    __inited = False

    #若更改路径，请将原路径注释再添加新的路径，而不是将原路径直接删去
    __resultPath = "./SearchSystem/data/result.pickle"
    __databasePath  = "./SearchSystem/data/database.csv"

    __database = None
    __result = None
    __queryDict = None

    def init(self):
        self.__inited = True

        #加载原始文件
        self.__database = pd.read_csv(self.__databasePath)
        
        with open(self.__resultPath,"rb") as f:
            self.__result = pickle.load(f)

        #加载query列表
        queryList = list((self.__database)["query"])
        self.__queryDict = dict()

        for word in queryList:
            
            if word in self.__queryDict.keys():
                self.__queryDict[word] += 1
            else:
                self.__queryDict[word] = 1

        #重新格式化database
        query = list( (self.__database)["query"])
        title = list((self.__database)["product_title"])
        description = list((self.__database)["product_description"])

        svm_pred = self.__result[0]
        rf_pred = self.__result[1]
        xgb_pred = self.__result[2]
        avg_pred = self.__result[3]
        
        sz = svm_pred.shape[0]

        for i in range(sz):
            title[i] = str(title[i])
            if(title[i]=="nan") :title[i]=""
            
            description[i] = str(description[i])
            if(description[i]=="nan"):description[i] =""

            svm_pred[i] += 1.0
            rf_pred[i]+=1.0
            xgb_pred[i] +=1.0
            avg_pred[i] += 1.0


        self.__database = []

        for i in range(sz):
            info = [query[i],title[i],description[i],float(avg_pred[i]),float(svm_pred[i]),float(rf_pred[i]),float(xgb_pred[i])]
            #print(type(info[3]))
            self.__database.append(info)
        
        
    def getQueryDict(self):
        ######################
        #返回keyword的字典
        #字典格式如下
        # query:cnt
        # query表示用户搜索的关键词，cnt表示关键词在数据库中出现的次数
        ###########################
        if(self.__inited == False):
            raise Exception("未初始化")

        return self.__queryDict.copy()


    def getSearchResult(self,query):
        if(self.__inited == False):
            raise Exception("未初始化")

        query = str(query)
        if(query not in self.__queryDict.keys()):
            raise Exception("不存在的候选词")

        #######遍历数据库
        #  [query[i],title[i],description[i],avg_pred[i],svm_pred[i],rf_pred[i],xgb_pred[i]]
        results = []
        for info in self.__database:
            if(query == info[0] ):
                #print(info)
                results.append(info)

        #根据avg排序
        results = sorted(results, key=lambda x:x[3],reverse=True )

        for i in range(len(results)):
            for j in range(3,len(results[i])):
                #if(type(results[i][j])== str):print(i,",,,",j)
                results[i][j] = "%.2lf" % float(results[i][j])
                results[i][j] = str(results[i][j])

        return results
        
    def getDatabase(self):
        return self.__database.copy()

        
if __name__ == "__main__":
    x=  Interface()
    x.init()

    d = x.getQueryDict()
    #print(d.keys())
    # phillips coffee maker
    res = x.getSearchResult("phillips coffee maker")

    print(res[0])
    '''
    for i in range(len(res)):
        print(res[i][3])
        if(i>10):break
    '''

