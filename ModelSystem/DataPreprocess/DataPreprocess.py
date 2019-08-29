import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords



def textCleaning(raw_text,remove_stopwords=False,\
    remove_number=False,remove_punctuation=False,\
        remove_HTMLtags=True):
    '''
    process the raw text(string) and return the processed text(string)
    remove the numbers,punctuations ,etc. from the text
    '''
    #remove HTML tags
    processed_text = raw_text
    if(remove_HTMLtags):
        processed_text = BeautifulSoup(raw_text).get_text()

    #remove \n \r \\ \ and so on
    processed_text  = re.sub(r"\\[a-z]"," ",processed_text)
    processed_text = re.sub(r'\\\\' , r'\\' ,processed_text)
    processed_text = re.sub(r"\\\"","\"",processed_text)
    processed_text = re.sub(r'\\\'' , '\'' ,processed_text)

    #remove number
    if(remove_number):
        processed_text = re.sub("[0-9]"," ",processed_text)
    
    if(remove_punctuation):
        processed_text = re.sub("[^0-9a-zA-Z]"," ",processed_text)

    processed_text = processed_text.lower()
    words = processed_text.split()

    #get the stop word
    #nltk.download() #you need to execute this code to download the dataset containing "stop words",
    #but i will upload this dataset to QQ group   (HY)
    meaningful_words=words
    if(remove_stopwords):
        stop_words = set(stopwords.words("english") )
        meaningful_words = [w for w in words if not w in stop_words]

    processed_text =" ".join(meaningful_words)
 
    return processed_text


if __name__ == "__main__":
    
    '''
    读取文件
    labeled_train_data = pd.read_csv( r"labeledTrainData.tsv",header=0,\
        delimiter='\t',quoting =3)

    读取文件中 “riview"列第一个单元格的数据
    example = labeled_train_data["review"][0]
    example = textCleaning(example)

    print(example)

    保存文件
    labeled_train_data.to_csv(path+filename,\
        index=False,\
        sep='\t',quoting=3) 
    '''

    
