import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender

# basic info define
nodeName = "LeftFoot"
nodeId = OpenMaya.MTypeId(0x100fff)

# ptr to gl function table
glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()



class LocatorNode(OpenMayaMPx.MPxLocatorNode):
    '''
        Info:
            The class is created for the custom node of Maya,
            defining the custom locator
    '''
    def __init__(self):
        '''
            Info: 构造函数，在这里进行了父类的初始化。
            Param:
                paramName: ...
                paramName: ...
        '''
        OpenMayaMPx.MPxLocatorNode.__init__(self)
    def compute(self, plug, dataBlock):
        return OpenMaya.kUnknownParameter
    def draw(self, view, path, style, status):
        # 
        '''
            Info: drawing View,dagpath,(wireframe...)
            Param:
                view:
                path:
                style:
                status:
        '''
        view.beginGL()#这里的opengl依然是状态机

        # Pushed current state
        glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
        
        # Enable blend mode(to enable transparency)
        glFT.glEnable(OpenMayaRender.MGL_BLEND)
        
        # Defined Blend function
        glFT.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)

        # Define colors for different selection modes
        if status == view.kActive:
            glFT.glColor4f(0.2, 0.5, 0.1, 0.3)
        elif status == view.kLead:
            glFT.glColor4f(0.5, 0.2, 0.1, 0.3)
        else:# status == view.kDormant:
            glFT.glColor4f(0.1, 0.1, 0.1, 0.3)

        # Draw a shape
        glFT.glBegin(OpenMayaRender.MGL_POLYGON)
        glFT.glVertex3f(-0.031, 0.0, -2.875)
        glFT.glVertex3f(-0.939, 0.1, -2.370)
        glFT.glVertex3f(-1.175, 0.2, -1.731)
        glFT.glVertex3f(-0.60, 0.3, 1.060)
        glFT.glVertex3f(0.473, 0.3, 1.026)
        glFT.glVertex3f(0.977, 0.2,-1.731)
        glFT.glVertex3f(0.809, 0.1, -2.337)
        glFT.glVertex3f(0.035, 0.0, -2.807)
        glFT.glEnd()

        glFT.glBegin(OpenMayaRender.MGL_POLYGON)
        glFT.glVertex3f(-0.587, 0.3, 1.33)
        glFT.glVertex3f(0.442, 0.3, 1.33)
        glFT.glVertex3f(0.442, 0.3, 1.92)
        glFT.glVertex3f(0.230, 0.3, 2.24)
        glFT.glVertex3f(-0.442, 0.3, 2.25)
        glFT.glVertex3f(-0.635, 0.3, 1.92)
        glFT.glVertex3f(-0.567, 0.3, 1.35)
        
        glFT.glEnd()

        if status == view.kActive:
            glFT.glColor4f(0.2, 0.5, 0.1, 1)
        elif status == view.kLead:
            glFT.glColor4f(0.5, 0.2, 0.1, 1)
        else:# status == view.kDormant:
            glFT.glColor4f(0.1, 0.1, 0.1, 1)
        view.drawText("Left Foot", OpenMaya.MPoint(0,0,0), view.kLeft)

        # Disable Blend mode
        glFT.glDisable(OpenMayaRender.MGL_BLEND)

        # Restore the state
        glFT.glPopAttrib()

        view.endGL()
             
        
def nodeCreator():
    '''
        Info: info比如这里就是：nodeCreator作用是创建一个LocatorNode的实例，
            并返回一个指向它的指针
        Param:
            ParamName: ...
            ParamName: ...
    '''
    return OpenMayaMPx.asMPxPtr(LocatorNode())

def nodeInitializer():
    pass
    
def initializePlugin(mobject):
    '''
        Info: 初始化,和maya pluginCommand是一样的
        Param:
            mObject: ...
            ParamName: ...
    '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        sys.stderr.write("Failed to register node:" + nodeName)
        
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(nodeId)
    except:
        sys.stderr.write("Failed to deregister node" + nodeName)


'''
注意绿色的注释，有在代码上方的，也有在代码右边的。
在代码上面的，表示这一步的作用，或者说在整个程序当中的步骤。每写一个步骤都空一行
在代码右边的，表示对这段代码语法上的解释。
'''