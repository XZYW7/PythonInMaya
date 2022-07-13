import maya.cmds as cmds
cmds.select(all=True)
cmds.delete()
width=10
height=10
subdx = 100
subdy = 100
terrain = cmds.polyPlane( axis=[0,1,0], w=width, h=height, sx=subdx, sy=subdy, ch=False)
deformerNode = cmds.textureDeformer()
noiseNode = cmds.createNode("noise")
place2DTextureNode = cmds.createNode("place2dTexture")
cmds.connectAttr(place2DTextureNode+".outUV", noiseNode+".uv")
cmds.connectAttr(place2DTextureNode+".outUvFilterSize", noiseNode+".uvFilterSize")
cmds.connectAttr(noiseNode+".outColor", deformerNode[0]+".texture")
cmds.setAttr(noiseNode+".amplitude", 0.641026)
cmds.setAttr(noiseNode+".frequencyRatio", 1.403846)
cmds.setAttr(noiseNode+".frequency", 4.487179)