# TEMPORARY
print '# TEMP.py #'
import maya.cmds as cmds
#from functools import partial
#import colorsys
#import sys
#import maya.mel as mel
#import getpass
#import json
import imp
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
	# Attribute Increment v4.0.0
	oChannel = [str(c+'.'+cmds.attributeName(c+'.'+b, l=True)) for a in 'msho' for b in cmds.channelBox('mainChannelBox', **{'q':True, 's%sa'%a:True}) or [] for c in cmds.channelBox('mainChannelBox', q = True, **{'%sol'%a:True})]
	iAmount  = -0.1

	iNewValue = None

	if oChannel:
		for c in oChannel:
			iVal = cmds.getAttr(c) + iAmount

			if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], minExists = True):
				if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], min = True)[0] >= iVal :
					iNewValue = cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], min = True)[0]

			if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], maxExists = True):
				if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], max = True)[0] <= iVal:
					iNewValue = cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], max = True)[0]

			if not iNewValue == None:
				cmds.setAttr(c, iNewValue)
			else:
				cmds.setAttr(c, iVal)

	else:
		aPrint = ['d8766c', 'No Attr Selected', 0x756b6b, 'midCenterBot']
		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = aPrint[3], fade = True, fts = 10, ft = 'arial',bkc = aPrint[2] )
