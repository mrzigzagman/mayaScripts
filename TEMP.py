# UI BUILDER TEMPLATE .6.1.3
# Adding the MayaBGColour feature.


import maya.cmds as cmds
import maya.mel as mel
import getpass
import os
from functools import partial

K = cmds.getModifiers()


### Class Assignment ###
class UIBuilder:

	### Class FUnctions ###
	def __init__(self):
		self.Temp = ''
		self.sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts'


		self.oUI = 'test'
		self.UISetWindow()
		self.UICreate()


	def UISetWindow(self):
		### Pre-Setup ###
		self.Width = 450 # Total Width of Window in pixel (Default 320)
		self.Height = 590 # Total Height of Window in pixel

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
					'lightgray':(0.6, 0.6, 0.6),
					'whitegray':(0.8, 0.8, 0.8),
					'white':(1,1,1),
					'darkgray':(0.3,0.3,0.3),
					'gray':(0.4, 0.4, 0.4),
					'blue':(0.8, 0.8, 0.8),
					'yellow':(1.0, 1.0, 0.8),
					'red':(0.7, 0.4, 0.4),
					'lightgray':(0.7, 0.7, 0.7),
					'mayabg':oRGB,}

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
		print aAP
		cmds.formLayout(self.oForm, edit = True, attachPosition = aAP)
		if aAC:
			cmds.formLayout(self.oForm, edit = True, attachControl = aAC)

		# Execute display UI
		cmds.showWindow( self.oWindow)

	def UILayout(self):
		'''
		The Most Customization happens here...
		self.UIDivision([1,1,1], None, 0) ; aRow = [    cmds.button(label = ' A Button!', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('Tone2'), enableBackground = False, command = self.ButtonAdd),]
					cmds.text(.....),
					cmds textField(), ] ; self.UIAddRow(aRow)
		'''








		aRow = []

		self.iRowHeight = 25





		## Row
		self.UIDivision([.6,.6,.6,1,1.8,.7,0.1,1], None, 0); aRow = [
		cmds.text(l = 'Range :', h = self.iRowHeight, w = self.Div[0][0]),
		cmds.textField(tx = '1001', h = self.iRowHeight, w = self.Div[0][1]),
		cmds.textField(tx = '1216', h = self.iRowHeight, w = self.Div[0][2]),
		cmds.button(label = 'Current range', h = self.iRowHeight, w = self.Div[0][3], bgc = self.UIBGColour('tone2'), enableBackground = False),
		cmds.button(label = 'PlayBlast            [1]', h = self.iRowHeight, w = self.Div[0][4], bgc = self.UIBGColour('tone2'), enableBackground = False),
		cmds.button(label = '[2]', h = self.iRowHeight, w = self.Div[0][5], bgc = (0, .1, .1), enableBackground = False),
		cmds.button(label = '', h = self.iRowHeight, w = self.Div[0][6]),
		cmds.button(label = 'Current', h = self.iRowHeight, w = self.Div[0][7], bgc = (0, .1, .1), enableBackground = False),
		]; self.UIAddRow(aRow)



		## Row
		self.UIDivision([.6,.6,.6,1,1.1,0.7,0.7,0.1,1], None, 0); aRow = [
		cmds.text(l = 'Set : ', h = self.iRowHeight, w = self.Div[0][0]),
		cmds.button(label = 'Bigger', h = self.iRowHeight, w = self.Div[0][1], bgc = (1,1,1), enableBackground = False, c = partial(self.UIButton_Bigger, 500) ),
		cmds.button(label = 'Smaller', h = self.iRowHeight, w = self.Div[0][2], bgc = (1,1,1), enableBackground = False, c = partial(self.UIButton_Smaller, 100) ),
		cmds.button(label = 'Prod Range', h = self.iRowHeight, w = self.Div[0][3], bgc = (1,1,1), enableBackground = False),
		cmds.text(l = '', h = self.iRowHeight, w = self.Div[0][4]),
		cmds.button(label = '[3]', h = self.iRowHeight, w = self.Div[0][5], bgc = (1,1,1), enableBackground = False),
		cmds.separator(height = 40, style = 'in', w = self.Div[0][6]),
		cmds.separator(height = 40, style = 'in', w = self.Div[0][7]),
		cmds.button(label = 'Marked', h = self.iRowHeight, w = self.Div[0][8], bgc = (1,1,1), enableBackground = False),
		]; self.UIAddRow(aRow)


		## Row
		self.UIDivision([.6,1.2,1,0.4,.7,1.4,0.1,1], None, 0); aRow = [
		cmds.text(l = 'Weta : ', h = self.iRowHeight, w = self.Div[0][0]),
		cmds.button(label = 'BLAST', h = self.iRowHeight, w = self.Div[0][1], bgc = (0,.1,.1), enableBackground = False),
		cmds.button(label = 'SHOTSUB', h = self.iRowHeight, w = self.Div[0][2], bgc = (0,.1,.1), enableBackground = False),
		cmds.text(l = '', h = self.iRowHeight, w = self.Div[0][3]),
		cmds.button(label = 'Saved', h = self.iRowHeight, w = self.Div[0][4], bgc = (0,.1,.1), enableBackground = False ),
		self.AddDropMenu('DropdownMenu', self.Div[0][5], 4, 'drop', partial(self.Dropdown_Changed, 1), ['1','2','3','4'], 1),
		cmds.text(l = '', h = self.iRowHeight, w = self.Div[0][6]),
		cmds.button(label = 'Range', h = self.iRowHeight, w = self.Div[0][7], bgc = (0,.1,.1), enableBackground = False ),
		]; self.UIAddRow(aRow)

		## Row
		self.UIDivision([.6,.6,.6,1,1.8,.7,0.1,1], None, 0); aRow = [
		cmds.floatSliderGrp('floatSlider1', label = 'Size', field = True, h = self.iRowHeight, w = self.Div[0][0], cw = [1, 25], cc = partial(self.FloatSlider_Changed, 'floatSlider1'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
		cmds.floatSliderGrp('floatSlider2', label = 'Size', field = True, h = self.iRowHeight, w = self.Div[0][0], cw = [1,25], cc = partial(self.FloatSlider_Changed, 'floatSlider1'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
		]; self.UIAddRow(aRow)

		## Row
		self.UIDivision([1,1,1,1,1], None, 0); aRow = [
		cmds.separator( height = 40, style = 'none', w = self.Div[0][0] ),
		cmds.separator( height = 40, style = 'single', w = self.Div[0][0] ),
		cmds.separator( height = 40, style = 'out', w = self.Div[0][0] ),
		cmds.separator( height = 40, style = 'in', w = self.Div[0][0] ),
		cmds.separator( height = 40, style = 'shelf', w = self.Div[0][0] ),
		]; self.UIAddRow(aRow)

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
