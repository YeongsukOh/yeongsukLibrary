import maya.cmds as cmds
from yeongsukLibrary.utilNode import constraintOption as cons

def createJoint():
    jnt = cmds.createNode('joint')
    