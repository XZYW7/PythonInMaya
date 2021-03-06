'''
    This is Chen Longxuan's working space
    Completed 
    Generate terrain according to a height map
    Generate terrain according to noise map
    Select area according to a mask image
    Code is packaged into functions
'''

from maya import cmds
from PIL import Image
import os.path
import random
import math


# Generate terrain according to a height map
# The height map requires a square map with pixels less than 256*256, which can be a color map
def HeightMapTerrain(HeightMapImageFile, maxHeight):
    '''
    This is the function method that imports the height map to generate the terrain
    
    HeightMapImageFile: path to the height map
    '''
    print(HeightMapImageFile)
    if not os.path.isfile(HeightMapImageFile):
        print("image doesn't exist")
        exit()

    img = Image.open(HeightMapImageFile)  # Read the pictures
    img = img.convert('L')  # graying
    pixels = img.load()
    width, height = img.size 
    
    if width>255 or height>255 or width!=height:
        print("the image does not meet the requirements")
        exit()
    

    terrain = cmds.polyPlane( axis=[0,1,0], w=100, h=100, sx=width-1, sy=height-1)

    # change the vertex position of the plan according tot he terrainData
    for i in range(height):
        for j in range(width):
            cmds.move(0, pixels[j,i]/255.0 * maxHeight, 0, terrain[0]+".vtx["+str(i*width+j)+"]", r=True)
        cmds.refresh(f = True)
    return terrain

# Generate terrain according to noise map
def noiseMap(width, height, scale):
    noise = [[r for r in range(int(width))] for i in range(int(height))]

    for i in range(0,int(height)):
        for j in range(0,int(width)):
            noise[i][j] = scale * random.random() # (0.2,1]
    return noise

def Elevation(terrain, width, height, sharpness, maxHeight):
    noiseMap3 = noiseMap(width/4, height/4, 1.4)
    noiseMap2 = noiseMap(width/2, height/2, 1.2)
    noiseMap1 = noiseMap(width, height, 1.0)
    for y in range(height):
        for x in range(width):
            pointy = 1/1.4*noiseMap3[int(x/4)][int(y/4)]  + 1/1.2* noiseMap2[int(x/2)][int(y/2)] * 0.5  + noiseMap1[x][y] * 0.25
            pointy /= 1.75
            pointy = math.pow(pointy, sharpness)
            cmds.move(0, pointy * maxHeight, 0, terrain+".vtx["+str(y*width+x)+"]", r=True)
        cmds.refresh(f = True)
        
def NoiseMapTerrain(maxHeight):
    '''
        This is the method to generate terrain by using randomly generated noise map
    '''

    height=200
    width=200
    smoothness = 2
    sharpness = 6.0
    terrain = cmds.polyPlane( axis=[0,1,0], w=100, h=100, sx=width-1, sy=height-1)
    Elevation(terrain[0], width, height, sharpness, maxHeight)    
    cmds.polyAverageVertex(iterations = smoothness)
    cmds.polySmooth()
    return terrain


#Select area according to a mask image
    #If the terrain is generated by a height map, the mask image should have the same pixels as the height map and can be a color map
    #If the terrain is generated by noise map, the mask image requires 200*200 pixels and can be a color map
def AreaSelection(MaskImageFile, f, w=200, h=200):
    '''
    This is the function method that imports the mask to select area
    
    MaskImageFile: path to the mask
    f: The way terrain is generated
        "0" means using the height map to generate
        "1" means using the noise map to generate
    w: width of height map
    h: height of height map
    '''
    if not os.path.isfile(MaskImageFile):
        print("image doesn't exist")
        exit()
    
    img = Image.open(MaskImageFile)  # Read the pictures
    img = img.convert('1')  # Change the image to a bitmap
    pixels = img.load()
    width, height = img.size
    
    if (w!=width or h!=height):
        print("the image does not meet the requirements")
    
    chooseArea=[]
    for i in range(height):
        for j in range(width):
            if pixels[j,i]==0:
                chooseArea.append(1)
            else:
                chooseArea.append(0)
    return chooseArea