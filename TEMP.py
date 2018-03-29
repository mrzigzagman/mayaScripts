from __future__ import print_function
# TEMPORARY
#import maya.cmds as cmds
#import maya.mel as mel
#import getpass
#import json
#import imp
#import os
#import redbox as rb # vv v
#from functools import partial

# CUSTOM
import StudioSettings
import StudioSettings_WIP
reload(StudioSettings_WIP)
import MayaBGColour

#K = cmds.getModifiers()

################################################################################

def main():
	# Start here
	i = 0
	if i:
		StudioSettings.ShotInfo(0, 1)
	else:
		StudioSettings_WIP.ShotInfo(0, 1)
