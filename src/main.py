# -*- coding: utf-8 -*- 
'''
    Info: This is the entrance of our program. Everything begins here.
    We create GUI controller there, and call different functions.
''' 
# prepare packages for GUI
#from distutils.command.build import build
from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from maya import OpenMayaUI as omui
import shiboken2
from maya import cmds
from importlib import reload
import sys

# confirm the working dir.
def workingDir():
    '''
        Info: User chooses the working dir, and add it into sys.path.
        prepare the working dir for the next steps like importing files.
    '''
    dir = QtWidgets.QFileDialog.getExistingDirectory(None,"Please Choose the File folder","C:/")
    projectdir = dir
    dir += '/src'
    if not dir in sys.path:
        sys.path.append(dir)
        print("Adding the working path to sys.path")
    return dir, projectdir
WORKINGDIR,PROJECTDIR = workingDir()

# import other module based on adding working dir into sys.path
try:
    import lsystem as ls
    import terrain
    import TerrainGeneration as tg
    reload(ls)
    reload(terrain)
    reload(tg)
except:
    print('The working directory is wrong')

# make the mayaWindow parent of our GUI
def getMayaMainWindow():
    '''
        Info: get a ptr of the Mainwindow of Maya
    '''
    win = omui.MQtUtil_mainWindow()
    ptr = shiboken2.wrapInstance(int(win),QtWidgets.QMainWindow)
    return ptr

def getDock(name = 'LandscapeSystemDock'):
    '''
        Info: get the dock ptr of the window
    '''
    deleteDock(name)
    ctrl = cmds.workspaceControl(name, dockToMainWindow = ('right',1), label = "LandscapeSystem")
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = shiboken2.wrapInstance(int(qtCtrl),QtWidgets.QWidget)
    return ptr

def deleteDock(name = 'LandscapeSystemDock'):
    '''
        Info: delete the dock ptr
    '''
    if cmds.workspaceControl(name, query = True, exists = True):
        cmds.deleteUI(name)

class LandscapeSystem(QtWidgets.QWidget):
    '''
        Info: The GUI system, we create our gui and connect them with our functions.
    '''
    treeNumbers = [0,0,0]
    terrain = []
    flag = -1
    oceanColor = [0, 0.3, 0.84]
    terrainColor = [0.24, 0.17, 0.14]
    leaveColor = [0.05, 0.25, 0.0]
    def __init__(self, dock = False):
        '''
            Info: Constructor.
                1. point our GUI into parent Qtwidgets.
                2. build UI system
            Param:
                dock: do we need to attach our window into Maya window
        '''
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                cmds.deleteUI('LandscapeSystem')
            except:
                print('No previous GUI exists')
            
            parent = QtWidgets.QDialog(parent = getMayaMainWindow())

            parent.setObjectName('LandscapeSystem')
            parent.setWindowTitle('LandscapeSystem')

            layout = QtWidgets.QVBoxLayout(parent)

        super().__init__(parent = parent)
        self.buildUI()
        self.parent().layout().addWidget(self)# self.parent - QtWidgets.QtWidget Ptr - LandsystemDock
        if not dock:
            parent.show()

        # Initialization of some varieble
        
        # Create an ocean
        self.ocean = cmds.polyCube(d = 100, w=100, h=0.1)
        cmds.setAttr(self.ocean[0] + '.translateY', 1/2)

        # Create Ocean Material
        self.oceanColorNode = cmds.createNode('lambert',name = "oceanColor")
        cmds.setAttr( self.oceanColorNode+'.color',0, 0.3, 0.84)
        cmds.setAttr( self.oceanColorNode+'.transparency', 0.7,0.7,0.7)

        # Set Ocean Material
        oceanShape = pm.PyNode(self.ocean[0]).getShape()
        cmds.defaultNavigation(connectToExisting=True, destination=oceanShape+'.instObjGroups[0]', source='oceanColor')

        # Create Other Materials
        self.terrainColorNode = cmds.createNode('lambert',name = "terrainColor")
        cmds.setAttr( self.terrainColorNode+'.color', 0.24, 0.17, 0.14)

        self.leaveColorNode = cmds.createNode('lambert',name = "leaveColor")
        cmds.setAttr( self.leaveColorNode+'.color', 0.05, 0.25, 0.0)

        self.trunkColorNode = cmds.createNode('lambert',name = "trunkColor")
        cmds.setAttr( self.trunkColorNode+'.color', 0.15, 0.05, 0.0)

    def buildUI(self):
        '''
            Create the GUI system, and create drawback of the GUI

        '''
        # Main Layout
        layout = QtWidgets.QGridLayout(self)
        backImgLabel = QtWidgets.QLabel()
        backImgLabel.resize(500, 100)
        pix = QtGui.QPixmap(QtGui.QImage(PROJECTDIR + '/artefacts/Picture/backgroundImg.jpg')).scaled(backImgLabel.size())
        backImgLabel.setPixmap(pix)

        layout.addWidget(backImgLabel,0,0,1,6)
        # 1.Create Terrain

        # Choose Noise Type
        chooseNoiseBtn = QtWidgets.QPushButton('Choose Noise')
        chooseNoiseBtn.clicked.connect(self.chooseNoise)
        layout.addWidget(chooseNoiseBtn, 1, 0, 1, 3)
        
        # Choose Height Map
        choosePicBtn = QtWidgets.QPushButton('Choose HeightMap')
        choosePicBtn.clicked.connect(self.chooseHeightMap)
        layout.addWidget(choosePicBtn, 1, 3, 1, 3)
        
        # Choose absolute Height of the terrain

        # label of terrain
        labelTerrain = QtWidgets.QLabel('Adjust the Height of the terrain' )
        self.labelTerrainNum = QtWidgets.QLabel('7')
        layout.addWidget(self.labelTerrainNum, 3, 5, 1, 1)

        # heightBar
        self.absHeight = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.absHeight.setMinimum(0)
        self.absHeight.setMaximum(25)
        self.absHeight.setValue(7)
        self.absHeight.sliderReleased.connect(self.generateTerrain)
        layout.addWidget(labelTerrain, 2, 0, 1, 6)
        layout.addWidget(self.absHeight, 3, 0, 1, 5)

        self.terrainColorBtn = QtWidgets.QPushButton()
        self.terrainColorBtn.setMaximumWidth(20)
        self.terrainColorBtn.setMaximumHeight(20)
        self.setButtonColor(self.terrainColorBtn, self.terrainColor)
        self.terrainColorBtn.clicked.connect(self.setTerrainColor)
        layout.addWidget(self.terrainColorBtn, 3, 5)

        # 2.Create Ocean
        labelOcean = QtWidgets.QLabel('Adjust the Height of the Ocean' )
        self.labelOceanNum = QtWidgets.QLabel('0.1')
        layout.addWidget(self.labelOceanNum, 5, 5, 1, 1)
        self.oceanHeight = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.oceanHeight.setMinimum(0)
        self.oceanHeight.setMaximum(25)
        self.oceanHeight.setValue(0)
        self.oceanHeight.valueChanged.connect(self.createOcean)
        layout.addWidget(labelOcean, 4, 0, 1, 6)
        layout.addWidget(self.oceanHeight, 5, 0, 1, 5)
        
        self.oceanColorBtn = QtWidgets.QPushButton()
        self.oceanColorBtn.setMaximumWidth(20)
        self.oceanColorBtn.setMaximumHeight(20)
        self.setButtonColor(self.oceanColorBtn, self.oceanColor)
        self.oceanColorBtn.clicked.connect(self.setOceanColor)
        layout.addWidget(self.oceanColorBtn, 5, 5)

        # 3.Choose region by mask
        chooseMaskBtn = QtWidgets.QPushButton('Choose Mask')
        chooseMaskBtn.clicked.connect(self.chooseMask)
        layout.addWidget(chooseMaskBtn, 6, 0, 1, 6)


        buildTreeBtn = QtWidgets.QPushButton('Build Tree')
        buildTreeBtn.clicked.connect(self.buildTree)
        layout.addWidget(buildTreeBtn, 7,0,1,6)

        # 4.Choose the number of trees and leave color
        labelTree = QtWidgets.QLabel('Adjust the Number of 3 Kinds of Trees' )
        layout.addWidget(labelTree, 8, 0, 1, 5)

        self.leaveColorBtn = QtWidgets.QPushButton()
        self.leaveColorBtn.setMaximumWidth(20)
        self.leaveColorBtn.setMaximumHeight(20)
        self.setButtonColor(self.leaveColorBtn, self.leaveColor)
        self.leaveColorBtn.clicked.connect(self.setLeaveColor)
        layout.addWidget(self.leaveColorBtn, 8, 5)

        self.treeNumbers[0] = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.treeNumbers[0].setMinimum(0)
        self.treeNumbers[0].setMaximum(15)
        self.treeNumbers[0].setValue(8)
        layout.addWidget(self.treeNumbers[0], 9, 0, 1, 2)

        self.treeNumbers[1] = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.treeNumbers[1].setMinimum(0)
        self.treeNumbers[1].setMaximum(15)
        self.treeNumbers[1].setValue(8)
        layout.addWidget(self.treeNumbers[1], 9, 2, 1, 2)

        self.treeNumbers[2] = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.treeNumbers[2].setMinimum(0)
        self.treeNumbers[2].setMaximum(15)
        self.treeNumbers[2].setValue(8)
        layout.addWidget(self.treeNumbers[2], 9, 4, 1, 2)

        # 5.Distribute the trees on the terrain, you can't run this without creating the terrain and tree models
        distributeBtn = QtWidgets.QPushButton('Distribute')
        distributeBtn.clicked.connect(self.distribute)
        layout.addWidget(distributeBtn, 10, 0, 1, 6)


        # 6.Clear all models but ocean in the scene
        clearBtn = QtWidgets.QPushButton('Clear')
        clearBtn.clicked.connect(self.clear)
        layout.addWidget(clearBtn,11,0,1,6)

    # These functions are all drawback function of GUI
    def setLeaveColor(self):
        color = pm.colorEditor(rgbValue = self.leaveColor)
        r,g,b,a = [float(c) for c in color.split()]
        self.setButtonColor(self.leaveColorBtn,(r,g,b))
        cmds.setAttr(self.leaveColorNode+'.color',r,g,b)
    def setTerrainColor(self):
        color = pm.colorEditor(rgbValue = self.terrainColor)
        r,g,b,a = [float(c) for c in color.split()]
        self.setButtonColor(self.terrainColorBtn,(r,g,b))
        cmds.setAttr(self.terrainColorNode+'.color',r,g,b)
    def setOceanColor(self):
        color = pm.colorEditor(rgbValue = self.oceanColor)
        r,g,b,a = [float(c) for c in color.split()]
        self.setButtonColor(self.oceanColorBtn,(r,g,b))
        cmds.setAttr(self.oceanColorNode+'.color',r,g,b)
    def setButtonColor(self,Btn,color):
        print(color)
        r,g,b = [c*255 for c in color]
        Btn.setStyleSheet('background-color: rgba({},{},{},1.0)'.format(r,g,b))
        
    def chooseNoise(self):
        self.flag = 0
        self.generateTerrain()

    def chooseHeightMap(self):
        self.flag = 1
        self.heightMap = QtWidgets.QFileDialog.getOpenFileName(None, 
            "Choose the Height Map",WORKINGDIR, "Image Files(*.jpg *.png)")[0]
        print(self.heightMap)
        self.generateTerrain()
    def generateTerrain(self):
        if self.terrain:
            cmds.delete(self.terrain[0])
        self.labelTerrainNum.setText(str(self.absHeight.value()))

        print('generate Terrain')
        print(self.absHeight.value())
        if self.flag == 0:
            self.terrain = tg.NoiseMapTerrain(self.absHeight.value())
        elif self.flag == 1:
            
            self.terrain = tg.HeightMapTerrain(self.heightMap, self.absHeight.value())
            #print("There is something wrong with the image")
        else:
            print("Please Choose a kind of Terrian")
            return

        terrianShape = pm.PyNode(self.terrain[0]).getShape()
        cmds.defaultNavigation(connectToExisting=True, destination=terrianShape+'.instObjGroups[0]', source='terrainColor')

    def createOcean(self):
        self.labelOceanNum.setText(str(self.oceanHeight.value()))
        cmds.setAttr(self.ocean[1]+'.h',self.oceanHeight.value())
        cmds.setAttr(self.ocean[0] + '.translateY', self.oceanHeight.value()/2)
        print("ocean:", self.oceanHeight.value())
        print('create Ocean')

    def chooseMask(self):
        self.mask = QtWidgets.QFileDialog.getOpenFileName(None, 
            "Choose the Height Map",WORKINGDIR, "Image Files(*.jpg *.png)")
        print(self.mask[0])
        self.region = tg.AreaSelection(self.mask[0], self.flag, w=200, h=200)
        print(self.region)

    def buildTree(self):
        self.tree1 = ls.Lsystem('tree1')
        self.tree1.ruleSet = {}
        self.tree1.addRule('A', '"[&FFFLA]++++[&FFFLA]++++[&FFFLA]')
        self.tree1.ruleIter()
        self.tree1.drawModel()
        print(self.tree1.Tree)

        self.treeList = []
        self.treeList.append(self.tree1.Tree)
        print(self.treeList)

        self.tree2 = ls.Lsystem('tree2')
        self.tree2.widthRate = 0.8
        self.tree2.iterations = 4
        self.tree2.rotateAngle = 25
        self.tree2.ruleSet = {}
        
        self.tree2.addRule('A', '"F[&/FL/A][&\\FL\\A][^FL^A]A')
        self.tree2.addRule('F', 'FF')
        self.tree2.addRule('F', 'F[&/F/A][&\\F\\A]')
        self.tree2.ruleIter()
        self.tree2.drawModel(1)
        self.treeList.append(self.tree2.Tree)

        self.tree3 = ls.Lsystem('tree3')
        self.tree3.widthRate = 0.8
        self.tree3.iterations = 3
        self.tree3.rotateAngle = 25
        self.tree3.ruleSet = {}
        self.tree3.addRule('A', '[&FL"A]/////^[&FL"A]///////^[&FL"A]')
        self.tree3.addRule('F', 'S/////F')
        self.tree3.addRule('S', 'FL')
        self.tree3.ruleIter()
        self.tree3.drawModel()
        self.treeList.append(self.tree3.Tree)

        print(self.terrain)
        print(self.treeList)

    def distribute(self):
        print("distributing")
        print('wocaonima')
        terrain.generate(self.terrain[0], self.treeList, [self.treeNumbers[0].value(),self.treeNumbers[1].value(),self.treeNumbers[2].value()], self.region)

        for i in self.treeList:
            cmds.delete(i)
    def clear(self):
        cmds.select(all=True)
        cmds.delete()
        self.ocean = cmds.polyCube(d = 100, w=100, h=0.1)
        cmds.setAttr(self.ocean[0] + '.translateY', 1/2)
        # set Ocean Material

        self.oceanColorNode = cmds.createNode('lambert',name = "oceanColor")
        cmds.setAttr( self.oceanColorNode+'.color',0, 0.3, 0.84)
        cmds.setAttr( self.oceanColorNode+'.transparency', 0.7,0.7,0.7)

        oceanShape = pm.PyNode(self.ocean[0]).getShape()
        cmds.defaultNavigation(connectToExisting=True, destination=oceanShape+'.instObjGroups[0]', source='oceanColor')

        self.terrainColorNode = cmds.createNode('lambert',name = "terrainColor")
        cmds.setAttr( self.terrainColorNode+'.color', 0.24, 0.17, 0.14)

        self.leaveColorNode = cmds.createNode('lambert',name = "leaveColor")
        cmds.setAttr( self.leaveColorNode+'.color', 0.05, 0.25, 0.0)
        self.trunkColorNode = cmds.createNode('lambert',name = "trunkColor")
        cmds.setAttr( self.trunkColorNode+'.color', 0.15, 0.05, 0.0)
        self.terrain = ''
        self.treeNumbers = [0,0,0]
        self.flag = -1
if __name__ == "__main__":
    cmds.select(all=True)
    cmds.delete()
    ui = LandscapeSystem()
    ui.show()