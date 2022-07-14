import maya.cmds as cmds
from random import uniform as rand

#------------ Initial Values -----------##
TerrName='My_Terrain'
RocName="My_Rock"
TerrWidth=200
TerrLenght=200
TerrSubW=100
TerrSubH=100
TerrHMin=-5
TerrHMax=20
ComponentType=0
SoftSel=True
MinRad=1
MaxRad=3
MaxRoc=30
MinX=-100
MaxX=100
MinY=-100
MaxY=100
MinZ=-100
MaxZ=100
GrpCheckBox=False
DropCheckBox=False
DiffObjCheckBox=False

######  Functions  #######

# TerrObjMaker Functions    
def TerrGenerator(*pArgs):
        cmds.polyPlane(n=TerrName,w=TerrWidth,h=TerrLenght,sw=TerrSubW,sh=TerrSubH)

# Terrain Deformation Functions    
def TerrDeformer(*pArgs):
    #Component conditions
    if cmds.objExists('My_Terrain'):
        if SoftSel==True:
            cmds.softSelect(sse=True,ssd=((TerrLenght+TerrWidth)/20))
            if ComponentType==0:
                cmds.ConvertSelectionToVertices()
                AllComp=cmds.ls(sl=True,fl=True)
            elif ComponentType==1:
                cmds.ConvertSelectionToEdges()
                AllComp=cmds.ls(sl=True,fl=True)
            elif ComponentType==2:
                cmds.ConvertSelectionToFaces()
                AllComp=cmds.ls(sl=True,fl=True)
            else:
                AllComp=cmds.ls(sl=True,fl=True)
             
            #at this point we are just deforming son
            for i in range (0,len(AllComp)):
                RandSelection=int(rand(0,len(AllComp)))
                cmds.select(cl=True)
                singleComp=AllComp[RandSelection]
                cmds.select(singleComp)
                RandH=rand(TerrHMin,TerrHMax)
                cmds.move(0,RandH,0,r=True)
            cmds.select(TerrName)   
            cmds.confirmDialog(t='It is done', m='Deformation completed',b=['Ok']) 
        else:
            cmds.softSelect(sse=False)
            if ComponentType==0:
                cmds.ConvertSelectionToVertices()
                AllComp=cmds.ls(sl=True,fl=True)
            elif ComponentType==1:
                cmds.ConvertSelectionToEdges()
                AllComp=cmds.ls(sl=True,fl=True)
            elif ComponentType==2:
                cmds.ConvertSelectionToFaces()
                AllComp=cmds.ls(sl=True,fl=True)
            else:
                AllComp=cmds.ls(sl=True,fl=True)
             
            #at this point we are just deforming son
            for i in range (0,len(AllComp)):
                RandSelection=int(rand(0,len(AllComp)))
                cmds.select(cl=True)
                singleComp=AllComp[RandSelection]
                cmds.select(singleComp)
                RandH=rand(TerrHMin,TerrHMax)
                cmds.move(0,RandH,0,r=True)
            cmds.select(TerrName)
            cmds.confirmDialog(t='It is done', m='Deformation completed',b=['Ok'])    
    else:
        cmds.confirmDialog(t='Object not found',m='Terrain not found. Create the Terrain first',b=['Ok'])
        
        
#Cancel Function
def cancel(*pArgs):
    if cmds.window('TerWindow',ex=True):
       cmds.deleteUI('TerWindow') 

# RocObjMaker Function
def RocObjMaker(*pArgs):
    cmds.softSelect(sse=False)
    if DropCheckBox==True:
        if GrpCheckBox==True:
            if cmds.objExists('TerrName'):
                cmds.ConvertSelectionToVertices()
                AllVerts=cmds.ls(sl=True,fl=True)
                cmds.select(deselect=True)
                cmds.group(n=RocName+'_Grp',empty=True)
                for rocks in range (0,MaxRoc+1):
                    Rnd=int(rand(0,len(AllVerts)))
                    Rad=rand(MinRad,MaxRad)
                    cmds.select(AllVerts[Rnd])
                    Location=cmds.pointPosition(w=True)
                    Rock=cmds.polySphere(n=RocName,r=Rad,sx=6,sh=6)
                    cmds.move(Location[0],Location[1],Location[2])
                    cmds.ConvertSelectionToVertices()
                    AllComps=cmds.ls(sl=True,fl=True)
                    for i in range(1,len(AllComps)):
                        MovX=rand(-MinRad/8,Rad/2)
                        MovY=rand(-MinRad/8,Rad/4)
                        MovZ=rand(-MinRad/10,Rad/4)
                        cmds.select(AllComps[i])
                        cmds.softSelect(sse=True,ssd=MinRad/5)
                        cmds.move(MovX,MovY,MovZ,r=True)
                        cmds.softSelect(sse=False)
                        cmds.displaySmoothness(divisionsU=3,divisionsV=3,pointsWire=16,pointsShaded=4,polygonObject=3)
                    cmds.select(RocName+'_Grp')
                    cmds.parent(Rock,RocName+'_Grp')
                cmds.select(RocName+'_Grp')
            else:
                cmds.error('Terrain not found. Create the Terrain or uncheck "put them on Terrain')
        else:
            if cmds.objExists(TerrName):
                cmds.select(TerrName)
                cmds.ConvertSelectionToVertices()
                AllVerts=cmds.ls(sl=True,fl=True)
                cmds.select(deselect=True)
                for rocks in range (0,MaxRoc+1):
                    Rnd=int(rand(0,len(AllVerts)))
                    Rad=rand(MinRad,MaxRad)
                    cmds.select(AllVerts[Rnd])
                    Location=cmds.pointPosition(w=True)
                    Rock=cmds.polySphere(n=RocName,r=Rad,sx=6,sh=6)
                    cmds.move(Location[0],Location[1],Location[2])
                    cmds.ConvertSelectionToVertices()
                    AllComps=cmds.ls(sl=True,fl=True)
                    cmds.softSelect(sse=True,ssd=MinRad/5)
                    for i in range(1,len(AllComps)):
                        MovX=rand(-MinRad/8,Rad/2)
                        MovY=rand(-MinRad/8,Rad/4)
                        MovZ=rand(-MinRad/10,Rad/4)
                        cmds.select(AllComps[i])
                        cmds.move(MovX,MovY,MovZ,r=True)
                        cmds.displaySmoothness(divisionsU=3,divisionsV=3,pointsWire=16,pointsShaded=4,polygonObject=3)
                    cmds.softSelect(sse=False)
                cmds.select(RocName) 
            else:
                cmds.confirmDialog(t='Not found', m='Could not find the Terrain object in your scene',b=['Check again'])
    else:
        if GrpCheckBox==True:
            cmds.group(n=RocName+'_Grp',empty=True)
            for rocks in range (0,MaxRoc+1):
                Rad=rand(MinRad,MaxRad)
                Rock=cmds.polySphere(n=RocName,r=Rad,sx=6,sh=6)
                LocX=rand(MinX,MaxX)
                LocY=rand(MinY,MaxY)
                LocZ=rand(MinZ,MaxZ)
                cmds.move(LocX,LocY,LocZ)
                cmds.ConvertSelectionToVertices()
                AllComps=cmds.ls(sl=True,fl=True)
                for i in range(1,len(AllComps)):
                    MovX=rand(-MinRad/8,Rad/2)
                    MovY=rand(-MinRad/8,Rad/4)
                    MovZ=rand(-MinRad/10,Rad/4)
                    cmds.select(AllComps[i])
                    cmds.softSelect(sse=True,ssd=MinRad/5)
                    cmds.move(MovX,MovY,MovZ,r=True)
                    cmds.softSelect(sse=False)
                    cmds.displaySmoothness(divisionsU=3,divisionsV=3,pointsWire=16,pointsShaded=4,polygonObject=3)
                cmds.select(RocName+'_Grp')
                cmds.parent(Rock,RocName+'_Grp')
            cmds.select(RocName+'_Grp')
        else:
            for rocks in range (0,MaxRoc+1):
                Rad=rand(MinRad,MaxRad)
                Rock=cmds.polySphere(n=RocName,r=Rad,sx=6,sh=6)
                LocX=rand(MinX,MaxX)
                LocY=rand(MinY,MaxY)
                LocZ=rand(MinZ,MaxZ)
                cmds.move(LocX,LocY,LocZ)
                cmds.ConvertSelectionToVertices()
                AllComps=cmds.ls(sl=True,fl=True)
                cmds.softSelect(sse=True,ssd=MinRad/5)
                for i in range(1,len(AllComps)):
                    MovX=rand(-MinRad/8,Rad/2)
                    MovY=rand(-MinRad/8,Rad/4)
                    MovZ=rand(-MinRad/10,Rad/4)
                    cmds.select(AllComps[i])
                    cmds.move(MovX,MovY,MovZ,r=True)
                    cmds.displaySmoothness(divisionsU=3,divisionsV=3,pointsWire=16,pointsShaded=4,polygonObject=3)
                cmds.softSelect(sse=False)
            cmds.select(RocName)
        

#-------Shader Function -------

def OpencolorMap(*pArgs):
    OpencolorMap.mapTypes="Image (*.jpg);;Bitmap (*.bmp);;PNG (*.png);; GIF (*.gif);; TIFF (*.gif);; All Files (*.*)"
    OpencolorMap.colorMap_path=cmds.fileDialog2(fileFilter=OpencolorMap.mapTypes, fileMode=1 , dialogStyle=2)
    print('the color map path is:',OpencolorMap.colorMap_path[0])

def OpennormalMap(*pArgs):
    OpennormalMap.mapTypes="Image (*.jpg);;Bitmap (*.bmp);;PNG (*.png);; GIF (*.gif);; TIFF (*.gif);; All Files (*.*)"
    OpennormalMap.normalMap_path=cmds.fileDialog2(fileFilter=OpennormalMap.mapTypes, fileMode=1 , dialogStyle=2)
    print('the normal map path is:',OpennormalMap.normalMap_path[0])
    
def OpenspecMap(*pArgs):
    OpenspecMap.mapTypes="Image (*.jpg);;Bitmap (*.bmp);;PNG (*.png);; GIF (*.gif);; TIFF (*.gif);; All Files (*.*)"
    OpenspecMap.specMap_path=cmds.fileDialog2(fileFilter=OpenspecMap.mapTypes, fileMode=1 , dialogStyle=2)
    print('the normal map path is:',OpenspecMap.specMap_path[0])


def TerrShader(*pArgs):
    TerShader=cmds.shadingNode("blinn",n=TerShaderName,asShader=True)
    colorMap_node=cmds.shadingNode("file",n='Color Map',asTexture=True)
    file=OpencolorMap.colorMap_path[0]
    cmds.setAttr(colorMap_node+".fileTextureName",file,type='string')
    cmds.connectAttr(colorMap_node+".outColor",TerShader+".color")
    Ter2Dplacer=cmds.shadingNode("place2dTexture",n="TerTxtPlacer",asUtility=True)
    cmds.connectAttr(Ter2Dplacer+".outUV",colorMap_node+".uvCoord")
    
    Normal_node=cmds.shadingNode("file",n='Normal Map',asTexture=True)
    NMfile=OpennormalMap.normalMap_path[0]
    cmds.setAttr(Normal_node+".fileTextureName",NMfile,type='string')
    cmds.connectAttr(Normal_node+".outColor",TerShader+".normalCamera")
    cmds.connectAttr(Ter2Dplacer+".outUV",Normal_node+".uvCoord")
      
    Spec_node=cmds.shadingNode("file",n='Specular Map',asTexture=True)
    SPfile=OpenspecMap.specMap_path[0]
    cmds.setAttr(Spec_node+".fileTextureName",SPfile,type='string')
    cmds.connectAttr(Spec_node+".outColor",TerShader+".specularColor")
    cmds.connectAttr(Ter2Dplacer+".outUV",Spec_node+".uvCoord")
    
    if TerrSel==True:
        SelList=cmds.ls(sl=True,o=True)
        for i in range(0,len(SelList)):
            cmds.select(SelList[0])
            cmds.hyperShade(assign=SelList[i])
       
    else:
        cmds.hyperShade(assign=TerShaderName)


    
    
#----------------- Warning Window ------------------

cmds.confirmDialog(t='Just before start',message='Please press the "Enter" button in each field\n -----> Please change all fields <-----',b=["Ok"])

#########  --------------------   Start of UI ---------------------------- #########

if cmds.window('TerWindow', exists=True):
    cmds.deleteUI('TerWindow')
cmds.window('TerWindow', title='Terrain Generator', sizeable=False,rtf=True)
cmds.rowColumnLayout(adjustableColumn=True,nc=2,columnWidth=[(1,130),(2,300)],columnOffset=[(1,'right',5),(2,'left',5)])

cmds.separator(h=10,style='none')
cmds.separator(h=10,style='none')

cmds.text(label='--> Terrain Object <--',al='right')
cmds.text(label='          ---  Please hit "Enter" in each field  ---  ',al='right')

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Name of Terrain:')
TerrNameUI=cmds.textField(text='My_Terrain',cc="TerrName=cmds.textField(TerrNameUI,q=True,tx=True)")

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')
# Terrain Dimensions
cmds.text(label='Terrain Width:')
TerrWidthUI=cmds.floatSliderGrp(v=200,maxValue=800,f=True,cc="TerrWidth=cmds.floatSliderGrp(TerrWidthUI,q=True,v=True)")

cmds.text(label='Terrain Lenght:')
TerrLenghtUI=cmds.floatSliderGrp(v=200,f=True,maxValue=800,cc="TerrLenght=cmds.floatSliderGrp(TerrWidthUI,q=True,v=True)")

#Terrain Subdivisions
cmds.text(label='Width Subdivisions:')
TerrSubWUI=cmds.intSliderGrp(minValue=1, maxValue=200, value=100,f=True,cc="TerrSubW=cmds.intSliderGrp(TerrSubWUI,query=True,v=True)")

cmds.text(label='Lenght Subdivisions:')
TerrSubHUI=cmds.intSliderGrp(minValue=1, maxValue=200, value=100,f=True,cc="TerrSubH=cmds.intSliderGrp(TerrSubHUI,query=True,v=True)")

# Create button
cmds.separator(h=20,style='none')
cmds.button(label='Create it now',align='left',w=120,h=20,command=TerrGenerator)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

#Cancel Button
cmds.separator(h=20,style='none')
cmds.button(label='Cancel',align='right',w=70,h=20,command=cancel)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

# ----- Deformation Section -----#
cmds.text(label='-->Deformation<--',al='center')
cmds.text(label='       ---- 10% of Terrain dimension is optimum for peaks ----',al='center')

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Depth of Valley:')
TerrHMinUI=cmds.floatSliderGrp(v=-5,minValue=-200, maxValue=0,f=True,cc="TerrHMin=cmds.floatSliderGrp(TerrHMinUI,q=True,v=True)")

cmds.text(label='Height of Peaks:')
TerrHMaxUI=cmds.floatSliderGrp(v=20,minValue=0, maxValue=500,f=True,cc="TerrHMax=cmds.floatSliderGrp(TerrHMaxUI,q=True,v=True)")
cmds.text(label='Component Type:')
cmds.radioCollection()
cmds.radioButton(l="Vertex",cc="ComponentType=0",sl=True)
cmds.separator(h=5,style='none')
cmds.radioButton(l="Edge",cc="ComponentType=1")
cmds.separator(h=5,style='none')
cmds.radioButton(l="Face",cc="ComponentType=2")
cmds.separator(h=5,style='none')
cmds.radioButton(l="User Selection",cc="ComponentType=4")
cmds.separator(h=5,style='none')

cmds.separator(h=10,style='none')
cmds.separator(h=10,style='none')

SoftSelUI=cmds.checkBox(label='Soft Selection',v=True,cc='SoftSel=cmds.checkBox(SoftSelUI,q=True,v=True)')
cmds.separator(h=5,style='none')

cmds.separator(h=10,style='none')
cmds.separator(h=10,style='none')
cmds.button(label='Deform it',align='left',w=120,h=20,command=TerrDeformer)


# -----------------------   Rock Generation Section  --------------------------


cmds.text(label='-->Rock Generation<--')
cmds.separator(w=280)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Rock Object Name:')
RocNameUI=cmds.textField(text="My_Rock",cc="RocName=cmds.textField(RocNameUI,q=True,tx=True)")

cmds.text(label='Min Radius')
MinRadUI=cmds.floatSliderGrp(minValue=0.01, maxValue=200, value=1,f=True,cc="MinRad=cmds.floatSliderGrp(MinRadUI,q=True,v=True)")

cmds.text(label='Max Radius')
MaxRadUI=cmds.floatSliderGrp(minValue=0.01, maxValue=200, value=3,f=True,cc="MaxRad=cmds.floatSliderGrp(MaxRadUI,q=True,v=True)")

cmds.text(label='Number of Rocks:')
MaxRocUI=cmds.intSliderGrp(minValue=1, maxValue=100, value=30,f=True,cc="MaxRoc=cmds.intSliderGrp(MaxRocUI,q=True,v=True)")

cmds.text(label='"X" axis (Min):')
MinXUI=cmds.floatSliderGrp(minValue=-500, maxValue=-1, value=-100,f=True,cc="MinX=cmds.floatSliderGrp(MinXUI,q=True,v=True)")

cmds.text(label='"X" axis (Max):')
MaxXUI=cmds.floatSliderGrp(minValue=1, maxValue=500, value=100,f=True,cc="MaxX=cmds.floatSliderGrp(MaxXUI,q=True,v=True)")

cmds.text(label='"Y" axis (Min):')
MinYUI=cmds.floatSliderGrp(minValue=-500, maxValue=-1, value=-100,f=True,cc="MinY=cmds.floatSliderGrp(MinYUI,q=True,v=True)")

cmds.text(label='"Y" axis (Max):')
MaxYUI=cmds.floatSliderGrp(minValue=1, maxValue=500, value=100,f=True,cc="MaxY=cmds.floatSliderGrp(MaxYUI,q=True,v=True)")

cmds.text(label='"Z" axis (Min)')
MinZUI=cmds.floatSliderGrp(minValue=-500, maxValue=-1, value=10,f=True,cc="MinZ=cmds.floatSliderGrp(MinZUI,q=True,v=True)")

cmds.text(label='"Z" axis (Max)')
MaxZUI=cmds.floatSliderGrp(minValue=1, maxValue=500, value=10,f=True,cc="MaxZ=cmds.floatSliderGrp(MaxZUI,q=True,v=True)")

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.separator(h=5,style='none')
GrpCheckBoxUI=cmds.checkBox(label='Group the Rocks',v=False,cc='GrpCheckBox=cmds.checkBox(GrpCheckBoxUI,q=True,v=True)')

cmds.separator(h=5,style='none')
DropCheckBoxUI=cmds.checkBox(label='Put them on Terrain',v=False,cc='DropCheckBox=cmds.checkBox(DropCheckBoxUI,q=True,v=True)')

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.separator(h=20,style='none')
cmds.button(label='Create Rocks',al='left',w=120,h=20,command=RocObjMaker)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

#Shader Section
cmds.text(label='--> Terrain Shader <--')
cmds.separator(w=280)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Shader Name :')
TerShaderNameUI=cmds.textField(text='Enter a name',cc="TerShaderName=cmds.textField(TerShaderNameUI,q=True,tx=True)")

cmds.separator(h=5,style='none')
TerrSelUI=cmds.checkBox(label='I have Selected different object',v=True,cc='TerrSel=cmds.checkBox(TerrSelUI,q=True,v=True)')

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Add Color Map :')
cmds.button(label='Browse',align='left',w=120,h=20,command=OpencolorMap)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Add Normal Map :')
cmds.button(label='Browse',align='left',w=120,h=20,command=OpennormalMap)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.text(label='Add Specular Map :')
cmds.button(label='Browse',align='left',w=120,h=20,command=OpenspecMap)

cmds.separator(h=5,style='none')
cmds.separator(h=5,style='none')

cmds.separator(h=5,style='none')
cmds.button(label='Assign the Shader to Terrain',align='left',w=170,h=25,command=TerrShader)

cmds.separator(h=20,style='none')
cmds.separator(h=20,style='none')


  
cmds.showWindow('TerWindow')