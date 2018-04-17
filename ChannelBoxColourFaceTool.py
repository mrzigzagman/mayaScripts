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


		# for all attributes for facial:
		sColour = 'default'
		dColour = UIColourControl.faceColour('getDict')
		sColourMatch = ''
		iColourDim = 1
		for a in aAttrList:
			sKey = a[3:]
			if sKey in dColour.keys():
				sColour = sKey

			aColour = UIColourControl.getRGBvalues(dColour[sColour][0])
			aFont = UIColourControl.getRGBvalues(dColour[sColour][1])

			if not 'fr_' in a:


				# Dim every second entry (L/R combined)
				if not a[:-1] in sColourMatch:
					iColourDim = iColourDim * -1 + 1
				sColourMatch = a
				if iColourDim:
					aHSV = list(colorsys.rgb_to_hsv(aColour[0],aColour[1],aColour[2]) )
					aHSV[2] *= 0.85
					aColour = list(colorsys.hsv_to_rgb(aHSV[0],aHSV[1],aHSV[2]))

				cmds.channelBox('mainChannelBox', edit = True, attrRegex = a, attrColor = aFont, attrBgColor = aColour )

			else:
				print
				aHSV = list(colorsys.rgb_to_hsv(aColour[0],aColour[1],aColour[2]) )
				aHSV[2] *= 0.60
				aColour = list(colorsys.hsv_to_rgb(aHSV[0],aHSV[1],aHSV[2]))
				print a, '[', aColour[0]*225, ',', aColour[1]*225, ',', aColour[2]*225, ']'

				sColourMatch = ''
				iColourDim = 1
