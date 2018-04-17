# TEMPORARY
print '# TEMP.py #'

from functools import partial
import maya.cmds as cmds
import colorsys
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

	import ChannelBoxColourFaceTool
	reload(ChannelBoxColourFaceTool)
	ChannelBoxColourFaceTool.main()
