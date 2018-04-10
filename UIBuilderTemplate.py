# UI BUILDER TEMPLATE 7.0.0
from functools import partial
import maya.cmds as cmds

# CUSTOM
import StudioSettings
import UIColourControl
import UIWindowControl

K = cmds.getModifiers()

def main():
	oWin = UIWindowControl.UIBuilder()

	oWin.oUI = 'TEMP_UI_WINDOW'
	oWin.Width = 450 # Total Width of Window in pixel (Default 320)
	oWin.Height = 1590 # Total Height of Window in pixel
	oWin.iRowHeight = 25

	UIReBuild()


def	UIReBuild():
	oWin.UIPrepare()
	UILayout()
	oWin.UICreate()

def UILayout():
	# Row
	oWin.UIDivision([.6,.6,.6,1,1.8,.7,0.1,1], None, 0); aRow = [
	cmds.text(l = 'Range :', h = oWin.iRowHeight, w = oWin.Div[0][0]),
	cmds.textField(tx = '1001', h = oWin.iRowHeight, w = oWin.Div[0][1]),
	cmds.textField(tx = '1216', h = oWin.iRowHeight, w = oWin.Div[0][2]),
	cmds.button(label = 'Current range', h = oWin.iRowHeight, w = oWin.Div[0][3], bgc = UIColourControl.keywordColour('tone2'), enableBackground = False),
	cmds.button(label = 'PlayBlast            [1]', h = oWin.iRowHeight, w = oWin.Div[0][4], bgc = UIColourControl.keywordColour('tone2'), enableBackground = False),
	cmds.button(label = '[2]', h = oWin.iRowHeight, w = oWin.Div[0][5], bgc = (0, .1, .1), enableBackground = False),
	cmds.button(label = '', h = oWin.iRowHeight, w = oWin.Div[0][6]),
	cmds.button(label = 'Current', h = oWin.iRowHeight, w = oWin.Div[0][7], bgc = (0, .1, .1), enableBackground = False),
	]; oWin.UIAddRow(aRow)


	## Row
	oWin.UIDivision([.6,.6,.6,1,1.1,0.7,0.7,0.1,1]); aRow = [
	cmds.text(l = 'Set : ', h = oWin.iRowHeight, w = oWin.Div[0][0]),
	cmds.button(label = 'Bigger', h = oWin.iRowHeight, w = oWin.Div[0][1], bgc = (1,1,1), enableBackground = False, c = partial(UIButton_Bigger, 500) ),
	cmds.button(label = 'Smaller', h = oWin.iRowHeight, w = oWin.Div[0][2], bgc = (1,1,1), enableBackground = False, c = partial(UIButton_Smaller, 100) ),
	cmds.button(label = 'Prod Range', h = oWin.iRowHeight, w = oWin.Div[0][3], bgc = (1,1,1), enableBackground = False),
	cmds.text(l = '', h = oWin.iRowHeight, w = oWin.Div[0][4]),
	cmds.button(label = '[3]', h = oWin.iRowHeight, w = oWin.Div[0][5], bgc = (1,1,1), enableBackground = False),
	cmds.separator(height = 40, style = 'in', w = oWin.Div[0][6]),
	cmds.separator(height = 40, style = 'in', w = oWin.Div[0][7]),
	cmds.button(label = 'Marked', h = oWin.iRowHeight, w = oWin.Div[0][8], bgc = (1,1,1), enableBackground = False),
	]; oWin.UIAddRow(aRow)


	## Row
	oWin.UIDivision([.6,1.2,1,0.4,.7,1.4,0.1,1]); aRow = [
	cmds.text(l = 'Weta : ', h = oWin.iRowHeight, w = oWin.Div[0][0]),
	cmds.button(label = 'BLAST', h = oWin.iRowHeight, w = oWin.Div[0][1], bgc = (0,.1,.1), enableBackground = False),
	cmds.button(label = 'SHOTSUB', h = oWin.iRowHeight, w = oWin.Div[0][2], bgc = (0,.1,.1), enableBackground = False),
	cmds.text(l = '', h = oWin.iRowHeight, w = oWin.Div[0][3]),
	cmds.button(label = 'Saved', h = oWin.iRowHeight, w = oWin.Div[0][4], bgc = (0,.1,.1), enableBackground = False ),
	AddDropMenu('DropdownMenu', oWin.Div[0][5], 4, 'drop', partial(Dropdown_Changed, 1), ['1','2','3','4'], 1),
	cmds.text(l = '', h = oWin.iRowHeight, w = oWin.Div[0][6]),
	cmds.button(label = 'Range', h = oWin.iRowHeight, w = oWin.Div[0][7], bgc = (0,.1,.1), enableBackground = False ),
	]; oWin.UIAddRow(aRow)

	## Row
	oWin.UIDivision([1,1]); aRow = [
	cmds.floatSliderGrp('floatSlider1', label = 'Size', field = True, h = oWin.iRowHeight, w = oWin.Div[0][0], cw = [1, 25], cc = partial(FloatSlider_Changed, 'floatSlider1'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
	cmds.floatSliderGrp('floatSlider2', label = 'Size', field = True, h = oWin.iRowHeight, w = oWin.Div[0][0], cw = [1,25], cc = partial(FloatSlider_Changed, 'floatSlider1'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
	]; oWin.UIAddRow(aRow)

	## Row
	oWin.UIDivision([1,1,1,1,1]); aRow = [
	cmds.separator( height = 40, style = 'none', w = oWin.Div[0][0] ),
	cmds.separator( height = 40, style = 'single', w = oWin.Div[0][0] ),
	cmds.separator( height = 40, style = 'out', w = oWin.Div[0][0] ),
	cmds.separator( height = 40, style = 'in', w = oWin.Div[0][0] ),
	cmds.separator( height = 40, style = 'shelf', w = oWin.Div[0][0] ),
	]; oWin.UIAddRow(aRow)


def UIButton_Bigger(iHeight, *args):
	oWin.Height = iHeight
	UIReBuild()

	aPrint = UIColourControl.inViewMessageColourPreset('Red', 'BIGGER!!')
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def UIButton_Smaller(iHeight, *args):
	oWin.Height = iHeight
	UIReBuild()


	aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'SMALLER!!')
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )


def FloatSlider_Changed(sGrp, *args):
	print 'Float Slider Changed %s'% sGrp
	cmds.floatSliderGrp(sGrp, e = True, v = 1)

def Dropdown_Changed(i, *args):
	print 'Dropped down! as : %s' % i


### UI CREATION FUNCTIONS ###
def AddDropMenu(sName, fWidth, iLen, sLabel, CC, aList, iMenu):
	'''
	A custom function to add optionMenu(...) to UIAddRow() WITH menus already attached.

	AddDropMenu(sName, FWidth, iLen, sLabel, CC, aList, iMenu)
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
