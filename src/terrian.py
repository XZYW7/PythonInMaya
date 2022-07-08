'''
    This is Xu Zhehao's working space
'''

import maya.cmds as cmds
import random as rand
import math 

terrainShape ='terrain'
treeNames = ["cow", "wolf"]     #输入的值，各个树的名称
treeNumbers=[50,20]     #输入的值，各个树的数量
treeData = {}
x=60
z=66
x-=1    #把开始下标从1改为0
z-=1
isAngle=True      #是否按角度倾斜，为输入的�?

for i in range(len(treeNames)):     #把树的名称和数量合成字典
    treeData[treeNames[i]]=treeNumbers[i]

numVertex = cmds.polyEvaluate(terrainShape, vertex=True)        #计算地面定点数量
chooseNumber=0      #记录选中的顶点的数量
chooseArea=[]       #记录选中区域的列表，选中�??1，不选中�??0，是输入，要改到前面�??
for i in range(numVertex):
    if 800<i<2000:
      t=1
    else:
      t=0
    chooseArea.append(t)     #随机生成01，后面要删掉
    if chooseArea[i]==1:
        chooseNumber +=1

#selectedVertices = rand.sample(range(numVertex), numVertex)     #随机生成一个定点序号range随机排列的列�??

currentIndex = 0        #现在种到第几棵树

for pair in treeData.items():       #遍历各个树模�??
  i=0
  while i < pair[1]:
      currentX=rand.random()*x    #在平面上随机选取一个点的x、z坐标
      currentZ=rand.random()*z
      #找到这个点周围四个点，因为random不会取到1所以不会出边界
      l1=int(currentZ)*(x+1)+int(currentX)    #左上
      l2=int(currentZ)*(x+1)+int(currentX)+1    #右上
      l3=int(currentZ+1)*(x+1)+int(currentX)    #左下
      l4=int(currentZ+1)*(x+1)+int(currentX)+1    #右下
      #检验这个点是否在框内
      k=0
      point=-1    #如果是3个点被选中，用于记录那个未被选中的点是哪个
      for t in [l1,l2,l3,l4]:
        if chooseArea[t]==1:
          k+=1
        else:
          point=t
      d1=math.sqrt((currentX-int(currentX))**2+(currentZ-int(currentZ))**2)
      d2=math.sqrt((1-currentX+int(currentX))**2+(currentZ-int(currentZ))**2)
      d3=math.sqrt((currentX-int(currentX))**2+(1-currentZ+int(currentZ))**2)
      d4=math.sqrt((1-currentX+int(currentX))**2+(1-currentZ+int(currentZ))**2)

      if k<=2:    #两个点及以下，不在框内，跳过
        continue
      elif k==3:    #需要计算和四个点的距离，判断是否在三角内
        if (point==l1 and d1<d4) or (point==l4 and d1>d4) or (point==l2 and d2<d3) or (point==l3 and d2>d3):
          continue

      #判断完在区域内后，开始放置树木
      pos1 = cmds.pointPosition (terrainShape+".vtx["+str(l1)+"]", world=True)       #获取该顶点世界坐�??
      pos2 = cmds.pointPosition (terrainShape+".vtx["+str(l2)+"]", world=True)
      pos3 = cmds.pointPosition (terrainShape+".vtx["+str(l3)+"]", world=True)
      pos4 = cmds.pointPosition (terrainShape+".vtx["+str(l4)+"]", world=True)
      #posFirst = cmds.pointPosition (terrainShape+".vtx["+str(0)+"]", world=True)
      #posLast = cmds.pointPosition (terrainShape+".vtx["+str(numVertex-1)+"]", world=True)
      posY=pos1[1]*d4/(d1+d4)+pos4[1]*d1/(d1+d4)
      newobj = cmds.instance(pair[0])
      posX=((pos2[0]-pos1[0])*(currentX-int(currentX))+pos1[0])*(1-currentZ+int(currentZ))+((pos4[0]-pos3[0])*(currentX-int(currentX))+pos3[0])*(currentZ-int(currentZ))
      posZ=((pos3[2]-pos1[2])*(currentZ-int(currentZ))+pos1[2])*(1-currentX+int(currentX))+((pos4[2]-pos2[2])*(currentZ-int(currentZ))+pos2[2])*(currentX-int(currentX))
      #posZ=posFirst[2]+(posLast[2]-posFirst[2])*(currentZ/z)
      cmds.move(posX,posY,posZ,newobj)        #将模型移动到顶点位置
      
      if not isAngle:
        cmds.rotate(0, rand.randint(0,360),0,newobj)      #y轴随机旋�?
      else:
        cmds.select(terrainShape+".vtx["+str(l1)+"]",r=True)
        ang1=cmds.polyNormalPerVertex( query=True, xyz=True )
        cmds.select(terrainShape+".vtx["+str(l2)+"]",r=True)
        ang2=cmds.polyNormalPerVertex( query=True, xyz=True )
        cmds.select(terrainShape+".vtx["+str(l3)+"]",r=True)
        ang3=cmds.polyNormalPerVertex( query=True, xyz=True )
        cmds.select(terrainShape+".vtx["+str(l4)+"]",r=True)
        ang4=cmds.polyNormalPerVertex( query=True, xyz=True )
        #有时候是6个值，重复两遍，有的时候是12个值，重复4遍，不知道为�?
        ang=[]
        ang.append((ang1[0]+ang2[0]+ang3[0]+ang4[0])/4)
        ang.append((ang1[1]+ang2[1]+ang3[1]+ang4[1])/4)
        ang.append((ang1[2]+ang2[2]+ang3[2]+ang4[2])/4)
        cmds.rotate(math.asin(ang[2])/math.pi*180, 0,-math.asin(ang[0])/math.pi*180,newobj, os = True)
        cmds.rotate(rand.randint(0,360),newobj,y=True,relative = True, os = True)

      currentIndex+=1
      i+=1