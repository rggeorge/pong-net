from PIL import Image
import numpy as np
img=Image.open("Maze_Big_Y.png")
n,m=img.size
imgMat=np.array(img.getdata())
imgMat=imgMat.reshape(n,m,4)
walls=[]
goal=[]

for i in range(n):
    for j in range(m):
        if imgMat[i,j,1]==0:
            walls.append((j,i))
        if imgMat[i,j,1]==242:
            goal.append((j, i, "green", 1))        
            
