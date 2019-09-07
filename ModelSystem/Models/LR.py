from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD
#from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from  kappa  import quadratic_weighted_kappa

import pickle
import numpy as np
#from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import minmax_scale

x_train_path = "./ModelSystem/Features/X_train.pickle"

with open(x_train_path,"rb") as f:
    x_train = pickle.load(f)
    #x_train = minmax_scale(x_train, axis=0)#归一化

y_train_path = "./ModelSystem/Features/Y_train.pickle"

with open(y_train_path,"rb") as f:
    y_train = pickle.load(f)


hist = np.bincount(y_train)
cdf = np.cumsum(hist) / float(sum(hist))

'''
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(\
    x_train,y_train,test_size = 0.3,random_state = 0)
'''
sz = 7000

x_test = x_train[sz:]
y_test = y_train[sz:]
x_train = x_train[:sz]
y_train = y_train[:sz]


#y_test = list(y_test)

def getWeights():
    import pandas as pd
    dfTrain =pd.read_csv('./ModelSystem/RawData/train.csv')
    var = list(dfTrain["relevance_variance"])
    weights = []
    for v in var:
        weights.append(1/(float(v) + 1.0))
    weights = np.array(weights,dtype=float)
    #print(weights)
    return weights[:sz]

def rounding_cdf(y_pred):
    y_pred = np.array(y_pred)
    sz =len(y_pred)
    y_index = y_pred.argsort()
    s = 0
    for i in range(4):
        t = cdf[i]*sz
        for j in range(int(s),int(t)):
            y_pred[ y_index[j] ] = i
        s = t

    y_pred = y_pred.astype(np.int32)
    return y_pred

def rounding_zo(y_pred):
    y_pred = minmax_scale(y_pred)
    sz = len(y_pred)

    for i in range(sz):
        if(y_pred[i]<0.33):y_pred[i] = 0
        elif (y_pred[i]<0.6):y_pred[i] = 1
        elif (y_pred[i]<0.77):y_pred[i] = 2
        else :y_pred[i] = 3
    y_pred = y_pred.astype(np.int32)
    return y_pred

def calcAcc(A,B):
    sz = len(A)
    acc=0

    m = np.zeros([4,4],dtype=float)
    for i in range(sz):
        if(A[i]==B[i]):acc+=1
        m[A[i]][B[i]]+=1
    
    print(m)
    for i in range(4):
        for j in range(4):
            m[i][j]/=sz
            #m[i][j] = float( "%.2lf" % str(m[i][j]) )
    
    print(m)

    return acc/sz


def svr():

    clf = SVR(C=4.0,gamma=0.2,cache_size=2048,kernel='rbf')
    clf.fit(x_train,y_train,sample_weight=getWeights())#,sample_weight=weights)
    y_pred = clf.predict(x_test)

    y_pred = list(y_pred)
    #print(y_pred)
    y_p = rounding_cdf(y_pred)

    qwk=quadratic_weighted_kappa(y_test,y_p)
    print("kappa",qwk)
    print("Rounding cdf 验证集 Acc = ",calcAcc(y_p,y_test))
    #################################################
    y_pred = clf.predict(x_train)
    y_pred = list(y_pred)

    y_p = rounding_cdf(y_pred)
    print("Rounding cdf 训练集 Acc = ",calcAcc(y_p,y_train))



svr()