from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial
from maya import OpenMayaUI as omui

import shiboken2
from PySide2.QtCore import Signal

def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = shiboken2.wrapInstance(int(win),QtWidgets.QMainWindow)
    return ptr
def getDock(name = 'LandscapeSystemDock'):
    deleteDock(name)
    ctrl = pm.workspaceControl(name, dockToMainWindow = ('right',1), label = "LandscapeSystem")
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = shiboken2.wrapInstance(int(qtCtrl),QtWidgets.QWidget)
    return ptr

def deleteDock(name = 'LandscapeSystemDock'):
    if pm.workspaceControl(name, query = True, exists = True):
        pm.deleteUI(name)


def showUI():
    ui = LandscapeSystem()
    ui.show()
    return ui
showUI()