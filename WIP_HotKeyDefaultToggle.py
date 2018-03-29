# HotKeyDefaultTogle v0.0.1
# Toggles Maya Hotkey to Custom / Maya Default

import maya.cmds as cmds

def main():
	sSet = 'CustomHotkeySet'
	sDefault = 'Maya_Default'
	sOriginalSet = 'CustomHotkeySet_BU'# This one is the BU set to be duplicated from.
	aSet = [str(s) for s in cmds.hotkeySet(q = True, hotkeySetArray = True)]
	sCurrentSet = cmds.hotkeySet(q = True, current = True)

	if sSet in aSet:
		cmds.hotkeySet(sSet, edit = True, delete = True)

	if sCurrentSet == sDefault:
		cmds.hotkeySet(sSet, current = True, source = sOriginalSet)
		aPrint = ['a7a8af', sSet, 0x6b6c75] # Gray
	else:
		cmds.hotkeySet(sSet)
		aPrint = ['a7a8af', sDefault, 0x6b6c75] # Gray

	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )
