
import pickle

x_train_path = "./ModelSystem/Features/X_train.pickle"

with open(x_train_path,"rb") as f:
    x_train = pickle.load(f)

y_train_path = "./ModelSystem/Features/Y_train.pickle"

with open(y_train_path,"rb") as f:
    y_train = pickle.load(f)

'''
import pandas as pd
data = pd.read_csv("./ModelSystem/ProcessedData/train.csv")
data = data["median_relevance"]
data = list(data)

for i in range(len(data)):
    data[i] -= 1

print(data[:20])

with open(y_train_path,"wb") as f:
    pickle.dump(data,f)
'''

from sklearn.model_selection import train_test_split
#data_x是一个n*m的矩阵，m是特征数，n是样本数
#data_t是一个长度为n的list
x_train,x_test,y_train,y_test = train_test_split(\
    x_train,y_train,test_size = 0.3,random_state = 0)

y_test = list(y_test)

##############
#逻辑回归
##############

def LogR():
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1, fit_intercept=True, \
        solver="saga",
        intercept_scaling=1.0, 
        multi_class="multinomial"
        #n_jobs = -1
        ) 
    lr.fit(x_train,y_train)
    y_pred = lr.predict(x_test)
    y_pred = list(y_pred)
    print("Log ,Acc = ",calcAcc(y_pred,y_test))
    


def rounding_common(data):
    sz = len(data)
    mx = max(data)  # 返回最小值
    mn = min(data)

    for i in range(sz):
        data[i] = (data[i] - mn) / (mx -mn) *3
        if(data[i] <0.5):data[i] = 0
        elif (data[i]<1.5):data[i] = 1
        elif (data[i]<2.5):data[i] = 2
        else :data[i] = 3
    return data

#7:6% to 1, 7:6% − 22% to 2, 22% − 40% to 3, and the rest to 4

def rounding_spec(data):
    sz = len(data)
    mx = max(data)  # 返回最小值
    mn = min(data)
    for i in range(sz):
        data[i] = (data[i] - mn) / (mx -mn) *3
        if(data[i] < 3 * 0.076):data[i] = 0
        elif (data[i]<3*0.22 ):data[i] = 1
        elif (data[i]< 3 * 0.4 ):data[i] = 2
        else :data[i] = 3
    return data

def calcAcc(A,B):
    sz = len(A)
    acc=0
    for i in range(sz):
        if(A[i]==B[i]):acc+=1
    return acc/sz

def LinearR():
    from sklearn.linear_model import LinearRegression

    model = LinearRegression(n_jobs = -1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_pred = list(y_pred)

    #y_pred = rounding_spec(y_pred)
    #for i in range(20):
    #    print("%.2lf" % y_pred[i],end=", ")
    
    #y_pred = rounding_common(y_pred)
    y_p = rounding_spec(y_pred)

    print("Linear Spec Rounding Acc = ",calcAcc(y_p,y_test))

    y_p = rounding_common(y_pred)
    print("Linear Common Acc = ",calcAcc(y_p,y_test))

#print(y_pred[0:20],end = " ")

def RF():
    from sklearn.ensemble import RandomForestClassifier

    #train
    #initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators= 500,
    max_features = "auto",
    max_depth = None,
    n_jobs = -1,
    )

    #use the data set labeled_train_data
    '''
    n_classes_ : int or list
    The number of classes (single output problem), or a list containing the number of classes for each output (multi-output problem).
    '''

    forest = forest.fit(x_train, y_train)

    #predict
    y_pred = forest.predict(x_test)
    y_pred = list(y_pred)

    print("RF Acc = ",calcAcc(y_pred,y_test))


def svm_c():
    
    from sklearn.svm import SVC
    # rbf核函数，设置数据权重
    svc = SVC(kernel='linear', class_weight='balanced',
    cache_size = 2048)
    '''
    linear ：线性核函数
    -- poly  ：多项式核函数
    --rbf  ：径像核函数/高斯核
    -- sigmoid ：sigmod核函数
    '''
    # 训练模型
    svc = svc.fit(x_train, y_train)
    # 计算测试集精度
    score = svc.score(x_test, y_test)
    print('svc Acc =%lf' % score)


def ridge():
    from sklearn.linear_model import Ridge#, Lasso, LassoLars, ElasticNet
    ridge = Ridge(alpha=1.0, normalize=True)
    ridge.fit(x_train, y_train)#, sample_weight=weight_train[index_base]
    y_pred = ridge.predict(x_test)

    y_pred = list(y_pred)
    print(y_pred[:10])
    y_p = rounding_spec(y_pred)

    print("Ridge Spec Rounding Acc = ",calcAcc(y_p,y_test))

    y_p = rounding_common(y_pred)
    print("Ridge Common Rounding Acc = ",calcAcc(y_p,y_test))


LinearR()

LogR()
RF()

svm_c()

ridge()