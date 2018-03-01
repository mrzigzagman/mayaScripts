import maya.cmds as cmds
import maya.mel as mel
import imp
import json


def main():
	# DO YOUR TEST HERE:

	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	sCamName = 'ANIM_CAM'
	aList = ['focalLength', 'focusDistance', 'centerOfInterest', 'locatorScale', 'nearClipPlane', 'farClipPlane']


	aTransform = []
	aAttr = []
	if cmds.objExists(sCamName):
		aTransform.append(cmds.xform(sCamName, q = True, ws = True, t = True))
		aTransform.append(cmds.xform(sCamName, q = True, ws = True, ro = True))
		for a in aList:
			aAttr.append(cmds.getAttr('%sShape.%s'%(sCamName,a)))
		cmds.delete(sCamName)

	oCamera = cmds.camera()
	cmds.rename(oCamera[0], '%s'%sCamName)

	if aTransform:
		cmds.xform(sCamName, ws = True, t = aTransform[0])
		cmds.xform(sCamName, ws = True, ro = aTransform[1])

		for i, v in enumerate(aAttr):
			cmds.setAttr('%sShape.%s'%(sCamName,aList[i]),v)
	cmds.select(oSel, r = True)

	mel.eval('setNamedPanelLayout "Custom_Anim";')
