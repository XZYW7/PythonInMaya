'''
    高度图生成地形
    噪波图生成地形
    遮罩选区
'''

from maya import cmds
from PIL import Image
import os.path
import random
import math


#高度图生成地形，高度图要求是像素小于256*256的正方形图,可以是彩色图
def HeightMapTerrain(imageFile):
    '''
    This is the function method that imports the height map to generate the terrain
    
    imageFile: path to the height map
    '''
    if not os.path.isfile(imageFile):
        print("image doesn't exist")
        exit()

    img = Image.open(imageFile)  # 读取图片
    img = img.convert('L')  # 灰度化
    pixels = img.load()
    
    cmds.select(all=True)
    cmds.delete()
    
    width, height = img.size  # 图像大小
    
    terrain = cmds.polyPlane( axis=[0,1,0], w=50, h=50, sx=width-1, sy=height-1, ch=False)

    # change the vertex position of the plan according tot he terrainData
    for i in range(height):
        for j in range(width):
            cmds.move(0, pixels[j,i]/255.0, 0, terrain[0]+".vtx["+str(i*width+j)+"]", r=True)
        cmds.refresh(f = True)


#噪波图生成地形
def noiseMap(width, height, scale):
    noise = [[r for r in range(int(width))] for i in range(int(height))]

    for i in range(0,int(height)):
        for j in range(0,int(width)):
            noise[i][j] = scale * (random.random()*0.8+0.2) # (0.2,1]
    return noise

def Elevation(terrain, width, height, sharpness):
	noiseMap3 = noiseMap(width/4, height/4, 1.4)
	noiseMap2 = noiseMap(width/2, height/2, 1.2)
	noiseMap1 = noiseMap(width, height, 1.0)
	for y in range(height):
		for x in range(width):
			pointy = noiseMap3[x/4][y/4] + 0.4* noiseMap2[x/2][y/2] + 0.2* noiseMap1[x][y]
			pointy = math.pow(pointy, sharpness)
			cmds.move(0, pointy*0.5, 0, terrain+".vtx["+str(y*width+x)+"]", r=True)
		cmds.refresh(f = True)
        
def NoiseMapTerrain():
	'''
    This is the method to generate terrain by using randomly generated noise map
    '''
	cmds.select(all=True)
	cmds.delete()

	height=200
	width=200
	smoothness = 2
	sharpness = 6.0
	terrain=cmds.polyPlane( axis=[0,1,0], w=50, h=50, sx=width-1, sy=height-1)
	Elevation(terrain[0], width, height, sharpness)    
	cmds.polyAverageVertex(iterations = smoothness)
	cmds.select(terrain)
	cmds.polySmooth()


#遮罩选区