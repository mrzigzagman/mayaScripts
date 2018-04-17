# Open/Save Tool v0 BOTSU
# Added opening without having a scene saved.
# W V 1/1
import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import os
from datetime import datetime
import getpass
import imp
import os.path

# Custom Modules
import StudioSettings
import UIWindowControl
import UIColourControl
import MayaBGColour

'''Scene files should be written like these
bt163_0235_DY.v000.01.Test.0001.ma
ata_2110_DY.v003.02.char1_publish.0003.ma'''

'''
Implement an error check to follow the format above. return an error if not following or/ to save a file with the format.
'''




### Class Assignment ###

class UIBuilder:

	### Class Functions ###
	def __init__(self):

		### Pre-Setup ###
		self.dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)

		self.oUI = UIWindowControl.UIBuilder()
		self.oUI.Width = 450 # Total Width of Window in pixel (Default 320)
		self.oUI.Height = 74 # Total Height of Window in pixel
		self.oUI.iBoarderW = 10 # Default Empty Pixels around window for Width
		self.oUI.iBoarderH = 10 # Default Empty Pixels around window for Height
		self.oUI.iRowHeight = 25
		self.oUI.sUI = 'SaveTool - %s %s' % (self.dShotInfo['sSeqNumber'], self.dShotInfo['sShotNumber'])


		self.sUser = getpass.getuser()

		self.aDropMenu = [[],[],[],[],]
		self.iButton1 = 0
		self.iButton2 = 0
		self.iTextField1 = 0
		self.iTextField2 = 0

		#self.sShotPath = '/'.join(self.dShotInfo['sScenePath'].split('/')[:-1]) ###
		self.sShotPath = os.path.join(os.path.split(self.dShotInfo['sScenePath'][:-1]))[0]
		#print self.sShotPath
		#print os.path.join(os.path.split(self.dShotInfo['sScenePath'][:-1]))[0]


		if self.ErrorCheckAndFolderCreation():
			self.aAllList = self.CollectMayaFiles()
			self.oWindow = None
		else:
			cmds.warning('Please Save your current scene.')


		self.UIReBuild()


	def	UIReBuild(self):
		self.oUI.UIPrepare()
		self.UILayout()
		self.oUI.UICreate()
		print self.oUI.Width
		print self.oUI.sUI


	def ErrorCheckAndFolderCreation(self):

		# if the current scene is not saved:
		aCurrentShot = os.getcwd().split('/')
		#aShots = self.sShotPath.split('/')
		#print aShots
		#print os.path.split(self.sShotPath)[0]
		#print os.path.normpath(self.sShotPath).split(os.sep)

		#path = os.path.normpath(path)
		#path.split(os.sep)

		aShots = os.path.normpath(self.sShotPath).split(os.sep)



		# Error check if the path is set to a Project
		iHealth = 1

		# vvv ?/? 6 is set to studio.
		if not len(aCurrentShot) == 6:
			iHealth = 0
		# /proj/mll/shots/ate/5120/motion/work/maya/dyabu/Scenes/ate_5120_dyabu.v000.00.FirstBuild.0000.ma
		if not aCurrentShot[1] == 'proj' and aCurrentShot[3] == 'shots':
			ihealth = 0


		# if all clear:
		'''
		if iHealth:
			# Check Folders Existance
			aPath = ['/Scenes',
			'/Scenes/Old',
			'/Exports',
			'/Images',
			'/Images/Refs',
			'/Images/Nuke',]

			for a in aPath:
				if not os.path.isdir(self.sShotPath + a):
					os.makedirs(self.sShotPath + a)'''

		if iHealth:
			# Check if there are any .ma files in /Scenes
			aMaFiles = []
			for o in os.listdir( self.dShotInfo['sScenePath']):
				if o.endswith('.ma'):
					if self.FileNameConventionCheck(o):
						aMaFiles.append(o)

			# Create the first scene if no ma file with correct naming exists.
			if not aMaFiles:
				sTempScene = self.dShotInfo['sScenePath']
				sTempScene += '/%s_%s_%s.v000.00.FirstBuild.0000.ma'%(dShotInfo['sSeqNumber'], dShotInfo['sShotNumber'], self.sUser)
				try:
					cmds.file( rename = sTempScene)
					cmds.file( save = True, type = 'mayaAscii')
				except Exception as e:
					print e # coding = utf-8




		return iHealth

	def FileNameConventionCheck(self, sFileName):
		iCheck = 1
		aFileName = sFileName.split('.')
		if not len(aFileName) == 6:
			iCheck = 0
		if iCheck:
			if not aFileName[1][0] =='v':
				iCheck = 0
			if not aFileName[2].isdigit() and aFileName[4].isDigit():
				iCheck = 0

		return iCheck




	def UILayout(self):
		'''
		The Most Customization happens here...
		self.UIDivision([1,1,1], None, 0)
		aRow = [    cmds.button(label = ' A Button!', h = self.iRowHeight, w = self.Div[0][0], bgc = UIColourControl.keywordColour('Tone2'), enableBackground = False, command = self.ButtonAdd),]
					cmds.text(.....),
					cmds.textField(),
					cmds.optionMenu(),
					self.fFUNCTION(),]
		self.UIAddRow(aRow)
		'''



		aRow = []



		self.oUI.iRowHeight = 15
		## Row
		self.oUI.UIDivision([3.8, .1, 1.2], None, 0)
		aRow = [
		cmds.button('oFolder', label = '', h = self.oUI.iRowHeight, w = self.oUI.Div[0][0], bgc = UIColourControl.keywordColour('Tone2'), enableBackground = False, command = self.Button_OpenFolder),
		cmds.text(label = '', h = self.oUI.iRowHeight, w = self.oUI.Div[0][1]),
		cmds.text('oTime', label = '', h = self.oUI.iRowHeight, w = self.oUI.Div[0][2]),
		]
		self.oUI.UIAddRow(aRow)


		self.oUI.iRowHeight = 20
		# Row
		self.oUI.UIDivision([1.2, .7, 2, .7, .5], None, 5)
		aRow = [
		self.AddDropMenu('DropdownMenu1_ShotNumber' , self.oUI.Div[0][0], len(self.aAllList[0]), '', partial(self.Dropdown_Changed, 1), self.aAllList[0], 1),
		self.AddDropMenu('DropdownMenu2_Version'    , self.oUI.Div[0][1], len(self.aAllList[1][0]), '', partial(self.Dropdown_Changed, 2), self.aAllList[1][0], 2),
		self.AddDropMenu('DropdownMenu3_Description', self.oUI.Div[0][2], len(self.aAllList[2][0][0]), '', partial(self.Dropdown_Changed, 3), self.aAllList[2][0][0], 3),
		self.AddDropMenu('DropdownMenu4_Increment'  , self.oUI.Div[0][3], len(self.aAllList[3][0][0][0]), '', partial(self.Dropdown_Changed, 4), self.aAllList[3][0][0][0], 4),
		cmds.button(label = 'Open', h = self.oUI.iRowHeight, w = self.oUI.Div[0][4], bgc = UIColourControl.keywordColour('Gray'), enableBackground = False, command = self.Button_Open),
		]
		self.oUI.UIAddRow(aRow)


		## Row

		self.oUI.UIDivision([1.1, 0.1, 0.6, 0.1, 1.9, 0.1, 0.6, 0.1,  0.5], None, 0)
		aRow = [
		cmds.textField('TextField1_ShotNumber', w = self.oUI.Div[0][0], bgc = UIColourControl.keywordColour('Gray'), cc = self.TextField_ShotName),
		cmds.text(l = '', w = self.oUI.Div[0][1]),

		cmds.button('Button1_VersionInc', label = '+', h = self.oUI.iRowHeight, w = self.oUI.Div[0][2], bgc = UIColourControl.keywordColour('Gray'), enableBackground = False, command = self.Button_IncrementVersion),
		cmds.text(label = '', w = self.oUI.Div[0][3]),
		cmds.textField('TextField2_Description', w = self.oUI.Div[0][4], bgc = UIColourControl.keywordColour('Gray'), cc = self.TextField_Description),
		cmds.text(label = '', w = self.oUI.Div[0][5]),

		cmds.button('Button2_SaveInc', label = '+', h = self.oUI.iRowHeight, w = self.oUI.Div[0][6], bgc = UIColourControl.keywordColour('Gray'), enableBackground = False, command = self.Button_IncrementSave),
		cmds.text(label = '', w = self.oUI.Div[0][7]),

		cmds.button('Button3_SaveInc', label = 'Save', h = self.oUI.iRowHeight, w = self.oUI.Div[0][8], bgc = UIColourControl.keywordColour('Tone2'), enableBackground = False, command = self.Button_Save),

		]

		self.oUI.UIAddRow(aRow)




		self.Refresh()
		self.GetTime()
		self.GetPath()
	def AddDropMenu(self, sName, fWidth, iLen, sLabel, CC, aList, iMenu):
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


	### BUTTON FUNCTIONS ###
	def Button_Save(self, *args):

		# Error Check
		iError = 0
		if self.iTextField1: # if First Box has been changed.
			sTextField1 = cmds.textField('TextField1_ShotNumber', q = True, text = True)
			sTextField2 = cmds.textField('TextField2_Description', q = True, text = True)
			if sTextField1 == '':
				iError = 2

			if sTextField2 == '':
				iError = 1

		elif self.iButton1 == 1: # if First Button has been changed.
			sTextField2 = cmds.textField('TextField2_Description', q = True, text = True)
			if sTextField2 == '':
				iError = 1

		elif self.iTextField2 == 1:
			sTextField2 = cmds.textField('TextField2_Description', q = True, text = True)
			if sTextField2 == '':
				iError = 1


		# if No error is found:
		if not iError:
			aMenu = [] # Collect current selection of menus and prepare to be used as index (-1)
			aMenu.append(cmds.optionMenu('DropdownMenu1_ShotNumber', q = True, sl = True) -1)
			aMenu.append(cmds.optionMenu('DropdownMenu2_Version', q = True, sl = True) -1)
			aMenu.append(cmds.optionMenu('DropdownMenu3_Description', q = True, sl = True) -1)

			aMenu.append(cmds.optionMenu('DropdownMenu4_Increment', q = True, sl = True) -1)

			# Getting the FileName separated in a list
			aFileName = [   self.aAllList[0][aMenu[0]],
							self.aAllList[1][aMenu[0]][aMenu[1]],
							self.aAllList[2][aMenu[0]][aMenu[1]][aMenu[2]].split('.')[0],
							self.aAllList[2][aMenu[0]][aMenu[1]][aMenu[2]].split('.')[1],
							self.aAllList[3][aMenu[0]][aMenu[1]][aMenu[2]][aMenu[3]],

							]

			# Preparing the new file name to be used as
			if self.iTextField1:
				aFileName[0] = cmds.textField('TextField1_ShotNumber', q = True, text = True)
				aFileName[2] = '01'
				aFileName[3] = cmds.textField('TextField2_Description', q = True, text = True)
				aFileName[4] = '0001'

			elif self.iButton1:
				aFileName[1] = 'v'+str(int(aFileName[1][1:])+1 ).zfill(3)
				aFileName[2] = '01'
				aFileName[3] = cmds.textField('TextField2_Description', q = True, text = True)
				aFileName[4] = '0001'

			elif self.iTextField2:
				aFileName[2] = str(int(aFileName[2]) +1).zfill(2)
				aFileName[3] = cmds.textField('TextField2_Description', q = True, text = True)
				aFileName[4] = '0001'

			elif self.iButton2:
				aFileName[4] = str(int(aFileName[4]) +1 ).zfill(4)


			# Saving New Scene FileName
			sFileName = '.'.join(aFileName)+'.ma'

			#aAllPath = cmds.file( q = True, sn = True).split('/')[:-1]
			#aAllPath.append(sFileName)
			sFileName = self.dShotInfo['sScenePath']+'/'+sFileName

			#sFileName = '/'.join(aAllPath)
			#print 'sFileName', sFileName
			cmds.file(rename = sFileName)
			cmds.file(save = True, type = 'mayaAscii')


			self.Refresh()
			self.Reset()
			print 'SAVED!! [%s]' % sFileName

		else:
			self.Reset()
			if iError == 1:
				cmds.warning('Please enter Description')
			elif iError == 2:

				cmds.warning('Please enter Shot Number')



		self.GetTime()
		self.GetPath()

	def Refresh(self):
		''' Refresh current Menu sets '''
		self.aAllList = self.CollectMayaFiles()

		# Delete All Menu ListSelection
		for i in range(0, len(self.aDropMenu)):
			for o in self.aDropMenu[i]:
				cmds.deleteUI(self.Underscore(o))


		## Recreate All Menu List from selectionConnection
		self.aDropMenu = [[], [], [], []]

		for o in self.aAllList[0]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu1_ShotNumber')
			self.aDropMenu[0].append(sMenu)

			if len(self.aAllList[0]) ==1:
				cmds.optionMenu('DropdownMenu1_ShotNumber', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu1_ShotNumber', e = True, en = True)


		for o in self.aAllList[1][0]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu2_Version')
			self.aDropMenu[1].append(sMenu)

			if len(self.aAllList[1][0]) == 1:

				cmds.optionMenu('DropdownMenu2_Version', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu2_Version', e = True, en = True)


		for o in self.aAllList[2][0][0]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu3_Description')
			self.aDropMenu[2].append(sMenu)

			if len(self.aAllList[2][0][0]) == 1:
				cmds.optionMenu('DropdownMenu3_Description', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu3_Description', e = True, en = True)


		for o in self.aAllList[3][0][0][0]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu4_Increment')
			self.aDropMenu[3].append(sMenu)

			if len(self.aAllList[3][0][0][0]) == 1:
				cmds.optionMenu('DropdownMenu4_Increment', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu4_Increment', e = True, en = True)

		self.GetTime()
		self.GetPath()

	def GetPath(self):
		cmds.button('oFolder', e = True, label = self.sShotPath.replace('/', ' / '))

	def GetTime(self):
		''' Getting Scene File Creation Time.'''
		sPath = self.GetScenePathFromUISelection()
		if os.path.exists(sPath):
			tCreateTime = os.path.getmtime(sPath)
			sTime = datetime.fromtimestamp(tCreateTime).strftime('%Y-%m-%d %H:%M:%S')
		else:
			sTime = '-'

		# Display time
		cmds.text('oTime', e = True, label = sTime)

	def Reset(self):
		''' Reset Save boxes to default.'''
		cmds.textField('TextField1_ShotNumber', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
		cmds.button('Button1_VersionInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
		cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
		cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
		self.iTextField1 = 0
		self.iButton1 = 0

		self.iTextField2 = 0
		self.iButton2 = 0

	def TextField_ShotName(self, *args): # Save Box1
		sText = cmds.textField('TextField1_ShotNumber', q = True, text = True)
		cmds.button('Button1_VersionInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
		cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Gray'))

		if sText:
			cmds.textField('TextField1_ShotNumber', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			self.iTextField1 = 1
		else:
			cmds.textField('TextField1_ShotNumber', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
			cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
			self.iTextField1 = 0

	def Button_IncrementVersion(self, *args): #Save Button 1
		cmds.textField('TextField1_ShotNumber', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
		cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Gray'))

		if self.iButton1:
			cmds.button('Button1_VersionInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
			cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
			self.iButton1 = 0
		else:
			cmds.button('Button1_VersionInc', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			self.iButton1 = 1

	def TextField_Description(self, *args): # Save Box 2
		sText = cmds.textField('TextField2_Description', q = True, text = True)

		if sText:
			cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Gray'))

			self.iTextField2 = 1
		else:
			if self.iTextField1:
				cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			else:
				cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
			cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
			self.iTextField2 = 0

	def Button_IncrementSave(self, *args): # Save Button 2
		cmds.textField('TextField1_ShotNumber', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')
		cmds.button('Button1_VersionInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
		cmds.textField('TextField2_Description', e = True, bgc = UIColourControl.keywordColour('Gray'), text = '')

		if self.iButton2:
			cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Gray'))
			self.iButton2 = 0
		else:
			cmds.button('Button2_SaveInc', e = True, bgc = UIColourControl.keywordColour('Tone2'))
			self.iButton2 = 1

	def Button_OpenFolder(self, *args):
		StudioSettings.ShotInfo(0,1) # (1,1) = (Folder Creation, Print paths.)

		if not cmds.getModifiers() == 0:
			StudioSettings.OSFileBrowserCommand(self.dShotInfo['sScenePath'])
			aPrint = ['a7a8af', 'Opening Folder.', 0x6b6c75]

		else:
			StudioSettings.CopyToClipBoard(self.dShotInfo['sScenePath'])
			aPrint = ['a7a8af', 'Copied to Clipboard.', 0x6b6c75]

		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

	def GetScenePathFromUISelection(self):
		''' Get current selection of menu from UI.'''
		self.aAllList = self.CollectMayaFiles()
		aAllPath = self.dShotInfo['sScenePath'].split('/')

		iDropDown1 = cmds.optionMenu('DropdownMenu1_ShotNumber', q = True, sl = True) -1
		iDropDown2 = cmds.optionMenu('DropdownMenu2_Version', q = True, sl = True) -1
		iDropDown3 = cmds.optionMenu('DropdownMenu3_Description', q = True, sl = True) -1
		iDropDown4 = cmds.optionMenu('DropdownMenu4_Increment', q = True, sl = True) -1

		sFileName = self.aAllList[0][iDropDown1]
		sFileName += '.'
		sFileName += self.aAllList[1][iDropDown1][iDropDown2]

		sFileName += '.'
		sFileName += self.aAllList[2][iDropDown1][iDropDown2][iDropDown3]
		sFileName += '.'
		sFileName += self.aAllList[3][iDropDown1][iDropDown2][iDropDown3][iDropDown4]
		sFileName += '.ma'

		aAllPath.append(sFileName)
		sAllPath = '/'.join(aAllPath)
		return sAllPath

	def Button_Open(self, *args):
		''' When Open Button is pressed.'''
		sAllPath = self.GetScenePathFromUISelection()
		if cmds.file(q = True, amf = True):
			self.MessageBox('Save?', sAllPath)

		else:
			# cmds.file(sAllPath, o = True)
			StudioSettings.OpenSceneCommand(sAllPath)

	def MessageBox(self, Message, sPath, *args):
		'''Displaying Entered Message as Popup '''

		self.oWindow = cmds.window(title = ' ', s = False)
		if cmds.windowPref(self.oWindow, exists = True):
			cmds.windowPref(self.oWindow, remove = True)
		cmds.columnLayout(adjustableColumn = True)
		cmds.text('/n/t%s/t/n'%Message, bgc = (.25,.25,.25), enableBackground = False)
		cmds.button(label = 'Cancel', command = ('cmds.deleteUI(\"'+self.oWindow+'\",window = True)'), bgc = (.2, .2, .2), enableBackground = False)
		cmds.button(label = "Don't Save", command = partial(self.Button_OpenFile, sPath, 1), bgc = (.2,.2,.2), enableBackground = False)
		cmds.button(label = "Save", command = partial(self.Button_OpenFile, sPath, 2), bgc = (.2,.2,.2), enableBackground = False)
		cmds.button(label = "Save Increment", command = partial(self.Button_OpenFile, sPath, 3), bgc = (.2,.2,.2), enableBackground = False)
		cmds.setParent('..')
		cmds.showWindow(self.oWindow)

	def Button_OpenFile(self, sPath, iVal, *args):
		if iVal == 1: # Don't save
			cmds.file(modified = False) # Fake the maya scene to force open that is has been saved already so it will load without asking.
		elif iVal == 2: # Save
			cmds.file(s = True, f = True)
		elif iVal == 3: # Increment Save
			mel.eval('incrementalSave;')

		if iVal: # if not Cancelled.
			StudioSettings.OpenSceneCommand(sPath)

		if self.oWindow:
			cmds.deleteUI(self.oWindow)

	def Dropdown_Changed(self, iMenu, *args):
		self.Reset()

		iDropDown1 = cmds.optionMenu('DropdownMenu1_ShotNumber', q = True, sl = True)
		iDropDown2 = cmds.optionMenu('DropdownMenu2_Version', q = True, sl = True)
		iDropDown3 = cmds.optionMenu('DropdownMenu3_Description', q = True, sl = True)
		iDropDown4 = cmds.optionMenu('DropdownMenu4_Increment', q = True, sl = True)
		aDropDown = [iDropDown1, iDropDown2, iDropDown3, iDropDown4]



		# Avoiding Previously slected menu number being more than the newly selected number. ex 3rd row selected, new list don't have 3rd row.
		if iMenu == 1:
			if len(self.aAllList[1][aDropDown[0]-1]) <= aDropDown[1]:
				aDropDown[1] = 1
				aDropDown[2] = 1
				aDropDown[3] = 1
		elif iMenu == 2:
			if len(self.aAllList[2][aDropDown[0]-1][aDropDown[1]-1]) <= aDropDown[2]:
				aDropDown[2] = 1
				aDropDown[3] = 1
		elif iMenu == 3:
			if len(self.aAllList[3][aDropDown[0]-1][aDropDown[1]-1][aDropDown[2]-1]) <= aDropDown[3]:
				aDropDown[3] = 1


		# Delete All Menu Lists
		for i in range(0, len(self.aDropMenu)):
			for o in self.aDropMenu[i]:
				cmds.deleteUI(self.Underscore(o))


		# Recreate All Menu list from recorded selection (aDropDown).
		self.aDropMenu = [[],[],[],[]]
		for o in self.aAllList[0]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu1_ShotNumber')
			self.aDropMenu[0].append(sMenu)


			if len(self.aAllList[aDropDown[0]-1]) == 1:
				cmds.optionMenu('DropdownMenu1_ShotNumber', e = True, en = False)

			else:
				cmds.optionMenu('DropdownMenu1_ShotNumber', e = True, en = True)

		for o in self.aAllList[1][aDropDown[0]-1]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu2_Version')
			self.aDropMenu[1].append(sMenu)

			if len(self.aAllList[1][aDropDown[0]-1]) == 1:
				cmds.optionMenu('DropdownMenu2_Version', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu2_Version', e = True, en = True)

		for o in self.aAllList[2][aDropDown[0]-1][aDropDown[1]-1]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu3_Description')
			self.aDropMenu[2].append(sMenu)

			if len(self.aAllList[2][aDropDown[0]-1][aDropDown[1]-1]) == 1:
				cmds.optionMenu('DropdownMenu3_Description', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu3_Description', e = True, en = True)

		for o in self.aAllList[3][aDropDown[0]-1][aDropDown[1]-1][aDropDown[2]-1]:
			sMenu = self.Underscore(o)
			cmds.menuItem(sMenu, label = sMenu, p = 'DropdownMenu4_Increment')
			self.aDropMenu[2].append(sMenu)

			if len(self.aAllList[3][aDropDown[0]-1][aDropDown[1]-1][aDropDown[2]-1]) == 1:
				cmds.optionMenu('DropdownMenu4_Increment', e = True, en = False)
			else:
				cmds.optionMenu('DropdownMenu4_Increment', e = True, en = True)


		# Reuse aDropDown to assign current selection
		if iMenu == 1:
			aDropDown[1] = 1
			aDropDown[2] = 1
			aDropDown[3] = 1
		elif iMenu == 2:
			aDropDown[2] = 1
			aDropDown[3] = 1
		if iMenu == 3:
			aDropDown[3] = 1

		cmds.optionMenu('DropdownMenu1_ShotNumber', e = True, sl = aDropDown[0])
		cmds.optionMenu('DropdownMenu2_Version', e = True, sl = aDropDown[1])
		cmds.optionMenu('DropdownMenu3_Description', e = True, sl = aDropDown[2])
		cmds.optionMenu('DropdownMenu4_Increment', e = True, sl = aDropDown[3])


		self.GetTime()
		self.GetPath()

	### General Fuctions ###

	def Underscore(self, sString):

		if sString[0].isdigit():
			sString = '_'+sString

		sNewString = ''
		for s in sString:
			if s.isalnum():
				sNewString += s
			else:
				sNewString += '_'

		return sNewString

	def CollectMayaFiles(self):
		aAllList = [[],[],[],[]]

		if self.dShotInfo['sScenePath']:
			aSceneFiles = []
			for o in os.listdir(self.dShotInfo['sScenePath']):
				if o.endswith('.ma'):
					if self.FileNameConventionCheck(o):
						aSceneFiles.append(o)

			aSceneFiles = list(reversed(aSceneFiles))


			# Create list of first dropdown (Shot Numbers) aAllList[0]
			for o in aSceneFiles:
				aFile = o.split('.')
				if not aFile[0] in aAllList[0]:
					aAllList[0].append(aFile[0])
					aAllList[0].sort(reverse = True)

			#Create list of each versions of each shot numbers (versions) aAllList[1]
			for i in range(0, len(aAllList[0])):
				aTemp = []
				for v in range(0, len(aSceneFiles)):

					if aAllList[0][i] in aSceneFiles[v]:
						#print aSceneFiles[v]

						iVer = aSceneFiles[v].split('.')[1]

						if not iVer in aTemp:
							aTemp.append(iVer)
							aTemp.sort(reverse = True)

					aAllList[1].append(aTemp)

				#Create list of definition of each files()

				for i in range(0, len(aAllList[0])):
					aTemp =[]
					for n in range(0, len(aAllList[1][i])):
						aTemp.append([])
						for o in aSceneFiles:
							if aAllList[0][i] +'.'+ aAllList[1][i][n] in o:
								sDes = '.'.join(o.split('.')[2:4])
								if sDes not in aTemp[n]:
									aTemp[n].append(sDes)
									aTemp[n].sort(reverse = True)

					aAllList[2].append(aTemp)


				# Continue here. List the Increment versions
				for i in range(0, len(aAllList[0])):
					aTemp = []
					for n in range(0, len(aAllList[1][i])):
						aTemp.append([])
						for v in range(0, len(aAllList[2][i][n])):
							aTemp[n].append([])

							sInc = aAllList[0][i] +'.'+ aAllList[1][i][n] + '.'+ aAllList[2][i][n][v]

							for o in aSceneFiles:
								if sInc in o:
									aTemp[n][v].append(o.split('.')[-2])

							# print sInc
							aTemp[n][v].sort(reverse = True)

					aAllList[3].append(aTemp)



			return aAllList

def main():
	oIsolationUI = UIBuilder()
	print '## OpenSaveTool.py'

if __name__ == '__main__':
	 main()
