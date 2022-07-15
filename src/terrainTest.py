from maya import cmds
from opensimplex import OpenSimplex
import random
import math
import numpy as np
from PIL import Image

cmds.select(all=True)
cmds.delete()

img = Image.open('noise2d.png')  # 读取图片
img = img.convert('L')  # 灰度化

cols, rows = img.size  # 图像大小

value = [[0] * cols for i in range(rows)]  # 创建一个大小与图片相同的二维数组

img_array = np.array(img)
#print(img_array)
#print('\n')

for x in range(0, rows):
    for y in range(0, cols):
        value[x][y] = img_array[x, y]  # 存入数组
#print(Value)
#print(rows)
#print(len(Value))

a=cols-1
b=rows-1

terrain = cmds.polyPlane( axis=[0,1,0], w=20, h=10, sx=a, sy=b, ch=False)


for i in range(rows):
	for j in range(cols):
		cmds.move(0, value[i][j], 0, terrain[0]+".vtx["+str(i*cols+j)+"]", r=True)
cmds.polySmooth(kb=False)



