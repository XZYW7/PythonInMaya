from maya import cmds
import random
import math

def noiseMap(width, height, scale):
    noise = [[r for r in range(int(width))] for i in range(int(height))]

    for i in range(0,int(height)):
        for j in range(0,int(width)):
            noise[i][j] = scale * (random.random()*0.8+0.2) # (0,1]
    return noise

def Elevation(terrain, width, height, sharpness):
	noiseMap3 = noiseMap(width/4, height/4, 1.4)
	noiseMap2 = noiseMap(width/2, height/2, 1.2)
	noiseMap1 = noiseMap(width, height, 1.0)
	for y in range(height):
		for x in range(width):
			pointy = noiseMap3[int(x/4)][int(y/4)] + 0.4* noiseMap2[int(x/2)][int(y/2)] + 0.2* noiseMap1[x][y]
			pointy = math.pow(pointy, sharpness)
			cmds.move(0, pointy*0.08, 0, terrain+".vtx["+str(y*width+x)+"]", r=True)
		cmds.refresh(f = True)
    
if __name__ == "__main__":
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