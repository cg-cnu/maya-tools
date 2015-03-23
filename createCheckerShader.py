import maya.cmds as cmds

# get the selected objects
selObjects = cmds.ls(selection=True)
# if no selected objects print a warning
if len(selObjects) == 0:
    cmds.warning("select an object to add checker map!")
else:
    # get the materials 
    materials = cmds.ls(materials = True)
    # if checkerShd already in materials: exit
    if "checkerShd" not in materials:
        # create a shader
        shader = cmds.shadingNode('lambert', asShader=True)
        cmds.select(selObjects)
        # assign the shader
        cmds.hyperShade( assign=shader )
        checkerShd = cmds.rename(shader, "checkerShd")        
        # create a checkerNode
        checkerNodeName = "checkerNode"
        checkerNode = cmds.shadingNode('checker', name=checkerNodeName, shared=True, asTexture=True)
        cmds.connectAttr(checkerNode+".outColor", checkerShd+".color")
        # create a placementNode        
        p2dNodeName = "checkerNodePlacement" 
        p2dNode = cmds.shadingNode('place2dTexture', shared=True, name=p2dNodeName, asUtility=True)        
        # connect the p2d to checkerNode
        try:
            cmds.connectAttr((p2dNodeName + '.outUvFilterSize'), (checkerNodeName + '.uvFilterSize'))
            cmds.connectAttr((p2dNodeName + '.outUV'), (checkerNodeName + '.uvCoord'))
        except RuntimeError, Error:
            print Error, "Connection already exits"  
        # set the attributes
        cmds.setAttr(p2dNodeName+".repeatU", 20)
        cmds.setAttr(p2dNodeName+".repeatV", 20)
    else:
        cmds.warning("checker map shader already exists!!!")

