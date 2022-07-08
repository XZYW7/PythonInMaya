from maya import cmds
import random
import math

def calculateSquareCentre( startXIndex, startYIndex, blockSize, width, terrainData, levelScale):
	#update the centre
	#levelScale=1.0
	terrainData[int(startXIndex+blockSize/2+(startYIndex+blockSize/2)*width)] = 0.25*( \
		terrainData[int(startXIndex           + startYIndex*width)] + \
		terrainData[int(startXIndex+blockSize + startYIndex*width)] + \
		terrainData[int(startXIndex           + (startYIndex+blockSize)*width)] + \
		terrainData[int(startXIndex+blockSize + (startYIndex+blockSize)*width)])+ math.sqrt(levelScale)*(random.random()-0.5)

def calculateDiamondCentre( startXIndex, startYIndex, blockSize, width, height, terrainData, levelScale):
	#update the diamond centre
	#levelScale=1.0
	tmp = 0
	count = 0
	if startXIndex>0:
		tmp = tmp + terrainData[int(startXIndex-blockSize+startYIndex*width)]
		count=count+1
	if startYIndex>0:
		tmp = tmp + terrainData[int(startXIndex+(startYIndex-blockSize)*width)]
		count=count+1
	if startXIndex<width-1:
		tmp = tmp + terrainData[int(startXIndex+blockSize+startYIndex*width)]
		count=count+1
	if startYIndex<height-1:
		tmp = tmp + terrainData[int(startXIndex+(startYIndex+blockSize)*width)]
		count=count+1
	terrainData[int(startXIndex+startYIndex*width)] = tmp/count + math.sqrt(levelScale)*(random.random()-0.5)


# the main code
cmds.select(all=True)
cmds.delete()

n = 5
subdx = subdy = 2 ** n 
width = height =  subdx + 1

terrain = cmds.polyPlane( axis=[0,1,0], w=10, h=10, sx=subdx, sy=subdy, ch=False)

terrainData = [0.0]*width*height
# the four corner
terrainData[0] = 0
terrainData[int(width-1)] = 0
terrainData[int((height-1)*width)] = 0
terrainData[int(height*width-1)] = 7

for i in range(n, 0, -1): # different resolution
    blockSize = 2**i
    # for each resolution level, we need to calculate the height level for many blocks
    # calculate the square centre
    num = 2**(n-i)
    for j in range(num):
        startXIndex = j * blockSize
        for k in range(num):
            startYIndex = k * blockSize
            calculateSquareCentre(startXIndex, startYIndex, blockSize, width, terrainData, 1.0*i/n)
    num = 2**(n-i+1)+1
    for j in range(num):
        startXIndex = j * blockSize/2
        for k in range(num):
            startYIndex = k * blockSize/2
            if (j+k)%2==1:
                calculateDiamondCentre(startXIndex, startYIndex, blockSize/2, width, height, terrainData, 1.0*i/n)
                
for i in range(height):
	for j in range(width):
		cmds.move(0, terrainData[i*width+j], 0, terrain[0]+".vtx["+str(i*width+j)+"]", r=True)
cmds.polySmooth(kb=False)
