# -*- coding: utf-8 -*- 
'''
    Info: Everything Begins Here
''' 

from maya import cmds
import lsystem as ls
import terrian

def landScapeSystem():
    '''
        Info: 程序入口
    '''
    terrian.create()

    ls.create()

if __name__ == "__main__":
    landScapeSystem()
    print('test')
