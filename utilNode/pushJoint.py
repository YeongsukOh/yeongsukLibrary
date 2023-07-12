import maya.cmds as cmds
import maya.OpenMaya as openMaya

# rom yeongsukLibrary.utilNode import constraintOption as cons

curveData = [[-0.4527093950179264, 0.01681009346272333, 0.0],[-0.4527093950179264, 3.6343020638176924, 0.0], [-0.9054187900356823, 3.181592668799869, 0.0], [-1.3581281850536016, 3.6343020638176924, 0.0], [0.0, 4.992430248871251, 0.0], [1.3581281850535234, 3.6343020638176924, 0.0], [0.9054187900356965, 3.181592668799869, 0.0], [0.4527093950177772, 3.6343020638176924, 0.0], [0.4527093950177772, 0.01681009346272333, 0.0], [-0.4527093950179264, 0.01681009346272333, 0.0]]

selectedJnt = cmds.ls(sl = True)

# def createJoint(selectedJnt):

baseList = []

mSelectionList = openMaya.MSelectionList()

groupList = []
lctList = []

for index in range(len(selectedJnt)):
	
	parentPath = cmds.listRelatives(selectedJnt[index], p = True)[0]
	
	pushJnt = cmds.createNode('joint', n = f'push_{selectedJnt[index]}')
	pushJntGrp = cmds.group(em = True, n = f'grp_push_{selectedJnt[index]}')
	cmds.parent(pushJntGrp, parentPath)
	cmds.parent(pushJnt,pushJntGrp)
	cmds.connectAttr(selectedJnt[index] + '.translate', pushJntGrp + '.translate')
	cmds.delete(cmds.orientConstraint(selectedJnt[index], pushJntGrp, mo = False))
	
	baseList.append(pushJntGrp)

	bindGroup = cmds.group(em = True, n = f'bind_group_{selectedJnt[index]}')

	# connect decompose node with source one
	# matching position
	
	decomposeNode = cmds.createNode('decomposeMatrix')
	controlGrp = cmds.group(em = True, n = f'grp_control_{selectedJnt[index]}')
	controlGrp_off = cmds.group(em = True, n = f'grp_control_off_{selectedJnt[index]}')
	groupList.append(controlGrp_off)
	cmds.parent(controlGrp_off, controlGrp)
	controlGrp_curve = cmds.curve(n = f'visualDirection_{selectedJnt[index]}', d = 1, p = curveData)
	cmds.connectAttr(selectedJnt[index] + '.worldMatrix[0]', decomposeNode + '.inputMatrix')
	cmds.connectAttr(decomposeNode + '.outputTranslate', controlGrp + '.translate')
	cmds.connectAttr(decomposeNode + '.outputRotate', controlGrp + '.rotate')
	decomposeNode_controlGrp = cmds.createNode('decomposeMatrix')
	cmds.connectAttr(controlGrp_off + '.worldMatrix[0]', decomposeNode_controlGrp + '.inputMatrix')
	cmds.connectAttr(decomposeNode_controlGrp + '.outputTranslate', controlGrp_curve + '.translate')
	cmds.connectAttr(decomposeNode_controlGrp + '.outputRotate', controlGrp_curve + '.rotate')
	
	n_decomposeNode = cmds.createNode('decomposeMatrix')
	n_controlGrp = cmds.group(em = True, n = f'n_grp_control_{selectedJnt[index]}')
	n_controlGrp_off = cmds.group(em = True, n = f'n_grp_control_off_{selectedJnt[index]}')
	n_controlGrp_control = cmds.group(em = True, n = f'n_grp_control_control_{selectedJnt[index]}')
	cmds.parent(n_controlGrp_off, n_controlGrp)
	cmds.parent(n_controlGrp_control, n_controlGrp_off)
	groupList.append(n_controlGrp_control)
	
	mSelectionList.add(n_controlGrp_off)
	cmds.setAttr(n_controlGrp_off + '.rotateX', 180)
	n_controlGrp_curve = cmds.curve(n = f'n_visualDirection_{selectedJnt[index]}', d = 1, p = curveData)
	cmds.connectAttr(selectedJnt[index] + '.worldMatrix[0]', n_decomposeNode + '.inputMatrix')
	cmds.connectAttr(n_decomposeNode + '.outputTranslate', n_controlGrp + '.translate')
	cmds.connectAttr(n_decomposeNode + '.outputRotate', n_controlGrp + '.rotate')
	n_decomposeNode_controlGrp = cmds.createNode('decomposeMatrix')
	cmds.connectAttr(n_controlGrp_control + '.worldMatrix[0]', n_decomposeNode_controlGrp + '.inputMatrix')
	cmds.connectAttr(n_decomposeNode_controlGrp + '.outputTranslate', n_controlGrp_curve + '.translate')
	cmds.connectAttr(n_decomposeNode_controlGrp + '.outputRotate', n_controlGrp_curve + '.rotate')

	guideGrp = cmds.group(em = True, n = f'grp_guide_{selectedJnt[index]}')
	guide_lct = cmds.spaceLocator(n = f'lct_guide_{selectedJnt[index]}')[0]
	skinJnt = cmds.createNode('joint', n = f'skin_joint_{selectedJnt[index]}')
	lctList.append(guide_lct)
	
	n_guideGrp = cmds.group(em = True, n = f'n_grp_guide_{selectedJnt[index]}')
	n_guide_lct = cmds.spaceLocator(n = f'n_lct_guide_{selectedJnt[index]}')[0]
	n_skinJnt = cmds.createNode('joint', n = f'n_skin_joint_{selectedJnt[index]}')
	lctList.append(n_guide_lct)
	
	cmds.parent(guide_lct,guideGrp)
	cmds.parent(skinJnt,guide_lct)
	cmds.parent(guideGrp,controlGrp_curve)
	
	val = 10
	
	cmds.setAttr(guideGrp + '.translateX', 0)
	cmds.setAttr(guideGrp + '.translateY', val)
	cmds.setAttr(guideGrp + '.translateZ', 0)
	
	cmds.setAttr(guideGrp + '.rotateX', 0)
	cmds.setAttr(guideGrp + '.rotateY', 0)
	cmds.setAttr(guideGrp + '.rotateZ', 0)
	
	cmds.parent(n_guide_lct,n_guideGrp)
	cmds.parent(n_skinJnt,n_guide_lct)
	cmds.parent(n_guideGrp,n_controlGrp_curve)

	cmds.setAttr(n_guideGrp + '.translateX', 0)
	cmds.setAttr(n_guideGrp + '.translateY', val)
	cmds.setAttr(n_guideGrp + '.translateZ', 0)
	
	cmds.setAttr(n_guideGrp + '.rotateX', 0)
	cmds.setAttr(n_guideGrp + '.rotateY', 0)
	cmds.setAttr(n_guideGrp + '.rotateZ', 0)
	
	for i in range(len(groupList)):
		pairBlend_node = cmds.createNode('pairBlend', n = f'pairBlend_{i}')
		remapValueNode = cmds.createNode('remapValue', n = f'remapValue_{i}')
		cmds.connectAttr(selectedJnt[index] + '.rotate', pairBlend_node + '.inRotate1')
		cmds.connectAttr(pushJnt + '.rotate', pairBlend_node + '.inRotate2')
		cmds.connectAttr(pairBlend_node + '.outRotateZ', groupList[i] + '.rotateZ')
		cmds.setAttr(pairBlend_node + '.weight', 0.5)
		cmds.connectAttr(pairBlend_node + '.outRotateZ', remapValueNode + '.inputValue')
		cmds.setAttr(remapValueNode + '.inputMin', -45)
		cmds.setAttr(remapValueNode + '.inputMax', 0)
		cmds.setAttr(remapValueNode + '.outputMin', 5)
		cmds.setAttr(remapValueNode + '.outputMax', 0)
		cmds.connectAttr(remapValueNode + '.outValue', lctList[i] + '.translateY')

	cmds.parent(controlGrp,bindGroup)
	cmds.parent(n_controlGrp,bindGroup)
	cmds.parent(controlGrp_curve,bindGroup)
	cmds.parent(n_controlGrp_curve,bindGroup)
	
	


####	
cmds.delete(baseList)