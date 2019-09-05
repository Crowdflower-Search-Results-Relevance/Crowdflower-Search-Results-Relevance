import pickle
with open("./ModelSystem/Features/Y_train.pickle","rb") as f:
    y = pickle.load(f)

ans = [0,0,0,0]
sz = len(y)
for i in y:
    ans[i] += 1

for i in range(4):
    ans[i] /= sz

print (ans)