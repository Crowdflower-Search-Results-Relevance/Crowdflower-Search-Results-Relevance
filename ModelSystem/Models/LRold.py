
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import minmax_scale
from  kappa  import quadratic_weighted_kappa


x_train_path = "./ModelSystem/Features/X_train.pickle"

with open(x_train_path,"rb") as f:
    x_train = pickle.load(f)
    #x_train = minmax_scale(x_train, axis=1)#归一化

y_train_path = "./ModelSystem/Features/Y_train.pickle"

with open(y_train_path,"rb") as f:
    y_train = pickle.load(f)

#######################
#统计cdf
#######################
#y_test = np.Array(y_test)
#y_sortIndex = y_test.argsort()

hist = np.bincount(y_train)
cdf = np.cumsum(hist) / float(sum(hist))
#print("cdf=",cdf)

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



from sklearn.model_selection import train_test_split
#data_x是一个n*m的矩阵，m是特征数，n是样本数
#data_t是一个长度为n的list
x_train,x_test,y_train,y_test = train_test_split(\
    x_train,y_train,test_size = 0.3,random_state = 0)

y_test = list(y_test)



##############
#逻辑回归
##############

def LogR(C=1):
    from sklearn.linear_model import LogisticRegression

    lr = LogisticRegression( C=C,
        penalty="l2", dual=False, tol=1e-5,
        fit_intercept=True, intercept_scaling=1.0,
        class_weight='balanced',
        n_jobs = -1,
        max_iter = 10000,
        solver="lbfgs"
        ) 

    lr.fit(x_train,y_train)
    y_pred = lr.predict(x_test)
    y_pred = list(y_pred)
    
    qwk=quadratic_weighted_kappa(y_test,y_pred)
    print("kappa",qwk)

    print("Log  验证集 Acc = ",calcAcc(y_pred,y_test))
    #################################################
    y_pred = lr.predict(x_train)
    y_pred = list(y_pred)

    print("Log  训练集 Acc = ",calcAcc(y_pred,y_train))

    return  y_pred
    


def calcAcc(A,B):
    sz = len(A)
    acc=0

    m = np.zeros([4,4],dtype=float)
    for i in range(sz):
        if(A[i]==B[i]):acc+=1
        m[A[i]][B[i]]+=1
    
    #print(m)
    for i in range(4):
        for j in range(4):
            m[i][j]/=sz
            #m[i][j] = float( "%.2lf" % str(m[i][j]) )
    
    #print(m)

    return acc/sz

def LinearR():
    from sklearn.linear_model import LinearRegression
    
    model = LinearRegression(n_jobs = -1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_pred = list(y_pred)

    y_p = rounding_cdf(y_pred)
    qwk=quadratic_weighted_kappa(y_test,y_p)
    print("kappa",qwk)
    print("Linear Rounding cdf 验证集 Acc = ",calcAcc(y_p,y_test))
    #################################################
    y_pred = model.predict(x_train)
    y_pred = list(y_pred)

    y_p = rounding_cdf(y_pred)
    print("Linear Rounding cdf 训练集 Acc = ",calcAcc(y_p,y_train))


    return y_p
    #y_p = rounding_common(y_pred)
    #print("Linear Common Acc = ",calcAcc(y_p,y_test))

#print(y_pred[0:20],end = " ")

def RF():
    from sklearn.ensemble import RandomForestClassifier

    #train
    #initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators= 15000,
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

    qwk=quadratic_weighted_kappa(y_test,y_pred)
    print("kappa",qwk)
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


def ridge(alpha=1.0):
    from sklearn.linear_model import Ridge#, Lasso, LassoLars, ElasticNet
    ridge = Ridge(alpha=alpha, normalize=False)
    ridge.fit(x_train, y_train)#, sample_weight=weight_train[index_base]
    y_pred = ridge.predict(x_test)

    y_pred = list(y_pred)
    #print(y_pred[:10])
    y_p = rounding_cdf(y_pred)
    qwk=quadratic_weighted_kappa(y_test,y_p)
    print("kappa",qwk)
    print("Ridge rounding cdf Acc = ",calcAcc(y_p,y_test))
    return y_p

def Lasso(alpha=1.0):
    from sklearn.linear_model import Lasso#, Lasso, LassoLars, ElasticNet
    
    lasso = Lasso(alpha=alpha, normalize=False)
    lasso.fit(x_train, y_train)
    y_pred = lasso.predict(x_test)

    y_pred = list(y_pred)
    y_p = rounding_cdf(y_pred)
    qwk=quadratic_weighted_kappa(y_test,y_p)
    print("kappa",qwk)
    print("LASSO rounding cdf Acc = ",calcAcc(y_p,y_test))

#LinearR()

LogR()
LinearR()
ridge()
Lasso()
RF()

'''
y_pred = np.array([y_1,y_2,y_3])
y_pred = np.mean(y_pred ,axis =0 )
y_pred = list(y_pred)
y_p = rounding_cdf(y_pred)
print(len(y_pred))
print(len(y_test))
print("avg Acc = ",calcAcc(y_p,y_test))
'''
#RF()
#svm_c()
#ridge()