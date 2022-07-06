# -*- coding: utf-8 -*- 
'''
    Info: Everything Begins Here
''' 

from maya import cmds
from importlib import reload
import lsystem as ls
import terrian
import os,sys,inspect
reload(ls)
reload(terrian)

def landScapeSystem():
    '''
        Info: 程序入口
    '''
    
    # Create a plant
    ls.Lsystem()

if __name__ == "__main__":
    dir = os.path.dirname(os.path.abspath(ls.__file__))
    print(dir)
    if not dir in sys.path:
        sys.path.append(dir)
        print("Adding the working path to sys.path")
    landScapeSystem()