# Constraint tool v5.0.1 wip 002
import maya.cmds as cmds

def CustomConst(oSrc, oFollow, iMo = False, aCond = [1, 1], sConst = 'Custom_2Const'):
	''' Apply parent constraint ONLY on keyable + unlocked attrs.'''
	# aCond [0, 1] : [trans, rot] 0 = no constraint. 1 = apply const.

	aAxis = []
	aKeyable = []
	for i, k in enumerate(['translate', 'rotate']):
		aAxis.append(['%s%s' % (k,a) for a in "XYZ"])
		aKeyable.append(['%s.%s' % (oSrc, a) for a in aAxis[i]])
		aAxis[i] =[str(s)[-1].lower() for s in list(set(aAxis[i]) - set(cmds.listAttr(aKeyable[i], keyable = True, u=True)or [])) if cmds.getAttr(s, s=True)]
		# aAxis[i] =[str(s)[-1].lower() for s in list(set(aAxis[i]) - set(cmds.listAttr(aKeyable[i], keyable = True, u=True)or []))]
		if not aCond[i]: aAxis[i] = ['x','y','z']

	if len(aAxis[0])== 3 and len(aAxis[1])== 3:
		return

	if cmds.objExists('%s|%s'%(oFollow, sConst)):
		aPrint = ['a7a8af', '%s already exists on "%s".'%(sConst, oSel[0]), 0x6b6c75]
		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = aPrint[2])
	else:
		cmds.parentConstraint(oFollow, oSrc, weight = 1, n = sConst, st=aAxis[0], sr = aAxis[1], mo = iMo )
	return aAxis # returns what's skipped

def main():
	K = cmds.getModifiers()
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	aPrint = None
	aPrintAxisNames = [	'Translate X',
						'Translate Y',
						'Translate Z',
						'Rotate X',
						'Rotate Y',
						'Rotate Z',
						'', # offset
						'',] # comment
	aPrintAxisColour = ['d8766c',
						'6bad64',
						'9bbcf2',
						'd8766c',
						'6bad64',
						'9bbcf2',
						'd8766c',
						'6b6c75',]#'a7a8af'

	dPrintAxis = {}
	for i, a in enumerate(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'offset', 'comment']):
		dPrintAxis.update({a:{'text':'', 'colour':''}})
		dPrintAxis[a]['text'] = aPrintAxisNames[i]
		dPrintAxis[a]['colour'] = aPrintAxisColour[i]

	#print dPrintAxis




	if K == 0:
		sMessage = '''
		Delete Constraint --- SFT [1]

		Point [Offset OFF] --- CTL [4]
		Orient [Offset OFF] --- ALT [8]
		Parent [Offset OFF] -- CTL + ALT [12]

		Point [Offset ON] --- SFT + CTL [5]
		Orient [Offset ON] --- SFT + ALT [9]
		Parent [Offset ON] --- SFT + CTL + ALT [13]
		'''
		aPrint = ['a7a8af', sMessage, 0x6b6c75]

	if oSel:
		aCond = [False, 1, 1]

		if K == 4: #Ctl
			aCond = [False, 1, 0]
			aPrint = ['9bbcf2', 'Point', 0x485872]



		elif K == 5: # SFT + CTL
			aCond = [True, 1, 0]
			aPrint = ['9bbcf2', 'Point w/offset', 0x485872]
			dPrintAxis['offset']['text'] = 'Offset'

		elif K == 8: # ALT
			aCond = [False, 0, 1]
			aPrint = ['9bbcf2', 'Orient', 0x485872]


		elif K == 9: # SFT + ALT
			aCond = [True, 0, 1]
			aPrint = ['9bbcf2', 'Orient w/offset', 0x485872]
			dPrintAxis['offset']['text'] = 'Offset'

		elif K == 12: # CTL + ALT
			aCond = [False, 1, 1]
			aPrint = ['9bbcf2', 'Point + Orient', 0x485872]


		elif K == 13: # SFT + CTL + ALT
			aCond = [True, 1, 1]
			aPrint = ['9bbcf2', 'Point + Orient w/offset', 0x485872]
			dPrintAxis['offset']['text'] = 'Offset'
		else:
			pass

		sDel = '%s|%s'%(oSel[0], 'Custom_2Const')
		if K == 1: # SFT
			if cmds.objExists(sDel):
				cmds.delete(sDel)
				aPrint = ['9bbcf2', 'Constraint Deleted', 0x485872] # Blue
				dPrintAxis['comment']['colour'] = 'd8766c'
				dPrintAxis['comment']['text'] = 'Constraint Deleted'

			else:
				aPrint = ['a7a8af', 'Constraint Not Found', 0x6b6c75]# Gray
				dPrintAxis['comment']['text'] = 'Constraint Not Found'




		elif K == 0:
			pass
		else:
			if len(oSel) > 1:
				for o in oSel[1:]:
					if cmds.objExists(sDel):
						aPrint = ['a7a8af', 'Already have a constraint', 0x6b6c75] # Gray
						dPrintAxis['comment']['colour'] = 'd8766c'
						dPrintAxis['comment']['text'] = 'Already Have a Constraint'
					else:
						aSkipped = CustomConst(oSel[0], o, aCond[0], aCond[1:])



				cmds.select(oSel[0], r = True)
			else:
				aPrint = ['d8766c', 'Need to select 2 or more ojbects.', 0x756b6b] # Red
				dPrintAxis['comment']['colour'] = 'd8766c'
				dPrintAxis['comment']['text'] = 'Need to select 2 or more objects.'

	if dPrintAxis['comment']['text']:

		sPrintAxis = '<text style="color:#%s";>%s</text>'%(dPrintAxis['comment']['colour'], dPrintAxis['comment']['text'])
		cmds.inViewMessage(amg = sPrintAxis, pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = 0x6b6c75)
	else:

		for x in ['x', 'y', 'z']:
			if x in aSkipped[0]:
				dPrintAxis['t%s'%x]['colour'] = 'a7a8af'
			if x in aSkipped[1]:
				dPrintAxis['r%s'%x]['colour'] = 'a7a8af'

		sPrintAxis = ''
		for p in [['tx', 'rx'], ['ty', 'ry'], ['tz', 'rz']]:
			sPrintAxis += '\n<text style="color:#%s";>%s</text><text style="color:#%s";> %s</text>'%(dPrintAxis[p[0]]['colour'], dPrintAxis[p[0]]['text'],dPrintAxis[p[1]]['colour'], dPrintAxis[p[1]]['text'])

		sPrintAxis += '\n<text style="color:#%s";>%s</text>'%(dPrintAxis['offset']['colour'], dPrintAxis['offset']['text'])





		cmds.inViewMessage(amg = sPrintAxis, pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = 0x6b6c75)

	if aPrint:

		pass
		#cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = aPrint[2])
