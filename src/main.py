# -*- coding: utf-8 -*- 
'''
    Info: Everything Begins Here
''' 
from PySide2 import QtWidgets, QtCore, QtGui
# import pymel.core as pm
from functools import partial
from maya import OpenMayaUI as omui

import shiboken2
from PySide2.QtCore import Signal

from maya import cmds
from importlib import reload
import os,sys

def workingDir():
    # Using the path of lsystem to find the working directorys
    dir = QtWidgets.QFileDialog.getExistingDirectory(None,"Please Choose the File folder","C:/")
    dir += '/src'
    if not dir in sys.path:
        sys.path.append(dir)
        print("Adding the working path to sys.path")
# workingDir()
WORKINGDIR = workingDir()
try:
    import lsystem as ls
    #import terrain
except:
    print('The working directory is wrong')

reload(ls)
#reload(terrain)

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
    def __init__(self, dock = True):
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
        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()
    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        choosePicBtn = QtWidgets.QPushButton('Choose Pic')
        choosePicBtn.clicked.connect(self.choosePic)
        layout.addWidget(choosePicBtn, 0, 0, 1, 2)
        
    def choosePic(self):
        self.heightMap = QtWidgets.QFileDialog.getOpenFileName(None, 
            "Choose the Height Map",WORKINGDIR, "Image Files(*.jpg *.png)")
        print(self.heightMap)
def landScapeSystem():
    '''
        Info: 程序入口
    '''

    ui = LandscapeSystem()
    ui.show()
    # Create a plant
    #ls.Lsystem()
    #a = ls.Lsystem()

if __name__ == "__main__":
    cmds.select(all=True)
    cmds.delete()
    landScapeSystem()