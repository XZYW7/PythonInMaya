from maya import cmds
from opensimplex import OpenSimplex
import random
import math

cmds.select(all=True)
cmds.delete()

x=int(input())

gen = OpenSimplex(x)#要输入数据
def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    #return gen.noise2(nx, ny) / 2.0 + 0.5
    return gen.noise2(nx,ny)+random.random()*0.5+0.5

height=33
width=33

terrain = cmds.polyPlane( axis=[0,1,0], w=10, h=10, sx=32, sy=32, ch=False)

value = []
for y in range(height):
    value.append([0] * width)
    for x in range(width):
        nx = x/width - 0.5
        ny = y/height - 0.5
        value[y][x] = noise(nx, ny)

for i in range(height):
	for j in range(width):
		cmds.move(0, value[i][j], 0, terrain[0]+".vtx["+str(i*width+j)+"]", r=True)
cmds.polySmooth(kb=False)
print(value)