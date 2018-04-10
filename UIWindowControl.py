# UI Window Control 0.0.0

import maya.cmds as cmds
#import maya.mel as mel
#import getpass
#import os
from functools import partial

# CUSTOM
#import StudioSettings
import UIColourControl

#K = cmds.getModifiers()

### Class Assignment ###
class UIBuilder:

	### Class FUnctions ###
	def __init__(self):
		#self.Temp = ''

		self.oUI = 'TEMP_UI'
		#self.UICreate()

		### Pre-Setup ###
		self.Width = 450 # Total Width of Window in pixel (Default 320)
		self.Height = 590 # Total Height of Window in pixel

		self.iBoarderW = 10 # Default Empty Pixels around window for Width
		self.iBoarderH = 10 # Default Empty Pixels around window for Height

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



	def UIPrepare(self):
		'''
		Creates the UI Window based on the info from UILayout. Core Logic.
		'''

		# Delete Current UI
		if cmds.window(self.oUI, exists = True):
			cmds.deleteUI(self.oUI, window=True)

		# Create window as formLayout
		self.oWindow = cmds.window(self.oUI, mnb = False, mxb = False, title = self.oUI, sizeable = False, bgc = UIColourControl.keywordColour('MayaBG'))
		self.oForm = cmds.formLayout()

		cmds.window(self.oWindow, edit=True, widthHeight = (self.Width, self.Height))

		self.Div = [] # [   [iP, iP, iP, iP], iGapBetweenCells, self.iRowHeightBetweenRows]
		self.Row = [] # Stores ALL creation for window separated by rows.

		#self. UILayout()

	def UICreate(self):
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
		cmds.showWindow( self.oWindow)


	def TEMP():
		def UIButton_Bigger(self, iHeight, *args):
			print 'Bigger'
			self.Height = iHeight
			self.UIReBuild()

			aPrint = UIColourControl.inViewMessageColourPreset('Red', 'BIGGER!!')
			cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

		def UIButton_Smaller(self, iHeight, *args):
			print 'Smaller'

			self.Height = iHeight
			self.UIReBuild()

			aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'SMALLER!!')
			cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )


		def FloatSlider_Changed(self, sGrp, *args):
			print 'Float Slider Changed %s'% sGrp
			cmds.floatSliderGrp(sGrp, e = True, v = 1)

		def Dropdown_Changed(self, i, *args):
			print 'Dropped down! as : %s' % i


		### UI CREATION FUNCTIONS ###
		def AddDropMenu(self, sName, fWidth, iLen, sLabel, CC, aList, iMenu):
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
	#print UIColourControl.keywordColour()
	UIBuilder()
