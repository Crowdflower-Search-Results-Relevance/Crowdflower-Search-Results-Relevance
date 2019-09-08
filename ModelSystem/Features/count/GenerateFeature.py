
import pickle

#读取n-gram的文件
'''
文件位于 ./ModelSystem/Features/ngram 文件夹下
'''

inputFolderPath = "./ModelSystem/Features/ngram"
outputFolderPath = "./ModelSystem/Features/count"

features = ["query","title","description"]
ngrams = ["unigram","bigram","trigram"]
catagories = ["train","test"]

#"i love china people"

#["i","love","chia"]
#["i_love"]

for feature in features:
    for ngram in ngrams:
        for cata in catagories:
            #读取文件
            inputFilePath = "%s/%s_%s_%s.pickle" % (inputFolderPath,feature,ngram,cata)
            with open(inputFilePath,"rb") as f:
                inputData = pickle.load(f)
            
            #input中的数据为
            #[A,B,C....,N]
            #A为第一个样本的ngram分词
            # 如对于第一个样本文本 "i get up,i get"
            #A == ['i','get','up',i get ] ,dtype(A) = List


            ###########
            #补全代码
            ############



            #生成特征文件
            outputFilePath = "%s/count_%s_%s_%s.pickle" % (outputFolderPath,feature,ngram,cata)
            with open(outputFilePath,"wb") as f:
                pickle.dump(outputdata,f)


# ratio_unique_query_trigram
#outputFilePath = "%s/ratio_%s_unique_%s_%s.pickle" % (outputFolderPath,feature,ngram,cata)

#generate missing indicator
# code is shown below

# indicator = 0, description is missing
#           = 1, otherwise

#输入的文件夹为 ./ModelSystem/ProcessedData 
#文件是 description_test.pickle,description_train.pickle
#outputFilePath = "%s/missing_indicator_%s.pickle" % (outputFolderPath,cata)    cata = "test"或"train"
