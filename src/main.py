# -*- coding: utf-8 -*- 
'''
    Info: This is the entrance of our program. Everything begins here.
    We create GUI controller there, and call different functions.
''' 
# prepare packages for GUI
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
    reload(ls)
    reload(terrain)
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
    def __init__(self, dock = True):
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

        self.ocean = cmds.polyCube(d = 50, w=50, h=1)
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
        self.absHeight.setMaximum(100)
        self.absHeight.setValue(1)
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


    def chooseNoise(self):
        print('chooseNoise')


    def chooseHeightMap(self):
        self.heightMap = QtWidgets.QFileDialog.getOpenFileName(None, 
            "Choose the Height Map",WORKINGDIR, "Image Files(*.jpg *.png)")
        print(self.heightMap)
    
    def generateTerrain(self):
        print('absHeight:', self.absHeight.value())
        print('generate Terrain')

    def createOcean(self):
        cmds.setAttr(self.ocean[1]+'.h',self.oceanHeight.value())
        cmds.setAttr(self.ocean[0] + '.translateY', self.oceanHeight.value()/2)
        print("ocean:", self.oceanHeight.value())
        print('create Ocean')

    def chooseMask(self):
        self.mask = QtWidgets.QFileDialog.getOpenFileName(None, 
            "Choose the Height Map",WORKINGDIR, "Image Files(*.jpg *.png)")
        print(self.mask[0])




if __name__ == "__main__":
    cmds.select(all=True)
    cmds.delete()
    ui = LandscapeSystem()
    ui.show()
    # Create a plant
    #ls.Lsystem()
    # a = ls.Lsystem()