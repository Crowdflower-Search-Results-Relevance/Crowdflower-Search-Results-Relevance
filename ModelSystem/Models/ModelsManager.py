
class ModelsManager():
    __models = []

    def init(self):
        #初始化所有模型
        for model in __models:
            model.init()
    
    #keyWord是用户输入的词语
    def predict(self,keyWord):
        relevance=[]
        for model in __models:
            relevance.append(model.predict(keyWord))

        return relevance


'''
所有模型都将继承这个类
'''
class Model():
    def init(self):
        raise Exception("子类中必须实现此函数")
    
    def predict(self,keyWord):
        #input是输入数据
        raise Exception("子类中必须实现此函数")
        #return float32


if __name__ == "__main__":
    pass






