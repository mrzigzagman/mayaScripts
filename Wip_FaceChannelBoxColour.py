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


	iColour = 1
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]

	if iColour: # Set Colour in ChannelBox

		# remove non-Facial attributes
		aAttrList = cmds.listAttr(oSel[0], v = True)
		#aAttrList = cmds.listAttr(self.aPuppet[self.iChar], v = True)
		for a in aAttrList[:]:
			if not a.startswith('fr_'):
				aAttrList.remove(a)
			else:
				break
			'''
		# for all attributes for facial:
		sColour = 'default'
		dColour = UIColourControl.faceColour('getDict')
		sColourMatch = ''
		iColourDim = 1
		for a in aAttrList:
			sKey = a[3:]
			if sKey in dColour.keys():
				sColour = sKey

			if not 'fr_' in a:
				aColour = aFont = UIColourControl.getRGBvalues(dColour[sColour])

				# Dim every second entry (L/R combined)
				if not a[:-1] in sColourMatch:
					iColourDim = iColourDim * -1 + 1
				sColourMatch = a
				if iColourDim:
					aColour = UIColourControl.offsetRGBvalues(aColour, [-0.06, -0.06, -0.06])

				# Make Font darker/brighter colour
				iColour = sum(aColour)
				aFont = aColour[:]
				if iColour > 1.50:
					aFont = UIColourControl.offsetRGBvalues(aFont, [-0.8, -0.8, -0.8])
				else:
					aFont = UIColourControl.offsetRGBvalues(aFont , [0.8, 0.8, 0.8])

				print a, aFont, aColour
				#cmds.channelBox('mainChannelBox', e = True, attrRegex = a, attrColor = aFont, attrBgColor = aColour )



			else:
				sColourMatch = ''
				iColourDim = 1
				'''
