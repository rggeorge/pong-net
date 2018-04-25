import numpy as np

m=100
n=1
epochs=100
LR=.01
N1=75

X=np.zeros((m,n))
for i in range(n):
    X[np.random.randint(m),i]=1
    
W1=np.random.rand(m,N1)-.5
W2=np.transpose(W1)

for i in range(epochs):
    H=np.matmul(np.transpose(W1),X)
    for j in range(N1):
        if H[j]<0:
            H[j]=0
            
    Xhat=np.matmul(np.transpose(W2),H)
    for j in range(m):
        if Xhat[j]<0:
            Xhat[j]=0
            
    D2=Xhat-X
    D1=np.matmul(W2,D2)
    
    W2=W2-LR*np.matmul(H,np.transpose(D2))
    W1=W1-LR*np.matmul(X,np.transpose(D1))
    
if np.argmax(X)==np.argmax(Xhat):
    print('Yay')