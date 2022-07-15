'''
    Info: This file is used to generate a plant with L-system
'''
import maya.cmds as cmds
import math 
from maya.api import OpenMaya
from maya.api.OpenMaya import MVector as vec
import random
class leave:
    leaveType = []
    def __init__(self):
        self.leaveType.append( [(-0.0375116, 0, -5.956661), (-0.0375116,0,-5.956661), (0.635531,0,-4.745183), (0.097097,0,-3.937532), ( -0.441337,0,-3.12988),
(-3.099857,0,-0.303099), (-3.099857,0,2.18716), (-3.099857,0,4.677419), (-0.00385947,0,6.124462), (0.0297927,0,6.427331),
(0.0634448, 0, 6.7302), (4.021403, 0, 5.176707), (4.067747, 0, 2.349765), (4.11409,0, -0.477177 ), (2.899479,0, -3.087925),
(2.313483,0, -3.841881), (1.727488,0, -4.595838), (2.125889,0, -4.173427), (1.172866, 0, -5.175323), (0.219843, 0, -6.177218),
(-0.0375116,0, -5.956661), (-0.0375116, 0, -5.956661)])
        self.leaveType.append( [(-0.177027, 0, 2.994705),(-0.177027, 0, 2.994705), (-3.01622, 0, 5.034767),(-3.01622, 0, 5.034767),
        (-3.01622, 0, 5.034767),(-5.986036, 0, 5.034767),(-5.986036, 0, 5.034767),(-5.986036, 0, 5.034767),(-4.965162, 0, 3.085825),
        (-4.965162, 0, 3.085825),(-4.965162, 0, 3.085825),(-4.083497, 0, 2.06495),(-4.083497, 0, 2.06495),(-4.083497, 0, 2.06495),
        (-6.960507, 0, 0.0696051),(-6.960507, 0, 0.0696051),(-6.960507, 0, 0.0696051),( -5.939633, 0, 0.116008),( -5.939633, 0, 0.116008),
        ( -5.939633, 0, 0.116008),( -6.960507, 0, -1.972144),( -6.960507, 0, -1.972144),( -6.960507, 0, -1.972144),(-4.965162, 0, -0.951269),
        (-4.965162, 0, -0.951269),(-4.965162, 0, -0.951269),(-4.965162, 0, -1.972144),(-4.965162, 0, -1.972144),(-4.965162, 0, -1.972144),
        (-3.01622, 0, -0.904866),(-3.01622, 0, -0.904866),(-3.01622, 0, -0.904866),(-2.552186, 0, -3.921086),(-2.552186, 0, -3.921086),
        (-2.552186, 0, -3.921086),(-1.438505, 0, -3.039421),(-1.438505, 0, -3.039421),(-1.438505, 0, -3.039421),(0, 0, -6.983709),
        (0, 0, -6.983709),(0, 0, -6.983709),(1.531312, 0, -3.039421),(1.531312, 0, -3.039421),(1.531312, 0, -3.039421),
        (2.459379, 0, -3.967489),(2.459379, 0, -3.967489),(2.459379, 0, -3.967489),(2.969816, 0, -0.951269),(2.969816, 0, -0.951269),
        (2.969816, 0, -0.951269),(5.011565, 0, -1.92574),(5.011565, 0, -1.92574),(5.011565, 0, -1.92574),(5.057968, 0, -0.951269),
        (5.057968, 0, -0.951269),(5.057968, 0, -0.951269),(7.00691, 0, -1.879337),(7.00691, 0, -1.879337),(7.00691, 0, -1.879337),
        (5.986036, 0, 0.0696051),(5.986036, 0, 0.0696051),(5.986036, 0, 0.0696051),(7.00691, 0, 0.116008),(7.00691, 0, 0.116008),
        (7.00691, 0, 0.116008),(3.990691, 0, 2.06495),(3.990691, 0, 2.06495),(3.990691, 0, 2.06495),(5.104372, 0, 3.085825),
        (5.104372, 0, 3.085825),(5.104372, 0, 3.085825),(6.078843, 0, 5.127574),(6.078843, 0, 5.127574),(6.078843, 0, 5.127574),
        (2.920944, 0, 5.001009),(2.920944, 0, 5.001009),(2.920944, 0, 5.001009),(0.206531, 0, 3.024209),(0.206531, 0, 3.024209),
        (0.206531, 0, 3.024209),(0.26554, 0, 7.036819),(0.26554, 0, 7.036819),(0.26554, 0, 7.036819),(-0.206531, 0, 7.036819),
        (-0.206531, 0, 7.036819),(-0.206531, 0, 7.036819),( -0.177027, 0, 2.994705),( -0.177027, 0, 2.994705),( -0.177027, 0, 2.994705)])

    def drawLeave(self, chooseType = 0):
        curve = cmds.curve( p= self.leaveType[chooseType])
        self.leave = cmds.planarSrf(curve)
        cmds.delete(curve)
        cmds.setAttr(self.leave[0]+'.scale', 0.05,1.0,0.05)
class status:
    def __init__(self, pos = vec(0.0,0.0,0.0)):
        self.pos = pos
        self.rotation = OpenMaya.MQuaternion(0.0,0.0,0.0,1.0)
        self.dir = vec(0.0,1.0,0.0)
        self.length = 1.0
        self.width = 1.0
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
    iterations = 3
    axiom = ""
    lstring = ""
    stepLength = 0.5
    lengthRate = 0.9
    width = 0.1
    widthRate = 0.5
    rotateAngle = 30
    Tree = ""
    def __init__(self, name):
        '''
            Info: Run the constructor, Initialize variebles, Iterate rules, create models
        '''
        print("Lsystem Initialization")
        # Initialize
        self.axiom = "FFFA"
        # self.addRule('F', 'F[F\\F][F/F][F&F][F^F]F')
        # self.addRule('F', 'FF')
        #self.addRule('F', '"F[\\F][/F]')
        #self.addRule('F', 'F[\\FA]')
        #self.addRule('F', 'F[/FA]')

        # Rule Iterate, get full Rule
        #self.lstring = self.ruleIter()

        # Draw Model according to Full Rule
        #self.Tree = self.drawModel()
        self.name = name

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
        self.lstring = root
    
    def createBranch(self, pos, dir):
        branch = cmds.polyCylinder(axis=dir, r=self.width, height=self.stepLength)
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
            elif i == "L":
                l = leave()#cmds.polySphere(r = self.stepLength)
                l.drawLeave(0)
                v = vec(0.0,0.0,0.32)
                #axis = vec(0.0,0.0,1.0)
                #radians = random.random() * math.pi / 2.0 
                #rotations = OpenMaya.MQuaternion(math.sin(radians/2)* axis[0], math.sin(radians/2)* axis[1] , math.sin(radians/2) * axis[2], math.cos(radians/2))
                
                cmds.rotate( 90*random.random(), 90*random.random(), 90*random.random(), l.leave[0], pivot=(0, 0, 0.32) )
                cmds.move(currentStatus.pos[0] - v[0], currentStatus.pos[1] - v[1], currentStatus.pos[2]-v[2])

                branchList.append(l.leave[0])
            elif i == '"':
                self.stepLength *= self.lengthRate
                self.width *= self.widthRate
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
                tmp.length = self.stepLength
                tmp.width = self.width
                statusStack.append(tmp)
            elif i == "]":
                currentStatus = statusStack.pop()
                self.stepLength = currentStatus.length
                self.width = currentStatus.width

        print(branchList)
        print('group')
        print('group2')

        print(self.Tree)
        groupName = cmds.group(branchList, n = self.name)
        self.Tree = groupName
        print(self.Tree)
        print(self.Tree)
        
