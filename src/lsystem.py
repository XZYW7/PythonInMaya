'''
    Info: This file is used to generate a plant with L-system
'''

from maya import cmds

import os,sys,inspect

class Lsystem:
    '''
        Info: The basic class for Lsystem. 
        You should instantiate the class when you create a plant
    '''
    def __init__(self):
        print("Lsystem Initialization")
