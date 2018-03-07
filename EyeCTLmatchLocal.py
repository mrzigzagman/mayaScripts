# Eye World Controller match Local Ctl v0.1.2
# W V
# Not working for current project T_T

import maya.cmds as cmds
def main():

	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]

	for sel in oSel:
		sNum = ''
		sModel = sel.rpartition(':')[0]
		if sModel[-2:].isdigit():
			sNum = sModel[-2:]
		elif sModel[-1].isdigit():
			sNum = sModel[-1]

		sWorld = 'FACE%s:eye_world_ctrl'%sNum
		sLocal = 'FACE%s:eye_local_ctrl'%sNum

		if cmds.objExists(sWorld):
			cmds.cutKey(sWorld, cl = True, at = ['tx', 'ty', 'tz'])
			cmds.pointConstraint(sLocal, sWorld, n = 'TempConst', weight = 1, offset = (0,0,0))
			cmds.delete('TempConst')
