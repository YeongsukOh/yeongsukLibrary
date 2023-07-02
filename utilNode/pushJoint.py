import maya.cmds as cmds
from yeongsukLibrary.utilNode import constraintOption as cons

sel = cmds.ls(sl = True)

target = sel[0]
base = sel[1]

curveData = [[-0.4527093950179264, 0.01681009346272333, 0.0],[-0.4527093950179264, 3.6343020638176924, 0.0], [-0.9054187900356823, 3.181592668799869, 0.0], [-1.3581281850536016, 3.6343020638176924, 0.0], [0.0, 4.992430248871251, 0.0], [1.3581281850535234, 3.6343020638176924, 0.0], [0.9054187900356965, 3.181592668799869, 0.0], [0.4527093950177772, 3.6343020638176924, 0.0], [0.4527093950177772, 0.01681009346272333, 0.0], [-0.4527093950179264, 0.01681009346272333, 0.0]]
# n_curveData = [[0.4527093950179264, -0.01681009346272358, 0.0], [0.4527093950179243, -3.6343020638176915, 0.0], [0.9054187900356813, -3.1815926687998686, 0.0], [1.358128185053599, -3.634302063817691, 0.0], [-1.1102230246251565e-15, -4.99243024887125, 0.0], [-1.3581281850535245, -3.6343020638176906, 0.0], [-0.9054187900356976, -3.1815926687998686, 0.0], [-0.45270939501777846, -3.634302063817692, 0.0], [-0.4527093950177771, -0.01681009346272308, 0.0], [0.4527093950179264, -0.01681009346272358, 0.0]]

def createJoint(target, base):
	
	bindGroup = cmds.group(em = True, n = 'bind_group')

	# connect decompose node with source one
	# matching position
	decomposeNode = cmds.createNode('decomposeMatrix')
	controlGrp = cmds.group(em = True, n = 'grp_control')
	controlGrp_curve = cmds.curve(n = 'visualDirection', d = 1, p = curveData)
	cmds.connectAttr(target + '.worldMatrix[0]', decomposeNode + '.inputMatrix')
	cmds.connectAttr(decomposeNode + '.outputTranslate', controlGrp + '.translate')
	decomposeNode_controlGrp = cmds.createNode('decomposeMatrix')
	cmds.connectAttr(controlGrp + '.worldMatrix[0]', decomposeNode_controlGrp + '.inputMatrix')
	cmds.connectAttr(decomposeNode_controlGrp + '.outputTranslate', controlGrp_curve + '.translate')
	cmds.connectAttr(decomposeNode_controlGrp + '.outputRotate', controlGrp_curve + '.rotate')
	
	n_decomposeNode = cmds.createNode('decomposeMatrix')
	n_controlGrp = cmds.group(em = True, n = 'n_grp_control')
	n_controlGrp_off = cmds.group(em = True, n = 'n_grp_control_off')
	cmds.parent(n_controlGrp_off,n_controlGrp)
	cmds.setAttr(n_controlGrp + '.rotateX', 180)
	n_controlGrp_curve = cmds.curve(n = 'n_visualDirection', d = 1, p = curveData)
	cmds.connectAttr(target + '.worldMatrix[0]', n_decomposeNode + '.inputMatrix')
	cmds.connectAttr(n_decomposeNode + '.outputTranslate', n_controlGrp + '.translate')
	n_decomposeNode_controlGrp = cmds.createNode('decomposeMatrix')
	cmds.connectAttr(n_controlGrp_off + '.worldMatrix[0]', n_decomposeNode_controlGrp + '.inputMatrix')
	cmds.connectAttr(n_decomposeNode_controlGrp + '.outputTranslate', n_controlGrp_curve + '.translate')
	cmds.connectAttr(n_decomposeNode_controlGrp + '.outputRotate', n_controlGrp_curve + '.rotate')

	guideGrp = cmds.group(em = True, n = 'grp_guide')
	guide_lct = cmds.spaceLocator(n = 'lct_guide')
	skinJnt = cmds.createNode('joint', n = 'skin_joint')
	
	n_guideGrp = cmds.group(em = True, n = 'n_grp_guide')
	n_guide_lct = cmds.spaceLocator(n = 'n_lct_guide')
	n_skinJnt = cmds.createNode('joint', n = 'n_skin_joint')
	
	cmds.parent(guide_lct,guideGrp)
	cmds.parent(skinJnt,guide_lct)
	cmds.parent(guideGrp,controlGrp_curve)
	
	val = 10
	
	cmds.setAttr(guideGrp + '.translateX', 0)
	cmds.setAttr(guideGrp + '.translateY', val)
	cmds.setAttr(guideGrp + '.translateZ', 0)	
	
	cmds.parent(n_guide_lct,n_guideGrp)
	cmds.parent(n_skinJnt,n_guide_lct)
	cmds.parent(n_guideGrp,n_controlGrp_curve)

	cmds.setAttr(n_guideGrp + '.translateX', 0)
	cmds.setAttr(n_guideGrp + '.translateY', val)
	cmds.setAttr(n_guideGrp + '.translateZ', 0)
	
	for i in (controlGrp, n_controlGrp_off):
		pairBlend_node = cmds.createNode('pairBlend', n = 'pairBlend_{}'.format(i))
		cmds.connectAttr(target + '.rotate', pairBlend_node + '.inRotate1')
		cmds.connectAttr(base + '.rotate', pairBlend_node + '.inRotate2')
		cmds.connectAttr(pairBlend_node + '.outRotate', i + '.rotate')
		cmds.setAttr(pairBlend_node + '.weight', 0.5)
		
		
	
	cmds.parent(controlGrp,bindGroup)
	cmds.parent(n_controlGrp,bindGroup)
	cmds.parent(controlGrp_curve,bindGroup)
	cmds.parent(n_controlGrp_curve,bindGroup)