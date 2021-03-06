# UI BUILDER TEMPLATE 7.1.0
from functools import partial
import maya.cmds as cmds

# CUSTOM
import StudioSettings
import UIColourControl

import UIWindowControl
reload(UIWindowControl)

K = cmds.getModifiers()

def main(): # UI BUILDER TEMPLATE 7.1.0
	global oUI
	oUI = UIWindowControl.UIBuilder()

	oUI.sUI = 'TEMP_UI_WINDOW'
	oUI.Width = 450 # Total Width of Window in pixel (Default 320)
	oUI.Height = 1590 # Total Height of Window in pixel
	oUI.iRowHeight = 25

	UIReBuild()

if __name__ == '__main__':
	 main()

def UILayout():

	# Row
	oUI.UIDivision([.6,.6,.6,1,1.8,.7,0.1,1], None, 0); aRow = [ # Optional Setting (  ...], None, 0) = (...], Gaps in pixel Between each Element, above row )
	cmds.text(l = 'Range :', h = oUI.iRowHeight, w = oUI.Div[0][0]),
	cmds.textField(tx = '1001', h = oUI.iRowHeight, w = oUI.Div[0][1]),
	cmds.textField(tx = '1216', h = oUI.iRowHeight, w = oUI.Div[0][2]),
	cmds.button(label = 'Current range', h = oUI.iRowHeight, w = oUI.Div[0][3], bgc = UIColourControl.keywordColour('tone2'), enableBackground = False),
	cmds.button(label = 'PlayBlast            [1]', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('tone2'), enableBackground = False),
	cmds.button(label = '[2]', h = oUI.iRowHeight, w = oUI.Div[0][5], bgc = (0, .1, .1), enableBackground = False),
	cmds.button(label = '', h = oUI.iRowHeight, w = oUI.Div[0][6]),
	cmds.button(label = 'Current', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = (0, .1, .1), enableBackground = False),
	]; oUI.UIAddRow(aRow)


	## Row
	oUI.UIDivision([.6,.6,.6,1,1.1,0.7,0.7,0.1,1]); aRow = [
	cmds.text(l = 'Set : ', h = oUI.iRowHeight, w = oUI.Div[0][0]),
	cmds.button(label = 'Bigger', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = (1,1,1), enableBackground = False, c = partial(UIButton_Bigger, 500) ),
	cmds.button(label = 'Smaller', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = (1,1,1), enableBackground = False, c = partial(UIButton_Smaller, 100) ),
	cmds.button(label = 'Prod Range', h = oUI.iRowHeight, w = oUI.Div[0][3], bgc = (1,1,1), enableBackground = False),
	cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][4]),
	cmds.button(label = '[3]', h = oUI.iRowHeight, w = oUI.Div[0][5], bgc = (1,1,1), enableBackground = False),
	cmds.separator(height = 40, style = 'in', w = oUI.Div[0][6]),
	cmds.separator(height = 40, style = 'in', w = oUI.Div[0][7]),
	cmds.button(label = 'Marked', h = oUI.iRowHeight, w = oUI.Div[0][8], bgc = (1,1,1), enableBackground = False),
	]; oUI.UIAddRow(aRow)


	## Row
	oUI.UIDivision([.6,1.2,1,0.4,.7,1.4,0.1,1]); aRow = [
	cmds.text(l = 'Weta : ', h = oUI.iRowHeight, w = oUI.Div[0][0]),
	cmds.button(label = 'BLAST', h = oUI.iRowHeight, w = oUI.Div[0][1], bgc = (0,.1,.1), enableBackground = False),
	cmds.button(label = 'SHOTSUB', h = oUI.iRowHeight, w = oUI.Div[0][2], bgc = (0,.1,.1), enableBackground = False),
	cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][3]),
	cmds.button(label = 'Saved', h = oUI.iRowHeight, w = oUI.Div[0][4], bgc = (0,.1,.1), enableBackground = False ),
	AddDropMenu('DropdownMenu', oUI.Div[0][5], 4, 'drop', Dropdown_Changed, ['test1','test2','test3','test4'], 1),
	cmds.text(l = '', h = oUI.iRowHeight, w = oUI.Div[0][6]),
	cmds.button(label = 'Range', h = oUI.iRowHeight, w = oUI.Div[0][7], bgc = (0,.1,.1), enableBackground = False ),
	]; oUI.UIAddRow(aRow)

	## Row
	oUI.UIDivision([1,1]); aRow = [
	cmds.floatSliderGrp('floatSlider1', label = 'Size', field = True, h = oUI.iRowHeight, w = oUI.Div[0][0], cw = [1, 25], cc = partial(FloatSlider_Changed, 'floatSlider1'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
	cmds.floatSliderGrp('floatSlider2', label = 'Size', field = True, h = oUI.iRowHeight, w = oUI.Div[0][0], cw = [1,25], cc = partial(FloatSlider_Changed, 'floatSlider2'), minValue = 0.1, maxValue = 2.0, fieldMinValue = 0.1, fieldMaxValue = 2.0, value = 1),
	]; oUI.UIAddRow(aRow)

	## Row
	oUI.UIDivision([1,1,1,1,1]); aRow = [
	cmds.separator( height = 40, style = 'none', w = oUI.Div[0][0] ),
	cmds.separator( height = 40, style = 'single', w = oUI.Div[0][0] ),
	cmds.separator( height = 40, style = 'out', w = oUI.Div[0][0] ),
	cmds.separator( height = 40, style = 'in', w = oUI.Div[0][0] ),
	cmds.separator( height = 40, style = 'shelf', w = oUI.Div[0][0] ),
	]; oUI.UIAddRow(aRow)

	## Row
	oUI.UIDivision([1]); aRow = [
	cmds.textField('uiTextField', w = oUI.Div[0][0], bgc = UIColourControl.keywordColour('tone1'), tcc = partial(TextField_TextCheck, 'uiTextField'), cc = partial(TextField_TextShow, 'uiTextField')),
	]; oUI.UIAddRow(aRow)

def	UIReBuild():
	global oUI
	oUI.UIPrepare()
	UILayout()
	oUI.UICreate()

def TextField_TextCheck(sFieldName, *args):
	oUI.StringCheck_FileName(sFieldName)

def TextField_TextShow(sFieldName, *args):
	sText = cmds.textField(sFieldName, tx = True, q = True)

	aPrint = UIColourControl.inViewMessageColourPreset('Red', sText)
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def UIButton_Bigger(iHeight, *args):
	oUI.Height = iHeight
	UIReBuild()

	aPrint = UIColourControl.inViewMessageColourPreset('Red', 'BIGGER!!')
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def UIButton_Smaller(iHeight, *args):
	oUI.Height = iHeight
	UIReBuild()


	aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'SMALLER!!')
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )


def FloatSlider_Changed(sGrp, *args):
	print 'Float Slider Changed %s'% sGrp
	print cmds.floatSliderGrp(sGrp, q = True, v = True)

	if sGrp.endswith('1'):
		cmds.floatSliderGrp(sGrp, e = True, v = 1)





def Dropdown_Changed(*args):
	print cmds.optionMenu('DropdownMenu', q = True, value = True)


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
