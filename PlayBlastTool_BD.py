# PlayBlast Tool v10.2.0
# Weta Custom 1/1

import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import os
import shutil
import getpass
import imp

### Class Assignment ###
# UIBuilder Template v006.0.2

### Class Assignment ###
class UIBuilder:

	### Class FUnctions ###
	def __init__(self):
		self.Temp = ''
		self.sTool = 'PBTool' # Tool name node under 'Anim_Tool'

		# Importing Studio Settings
		self.sScriptName = 'StudioSettings' # remove '.py'
		self.sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts'
		self.StudioSettings = imp.load_source(self.sScriptName, '%s/%s.py'%(self.sScriptPath,self.sScriptName))

		# Getting info using StudioSettings
		self.aShotInfo = self.StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)
		self.sRvPath = self.aShotInfo[6] + 'Active.rv'
		self.oUI = 'PB_%s_%s' % (self.aShotInfo[4], self.aShotInfo[3]) # Watch out when this is only numbers, the tool fails.

		# Setting up tool custom dictionary for storage
		self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
		if not self.dDict:
			self.dDict = {  '1': '1',
							'2': '-',
							'3': '-',
							'4': '-',
							'currentStartFrame': 1001,
							'currentEndFrame': 1010,
							'prodStartFrame': None,
							'prodEndFrame': None,
							'markedFrames':[],
							'CalcTool': 0,
							'AnnotateTool': 0,
							'ConvertTool': 0,
							'ConvertToolFrom': [0,0,0,0,0],
							'ConvertToolTo': [0,0,0,0,0],
							'PickedFile':'',
							'LastCapture':'',
							}

		# Reset display and sizes of extra tools.
		for tool in ['CalcTool', 'ConvertTool', 'AnnotateTool']:
			self.dDict[tool] = 0

		# Reset Convert tool
		self.dDict['ConvertToolFrom'] = [0,0,0,0,0]
		self.dDict['ConvertToolTo'] =[0,0,0,0,0]

		self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict) # Store dDict



		self.UISetWindow()

		self.UICreate()

		self.UIDisplayChecker()


	def UISetWindow(self):
		### Pre-Setup ###

		self.Width = 450 # Total Width of Window in pixel (Default 320)
		self.Height = 75 # Total Height of Window in pixel

		self.iBoarderW = 10 # Default Empty Pixels around window for Width
		self.iBoarderH = 10 # Default Empty Pixels around window for Height

		self.iRowHeight = 20
		# self. sCurrentPanel = cmds.getPanel(withFocus = True)


		### Initial Setup ###

	def UIReBuild(self):
		'''Re-Create all UI'''
		if cmds.window(self.oUI, exists = True):
			cmds.deleteUI(self.oUI, window = True)

		self.UICreate()

	def UIConvertTool(self, sType, *args):
		self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
		#self.dDict['ConvertToolTo'][0] = 0
		iNukeConversion = 0

		sPickedFile = ''

		if sType == 'Pick': # Pick Button
			for i in range(5):
				self.dDict['ConvertToolFrom'][i] = 0
			self.dDict['PickedFile'] = ''

			sPickedFile = cmds.fileDialog2(ds = 1, cap = 'Title', fm = 1)
			if sPickedFile:
				self.dDict['ConvertToolFrom'][0] = 1
				self.dDict['PickedFile'] = sPickedFile
				self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict) # Store dDict

				# cmds.button()


		elif sType.isdigit(): # From : 1-4, To : 5-8
			iIndex = int(sType)

			if iIndex <5: # From: 1-4
				sVar = 'ConvertToolFrom'
				self.aShotInfo[7]
				iVal = 1

				self.dDict['ConvertToolTo'][iIndex] = 0

			else: # To : 5 - 8
				sVar = 'ConvertToolTo'
				iIndex = iIndex - 4
				iVal = 1
				if self.dDict['ConvertToolFrom'][iIndex] == 1:
					iVal = 0


			for i in range(5):
				self.dDict[sVar][i] = 0

			self.dDict[sVar][iIndex] = iVal


		else: # Convert
			if self.dDict['ConvertToolTo'][0]:

				# Empty destination Folder
				iTarget =  self.dDict['ConvertToolTo'][1:].index(1)+1
				sTargetPath = self.aShotInfo[7] + '/%s/' % iTarget


				if os.path.exists(sTargetPath):
					shutil.rmtree(sTargetPath) # delete .../PB/3/
					#print 'delete ', sTargetPath

				if not os.path.exists(sTargetPath):
					os.makedirs(sTargetPath) # create .../PB/3/
					#print 'create ', sTargetPath



				# Get SourcePath
				if self.dDict['ConvertToolFrom'][0]: #if user selecting files:

					self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
					if self.dDict['PickedFile']:
						if not self.dDict['PickedFile'][0].endswith('jpg'):
							iNukeConversion = 1
						else:
							aPickedPath = self.dDict['PickedFile'][0].split('/')
							sPickedFile = aPickedPath[-1]
							sSourcePath = '/'.join(aPickedPath[:-1])


				else: # if not picked ( if sSourcePath is none)
					iSource = self.dDict['ConvertToolFrom'].index(1)
					sSourcePath = self.aShotInfo[7] + '/%s/' % iSource



				# Get files to be copied over.
				aTransferFiles = []
				aFileName = [str(_) for _ in sPickedFile.split('.')]

				if not aFileName[-1].lower() == 'jpg':
					iNukeConversion = 1

				for  f in os.listdir(sSourcePath):
					if f.startswith(aFileName[0]):
						aTransferFiles.append(f)
				aTransferFiles.sort()
				# print aTransferFiles


				sFileName = 'PlayBlast_%s'%iTarget
				for tf in aTransferFiles:
					aName = tf.split('.')
					aName[0] = sFileName
					# print sSourcePath + tf
					# print sTargetPath+'.'.join(aName)
					shutil.copy(sSourcePath+'/' + tf, sTargetPath+'/'+'.'.join(aName))


				if iNukeConversion:
					print 'start nuke'










		iCheck = sum(self.dDict['ConvertToolFrom']) + sum(self.dDict['ConvertToolTo'][1:])
		# print self.dDict['ConvertToolTo'][1:]
		if iCheck == 2:
			self.dDict['ConvertToolTo'][0] = 1
		else:
			self.dDict['ConvertToolTo'][0] = 0



		self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)
		self.UIConvertTool_DisplayChecker()

	def UIConvertTool_DisplayChecker(self):
		self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
		aList = ['oUIConvertPick','oUIConvert1','oUIConvert2','oUIConvert3','oUIConvert4']
		aList2 = ['oUIConvertIT','oUIConvert5','oUIConvert6','oUIConvert7','oUIConvert8']
		aColour = ['darkgray', 'tone5']
		aColour2 = ['darkgray', 'tone1']


		# run only if the tool is (UI is) extended. having the conv tools (on extra UI page) displaying
		if self.dDict['ConvertTool']:
			for i in range(5):

				iVal = self.dDict['ConvertToolTo'][i]
				cmds.button(aList2[i], e = True, bgc = self.UIBGColour(aColour[iVal]), en = True)
				if i == 0: # special colour for convert button
					cmds.button(aList2[i], e = True, bgc = self.UIBGColour(aColour2[iVal]), en = True)

				iVal = self.dDict['ConvertToolFrom'][i]
				cmds.button(aList[i], e = True, bgc = self.UIBGColour(aColour[iVal]))

				if iVal:
					if i:
						cmds.button(aList2[i], e = True, bgc = self.UIBGColour(aColour[0]), en = False)



				if i:
					iVal = self.dDict[str(i)]
					if iVal == '-':
						cmds.button(aList2[i], e = True, bgc = self.UIBGColour(aColour[0]), en = False)



			self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)



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


	def UIBGColour(self, sColour = 'red'):
		# Get Maya BG Colour from pallette.
		sScriptName = 'MayaBGColour' # state the filename without '.py'
		MayaBGColour = imp.load_source(sScriptName, '%s/MayaBGColour.py'%self.sScriptPath)

		oRGB = MayaBGColour.getBGColour()


		dColour = { 'MayaBG':oRGB,
					'tone1':(0.822, 0.967, 1.000),
					'tone2':(0.349, 0.447, 0.537),
					'tone3':(0.231, 0.384, 0.525),
					'tone4':(0.188, 0.231, 0.271),
					'tone5':(0.224, 0.420, 0.502),
					'tone6':(0.224, 0.369, 0.502),
					'tone7':(0.224, 0.298, 0.502),

					'CaptureTone1':(0.8196, 0.9020, 1.000), # Ugly Purple

					#'CaptureTone2':(0.6471, 0.7608, 0.8941),

					'CaptureTone3':(0.2275, 0.2471, 0.2706),


					'RangeButton' : (0.356, 0.341, 0.478),
					'CurrentButton' : (0.3411, 0.3411, 0.478),
					'MarkedButton' : (0.407, 0.3411, 0.478),


					'ProdButton' : (0.2196, 0.2667, 0.3255),
					'_rvButton' : (0.2196, 0.2667, 0.3255),

					'ConvertToolButtonOn' : (0.2392, 0.3294, 0.4000),
					'ConvertToolButtonOff' : (0.2275, 0.2510, 0.2706),
					'CalcToolButtonOn' : (0.2392, 0.4000, 0.2627),
					'CalcToolButtonOff' : (0.2275, 0.2706, 0.2314),
					'AnnotateToolButtonOn' : (0.2392, 0.4000, 0.4000),
					'AnnotateToolButtonOff' : (0.2275, 0.2706, 0.2706),

					'seqButton' : (0.1882, 0.2627, 0.2706),
					'rvButton' : (0.1216, 0.2471, 0.2706),

					# Need Revise on colour
					'darkgray':(0.3,0.3,0.3),
					'gray':(0.4, 0.4, 0.4),
					'blue':(0.8, 0.8, 0.8),
					'yellow':(1.0, 1.0, 0.8),
					'red':(0.7, 0.4, 0.4),
					'lightgray':(0.7, 0.7, 0.7),
					'white' : (1,1,1),}
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
						aAP.append( (self.Row[r][0][i], 'top' , self.iBoarderH, 0) )
						aAP.append( (self.Row[r][0][i], 'left', self.iBoarderW, 0) )

					else:
						aAP.append( (self.Row[r][0][i], 'top' , self.iBoarderH, 0) )
						aAC.append( (self.Row[r][0][i], 'left', self.Row[r][1], self.Row[r][0][i-1]) )
				else:
					if i == 0:
						aAC.append( (self.Row[r][0][i], 'top' , self.Row[r][2], self.Row[r-1][0][0]) )
						aAP.append( (self.Row[r][0][i], 'left', self.iBoarderW, 0) )

					else:
						aAC.append( (self.Row[r][0][i], 'top' , self.Row[r][2], self.Row[r-1][0][0]) )
						aAC.append( (self.Row[r][0][i], 'left', self.Row[r][1], self.Row[r][0][i-1]) )

		# Create Layout
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

		self.iRowHeight = 20

		sStart = str(self.dDict['currentStartFrame'])
		sEnd = str(self.dDict['currentEndFrame'])
		sColour = 'red'
		if self.dDict['prodEndFrame']:
			sColour = 'ProdButton'

		##Row
		self.UIDivision([1, 1.7, 1.7, .6, .3, 1.3, 1.3, .6, .4, .3, 1.2], None, 0)
		aRow = [

		cmds.text(l = 'Range :', h = self.iRowHeight, w = self.Div[0][0]),
		cmds.button('oUIStartButton', label = sStart, h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_InOut, 'Start')),
		cmds.button('oUIEndButton', label = sEnd, h = self.iRowHeight, w = self.Div[0][2], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_InOut, 'End')),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][3]),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][4]),
		cmds.button('oUICapture1Button', label = '1', h = self.iRowHeight, w = self.Div[0][5], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_Capture, '1')),
		cmds.button('oUICapture2Button', label = '2', h = self.iRowHeight, w = self.Div[0][6], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_Capture, '2')),
		cmds.button(label = 'seq', h = self.iRowHeight, w = self.Div[0][7], bgc = self.UIBGColour('seqButton'), enableBackground = False, command = partial(self.UIButton_OpenFolder, 'seq')),
		cmds.button(label = 'rv', h = self.iRowHeight, w = self.Div[0][8], bgc = self.UIBGColour('rvButton'), enableBackground = False, command = partial(self.UIButton_OpenFolder, 'rv')),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][9]),
		cmds.button(label = 'Range', h = self.iRowHeight, w = self.Div[0][10], bgc = self.UIBGColour('RangeButton'), command = partial(self.UIButton_RVInfoToMaya, 'Range')),

		]
		self.UIAddRow(aRow)


		## Row
		self.UIDivision([1, 1.5, 1, .9, .9, 1.3, 1.3, 1, .3, 1.2], None, 0)
		aRow = [

		cmds.text(l = 'Set to : ', h = self.iRowHeight, w = self.Div[0][0]),
		cmds.button('oUIProdButton', label = 'Prod', h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour(sColour), command = self.UIButton_ProdRange),
		cmds.button(label = '.rv', h = self.iRowHeight, w = self.Div[0][2], bgc = self.UIBGColour('_rvButton'), command = self.UIButton_SetRangeFromRV),
		cmds.text('oUIFrameCout', l = '0000f', h = self.iRowHeight, w = self.Div[0][3]),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][4]),
		cmds.button('oUICapture3Button', label = '3', h = self.iRowHeight, w = self.Div[0][5], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_Capture, '3')),
		cmds.button('oUICapture4Button', label = '4', h = self.iRowHeight, w = self.Div[0][6], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_Capture, '4')),
		cmds.button(label = 'Open', h = self.iRowHeight, w = self.Div[0][7], bgc = self.UIBGColour('tone1'), command = partial(self.UIButton_Open, 'PB')),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][8]),
		cmds.button(label = 'Current', h = self.iRowHeight, w = self.Div[0][9], bgc = self.UIBGColour('CurrentButton'), command = partial(self.UIButton_RVInfoToMaya, 'Current')),
		]
		self.UIAddRow(aRow)


		## Row
		self.UIDivision([1.2, 1.2, .6, .3, 4.8, 1, .3, 1.2], None, ); aRow = [
		cmds.button('oUIConvert', label = 'Convert', h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('ConvertToolButtonOff'), enableBackground = False, command = partial(self.UIButton_ExtraToolExpand, 'ConvertTool')),
		cmds.button('oUICalc', label = 'Calc', h = self.iRowHeight, w = self.Div[0][2], bgc = self.UIBGColour('CalcToolButtonOff'), enableBackground = False, command = partial(self.UIButton_ExtraToolExpand, 'CalcTool')),
		cmds.button('oUIAnnotate', label = 'Annotate', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('AnnotateToolButtonOff'), enableBackground = False, command = partial(self.UIButton_ExtraToolExpand, 'AnnotateTool')),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][3]),
		cmds.textField(tx = '3', h = self.iRowHeight, w = self.Div[0][4]),
		cmds.button(label = 'Open', h = self.iRowHeight, w = self.Div[0][5], bgc = (0, .1, .1), enableBackground = False),
		cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][6]),
		cmds.button(label = 'Marked', h = self.iRowHeight, w = self.Div[0][7], bgc = self.UIBGColour('MarkedButton'), command = partial(self.UIButton_RVInfoToMaya, 'Marked')),
		]; self.UIAddRow(aRow)




		if self.dDict['ConvertTool']:
			## Row
			self.UIDivision([1], None, 0); aRow = [
			cmds.separator(height = self.iRowHeight, style = 'in', w = self.Div[0][0]),
			]; self.UIAddRow(aRow)



			## Row
			self.UIDivision([4, 1, 1, .5, 1, 1, 1.5], None, 0) ; aRow = [
			cmds.text(l = 'Convert Tool :                    [ From ]', h = self.iRowHeight, w = self.Div[0][0]),
			cmds.button('oUIConvert1', label = '1', h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '1')),
			cmds.button('oUIConvert2', label = '2', h = self.iRowHeight, w = self.Div[0][2], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '2')),
			cmds.separator( height = self.iRowHeight, style = 'none', w = self.Div[0][3]),
			cmds.button('oUIConvert5', label = '1', h = self.iRowHeight, w = self.Div[0][4], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '5')),
			cmds.button('oUIConvert6', label = '2', h = self.iRowHeight, w = self.Div[0][5], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '6')),
			cmds.text(l = '[ To ]         ', h = self.iRowHeight, w = self.Div[0][6]),
			] ; self.UIAddRow(aRow)


			## Row
			self.UIDivision([4, 1, 1, .5, 1, 1, 1.5], None, 0); aRow = [
			cmds.button('oUIConvertPick', label = 'pick', h = self.iRowHeight, w = self.Div[0][0], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, 'Pick')),
			cmds.button('oUIConvert3', label = '3', h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '3')),
			cmds.button('oUIConvert4', label = '4', h = self.iRowHeight, w = self.Div[0][2], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '4')),
			cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][3]),
			cmds.button('oUIConvert7', label = '3', h = self.iRowHeight, w = self.Div[0][4], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '7')),
			cmds.button('oUIConvert8', label = '4', h = self.iRowHeight, w = self.Div[0][5], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, '8')),
			cmds.button('oUIConvertIT', label = 'Convert!!', h = self.iRowHeight, w = self.Div[0][6], bgc = self.UIBGColour('darkgray'), command = partial(self.UIConvertTool, 'Convert')),
			] ; self.UIAddRow(aRow)


		if self.dDict['CalcTool']:
			## Row
			self.UIDivision([1], None, 0); aRow = [
			cmds.separator(height = self.iRowHeight, style = 'in', w = self.Div[0][0]),
			] ; self.UIAddRow(aRow)

			sDefault = '1001'

			## Row
			self.UIDivision([3, 1.4, 1, 1, 1.4, 5.2, 1.4, .1], None, 0); aRow = [
			cmds.text(l = 'Target Frame :', h = self.iRowHeight, w = self.Div[0][0]),
			cmds.textField('oCalcTarget', tx = sDefault, h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('tone1'), fn = 'fixedWidthFont', tcc = self.UICalcTool),
			cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][2]),
			cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][3]),
			cmds.textField('oCalcFirstFrame', tx = sDefault, h = self.iRowHeight, w = self.Div[0][4], bgc = self.UIBGColour('tone2'), fn = 'fixedWidthFont', tcc = self.UICalcTool),
			cmds.textField(tx = '       - Range Checker - ', h = self.iRowHeight, w = self.Div[0][5], ed = False), #bgc = self.UIBGColour('tone2')),
			cmds.textField('oCalcLastFrame', tx = sDefault, h = self.iRowHeight, w = self.Div[0][6], bgc = self.UIBGColour('tone2'), tcc = self.UICalcTool),
			cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][7]),
			] ; self.UIAddRow(aRow)

			## Row
			self.UIDivision([3, 1.4, 1.5, .5, 1.4, 5.2, 1.4, .1], None, 0); aRow = [
			cmds.text(l = 'Moving To :', h = self.iRowHeight, w = self.Div[0][0]),
			cmds.textField('oCalcMoveTo', tx = sDefault, h = self.iRowHeight, w = self.Div[0][1], bgc = self.UIBGColour('tone2'), fn = 'fixedWidthFont', tcc = self.UICalcTool ),
			cmds.textField('oCalcDifference', tx = '0f', h = self.iRowHeight, w = self.Div[0][2], bgc = self.UIBGColour('tone4'), ed = False ),
			cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][3]),
			cmds.textField('oCalcAdjFirstFrame', tx = sDefault, h = self.iRowHeight, w = self.Div[0][4], bgc = self.UIBGColour('tone4'), fn = 'fixedWidthFont'),
			cmds.textField('oCalcRange', tx = '          ----- 0f -----', h = self.iRowHeight, w = self.Div[0][5], bgc = self.UIBGColour('tone4')),
			cmds.textField('oCalcAdjLastFrame', tx = sDefault, h = self.iRowHeight, w = self.Div[0][6], bgc = self.UIBGColour('tone4'), fn = 'fixedWidthFont'),
			cmds.separator(height = self.iRowHeight, style = 'none', w = self.Div[0][7]),
			] ; self.UIAddRow(aRow)

	def UIButton_OpenFolder(self, sFolder, *args):
		K = cmds.getModifiers()
		if sFolder == 'rv':
			sPath = self.aShotInfo[6]
		elif sFolder == 'seq':
			sPath = self.aShotInfo[7]

		if K:
			self.StudioSettings.OSFileBrowserCommand(sPath)
			aPrint = ['a7a8f', 'Opening a FileBrowser.', 0x6b6c75]

		else:
			self.StudioSettings.CopyToClipBoard(sPath)
			aPrint = ['a7a8af', 'Copied Path to Clipboard.', 0x6b6c75]

		self.PrintOnScreen(aPrint)

	def UICalcTool(self, *args):
		aVars = ['oCalcTarget', 'oCalcMoveTo', 'oCalcFirstFrame', 'oCalcLastFrame']
		aAdjVars = []


		for v in aVars:
			sVal = cmds.textField(v, q = True, tx = True)
			if sVal:
				sVal = ''.join(s for s in sVal if s.isdigit())
			else:
				sVal = '0'
			sVal = int(sVal)
			aAdjVars.append(sVal)
			cmds.textField(v, e = True, tx = sVal)
		iDifference = aAdjVars[1]-aAdjVars[0] #+1
		cmds.textField('oCalcDifference', e = True, tx = '%s f'%iDifference)
		cmds.textField('oCalcAdjFirstFrame', e = True, tx = str(aAdjVars[2]+iDifference))
		cmds.textField('oCalcAdjLastFrame', e = True, tx = str(aAdjVars[3]+iDifference))
		cmds.textField('oCalcRange', e = True, tx = '          ----- %s f -----'%str(aAdjVars[3]-aAdjVars[2]+1))


	def SoundCheck(self):
		sSound = ''
		sOffset = ''

		#Get Current SoundTrack from timeslider
		aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
		sSoundTest = cmds.timeControl(aPlayBackSliderPython, q = True, sound = True)

		if sSoundTest:
			sSound = '"%s"'%cmds.sound( sSoundTest, q = True, f = True)
			sOffsetPath = '/'.join(aAllPath[1]+['000.sound.rv'])
			sOffset = ''

			if os.path.exists(sOffsetPath):
				iOffset = None
				oRvFile = open(sOffsetPath, 'r')
				aLines = oRvFile.readlines()
				oRvFile.close()

				for line in aLines:
					sLine = line.strip()
					if 'float audioOffset = ' in sLine:
						iOffset = float(sLine.split(' ')[-1])

				if iOffset:
					sOffset = '''
					group
					{
						float audioOffset = %s
					}
					''' % iOffset

			else:
				cmds.warning('000.sound.rv not found! Better create NOW. (The offset value will be based on this file.)')

		return [sSound, sOffset]


	def UIButton_ExtraToolExpand(self, sTool, *args):
		self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)

		# Set height of each custom tools.
		dTools = {  'CalcTool' : 62,
					'ConvertTool' : 62,
					'AnnotateTool' : 200,}

		# Change height accordingly
		for tool in dTools.keys():
			if tool == sTool:
				# Toggle and change height
				if self.dDict[tool]:
					dTools[tool] *= -1
				self.Height += dTools[tool]
				self.dDict[tool] = 1 - self.dDict[tool]

		self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)
		self.UIReBuild()
		self.UIDisplayChecker()
		self.UIConvertTool_DisplayChecker()


	def UIButton_SetRangeFromRV(self, *args):
		aContent = self.GetActiveRVinfo()
		iIn = aContent[1][0]
		iOut = aContent[1][1]

		self.dDict['currentStartFrame'] = iIn
		self.dDict['currentEndFrame'] = iOut
		cmds.button('oUIStartButton', e = True, label = iIn)
		cmds.button('oUIEndButton', e = True, label = iOut)

		self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)
		self.UIDisplayChecker()

	def UIButton_RVInfoToMaya(self, sType, *args):
		K = cmds.getModifiers()



		aContent = self.GetActiveRVinfo()
		# aContent[0] : Capture Frame Range
		# aContent[1] : RV Region
		# aContent[2] : RV Marked Frames
		# aContent[3] : Current Frame
		#self.PrintOnScreen(['a7a8af', 'Testing Here', 0x6b6c75 ])

		if aContent:
			if sType == 'Range':
				cmds.playbackOptions(min = aContent[1][0])

			elif sType == 'Current':
				cmds.currentTime(aContent[3][0])

			elif sType == 'Marked':

				oAnimTools = 'ANIM_TOOLS'
				self.sTool = 'PBTool'
				if K:
					oTick = 'KeyPoseFrames'
				else:
					oTick = 'MarkedFrames'


				if aContent[2]:
					if cmds.objExists(oTick):
						cmds.delete(oTick)

					#self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
					self.dDict['markedFrames'] = aContent[2]



					cmds.group(name = oTick, em = True, p = self.sTool)

					cmds.setKeyframe( oTick, attribute = 'translateX', t = self.dDict['markedFrames'])
					self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)

	def GetActiveRVinfo(self):

		oRvFile = open(self.sRvPath, 'r')
		aLines = oRvFile.readlines()
		oRvFile.close()


		# aContent = GetActiveRVinfo()
		# aContent[0] : Capture Frame Range
		# aContent[1] : RV Region
		# aContent[2] : RV Marked Frames
		# aContent[3] : Current Frame


		# parse necessary info from .rv file
		aSearch = [ 'string movie = "',
					'int[2] region = [',
					'int marks',
					'int currentFrame =']
		aExtract = [None, None, None, None]
		for line in aLines:
			sLine = line.strip()
			for i in range(len(aSearch)):
				if aSearch[i] in sLine:
					if not aExtract[i]:
						aExtract[i] = sLine

		# Extracting only in numbers
		aContent = []
		if aExtract[0]:
			for i in range(len(aExtract)):
				if i == 0: # only for extracting frame range from 'string movie =' path

					# converting exactly this : string movie = "/proj/mll/shots/ate/4120/motion/work/maya/dyabu/Images/PB/1/PlayBlast_1.1001-1050@@@@.jpg"
					sExtract = aExtract[i].split('.')[-2].replace('@', '')
					aContent.append([int(x) for x in sExtract.split('-')])

				else:
					aContent.append([])
					if aExtract[i]:
						for s in aExtract[i].split(' '):
							if s.isdigit():
								aContent[i].append(int(s))

		else:
			cmds.warning('SAVE Active.rv once first.')


		# Convert to Maya Frames
		if aContent:
			aContent[1][0] += aContent[0][0] -1
			aContent[1][1] += aContent[0][0] -2
			if aContent[2]:
				for i in range(len(aContent[2])):
					aContent[2][i] += aContent[0][0] -1
			aContent[3][0] += aContent[0][0] -1

		return aContent

	def UIDisplayChecker(self):
		self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
		# Frame Count

		iCurrentStart = self.dDict['currentStartFrame']
		iCurrentEnd = self.dDict['currentEndFrame']
		iProdStart = self.dDict['prodStartFrame']
		iProdEnd = self.dDict['prodEndFrame']

		cmds.text('oUIFrameCout', e = True, l = str(iCurrentEnd - iCurrentStart + 1)+ ' f')


		# Frames Section
		aTones = ['tone5', 'tone5']

		if iCurrentStart == iProdStart:
			aTones[0] = 'tone1'
		if iCurrentEnd == iProdEnd:
			aTones[1] = 'tone1'


		# if aTones[0]:
		cmds.button('oUIStartButton', e = True, bgc = self.UIBGColour(aTones[0]))
		# if aTones[1]:
		cmds.button('oUIEndButton', e = True, bgc = self.UIBGColour(aTones[1]))



		# Views Section
		aView = ['1', '2', '3', '4']

		for v in aView:
			if self.dDict[v] == '-':
				sBGC = 'CaptureTone3'
				sLabel = '-'
			else:
				sBGC = 'tone4'
				sLabel = v
				if self.dDict['LastCapture'] == v:
					sBGC = 'tone1'
			cmds.button('oUICapture%sButton'%v, e = True, bgc = self.UIBGColour(sBGC), label = sLabel)





		# Extra tools

		aTones = ['ConvertToolButtonOff', 'ConvertToolButtonOn']
		aTones2 = ['CalcToolButtonOff', 'CalcToolButtonOn']
		aTones3 = ['AnnotateToolButtonOff', 'AnnotateToolButtonOn']
		cmds.button('oUIConvert', e = True, bgc = self.UIBGColour(aTones[self.dDict['ConvertTool']]))
		cmds.button('oUICalc',    e = True, bgc = self.UIBGColour(aTones[self.dDict['CalcTool']]))
		cmds.button('oUIAnnotate',    e = True, bgc = self.UIBGColour(aTones[self.dDict['AnnotateTool']]))

	def UIButton_ProdRange(self, *args):


		iRange = self.StudioSettings.StudioProductionFrameRange()
		iIn = int(cmds.playbackOptions(q = True, minTime = True))
		iOut = int(cmds.playbackOptions(q = True, maxTime = True))
		if iRange:
			cmds.button('oUIProdButton', e = True, bgc = self.UIBGColour('tone2'))
		else:
			self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)
			cmds.button('oUIProdButton', e = True, bgc = self.UIBGColour('tone3'))

		self.dDict['currentStartFrame'] = iIn
		self.dDict['currentEndFrame'] = iOut
		cmds.button('oUIStartButton', e = True, label = str(iIn))
		cmds.button('oUIEndButton', e = True, label = str(iOut))

		self.dDict['prodStartFrame'] = iIn
		self.dDict['prodEndFrame'] = iOut



		self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict) # To update the info
		self.UIDisplayChecker()

	def UIButton_InOut(self, sInOut, *args):
		self.dDict = self.StudioSettings.AnimToolAttributes(self.sTool)

		iCurrent = int(cmds.currentTime(q = True))
		if sInOut == 'Start':
			self.dDict['currentStartFrame'] = iCurrent
			cmds.button('oUIStartButton', e = True, label = iCurrent)

			#print iCurrent, self.dDict['currentEndFrame']
			# if End frame is before current frame.
			if self.dDict['currentEndFrame'] <= iCurrent:
				self.dDict['currentEndFrame'] = iCurrent + 1
				cmds.button('oUIEndButton', e = True, label = iCurrent + 1)


		elif sInOut == 'End':
			self.dDict['currentEndFrame'] = iCurrent
			cmds.button('oUIEndButton', e = True, label = iCurrent)

			#print iCurrent, self.dDict['currentStartFrame']
			# if End frame is before current frame.
			if self.dDict['currentStartFrame'] >= iCurrent:
				self.dDict['currentStartFrame'] = iCurrent - 1
				cmds.button('oUIStartButton', e = True, label = iCurrent - 1)


		elif sInOut == 'Current':
			iIn = int(cmds.playbackOptions(q = True, minTime = True))
			iOut = int(cmds.playbackOptions(q = True, maxTime = True))
			self.dDict['currentStartFrame'] = iIn
			self.dDict['currentEndFrame'] = iOut
			cmds.button('oUIStartButton', e = True, label = iIn)
			cmds.button('oUIEndButton', e = True, label = iOut)

		else:
			pass

		self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)

		self.UIDisplayChecker()

	def UIButton_Open(self, sOpen, *args):
		# 'PB' for quad view, 'Anno' for opening Annotation.rv
		K = cmds.getModifiers()
		if sOpen =='PB':
			if not os.path.exists(self.sRvPath):
				K = 100
			if K: # If with any Modifiers, Create a fresh Active.rv. (deletes all markings etc.)
				dInfo = self.StudioSettings.AnimToolAttributes(self.sTool) # Check function for more info.

				sIn = dInfo['prodStartFrame']
				if sIn == None:
					sIn = dInfo['currentStartFrame']

				sOut = dInfo['prodEndFrame']
				if sOut == None:
					sOut = dInfo['currentEndFrame']


				aPath = [None, None, None, None, ]
				for i in range(0, len(aPath)):
					aPath[i] = self.aShotInfo[7] + '/%s/PlayBlast_%s.%s-%s@@@@.jpg'%(str(i+1), str(i+1), sIn, sOut)

				sContent = self.CreateLatestQuadRvFile(aPath)

				if sContent:
					oRvFile = open(self.sRvPath, 'w')
					oRvFile.write(sContent)
					oRvFile.close()

				aPrint = ['a7a8af', 'Creating a New .rv', 0x6b6c75 ]

			else:
				aPrint = ['a7a8af', 'Opening Existing .rv', 0x6b6c75 ]

			try:
				cmd = 'rv %s &' % (self.sRvPath)
				#print cmd
				os.system(cmd)
			except Exception as e:
				print e
			#print aPrint
			self.PrintOnScreen(aPrint)

		self.UIDisplayChecker()

	def UIButton_Capture(self, sView, *args):
		# Display Logic
		K = cmds.getModifiers()
		sGrayOut = 'darkgray'

		dToolInfo = self.StudioSettings.AnimToolAttributes(self.sTool)
		sLabel = dToolInfo[sView]


		iStartCapture = 0
		if K:

			if sLabel == '-':
				sLabel = sView
			else:
				sLabel = '-'

			dToolInfo[sView] = sLabel



			self.StudioSettings.AnimToolAttributes(self.sTool, dToolInfo)

		else:
			if not sLabel == '-':
				iStartCapture = 1

		#self.UIDisplayChecker()

		# PlayBlast time!
		if iStartCapture:

			sCapturePath = self.aShotInfo[7]+'/'+sView+'/PlayBlast_%s'%sView
			sIn = dToolInfo['currentStartFrame']
			sOut = dToolInfo['currentEndFrame']

			cmds.playblast(format = 'image', filename = sCapturePath, st = int(sIn), et = int(sOut), sequenceTime = 0, clearCache = 1, viewer = 0, showOrnaments = 1, offScreen = True, fp = 4, percent = 100, compression = "jpg", quality = 70, fo = True)

			cmds.warning('Capture Process All Finished')
			#self.UIDisplayChecker()

			cmds.button('oUICapture%sButton'%sView, e = True, bgc = self.UIBGColour('tone1'))
			#self.dDict['LastCapture'] = sView
			dToolInfo['LastCapture'] = sView

			self.PrintOnScreen = ['a7a8af', 'Playblast done [%s]'%sView, 0x6b6c75]



		#self.StudioSettings.AnimToolAttributes(self.sTool, self.dDict)
		#print 'sView', dToolInfo
		self.StudioSettings.AnimToolAttributes(self.sTool, dToolInfo)

		self.UIConvertTool_DisplayChecker()
		self.UIDisplayChecker()



	def PrintOnScreen(self, aPrint):
		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = aPrint[2])

	def UIButton_Size(self, iHeight, *args):
		self.Height += iHeight
		self.UIRebuild()

	def FloatSlider_Changed(self, sGrp, *args):
		print 'Float Slider Changed %s' % sGrp
		cmds.floatSliderGrp(sGrp, e = True, v = 1)

	def Dropdown_Changed(self, i, *args):
		print 'Dropped down! as : %s' %i

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

	def CreateLatestQuadRvFile(self, aPath):
		sContent = None
		print 'aPath', aPath
		if aPath:
			sContent = '''GTOa (3)

rv : RVSession (2)
{
	session
	{
		string viewNode = "defaultLayout"
		int[2] range = [ [ 1 35]]
		float fps = 24
	}
}

sourceGroup000000_source : RVFileSource (1)
{
	media
	{
		string movie = "%s"
	}
}

sourceGroup000001_source : RVFileSource (1)
{
	media
	{
		string movie = "%s"
	}
}

sourceGroup000002_source : RVFileSource (1)
{
	media
	{
		string movie = "%s"
	}
}

sourceGroup000003_source : RVFileSource (1)
{
	media
	{
		string movie = "%s"
	}
}'''% (aPath[0], aPath[1],aPath[2], aPath[3])


		return sContent

def main():
	UIBuilder()
