
'''
多分类转换为二分类

from sklearn.preprocessing import LabelBinarizer

lb = LabelBinarizer(sparse_output=False)
dfTrain = [1,2,3,4,1,2,4]
X_train = lb.fit_transform(dfTrain)
print(X_train)

结果
[[1 0 0 0]
 [0 1 0 0]
 [0 0 1 0]
 [0 0 0 1]
 [1 0 0 0]
 [0 1 0 0]
 [0 0 0 1]]

'''
import numpy as np
a = np.array([[1,2,3]])
print(a.shape)
print(len(a.shape))