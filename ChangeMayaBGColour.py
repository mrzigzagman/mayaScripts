import maya.cmds as cmds

def main():

	K = cmds.getModifiers()

	if K == 0:
		sBGC = (0.3, 0.3 ,0.3 )
	elif K == 8:
		sBGC = (0.3, 0.2 ,0.2 )
	elif K == 4:
		sBGC = (0.2, 0.2 ,0.3 )
	elif K == 1:
		sBGC = (0.3, 0.3 ,0.0 )
	elif K == 5:
		sBGC = (0.2, 0.3 ,0.2 )
	elif K == 9:
		sBGC = (0.4, 0.2 ,0.0 )
	elif K == 12:
		sBGC = (0.2, 0.15 ,0.2 )
	elif K == 13:
		sBGC = (0.6, 0.6 ,0.6 )

	sMenu = '''
	ALT [8]
	CTL [4]
	SFT [1]
	CTL + SFT [5]
	ALT + SFT [9]
	CTL + ALT [12]
	CTL + ALT + SFT [13]
	'''

	for ctrl in cmds.lsUI(type = 'control'):
		try:
			cmds.layout(ctrl, e = True, bgc = sBGC)
		except RuntimeError:
			pass
	cmds.refresh(f = True)
