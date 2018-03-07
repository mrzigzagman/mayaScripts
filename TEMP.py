import maya.cmds as cmds
#import imp
#import json
#import maya.mel as mel
#import getpass
#import os
from functools import partial

K = cmds.getModifiers()


### Class Assignment ###
class UIBuilder:

	### Class FUnctions ###
	def __init__(self):
		self.Temp = ''

		# Keywords must start with Capital letters.
		self.oFilter = None
		self.aCategoryList = [	'Brow',
								'Eye',
								'Nose',
								'Cheek',
								'Lip',
								'Jaw',
								'Neck',
								'Extra',]

		self.dFilterList = {	'Brow': {'KeyWords':['*Brow*', '*Procerus*'],
										'Colour':'gray',
										'Key': 'Brow',},
								'Eye':  {'KeyWords':['*Eye*',],
										'Colour':'gray',
										'Key': 'Eye',},
								'Nose': {'KeyWords':['*Nose*',],
										'Colour':'gray',
										'Key': 'Nose',},
								'Cheek':{'KeyWords':['*Cheek*',],
										'Colour':'gray',
										'Key': 'Cheek',},
								'Lip':  {'KeyWords':['*Lip*',],
										'Colour':'gray',
										'Key': 'Lip',},
								'Jaw':  {'KeyWords':['*Jaw*',],
										'Colour':'gray',
										'Key': 'Jaw',},
								'Neck': {'KeyWords':['*Neck*'],
										'Colour':'gray',
										'Key': 'Neck',},
								'Extra':{'KeyWords':['*Close*', ],
										'Colour':'gray',
										'Key': 'Extra',},
								}
		aAddList = ['B','L','R']

		for n in self.aCategoryList:
			for a in aAddList:
				self.dFilterList[n].update({a:'b%s%s'%(n,a)})

		self.aActiveButtons = []


		self.oUI = 'Facial Panel'
		self.UISetWindow()
		self.UICreate()




	def UISetWindow(self):
		### Pre-Setup ###
		self.Width = 150 # Total Width of Window in pixel (Default 320)
		self.Height = 185 # Total Height of Window in pixel

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
		sColour = sColour.lower()
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
		self.oWindow = cmds.window(self.oUI, mnb = False, mxb = False, title = self.oUI, sizeable = False)
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
		self.UIDivision([1], None, 0); aRow = [
		cmds.button('bChar',label = 'FACE chr Dr Strange', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('darkgray'),c = partial(self.UIButton_CharSwitch)),
		]; self.UIAddRow(aRow)


		for i, r in enumerate(self.aCategoryList):
			if i == 0:
				iH = 10
			else:
				iH = 0
			## Row
			self.UIDivision([1,2,1], None, iH); aRow = [
			cmds.button('b%sR'%r,label = '', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour(self.dFilterList[r]['Colour']),c = partial(self.UIButton_Filter, i, 'R')),
			cmds.button('b%sB'%r,label = r, h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour(self.dFilterList[r]['Colour']),c = partial(self.UIButton_Filter, i, 'B')),
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
		print 'character'


	def UIRefresh(self):
		for k in self.aCategoryList:
			for s in ['R','B','L']:
				cmds.button(self.dFilterList[k][s], e = True, bgc = self.UIBGColour('gray'))

		for a in self.aActiveButtons:
			cmds.button(a, e = True, bgc = self.UIBGColour('lightgray'))
			cmds.button(a[:-1]+'B', e = True, bgc = self.UIBGColour('lightgray'))

		for a in self.aActiveButtons:
			if a[-1] == 'B':
				for s in ['R','B','L']:
					cmds.button(a[:-1]+s, e = True, bgc = self.UIBGColour('whitegray'))



	def	UIButton_Filter(self, iIndex, sSide, *args):
		K = cmds.getModifiers()

		b = self.dFilterList[self.aCategoryList[iIndex]][sSide]
		# Logic to set self.aActiveButtons for UI colour and filter objects
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
				self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['L'])
			elif b[:-1]+'R' in self.aActiveButtons:
				self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['R'])
			elif b[:-1]+'L' in self.aActiveButtons:
				self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['L'])
				self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['B'])
			else:
				self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['R'])
		else: # if b[-1] == 'L':
			if b[:-1]+'B' in self.aActiveButtons:
				self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['B'])
				self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['R'])
			elif b[:-1]+'R' in self.aActiveButtons:
				self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['R'])
				self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['B'])
			elif b[:-1]+'L' in self.aActiveButtons:
				self.aActiveButtons.remove(self.dFilterList[self.aCategoryList[iIndex]]['L'])
			else:
				self.aActiveButtons.append(self.dFilterList[self.aCategoryList[iIndex]]['L'])

		#print self.aActiveButtons

		# Create a List of Keywords to be Filtered.
		self.oFilter = cmds.itemFilterAttr(bns = [])

		aTweaks = cmds.listAttr(r = True, st = '*Tweaks*') or []
		oTweaks = cmds.itemFilterAttr(bns = aTweaks)

		for a in self.aActiveButtons:
			aKeyWords = self.dFilterList[a[1:-1]]['KeyWords']
			aKeyWordList = cmds.listAttr(r = True, st = aKeyWords) or []
			oKeyWordList = cmds.itemFilterAttr(bns = aKeyWordList)

			if not a[-1] == 'B':
				aKeyWords.append('*%s'%a[-1])
				self.oFilter = cmds.itemFilterAttr(intersect = (oKeyWordList, oTweaks))











		print aKeyWords




		self.UIRefresh()

		iAdd = 0
		aList = cmds.listAttr(r = True, st = aKeyWords) or []
		if self.oFilter == None:
			self.oFilter = cmds.itemFilterAttr(bns = aList)
		elif iAdd == 0:
			pass
		elif iAdd == 1:
			self.oFilter = cmds.itemFilterAttr(union = (self.oFilter, cmds.itemFilterAttr(bns = aList)))

		#print 1
		cmds.channelBox('mainChannelBox', e = True, attrFilter = self.oFilter)
		#print 2



		'''
		# Getting the General Filter
		oFilter = None
		for f in aList:
			oTemp = cmds.itemFilter(bn = f)
			oTemp = cmds.itemFilter(union = (oTemp, cmds.itemFilter(bn = f.lower())))
			if oFilter:
				oFilter = cmds.itemFilter(union = (oFilter, oTemp))
			else:
				oFilter = oTemp

		# Filtering out L/R
		if sSide == 'L':
			oComparisonFilter = cmds.itemFilter(bn = '*L')
		elif sSide == 'R':
			oComparisonFilter = cmds.itemFilter(bn = '*R')
		else:
			oComparisonFilter = None

		if oComparisonFilter:
			oFilter = cmds.itemFilter(intersect = (oFilter, oComparisonFilter))




		# Filtering Tweaks
		oTweak = None
		oTweak = cmds.itemFilter(bn = '*Tweak*')
		oTweak = cmds.itemFilter(union = (oTweak, cmds.itemFilter(bn = f.lower())))
		if K == 8: # ALT
			oFilter = cmds.itemFilter(intersect =(oFilter, oTweak))
		elif K == 4: # CTL
			pass
		elif K == 1: # Shift
			oFilter = oTweak


		else: # None
			oIntersect = cmds.itemFilter(intersect = (oFilter, oTweak))
			oFilter = cmds.itemFilter(difference = (oFilter, oIntersect))

		#if oTweak:
		#	oFilter = cmds.itemFilter(intersect = (oFilter, oComparisonFilter))




		cmds.channelBox('mainChannelBox', e = True, attrFilter = oFilter)

		cmds.delete(oTemp)
		#print sPart, sSide
		'''


	def UIButton_Bigger(self, iHeight, *args):
		print 'Bigger'
		self.Height = iRowHeight
		self.UIReBuild()

	def UIButton_Smaller(self, iHeight, *args):
		print 'Smaller'
		self.Height = iRowHeight
		self.UIReBuild()

	def FloatSlider_Changed(self, sGrp, *args):
		print 'Float Slider Changed %s'% sGrp
		cmds.floatSliderGrp(sGrp, e = True, v = 1)

	def Dropdown_Changed(self, i, *args):
		print 'Dropped down! as : %s' % i


	### UI CREATION FUNCTIONS ###
	def AddDropMenu(self, sName, fWidth, iLen, sLabel, CC, aList, iMenu):
		print 1
		'''
		A custom function to add optionMenu(...) to UIAddRow() WITH menus already attached.

		AddDropMenu(self, sName, FWidth, iLen, sLabel, CC, aList, iMenu)
		sName : Unique ID Name to refer back to edit later.
		fWidth : Width of the menu item
		iLen : The number of selectable menus. (To be used as : if only one: gray out and lock it.)
		sLabel : label of the menu = '' nothing. don't need in this case.
		CC: Change Command : to run when menu is changed.
		aList : list of menus to display

		iMenu : to be used as index of aDropMenu to store what's listing currently. (Later to be deleted all and re-created at change command)
		'''

		iMenu -= 1 # Be used as index of aDropMenu

		# Set the dropmenu to gray if there is only one menu. (no need to change anyways.)
		if iLen == 1:
			iLen = False
		else:
			iLen = True

		oCMD = cmds.optionMenu(sName, label = sLabel, en = iLen, w = fWidth, cc = CC)

		# Add selectable menus to above optionMenu.
		for l in aList:
			cmds.menuItem(l, label = l)
			#aDropMenu[iMenu].append(l)

		return oCMD


def main():
	UIBuilder()

if __name__ == '__main__':
	 main()
