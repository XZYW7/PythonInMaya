# -*- coding: utf-8 -*- 
'''
    Info: Everything Begins Here
''' 

from maya import cmds
import lsystem as ls
import terrian
import os,sys,inspect


def landScapeSystem():
    '''
        Info: 程序入口
    '''
    
    # Create a plant
    ls.Lsystem()

if __name__ == "__main__":
    dir = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
    if not dir in sys.path:
        sys.path.append(dir)
    landScapeSystem()