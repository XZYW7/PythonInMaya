'''
    This is Xu Zhehao's working space
    Completed:
      Trees range on the surface in chosen region according to the 01 Matrix,
      The y axis of trees rotates randomly, they are perpendicular with ground or surface.
      Collision Detection of the models of trees. If launched, prevent trees from intersection. 
'''

import maya.cmds as cmds
import random
import math 

def setTree(terrainShape,treeNames,treeNumbers,x,z,isAngle,isAvoidBounding,chooseArea,*others):
  '''
  this is the function to set the trees to the ground

  terrainShape: the name of the gournd
  treeNames: a list of the names of trees
  treeNumbers: a list of the numbers of trees
  x: the number of vertexs of the ground on the x-axis
  z: the number of vertexs of the ground on the z-axis
  isAngle: judge whether it is inclined according to the normal of the ground
  isAvoidBounding: judge whether to avoid tree intersection while setting
  chooseArea: a list that uses 0 and 1 to record whether each vertex of the ground is chosen to plant trees or not
  '''

  treeData = {} 
  x-=1    #把开始下标从1改为0
  z-=1
  currentIndex = 0        #现在种到第几棵树
  boundBox=[]   #用来记录每棵树的位置和边界尺寸，检测是否会相交

  for i in range(len(treeNames)):     #把树的名称和数量合成字典
    treeData[treeNames[i]]=treeNumbers[i]
  numVertex = cmds.polyEvaluate(terrainShape, vertex=True)        #计算地面定点数量

  for pair in treeData.items():       #遍历各个树模�??
    i=0
    while i < pair[1]:
        currentX=random.random()*x    #在平面上随机选取一个点的x、z坐标
        currentZ=random.random()*z

        l1,l2,l3,l4=find4Point(currentX,currentZ,x)

        d1,d2,d3,d4=distance4Point(currentX,currentZ)
        
        isInArea=checkArea(l1,l2,l3,l4,chooseArea,d1,d2,d3,d4)
        if not isInArea:
          continue

        #判断完在区域内后，开始放置树木
        pos1 = cmds.pointPosition (terrainShape+".vtx["+str(l1)+"]", world=True)       #获取该顶点世界坐�??
        pos2 = cmds.pointPosition (terrainShape+".vtx["+str(l2)+"]", world=True)
        pos3 = cmds.pointPosition (terrainShape+".vtx["+str(l3)+"]", world=True)
        pos4 = cmds.pointPosition (terrainShape+".vtx["+str(l4)+"]", world=True)
        posY=pos1[1]*d4/(d1+d4)+pos4[1]*d1/(d1+d4)
        posX=((pos2[0]-pos1[0])*(currentX-int(currentX))+pos1[0])*(1-currentZ+int(currentZ))+((pos4[0]-pos3[0])*(currentX-int(currentX))+pos3[0])*(currentZ-int(currentZ))
        posZ=((pos3[2]-pos1[2])*(currentZ-int(currentZ))+pos1[2])*(1-currentX+int(currentX))+((pos4[2]-pos2[2])*(currentZ-int(currentZ))+pos2[2])*(currentX-int(currentX))
        
        newobj = cmds.instance(pair[0])
        cmds.move(posX,posY,posZ,newobj)        #将模型移动到顶点位置

        if not isAngle:
          cmds.rotate(0, random.randint(0,360),0,newobj)      #y轴随机旋�?
        else:
          ang=noraml4Point(l1,l2,l3,l4,terrainShape)
          cmds.rotate(math.asin(ang[2])/math.pi*180, 0,-math.asin(ang[0])/math.pi*180,newobj, os = True)
          cmds.rotate(random.randint(0,360),newobj,y=True,relative = True, os = True)

        #判断是否和其他树相交
        if isAvoidBounding:
          posSize=cmds.exactWorldBoundingBox(newobj,ce=True)    #检测当前树模型的xyz尺寸
          isBounding=boundingCheck(boundBox,posSize)
          if isBounding:
            cmds.select(newobj)
            cmds.delete()
            continue
          else:
            boundBox.append([posSize[0],posSize[3],posSize[2],posSize[5]])

        currentIndex+=1
        i+=1


def  find4Point(currentX,currentZ,x,*others):
  '''
  this is the function to find the number of the 4 vertexs on the ground around the point

  currentX: the x coordinate of the point
  currentZ: the z coordinate fo the point
  x: the number of vertexs of the ground on the x-axis
  '''
  p1=int(currentZ)*(x+1)+int(currentX)    #左上
  p2=int(currentZ)*(x+1)+int(currentX)+1    #右上
  p3=int(currentZ+1)*(x+1)+int(currentX)    #左下
  p4=int(currentZ+1)*(x+1)+int(currentX)+1    #右下
  return p1,p2,p3,p4


def checkArea(l1,l2,l3,l4,chooseArea,d1,d2,d3,d4,*others):
  '''
  this is the function to check whether the point is in the chosen area

  l1,l2,l3,l4: the number of the 4 vertexs on the ground around the point
  chooseArea: a list that uses 0 and 1 to record whether each vertex of the ground is chosen to plant trees or not
  d1,d2,d3,d4: the distance between the point and 4 vertexs
  '''
  flag=True
  k=0
  point=-1    #如果是3个点被选中，用于记录那个未被选中的点是哪个
  for t in [l1,l2,l3,l4]:
    if chooseArea[t]==1:
      k+=1
    else:
      point=t
  
  if k<=2:    #两个点及以下，不在框内，跳过
    flag=False
  elif k==3:    #需要计算和四个点的距离，判断是否在三角内
    if (point==l1 and d1<d4) or (point==l4 and d1>d4) or (point==l2 and d2<d3) or (point==l3 and d2>d3):
      flag=False
  return flag


def distance4Point(currentX,currentZ,*others):
  '''
  this is the function to calculate the distance between the point and 4 vertexs

  currentX: the x coordinate of the point
  currentZ: the z coordinate fo the point
  '''
  dis1=math.sqrt((currentX-int(currentX))**2+(currentZ-int(currentZ))**2)
  dis2=math.sqrt((1-currentX+int(currentX))**2+(currentZ-int(currentZ))**2)
  dis3=math.sqrt((currentX-int(currentX))**2+(1-currentZ+int(currentZ))**2)
  dis4=math.sqrt((1-currentX+int(currentX))**2+(1-currentZ+int(currentZ))**2)
  return dis1,dis2,dis3,dis4


def noraml4Point(l1,l2,l3,l4,terrainShape,*others):
  '''
  this is the function to calculate the average normal vector of the 4 vertexs

  l1,l2,l3,l4: the number of the 4 vertexs on the ground around the point
  terrainShape: the name of the gournd
  '''
  cmds.select(terrainShape+".vtx["+str(l1)+"]",r=True)
  ang1=cmds.polyNormalPerVertex( query=True, xyz=True )
  cmds.select(terrainShape+".vtx["+str(l2)+"]",r=True)
  ang2=cmds.polyNormalPerVertex( query=True, xyz=True )
  cmds.select(terrainShape+".vtx["+str(l3)+"]",r=True)
  ang3=cmds.polyNormalPerVertex( query=True, xyz=True )
  cmds.select(terrainShape+".vtx["+str(l4)+"]",r=True)
  ang4=cmds.polyNormalPerVertex( query=True, xyz=True )
  ang=[]
  ang.append((ang1[0]+ang2[0]+ang3[0]+ang4[0])/4)
  ang.append((ang1[1]+ang2[1]+ang3[1]+ang4[1])/4)
  ang.append((ang1[2]+ang2[2]+ang3[2]+ang4[2])/4)
  return ang


def boundingCheck(boundBox,posSize,*others):
  '''
  this is the funciton to check the tree intersection

  boundBox: a list that contains the xyz size positions of the trees
  posSize: the xyz size position of the current tree
  '''
  isBounding=False
  if boundBox!=[]:
    for tree in boundBox:
      if tree[0]<=posSize[3] and tree[1]>=posSize[0]:   #如果xmin<xmax且xmax>xmin，说明x轴有相交
        if tree[2]<=posSize[5] and tree[3]>=posSize[2]:   #z轴相交
          isBounding=True
          break
  return isBounding

def generate():
  terrainShape ='terrain'
  treeNames = ["cow", "wolf"]     #输入的值，各个树的名称
  treeNumbers=[50,20]     #输入的值，各个树的数量
  isAngle=True      #是否按角度倾斜，为输入的�?
  isAvoidBounding=True    #防止交集碰撞盒选项
  x=60
  z=66
  numVertex = cmds.polyEvaluate(terrainShape, vertex=True)        #计算地面定点数量
  chooseArea=[]       #记录选中区域的列表，选中�??1，不选中�??0，是输入，要改到前面�??
  for i in range(numVertex):
      if 800<i<2000:
        t=1
      else:
        t=0
      chooseArea.append(t)     #随机生成01，后面要删掉

  setTree(terrainShape,treeNames,treeNumbers,x,z,isAngle,isAvoidBounding,chooseArea)