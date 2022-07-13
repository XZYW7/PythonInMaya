'''
    Info: This file is used to generate a plant with L-system
'''
import maya.cmds as cmds
import math 
from maya.api import OpenMaya
from maya.api.OpenMaya import MVector as vec
import random

class status:
    def __init__(self, pos = vec(0.0,0.0,0.0)):
        self.pos = pos
        self.rotation = OpenMaya.MQuaternion(0.0,0.0,0.0,1.0)
        self.dir = vec(0.0,1.0,0.0)
    def getFront(self):
        defaultFront = vec(0.0,0.0,1.0)
        return defaultFront.rotateBy(self.rotation)
    def getUp(self):
        defaultUp = vec(0.0,1.0,0.0)
        return defaultUp.rotateBy(self.rotation)
    def getRight(self):
        defaultRight= vec(-1.0,0.0,0.0)
        return defaultRight.rotateBy(self.rotation)

class Lsystem:
    '''
        Info: The basic class for Lsystem. 
        You should instantiate the class when you create a plant
    '''
    ruleSet = {}
    iterations = 4
    axiom = ""
    lstring = ""
    stepLength = 1
    rotateAngle = 30
    Tree = ""
    def __init__(self, *args):
        '''
            Info: Run the constructor, Initialize variebles, Iterate rules, create models
        '''
        print("Lsystem Initialization")

        cmds.select(all=True)
        cmds.delete()
        # Initialize
        self.axiom = "FFFA"
        self.addRule('A', '[&FFFA]++++[&FFFA]++++[&FFFA]')
        #self.addRule('F', 'F[F\\F][F/F][F&F][F^F]F')
        #self.addRule('F', 'FF')
        #self.addRule('F', 'F[\\F]F[/F]F')
        #self.addRule('F', 'F[\\F]F')
        #self.addRule('F', 'F[/F]F')

        # Rule Iterate, get full Rule
        self.lstring = self.ruleIter()

        # Draw Model according to Full Rule
        self.Tree = self.drawModel()


    def addRule(self, replaceStr, newStr):
        if replaceStr not in self.ruleSet:
            self.ruleSet[replaceStr] = []
        self.ruleSet[replaceStr].append(newStr)# uniform sampling
        

    def ruleIter(self):
        root = self.axiom
        for i in range(self.iterations):
            temp = ""
            for j in root:
                temp = temp +  random.choice(self.ruleSet.get(j,j)) if self.ruleSet.get(j,j) else self.ruleSet.get(j,j)# get(key, value) if can't find key, return value
            root = temp

        print('lstring', root)
        return root
    
    def createBranch(self, pos, dir):
        branch = cmds.polyCylinder(axis=dir, r=self.stepLength/5.0, height=self.stepLength)
        cmds.move(pos[0] + 0.5 * self.stepLength * dir*vec(1.0,0.0,0.0), pos[1]+ 0.5 * self.stepLength * dir*vec(0.0,1.0,0.0), pos[2]+ 0.5 * self.stepLength * dir*vec(0.0,0.0,1.0))
        return branch[0]

    def drawModel(self):
        statusStack = []
        branchList = []
        currentStatus = status(vec(0.0, 0.0, 0.0))
        for i in self.lstring:
            if i == "F":

                # calculate current orientation status by Quaternion
                dir = currentStatus.dir.rotateBy(currentStatus.rotation)
                branch = self.createBranch(currentStatus.pos, dir)
                
                branchList.append(branch)
                
                # update the status
                currentStatus.pos = currentStatus.pos + dir * self.stepLength
                
            elif i == "+":
                radians = self.rotateAngle * math.pi /180.0
                # rotations = OpenMaya.MEulerRotation(0.0,0.0,radians)
                # currentStatus.dir = currentStatus.dir.rotateBy(rotations).normalize()
                # change the EulerAngle into Quaternions, I can't find an easy way to store a directional vector to represent dynamic EulerAngle
                axis = currentStatus.getUp()
                rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                currentStatus.rotation = currentStatus.rotation * rotations
            elif i == "-":
                radians = -self.rotateAngle * math.pi /180.0
                axis = currentStatus.getUp()
                rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                currentStatus.rotation = currentStatus.rotation * rotations
            elif i == "&":
                radians = -self.rotateAngle * math.pi /180.0
                axis = currentStatus.getRight()
                rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                currentStatus.rotation = currentStatus.rotation * rotations
            elif i == "^":
                radians = self.rotateAngle * math.pi /180.0
                axis = currentStatus.getRight()
                rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                currentStatus.rotation = currentStatus.rotation * rotations
            elif i == "/":
                radians = -self.rotateAngle * math.pi /180.0
                axis = currentStatus.getFront()
                rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                currentStatus.rotation = currentStatus.rotation * rotations
            elif i == "\\":
                radians = self.rotateAngle * math.pi /180.0
                axis = currentStatus.getFront()
                rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                currentStatus.rotation = currentStatus.rotation * rotations
            elif i == "|":
                pass
            elif i == "[":
                tmp = status(currentStatus.pos) # we cant add currentStatus directly to the stack, it's a pointer, the operations on currentStatus will change the value in stack
                tmp.rotation = currentStatus.rotation
                tmp.dir = currentStatus.dir
                statusStack.append(tmp)
            elif i == "]":
                currentStatus = statusStack.pop()
        groupName = cmds.group(branchList, n = "tree")
        return groupName
a = Lsystem()