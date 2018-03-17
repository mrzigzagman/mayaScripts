# TEMPORARY
import maya.cmds as cmds
#import maya.mel as mel
#import getpass
#import os
#from functools import partial

#K = cmds.getModifiers()

################################################################################

def main():


	oKeyPoseFrames = 'KeyPoseFrames'
	aKeyFrames= []
	if cmds.objExists(oKeyPoseFrames):
		for i in range(cmds.keyframe(oKeyPoseFrames+'.tx', kc = True, q = True)):
			aKeyFrames.extend(cmds.keyframe(oKeyPoseFrames+'.tx', index = (i,i), q = True))


		iIn = int(cmds.playbackOptions(q = True, minTime = True))
		iOut = int(cmds.playbackOptions(q = True, maxTime = True))
		for i in range(iIn, iOut+1):
			if i in aKeyFrames:
				cmds.keyframe(t = (i, i), tds = True)
			else:
				cmds.keyframe(t = (i, i), tds = False)

		'''
		aObjList = [str(s) for s in cmds.selectionConnection('graphEditor1FromOutliner', q = True, object = True)  or [] ]
		#aCurveList = [str(s) for s in cmds.keyframe(q = True, name = True)]

		# Store Selected Keys
		aSelection = []
		for o in aObjList:
			aName = cmds.keyframe(o, query = True, name = True)
			aKeys = cmds.keyframe(o, sl = True, q = True)

			if aName and aKeys:
				aSelection.append([str(aName[0]), aKeys])

		# Clear keys
		cmds.selectKey( clear = True)

		# DO
		fTime = cmds.currentTime(q = True)
		if fTime in aKeyFrames:
			cmds.keyframe(t = (fTime, fTime), tds = True)

		# Select Stored keys
		if aSelection:
			for a in aSelection:
				sName = a[0]
				for t in a[1]:
					cmds.selectKey(sName, t = (t,t), tgl = True)
					'''
