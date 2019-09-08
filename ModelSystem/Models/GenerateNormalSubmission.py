from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD
from sklearn.svm import SVR
from  kappa  import quadratic_weighted_kappa

import pickle
import numpy as np
from sklearn.preprocessing import minmax_scale
import pandas as pd

x_train_path = "./ModelSystem/Features/X_train.pickle"

with open(x_train_path,"rb") as f:
    x_train = pickle.load(f)

y_train_path = "./ModelSystem/Features/Y_train.pickle"

with open(y_train_path,"rb") as f:
    y_train = pickle.load(f)


x_test_path = "./ModelSystem/Features/X_test.pickle"
with open(x_test_path,"rb") as f:
    x_test = pickle.load(f)

hist = np.bincount(y_train)
cdf = np.cumsum(hist) / float(sum(hist))
print("cdf =",cdf)

#获取样本权重
def getWeights():
    import pandas as pd
    dfTrain =pd.read_csv('./ModelSystem/RawData/train.csv')
    var = list(dfTrain["relevance_variance"])
    weights = []
    for v in var:
        weights.append(1/(float(v) + 1.0))
    weights = np.array(weights,dtype=float)
    #print(weights)
    return weights

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

    cnt = np.zeros([4])
    for i in y_pred:
        cnt[i] += 1

    print("cnt=",cnt)
    return y_pred



def svr():

    clf = SVR(C=4.0,gamma=0.2,cache_size=2048,kernel='rbf')
    clf.fit(x_train,y_train,sample_weight=getWeights())#,sample_weight=weights)
    y_pred = clf.predict(x_test)

    y_pred = list(y_pred)
    y_pred = rounding_cdf(y_pred)

    submission = pd.read_csv("./ModelSystem/RawData/sampleSubmission.csv")
  
    print(len(y_pred))
    print(len(submission["prediction"]))

    for i in range(len(y_pred)):
        y_pred[i] = y_pred[i] +1
        submission["prediction"][i] =  y_pred[i]
    
    submission.to_csv("./ModelSystem/Models/NormalSubmission.csv",index=False)
    


svr()