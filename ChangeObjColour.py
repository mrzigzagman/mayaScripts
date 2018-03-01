# Change Obj Colour v006
import maya.cmds as cmds
from functools import partial

K = cmds.getModifiers()

def ListSelection():
	''' List section into an array of strings'''
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	return oSel


def MessageBox(Message):
	'''Displaying Entered Message as Popup '''
	oWindow = cmds.window(title = 'Message Box', s = False)
	if cmds.windowPref(oWindow, exists = True):
		cmds.windowPref(oWindow, remove = True)
	cmds.columnLayout(adjustableColumn = True)
	cmds.text('\n\t%s\t\n' % Message, bgc = (.25,.25,.25),enableBackground = False)
	cmds.button(label = 'Close', command = ('cmds.deleteUI(\"'+oWindow+'\",window = True)'), bgc = (.2,.2,.2),enableBackground = False)
	cmds.setParent('..')
	cmds.showWindow(oWindow)


def Button_ChangeColour(iColour, *args):
	oSel = ListSelection()
	ChangeColour(oSel, iColour)

def ChangeColour(oSel, iColour):
	for o in oSel:
		cmds.setAttr("%s.overrideEnabled"%o, 1)
		cmds.setAttr ("%s.overrideColor"%o , iColour)

		if cmds.objExists("%sShape.overrideEnabled"%o):
			cmds.setAttr("%sShape.overrideEnabled"%o, 1)
			cmds.setAttr("%sShape.overrideColor"%o , iColour)

		if cmds.objExists("%s_CRVShape.overrideEnabled"%o):
			cmds.setAttr("%s_CRVShape.overrideEnabled"%o, 1)
			cmds.setAttr("%s_CRVShape.overrideColor"%o , iColour)



def ColourPalette():

	oUI = 'Colour Picker'

	aBG = [
		[16 ,[ 1.0 , 1.0 , 1.0 ]],
		[11 ,[ 0.25 , 0.14 , 0.12 ]],
		[24 ,[ 0.63 , 0.41 , 0.19 ]],
		[10 ,[ 0.54 , 0.28 , 0.2 ]],
		[12 ,[ 0.6 , 0.15 , 0 ]],
		[13 ,[ 1.0 , 0 , 0 ]],
		[4 ,[ 0.61 , 0 , 0.16 ]],
		[31 ,[ 0.63 , 0.19 , 0.41 ]],
		[3 ,[ 0.5 , 0.5 , 0.5 ]],
		[25 ,[ 0.62 , 0.63 , 0.19 ]],
		[22 ,[ 1.0 , 1.0 , 0.39 ]],
		[17 ,[ 1.0 , 1.0 , 0 ]],
		[21 ,[ 0.89 , 0.67 , 0.47 ]],
		[20 ,[ 1.0 , 0.69 , 0.69 ]],
		[9 ,[ 0.78 , 0 , 0.78 ]],
		[30 ,[ 0.44 , 0.19 , 0.63 ]],
		[2 ,[ 0.25 , 0.25 , 0.25 ]],
		[26 ,[ 0.41 , 0.63 , 0.19 ]],
		[14 ,[ 0 , 1.0 , 0 ]],
		[19 ,[ 0.26 , 1.0 , 0.64 ]],
		[18 ,[ 0.39 , 0.86 , 1.0 ]],
		[29 ,[ 0.19 , 0.4 , 0.63 ]],
		[15 ,[ 0 , 0.25 , 0.6 ]],
		[8 ,[ 0.15 , 0 , 0.26 ]],
		[1 ,[ 0 , 0 , 0 ]],
		[7 ,[ 0 , 0.27 , 0.1 ]],
		[23 ,[ 0 , 0.6 , 0.33 ]],
		[27 ,[ 0.19 , 0.63 , 0.36 ]],
		[28 ,[ 0.19 , 0.63 , 0.63 ]],
		[6 ,[ 0 , 0 , 1.0 ]],
		[5 ,[ 0 , 0.02 , 0.38 ]],
		[0 ,[ 0.3 , 0.3 , 0.3 ]],]

	iWidth  = 160	# Total  Width of Window in pixel
	iHeight = 100	# Total Height of Window in pixel

	oWindow = cmds.window(w = iWidth, h = iHeight, mnb = False, mxb = False, title = oUI, sizeable = False)

	cmds.rowColumnLayout(numberOfRows = 4, height = iHeight )
	iWidth = 25
	cmds.rowColumnLayout(numberOfColumns = 8, columnWidth = [(1,iWidth),(2,iWidth),(3,iWidth),(4,iWidth),(5,iWidth),(6,iWidth),(7,iWidth),(8,iWidth)])

	for o in aBG:
		if o[0] == 0:
			sLabel = 'Def'
		else:
			sLabel = o[0]
		cmds.button(label = str(sLabel), bgc = [o[1][0],o[1][1],o[1][2]], command = partial (Button_ChangeColour, o[0]), enableBackground = False)

	cmds.showWindow( oWindow )

def main():
	global oUI, aBG
	oSel = ListSelection()
	iColour = -1
	if K == 8:
		iColour = 13

	elif K == 1:
		iColour = 17

	elif K == 4:
		iColour = 6

	elif K == 5:
		iColour = 14

	elif K == 9:
		iColour = 12

	elif K == 12:
		iColour = 30

	elif K == 0:
		ColourPalette()


	else:
		sString = '''
		- Colour Picker Menu -

		RED ---------------------- ALT [8]
		BLUE -------------------- CTL [4]
		YELLOW ---------------- SFT [1]


		GREEN ---------- SFT + CTL [5]
		ORANGE --------- SFT + ALT [9]
		PURPLE -------- CTL + ALT [12]

		Colour Picker ----- S + C + A [13]  '''

		MessageBox(sString)




	if oSel == ['']:
		MessageBox('Nothing is selected.')
	else:
		if iColour > -1:
			ChangeColour(oSel, iColour)
