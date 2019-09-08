import pickle
import numpy as np
import pandas as pd
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
            outputdata=[]
            num=0
            ratio=[]
            for i in range(0,len(inputData)):
                once_word=[]
                twice_word=[]
                for j in range(0,len(inputData[i])):
                    word=inputData[i][j]
                    if word not in once_word:
                        once_word.append(word)
                    elif word not in twice_word:
                        twice_word.append(word)
                
                outputdata.append(len(inputData[i]))
                ratio.append((len(once_word)-len(twice_word))/len(inputData[i]))
            outputFilePath = "%s/count_%s_%s_%s.pickle" % (outputFolderPath,feature,ngram,cata)
            with open(outputFilePath,"wb") as f:
                pickle.dump(outputdata,f)
                              
            outputFilePath = "%s/ratio_%s_unique_%s_%s.pickle" % (outputFolderPath,feature,ngram,cata)
            with open(outputFilePath,"wb") as f:
                pickle.dump(ratio,f)


# ratio_unique_query_trigram

#outputFilePath = "%s/ratio_%s_unique_%s_%s.pickle" % (outputFolderPath,feature,ngram,cata)

#generate missing indicator
# code is shown below

# indicator = 0, description is missing
#           = 1, otherwise

for cata in catagories:
    inputFilePath = "./ModelSystem/ProcessedData/description_%s.pickle" % cata
    with open(inputFilePath,"rb") as f:
        inputData = pickle.load(f)

    missing=[]
    indicator=0
    for i in range(0,len(inputData)):
        if pd.isnull(inputData[i]):
            indicator=0
        else :
            indicator=1
        missing.append(indicator)
    outputFilePath = "%s/missing_indicator_%s.pickle" % (outputFolderPath,cata)
    with open(outputFilePath,"wb") as f:
        pickle.dump(missing,f)

#输入的文件夹为 ./ModelSystem/ProcessedData 
#文件是 description_test.pickle,description_train.pickle
#outputFilePath = "%s/missing_indicator_%s.pickle" % (outputFolderPath,cata)    cata = "test"或"train"
