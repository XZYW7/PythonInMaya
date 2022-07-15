# -*- coding: utf-8 -*- 
'''
    Info: This is the entrance of our program. Everything begins here.
    We create GUI controller there, and call different functions.
''' 
# prepare packages for GUI
from distutils.command.build import build
from PySide2 import QtWidgets, QtCore, QtGui
# import pymel.core as pm
from functools import partial
from maya import OpenMayaUI as omui
import shiboken2
from PySide2.QtCore import Signal

from maya import cmds
from importlib import reload
import os,sys

# confirm the working dir.
def workingDir():
    '''
        Info: User chooses the working dir, and add it into sys.path.
        prepare the working dir for the next steps like importing files.
    '''
    dir = QtWidgets.QFileDialog.getExistingDirectory(None,"Please Choose the File folder","C:/")
    dir += '/src'
    if not dir in sys.path:
        sys.path.append(dir)
        print("Adding the working path to sys.path")
WORKINGDIR = workingDir()

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
    win = omui.MQtUtil_mainWindow()
    ptr = shiboken2.wrapInstance(int(win),QtWidgets.QMainWindow)
    return ptr

def getDock(name = 'LandscapeSystemDock'):
    deleteDock(name)
    ctrl = cmds.workspaceControl(name, dockToMainWindow = ('right',1), label = "LandscapeSystem")
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = shiboken2.wrapInstance(int(qtCtrl),QtWidgets.QWidget)
    return ptr

def deleteDock(name = 'LandscapeSystemDock'):
    if cmds.workspaceControl(name, query = True, exists = True):
        cmds.deleteUI(name)

class LandscapeSystem(QtWidgets.QWidget):
    '''
        Info: The GUI system, we create our gui and connect them with our functions.
    '''
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

        self.ocean = cmds.polyCube(d = 150, w=150, h=0.01)
        self.terrain = []
        cmds.setAttr(self.ocean[0] + '.translateY', 1/2)
    def buildUI(self):
        '''
            Create the UI system

        '''
        # Main Layout
        layout = QtWidgets.QGridLayout(self)

        # 1.Create Terrain

        # Choose Noise Type
        chooseNoiseBtn = QtWidgets.QPushButton('Choose Noise')
        chooseNoiseBtn.clicked.connect(self.chooseNoise)
        layout.addWidget(chooseNoiseBtn, 0, 0, 1, 1)
        
        # Choose Height Map
        choosePicBtn = QtWidgets.QPushButton('Choose HeightMap')
        choosePicBtn.clicked.connect(self.chooseHeightMap)
        layout.addWidget(choosePicBtn, 0, 1, 1, 1)
        
        # Choose absolute Height of the terrain
        self.absHeight = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.absHeight.setMinimum(0)
        self.absHeight.setMaximum(25)
        self.absHeight.setValue(7)
        self.absHeight.sliderReleased.connect(self.generateTerrain)
        layout.addWidget(self.absHeight, 1, 0, 1, 2)


        # 2.Create Ocean
        self.oceanHeight = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.oceanHeight.setMinimum(0)
        self.oceanHeight.setMaximum(100)
        self.oceanHeight.setValue(0)
        self.oceanHeight.valueChanged.connect(self.createOcean)
        layout.addWidget(self.oceanHeight, 2, 0, 1, 2)
        

        # 3.Choose region by mask
        chooseMaskBtn = QtWidgets.QPushButton('Choose Mask')
        chooseMaskBtn.clicked.connect(self.chooseMask)
        layout.addWidget(chooseMaskBtn, 3, 0, 1, 2)


        buildTreeBtn = QtWidgets.QPushButton('Build Tree')
        buildTreeBtn.clicked.connect(self.buildTree)
        layout.addWidget(buildTreeBtn, 4,0,1,1)

        distributeBtn = QtWidgets.QPushButton('Distribute')
        distributeBtn.clicked.connect(self.distribute)
        layout.addWidget(distributeBtn, 4, 1, 1, 1)


        # Clear
        clearBtn = QtWidgets.QPushButton('Clear')
        clearBtn.clicked.connect(self.clear)
        layout.addWidget(clearBtn,5,0,1,2)
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
    
        print('generate Terrain')
        print(self.absHeight.value())
        if self.flag == 0:
            self.terrain = tg.NoiseMapTerrain(self.absHeight.value())
        else:
            
            self.terrain = tg.HeightMapTerrain(self.heightMap, self.absHeight.value())
            #print("There is something wrong with the image")

    def createOcean(self):
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
        self.tree2.iterations = 5
        self.tree2.ruleSet = {}
        self.tree2.addRule('A', '"[&FFFA]++++[&FFFA]++++[&FFFA]')
        self.tree2.addRule('F', '"FF')
        self.tree2.addRule('F', 'F[/F]')
        self.tree2.addRule('F', 'F[\F]')
        self.tree2.ruleIter()
        self.tree2.drawModel()

        self.treeList.append(self.tree2.Tree)
        print(self.terrain)
        print(self.treeList)
    def distribute(self):
        print("distributing")
        print('wocaonima')
        terrain.generate(self.terrain[0], self.treeList, self.region)

        cmds.delete(self.tree1.Tree)
        cmds.delete(self.tree2.Tree)
    def clear(self):
        cmds.select(all=True)
        cmds.delete()
if __name__ == "__main__":
    cmds.select(all=True)
    cmds.delete()
    ui = LandscapeSystem()
    ui.show()
    # Create a plant
    #ls.Lsystem()
    # a = ls.Lsystem()