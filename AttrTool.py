# AttrFilterTool v0.4.0
# Select the faceCtrl when filter is checked.
# Add a button to select Eye Controller.

import maya.cmds as cmds
import imp
#import json
#import maya.mel as mel
#import getpass
#import os
from functools import partial

# CUSTOM
import UIColourControl
reload(UIColourControl)

K = cmds.getModifiers()


### Class Assignment ###
class UIBuilder: # UI BUILDER TEMPLATE .6.1.3

	### Class FUnctions ###
	def __init__(self):

		self.Temp = ''

		self.sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts'
		# Keywords must start with Capital letters.
		self.oFilter = None
		self.aCategoryList = [	'Brow',
								'Eye',
								'Nose',
								'Cheek',
								'UpperLip',
								'Lip',
								'LowerLip',
								'Jaw',
								'Neck',
								'Extra',]

		# Keywords : Always with Caps. (smaller case tobe added later. with .lowercase() )
		# Except : In Caps but, Without any '*'s (direct find of of words)
		self.dFilterList = {	'Brow': {'KeyWords':['*Brow*', '*Procerus*', '*Supercilii*', '*Scalp*' ],
										'Except': [],
										'Colour':'gray',
										'Key': 'Brow',},
								'Eye':  {'KeyWords':['*Eye*','*Pupil*', '*LidTightner*', '*Procerus*', '*Squint*', '*Lid*', '*Epicanthic*',  ],
										'Except': ['Scalp'],
										'Colour':'gray',
										'Key': 'Eye',},
								'Nose': {'KeyWords':['*Nose*', '*Nasolabial*', '*Nostril*', '*Philtrum*' ],
										'Except': [],
										'Colour':'gray',
										'Key': 'Nose',},
								'Cheek':{'KeyWords':['*Cheek*',],
										'Colour':'gray',
										'Except': [],
										'Key': 'Cheek',},
								'UpperLip':  {'KeyWords':['*Lip*','*Upper*',],
										'Colour':'gray',
										'Except': ['Platysma', 'Brow'],
										'Key': 'UpperLip',},
								'Lip':  {'KeyWords':['*Lip*', '*Dimpler*', '*Grin*', '*Chin*', '*Pressor*', '*Funneler*'],
										'Colour':'gray',
										'Except': ['Nose'],
										'Key': 'Lip',},
								'LowerLip':  {'KeyWords':['*Lip*','*Lower*', '*Chin*'],
										'Colour':'gray',
										'Except': ['Platysma', 'Brow'],
										'Key': 'LowerLip',},
								'Jaw':  {'KeyWords':['*Jaw*', '*Chin*'],
										'Colour':'gray',
										'Except': [],
										'Key': 'Jaw',},
								'Neck': {'KeyWords':['*Neck*', '*Swallow*', '*Throat*', '*Platysma*'],
										'Colour':'gray',
										'Except': [],
										'Key': 'Neck',},

								'Extra':{'KeyWords':['*Tongue*', '*Ears*' ],
										'Colour':'gray',
										'Except': [],
										'Key': 'Extra',},
								}
		for key in self.dFilterList.keys():
			aKeys = self.dFilterList[key]['KeyWords']
			self.dFilterList[key]['KeyWords'].extend([str(s).lower() for s in aKeys ])

		aAddList = ['B','L','R']

		for n in self.aCategoryList:
			for a in aAddList:
				self.dFilterList[n].update({a:'b%s%s'%(n,a)})

		self.aActiveButtons = []
		self.colourTweak = 0



		self.iChar = 0
		self.aFaces = ['   ']
		self.aPuppet = cmds.ls('*:FacialActionControl')
		if self.aPuppet:
			self.aFaces = []
			for f in cmds.ls('*:FacialActionControl'):
				self.aFaces.extend([str(s).replace(':chr',' ').replace('FacePuppet', '') for s in cmds.ls('%s:chr*'%f.split(':')[0]) if s.endswith('Puppet') ])
		oSel = [str(s) for s in cmds.ls(sl = True, o = True)]
		if oSel:
			if oSel[0] in self.aPuppet:
				self.iChar = self.aPuppet.index(oSel[0])

		self.oUI = 'Facial Panel'
		self.UISetWindow()
		self.UICreate()



	def UISetWindow(self):
		### Pre-Setup ###
		self.Width = 130 # Total Width of Window in pixel (Default 320)
		self.Height = 235 # Total Height of Window in pixel

		self.iBoarderW = 10 # Default Empty Pixels around window for Width
		self.iBoarderH = 10 # Default Empty Pixels around window for Height

		self.iRowHeight = 25
		# self. sCurrentPanel = cmds.getPanel(withFocus = True)


		### Initial Setup ###

	def UIReBuild(self):
		'''Re-Create all UI'''
		if cmds.window(self.oUI, exists = True):
			cmds.deleteUI(self.oUI, window = True)
		# self. UISetWindow()
		self.UICreate()


	def UIAddRow(self, Entry):
		'''
		Collects List of maya commands for each entry in 'self.Row'. (Buttons, Boxes, Text Fields, etc.)
		'''
		self.Row.append([Entry, self.Div[1], self.Div[2]])

	def UIDivision(self, aList, iGap = None, iVerticalSpace = None):
		'''
		Automated width calculation function to find the ratio of entered number to divide into the UI elements

		ex:
		self.UIDivision([2,1,1,1], None, 0)

		- [2,1,1,1] is used to calculate the ratio. first element will get 2/5 ratio of the width. the rest will be 1/5/2
		- None = Number in pixels between UI elements
		- 0 = Number in pixels between the whole row of UI elements and a row above.
		'''

		# Logic #
		if iGap == None:
			iGap = 0

		if iVerticalSpace == None:

			iVerticalSpace = 0

		iGapPixel = (len(aList)-1) * iGap
		iSide = self.iBoarderW * 2
		iUseable = self.Width - iGapPixel - iSide

		iProp = 0
		for i in aList:
			iProp += i

		iSingle = iUseable / iProp


		self.Div = [[]]
		for l in range(len(aList)):
			self.Div[0].append(int(iSingle*aList[l]))

		iSum = sum(self.Div[0])
		iRemain = iUseable - iSum

		if iRemain:
			iCounter = 0
			iMax = len(self.Div[0])
			for i in range(iRemain):
				if iCounter > iMax - 1:
					iCounter = 0

				self.Div[0][iCounter] += 1
				iCounter += 1
		self.Div.extend([iGap, iVerticalSpace])

	def UIBGColour(self, sColour = 'Red'):

		# Get Maya BG Colour from pallette.
		sScriptName = 'MayaBGColour' # state the filename without '.py'
		MayaBGColour = imp.load_source(sScriptName, '%s/MayaBGColour.py'%self.sScriptPath)

		oRGB = MayaBGColour.getBGColour()

		sColour = sColour.lower()

		# List all keys in lowerCase
		dColour = { 'tone1':(1.000, 0.513, 0),
					'tone2':(0.814, 0.521, 0.189),
					'tone3':(0.745, 0.586, 0.341),
					'tone4':(0.492, 0.430, 0.334),

					# Need Revise on colour
					'white':(1,1,1),
					'darkgray':(0.3,0.3,0.3),
					'gray':(0.4, 0.4, 0.4),
					'blue':(0.6, 0.6, 0.8),
					'yellow':(1.0, 1.0, 0.8),
					'red':(0.7, 0.4, 0.4),
					'lightgray':(0.6, 0.6, 0.6),
					'whitegray':(0.8, 0.8, 0.8),

					'lightred':(0.7, 0.5, 0.5),
					'brightred':(0.9, 0.7, 0.7),

					'bluetone':(0.725, 0.921, 1.000),
					'bluegray':(0.425, 0.621, 0.700),


					# Need Revise on colour
					'white':(1,1,1),
					'darkgray':(0.3,0.3,0.3),
					'gray':(0.4, 0.4, 0.4),
					'blue':(0.8, 0.8, 0.9),
					'mayabg':oRGB,
					}

		return dColour[sColour]

	def UICreate(self):
		'''
		Creates the UI Window based on the info from UILayout. Core Logic.
		'''

		# Delete Current UI
		if cmds. window(self.oUI, exists = True):
			cmds.deleteUI(self.oUI, window=True)

		# Create window as formLayout
		self.oWindow = cmds.window(self.oUI, mnb = False, mxb = False, title = self.oUI, sizeable = False, bgc = self.UIBGColour('MayaBG'))
		self.oForm = cmds.formLayout()

		cmds.window(self.oWindow, edit=True, widthHeight = (self.Width, self.Height))

		self.Div = [] # [   [iP, iP, iP, iP], iGapBetweenCells, self.iRowHeightBetweenRows]
		self.Row = [] # Stores ALL creation for window separated by rows.

		self. UILayout()

		# Core Logic #
		aAP = []
		aAC = []
		for r in range(len(self.Row)):
			for i in range(len(self.Row[r][0])):
				if r == 0:
					if i == 0:
						aAP.append( (self.Row[r][0][i], 'top', self.iBoarderH, 0) )
						aAP.append( (self.Row[r][0][i], 'left', self.iBoarderW, 0) )

					else:
						aAP.append( (self.Row[r][0][i], 'top', self.iBoarderH, 0) )
						aAC.append( (self.Row[r][0][i], 'left', self.Row[r][1], self.Row[r][0][i-1]) )
				else:
					if i == 0:
						aAC.append( (self.Row[r][0][i], 'top', self.Row[r][2], self.Row[r-1][0][0]) )
						aAP.append( (self.Row[r][0][i], 'left', self.iBoarderW, 0) )

					else:
						aAC.append( (self.Row[r][0][i], 'top', self.Row[r][2], self.Row[r-1][0][0]) )
						aAC.append( (self.Row[r][0][i], 'left', self.Row[r][1], self.Row[r][0][i-1]) )
		# Create Layout
		#print aAP
		cmds.formLayout(self.oForm, edit = True, attachPosition = aAP)
		if aAC:
			cmds.formLayout(self.oForm, edit = True, attachControl = aAC)

		# Execute display UI
		cmds.showWindow(self.oWindow)

	def UILayout(self):
		'''
		The Most Customization happens here...
		self.UIDivision([1,1,1], None, 0) ; aRow = [    cmds.button(label = ' A Button!', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('Tone2'), enableBackground = False, command = self.ButtonAdd),]
					cmds.text(.....),
					cmds textField(), ] ; self.UIAddRow(aRow)
		'''

		aRow = []

		self.iRowHeight = 15


		## Row
		self.UIDivision([3,1], None, 0); aRow = [
		cmds.text('bChar1',label = self.aFaces[self.iChar].split(' ')[0], h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('MayaBG')),
		cmds.button('bEyeCtl',label = 'Eye', h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('bluetone'),c = partial(self.UIButton_EyeCtl)),
		]; self.UIAddRow(aRow)

		## Row
		self.UIDivision([1], None, 0); aRow = [
		cmds.button('bChar2',label = self.aFaces[self.iChar].split(' ')[1], h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('bluetone'),c = partial(self.UIButton_CharSwitch)),
		]; self.UIAddRow(aRow)



		for i, r in enumerate(self.aCategoryList):
			s = r
			if i in [0]:
				iH = 10
			elif i in [4]:
				iH = 2
				s = ''
			elif i in [6]:
				s = ''
			elif i in [7]:
				iH = 2
			else:
				iH = 0

			## Row
			self.UIDivision([1,2,1], None, iH); aRow = [
			cmds.button('b%sR'%r,label = '', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour(self.dFilterList[r]['Colour']),c = partial(self.UIButton_Filter, i, 'R')),
			cmds.button('b%sB'%r,label = s, h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour(self.dFilterList[r]['Colour']),c = partial(self.UIButton_Filter, i, 'B')),
			cmds.button('b%sL'%r,label = '', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour(self.dFilterList[r]['Colour']),c = partial(self.UIButton_Filter, i, 'L')),
			]; self.UIAddRow(aRow)

		## Row
		self.UIDivision([1], None, 10); aRow = [
		cmds.button('bClear',label = 'Clear All ', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('darkgray'),c = partial(self.UIButton_Clear)),
		]; self.UIAddRow(aRow)

	def UIButton_Clear(self, *args):
		cmds.channelBox('mainChannelBox', e = True, attrFilter = 0)
		self.aActiveButtons = []
		self.UIRefresh()

	def	UIButton_CharSwitch(self, *args):
		sModel = cmds.button('bChar2', q = True, l = True)


		if sModel in self.aFaces:
			self.iChar = self.aFaces.index(sModel)



		if self.iChar == len(self.aFaces)-1:
			self.iChar = 0
		else:
			self.iChar += 1

		cmds.text('bChar1', e = True, l = self.aFaces[self.iChar].split(' ')[0])
		cmds.button('bChar2', e = True, l = self.aFaces[self.iChar].split(' ')[1])

		iColour = 0
		try:
			cmds.select(self.aPuppet[self.iChar], r = True)
			iColour = 1
		except:
			pass


		if iColour: # Set Colour in ChannelBox

			# remove non-Facial attributes
			aAttrList = cmds.listAttr(self.aPuppet[self.iChar], v = True)
			for a in aAttrList[:]:
				if not a.startswith('fr_'):
					aAttrList.remove(a)
				else:
					break

			# for all attributes for facial:
			sColour = 'default'
			dColour = UIColourControl.faceColour('getDict')
			for a in aAttrList:
				sKey = a[3:]
				if sKey in dColour.keys():
					sColour = sKey
				# NOT DONE HERE...
				#cmds.channelBox(self.aPuppet[self.iChar], attrRegex = a, attrColor = UIColourControl.offsetRGBvalues(dColour[sColour], -0.2, -0.2, -0.2), attrBgColor = dColour[sColour])
				#cmds.channelBox(self.aPuppet[self.iChar], attrRegex = a, attrBgColor = dColour[sColour])

				#print a,
			print self.aPuppet[self.iChar]


	def UIButton_EyeCtl(self, *args):

		oModel = cmds.text('bChar1', q = True, l = True)
		#print cmds.button('bChar2', q = True, l = True)
		#iLocal = cmds.getAttr('%s:eye_convergence_ctrl|%s:eye_settingsShape.local_world')
		cmds.select('%s:eye_settingsShape'%oModel)
		iLocal = cmds.getAttr('%s:eye_settingsShape.local_world' % oModel)

		if iLocal:
			cmds.select('%s:eye_world_ctrl'%oModel, r = True)
		else:
			cmds.select('%s:eye_local_ctrl'%oModel, r = True)


	def UIRefresh(self):
		aColour = ['bluegray','bluetone']
		if self.colourTweak == 1:
			aColour = ['lightred','brightred']

		for k in self.aCategoryList:
			for s in ['R','B','L']:
				cmds.button(self.dFilterList[k][s], e = True, bgc = self.UIBGColour('gray'))

		for a in self.aActiveButtons:
			cmds.button(a, e = True, bgc = self.UIBGColour(aColour[1]))
			cmds.button(a[:-1]+'B', e = True, bgc = self.UIBGColour(aColour[0]))

		for a in self.aActiveButtons:
			if a[-1] == 'B':
				for s in ['R','B','L']:
					cmds.button(a[:-1]+s, e = True, bgc = self.UIBGColour(aColour[1]))



	def	UIButton_Filter(self, iIndex, sSide, *args):

		# Re-Select Face Control
		sModel = cmds.button('bChar2', q = True, l = True)
		if sModel in self.aFaces:
			self.iChar = self.aFaces.index(sModel)
		cmds.select(self.aPuppet[self.iChar], r = True)


		K = cmds.getModifiers()

		if K == 0:
			self.aActiveButtons = []

		b = self.dFilterList[self.aCategoryList[iIndex]][sSide]
		# Logic to set self.aActiveButtons for UI colour and filter objects
		if  K in [0, 8]:
			self.colourTweak = 0
			if b[-1] == 'B':
				if b[:-1]+'B' in self.aActiveButtons:
					self.aActiveButtons.remove(b)
				elif b[:-1]+'R' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['R'])
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['B'])
				elif b[:-1]+'L' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['L'])
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['B'])
				else:
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['B'])

			elif b[-1] == 'R':
				if b[:-1]+'B' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['B'])
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['R'])
				elif b[:-1]+'R' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['R'])
				elif b[:-1]+'L' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['L'])
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['R'])
				else:
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['R'])
			else: # if b[-1] == 'L':
				if b[:-1]+'B' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['B'])
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['L'])
				elif b[:-1]+'R' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['R'])
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['L'])
				elif b[:-1]+'L' in self.aActiveButtons:
					self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['L'])
				else:
					self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['L'])




		else:
			if self.colourTweak: # 0 = without Tweaks / 1 = with tweaks.
				self.colourTweak = 0
			else:
				self.colourTweak = 1

		#print self.aActiveButtons


		### Create a List of Keywords to be Filtered. ###
		self.oFilter = cmds.itemFilterAttr(bns = 'Seach for an attr that NEVER EXIST')


		if self.aActiveButtons:
			for a in self.aActiveButtons:

				aKeyWords = self.dFilterList[a[1:-1]]['KeyWords']
				aKeyWordList = cmds.listAttr(r = True, st = aKeyWords) or []

				aExcept = self.dFilterList[a[1:-1]]['Except']


				for k in aKeyWordList[:]:
					iRemove = 0
					if K in [0, 8]: # Remove Tweaks unless Modifiers are activated.
						if 'tweak' in k.lower():
							iRemove = 1
					else:
						if self.colourTweak == 0:
							if 'tweak' in k.lower():
								iRemove = 1
					if 'upper' in a.lower():
						if not 'upper' in k.lower():
							iRemove = 1
					if 'lower' in a.lower():
						if not 'lower' in k.lower():
							iRemove = 1

					if aExcept:
						for e in aExcept:
							if e.lower() in k.lower():
								aKeyWordList.remove(k)

					if not a[-1] == 'B':
						if not k[-1] == sSide:
							iRemove = 1
					if 'fr_' in k.lower():
						iRemove = 0




					if iRemove:
						if k in aKeyWordList:
							aKeyWordList.remove(k)


				oKeyWordList = cmds.itemFilterAttr(bns = aKeyWordList)
				self.oFilter = cmds.itemFilterAttr(union = (self.oFilter, oKeyWordList))


		print aKeyWordList


		if self.aActiveButtons == []:
			self.oFilter = 0
		cmds.channelBox('mainChannelBox', e = True, attrFilter = self.oFilter)



		self.UIRefresh()


def main():
	UIBuilder()

if __name__ == '__main__':
	 main()
