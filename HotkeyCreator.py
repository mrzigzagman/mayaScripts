


# ShortCut Creator. v 0.0.1
# Run this tool to create shortcut commands in the Hotkey Editor. This tool picks up the keys in Hotkeys.py dictionary
# to create commands. Following "P_ALT_R" format. One button creates all commands, clears the hotkey and assign to
# the key with Press/Release and Alt/etc modifiers.

# Run once with in relation to Hotkeys.py
# Current version doesn't assign Press and Release correctly. But all commands will be created. much easier to assign shortcuts.

import maya.cmds as cmds
import maya.mel as mel
import imp

def main():
	print '# Custom Hotkey Set Creation Tool'
	# HotKey Set Creation. Omitting now. Currently
	'''
	### Delete Current Custom Hotkey Sets.
	sSet = 'CustomHotkeySet'
	sSetBU = '%sBU'%sSet# This one is the BU set to be duplicated from.
	aSet = [str(s) for s in cmds.hotkeySet(q = True, hotkeySetArray = True)]

	# Delete previously created Custom Hotkey Sets.
	if sSet in aSet:
		cmds.hotkeySet(sSet, edit = True, delete = True)
		print '%s found. Deleted.'% sSet
	if sSetBU in aSet:
		cmds.hotkeySet(sSetBU, edit = True, delete = True)
		print '%s found. Deleted.'% sSetBU

	# Create a fresh custom Set. (Create BU first for Toggle tool. WIll create sSet at the end of the run.)

	cmds.hotkeySet(sSetBU, current = True)
	print '%s Created.'% sSetBU
	'''


	### Create Scripts in the Editor. ##

	# Get List of Hotkeys from HotKeys.py
	sScriptName = 'HotKeys' # remove '.py'
	sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts'
	oHotKeys = imp.load_source(sScriptName, '%s/%s.py'%(sScriptPath,sScriptName))

	# Getting List of keys from HotKeys.py (List of all Custom Hotkeys.)
	aKeyList = oHotKeys.KeyList().keys()

	#print aKeyList
	#aKeyList = ['9_N_P','N_ALT_R',] # temp. for testing
	aKeyList = ['L_ALT_P','L_ALT_R'] # temp. for testing
	for k in aKeyList:

		if not cmds.runTimeCommand(k, ex = True):

			#mel.eval('runTimeCommand -delete %s '%k) # Not working....
			#cmds.runTimeCommand(k, delete = True)

			aKey = k.split('_')

			# Custom Shortcut command.
			sCommand = '''# Custom Hotkey - Consolidated - v0.0.2

# CUSTOMIZE HERE:
p = '%s/' # Path to HotKeys.py
sChar = '%s' # Key on Keyboard. not case sensitive.
sPress = '%s' # 'P' or 'R' Pressed or Release

# -- Start --
import maya.cmds as cmds
import sys
if p not in sys.path: sys.path.append(p)
import Hotkeys # Hotkeys.py

reload(HotKeys) #Use reload when testing. Comment out when in actual use.

iModifier = cmds.getModifiers()
HotKeys.Execute(sChar, iModifier, sPress)
'''% (sScriptPath, aKey[0], aKey[2])
			aMod = [False, False, False, False]
			if 'SFT' in aKey:
				aMod[0] = True
			if 'CTL' in aKey:
				aMod[1] = True
			if 'ALT' in aKey:
				aMod[2] = True
			if 'CMD' in aKey:
				aMod[3] = True


			sNameCommand = k+aKey[2] # Specific name of the command to assign to a key.
			if 'P' in aKey[2]:
				aRelease = [sNameCommand, False]
			else:
				aRelease = [False, sNameCommand]


			# Key Exceptions
			dExceptions = { 'SPACE': 'Space',
							'COMMA': ',',}
			if aKey[0] in dExceptions.keys():
				sKey = dExceptions[aKey[0]]
			else:
				sKey = aKey[0]

			# Continue here : Shift turns on for some reason
			cmds.runTimeCommand(k, annotation=k.replace('_', ' '), category="Custom Scripts", command=(sCommand), showInHotkeyEditor=1)
			cmds.hotkey(keyShortcut = aKey[0].lower(), sht = aMod[0], ctl = aMod[1], alt = aMod[2], cmd = aMod[3], name = None, rn = None)
			cmds.nameCommand( sNameCommand, ann=k.replace('_', ' '), c = k, stp = 'python')

			cmds.hotkey(keyShortcut = aKey[0].lower(), sht = aMod[0], ctl = aMod[1], alt = aMod[2], cmd = aMod[3], name = aRelease[0], rn = aRelease[1])
			print '%s : CREATED!'%k


	#cmds.hotkeySet(sSet, current = True, source = sSetBU) # Duplicate the
	#cmds.hotkey(keyShortcut='u', ctrlModifier=True, name='')
	#print cmds.hotkeyCtx( typeArray = True, query = True)
	#cmds.nameCommand( 'hotkeyTest', ann='Hotkey Test', c='python("print 123")')
	#cmds.hotkey( keyShortcut='u', ctrlModifier=True, name='hotkeyTest')
