# TEMPORARY
import maya.cmds as cmds
import maya.mel as mel
#import getpass
import json
import imp
#import os
import redbox as rb # vv v
#from functools import partial

#K = cmds.getModifiers()

################################################################################


def CustomParentConst(oSrc, oFollow, sConst = 'Custom_2Const'):
	''' Apply parent constraint ONLY on keyable + unlocked attrs.'''

	aAxis = []
	aKeyable = []
	for i, k in enumerate(['translate', 'rotate']):
		aAxis.append(['%s%s' % (k,a) for a in "XYZ"])
		aKeyable.append(['%s.%s' % (oSrc, a) for a in aAxis[i]])
		aAxis[i] =[str(s)[-1].lower() for s in list(set(aAxis[i]) - set(cmds.listAttr(aKeyable[i], keyable = True, u=True)or []))]

	if len(aAxis[0])== 3 and if len(aAxis[1])== 3:
		return

	cmds.parentConstraint(oFollow, oSrc, weight = 1, n = sConst, st=aAxis[0], sr = aAxis[1], offset = )

def main():
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	CustomParentConst(oSel[0], oSel[-1]) # Src, Target, Custom_2Const(optional custom const name)
