# TEMPORARY
print '# TEMP.py #'

from functools import partial
import maya.cmds as cmds
#import maya.mel as mel
#import getpass
#import json
#import imp
#import os
#import redbox as rb # vv v

# CUSTOM
import StudioSettings
reload(StudioSettings)

import UIColourControl
reload(UIColourControl)

import UIWindowControl
reload(UIWindowControl)

K = cmds.getModifiers()

################################################################################

def main():
	#import UIBuilderTemplate
	#reload(UIBuilderTemplate)
	#UIBuilderTemplate.main()

	import UIColourControl
	reload(UIColourControl)
	print 'dColour = {'
	aList = [
	'eyeBalls',[102, 0, 0],
	'eyeLids',[170, 0, 0],
	'brows',[170, 170, 0],
	'cheeks',[0, 85, 0],
	'nose',[170, 85, 0],
	'lipSticky',[71, 71, 71],
	'lipZipper',[151, 151, 151],
	'jaw',[255, 255, 255],
	'lipCorners',[0, 75, 110],
	'lipsPart',[0, 125, 178],
	'lipsFold',[84, 218, 255],
	'puff',[38, 0, 59],
	'throat',[96, 48, 0],
	'tongue',[255, 85, 0],
	'ears',[0, 28, 0],
	'neck',[85, 85, 0],
	'gravity',[0, 0, 0],
	'eyeLidTweaks',[170, 93, 93],
	'browTweaks',[255, 255, 127],
	'cheekTweaks',[120, 120, 120],
	'noseTweak',[255, 170, 0],
	'lipTweaks',[174, 108, 255],
	'default',[68, 68, 68]
	]
	for i in range (1, len(aList), 2):
		print "'%s':"%aList[i-1], UIColourControl.getRGBvalues(aList[i][0], aList[i][1], aList[i][2],), ','

	print '}'
