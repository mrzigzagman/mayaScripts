# Match One pose and move to next frame.
import maya.cmds as cmds

def CustomConst(oSrc, oFollow, iMo = False, iRot = 1, iTrans = 1, sConstName = 'Custom_2Const'):
	aSkipTrans = ['x', 'y', 'z']
	aSkipRot = ['x', 'y', 'z']

	aList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ',]

	aConstList = [str(c) for c in cmds.listAttr(oFollow, keyable = True)]

	for c in aConstList:
		for l in aList:
			if l == c:
				if 'translate' in c:
					print c[-1].lower()
					aSkipTrans.remove(c[-1].lower())
				else:
					aSkipRot.remove(c[-1].lower())

	if iRot == 0:
		aSkipRot = ['x','y','z']
	if iTrans == 0:
		aSkipTrans = ['x','y','z']

	oCheck = cmds.objExists('%s|%s'%(oFollow, sConstName))
	if oCheck:
		MessageBox('Message : %s already exists on "%s".' % (sConstName, oSel[0]))
	else:
		cmds.parentConstraint(oSrc, oFollow, weight = 1, n = sConstName, st = aSkipTrans, sr = aSkipRot, mo = iMo)

oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
sConstName = 'Custom_2Const'
iFrame = int(cmds.currentTime(q = True))

if K == 0:
	if oSel:
		for o in oSel[:-1]:
			CustomConst(oSel[-1], o, False, 1, 1, sConstName)

	cmds.setKeyframe(oSel[0], breakdown = 0, at = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', ])

	cmds.delete('%s|Custom_2Const'%oSel[0])

	iFrame = int(cmds.currentTime(q = True))
	cmds.currentTime(iFrame +1)
