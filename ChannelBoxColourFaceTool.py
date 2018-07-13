# ChannelBox attr Colour change for Facial v0.0.0

import maya.cmds as cmds
import colorsys

# CUSTOM
import UIColourControl


def main():
	iColour = 1
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	if not oSel:
		iColour = 0
		aPrint = UIColourControl.inViewMessageColourPreset('Red', 'SELECT a FacialActionControl.')
		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 12, ft = 'arial',bkc = aPrint[2] )


	if iColour: # Set Colour in ChannelBox

		# remove non-Facial attributes
		aAttrList = cmds.listAttr(oSel[0], v = True)
		#aAttrList = cmds.listAttr(self.aPuppet[self.iChar], v = True)

		# Remove all attributes before 'fr_'
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
			sKey = a[3:]# .lower() To set keys all lowercase? to be decided

			if sKey in dColour.keys():
				sColour = sKey

			aColour = UIColourControl.convertRGBvaluesToScaleOf(1, dColour[sColour][0])
			aFont = UIColourControl.convertRGBvaluesToScaleOf(1, dColour[sColour][1])

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
				sColourMatch = ''
				iColourDim = 1

if __name__ == '__main__':
	 main()
