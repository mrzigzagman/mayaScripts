# PlayBlast Tool v10.3.0
# Re Construct with New UIBuilderTemplate
# vvv 3/3

import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import os
import shutil
import getpass
import imp

# Custom
import StudioSettings
import UIColourControl
import UIWindowControl

def main():
	GlobalVar()
	UISetUp()
	UIReBuild()
	UIDisplayChecker() # UI BUILDER TEMPLATE 7.1.0

if __name__ == '__main__':
	 main()

def UILayout():
	'''
	The Most Customization happens here...
	oUI.UIDivision([1,1,1], None, 0) ; aRow = [    cmds.button(label = ' A Button!', h = iRowHeight, w = oUI.Div[0][0], bgc = UIColourControl.keywordColour('Tone2'), enableBackground = False, command = ButtonAdd),]
	cmds.text(.....),
	cmds textField(), ] ; UIAddRow(aRow)
	'''

	dDict = StudioSettings.SceneInfoStorage(sSceneTool)
	aRow = []

	iRowHeight = 20

	sStart = str(dDict['currentStartFrame'])
	sEnd = str(dDict['currentEndFrame'])
	sColour = 'Red'
	if dDict['prodEndFrame']:
		sColour = 'ProdButton'

	##Row
	oUI.UIDivision([1, 1.7, 1.7, .6, .3, 1.3, 1.3, .6, .4, .3, 1.2], None, 0); aRow = [

	cmds.text(l = 'Range :', h = iRowHeight, w = oUI.Div[0][0]),
	cmds.button('oUIStartButton', label = sStart, h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_InOut, 'Start')),
	cmds.button('oUIEndButton', label = sEnd, h = iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_InOut, 'End')),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][3]),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][4]),
	cmds.button('oUICapture1Button', label = '1', h = iRowHeight, w = oUI.Div[0][5], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_Capture, '1')),
	cmds.button('oUICapture2Button', label = '2', h = iRowHeight, w = oUI.Div[0][6], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_Capture, '2')),
	cmds.button(label = 'seq', h = iRowHeight, w = oUI.Div[0][7], bgc = UIColourControl.keywordColour('SeqButton'), enableBackground = False, command = partial(UIButton_OpenFolder, 'seq')),
	cmds.button(label = 'rv', h = iRowHeight, w = oUI.Div[0][8], bgc = UIColourControl.keywordColour('RvButton'), enableBackground = False, command = partial(UIButton_OpenFolder, 'rv')),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][9]),
	cmds.button(label = 'Range', h = iRowHeight, w = oUI.Div[0][10], bgc = UIColourControl.keywordColour('RangeButton'), command = partial(UIButton_RVInfoToMaya, 'Range')),
	]; oUI.UIAddRow(aRow)


	## Row
	oUI.UIDivision([1, 1.5, 1, .9, .9, 1.3, 1.3, 1, .3, 1.2]); aRow = [
	cmds.text(l = 'Set to : ', h = iRowHeight, w = oUI.Div[0][0]),
	cmds.button('oUIProdButton', label = 'Prod', h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour(sColour), command = UIButton_ProdRange),
	cmds.button(label = '.rv', h = iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('_rvButton'), command = UIButton_SetRangeFromRV),
	cmds.text('oUIFrameCout', l = '0000f', h = iRowHeight, w = oUI.Div[0][3]),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][4]),
	cmds.button('oUICapture3Button', label = '3', h = iRowHeight, w = oUI.Div[0][5], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_Capture, '3')),
	cmds.button('oUICapture4Button', label = '4', h = iRowHeight, w = oUI.Div[0][6], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_Capture, '4')),
	cmds.button(label = 'Open', h = iRowHeight, w = oUI.Div[0][7], bgc = UIColourControl.keywordColour('Tone1'), command = partial(UIButton_Open, 'PB')),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][8]),
	cmds.button(label = 'Current', h = iRowHeight, w = oUI.Div[0][9], bgc = UIColourControl.keywordColour('CurrentButton'), command = partial(UIButton_RVInfoToMaya, 'Current')),
	]; oUI.UIAddRow(aRow)


	## Row
	oUI.UIDivision([1.2, 1.2, .6, .3, 4.8, 1, .3, 1.2], None, ); aRow = [
	cmds.button('oUIConvert', label = 'Convert', h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('ConvertToolButtonOff'), enableBackground = False, command = partial(UIButton_ExtraToolExpand, 'ConvertTool')),
	cmds.button('oUICalc', label = 'Calc', h = iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('CalcToolButtonOff'), enableBackground = False, command = partial(UIButton_ExtraToolExpand, 'CalcTool')),
	cmds.button('oUIAnnotate', label = 'Annotate', h = iRowHeight, w = oUI.Div[0][0], bgc = UIColourControl.keywordColour('AnnotateToolButtonOff'), enableBackground = False, command = partial(UIButton_ExtraToolExpand, 'AnnotateTool')),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][3]),
	cmds.textField(tx = '3', h = iRowHeight, w = oUI.Div[0][4]),
	cmds.button(label = 'Open', h = iRowHeight, w = oUI.Div[0][5], bgc = (0, .1, .1), enableBackground = False),
	cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][6]),
	cmds.button(label = 'Marked', h = iRowHeight, w = oUI.Div[0][7], bgc = UIColourControl.keywordColour('MarkedButton'), command = partial(UIButton_RVInfoToMaya, 'Marked')),
	]; oUI.UIAddRow(aRow)




	if dDict['ConvertTool']:
		## Row
		oUI.UIDivision([1], None, 0); aRow = [
		cmds.separator(height = iRowHeight, style = 'in', w = oUI.Div[0][0]),
		]; oUI.UIAddRow(aRow)



		## Row
		oUI.UIDivision([4, 1, 1, .5, 1, 1, 1.5], None, 0) ; aRow = [
		cmds.text(l = 'Convert Tool :                    [ From ]', h = iRowHeight, w = oUI.Div[0][0]),
		cmds.button('oUIConvert1', label = '1', h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '1')),
		cmds.button('oUIConvert2', label = '2', h = iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '2')),
		cmds.separator( height = iRowHeight, style = 'none', w = oUI.Div[0][3]),
		cmds.button('oUIConvert5', label = '1', h = iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '5')),
		cmds.button('oUIConvert6', label = '2', h = iRowHeight, w = oUI.Div[0][5], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '6')),
		cmds.text(l = '[ To ]         ', h = iRowHeight, w = oUI.Div[0][6]),
		] ; oUI.UIAddRow(aRow)


		## Row
		oUI.UIDivision([4, 1, 1, .5, 1, 1, 1.5], None, 0); aRow = [
		cmds.button('oUIConvertPick', label = 'pick', h = iRowHeight, w = oUI.Div[0][0], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, 'Pick')),
		cmds.button('oUIConvert3', label = '3', h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '3')),
		cmds.button('oUIConvert4', label = '4', h = iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '4')),
		cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][3]),
		cmds.button('oUIConvert7', label = '3', h = iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '7')),
		cmds.button('oUIConvert8', label = '4', h = iRowHeight, w = oUI.Div[0][5], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, '8')),
		cmds.button('oUIConvertIT', label = 'Convert!!', h = iRowHeight, w = oUI.Div[0][6], bgc = UIColourControl.keywordColour('DarkGray'), command = partial(UIConvertTool, 'Convert')),
		] ; oUI.UIAddRow(aRow)


	if dDict['CalcTool']:
		## Row
		oUI.UIDivision([1], None, 0); aRow = [
		cmds.separator(height = iRowHeight, style = 'in', w = oUI.Div[0][0]),
		] ; oUI.UIAddRow(aRow)

		sDefault = '1001'

		## Row
		oUI.UIDivision([3, 1.4, 1, 1, 1.4, 5.2, 1.4, .1], None, 0); aRow = [
		cmds.text(l = 'Target Frame :', h = iRowHeight, w = oUI.Div[0][0]),
		cmds.textField('oCalcTarget', tx = sDefault, h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('Tone1'), fn = 'fixedWidthFont', tcc = UICalcTool),
		cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][2]),
		cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][3]),
		cmds.textField('oCalcFirstFrame', tx = sDefault, h = iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('Tone2'), fn = 'fixedWidthFont', tcc = UICalcTool),
		cmds.textField(tx = '       - Range Checker - ', h = iRowHeight, w = oUI.Div[0][5], ed = False), #bgc = UIColourControl.keywordColour('Tone2')),
		cmds.textField('oCalcLastFrame', tx = sDefault, h = iRowHeight, w = oUI.Div[0][6], bgc = UIColourControl.keywordColour('Tone2'), tcc = UICalcTool),
		cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][7]),
		] ; oUI.UIAddRow(aRow)

		## Row
		oUI.UIDivision([3, 1.4, 1.5, .5, 1.4, 5.2, 1.4, .1], None, 0); aRow = [
		cmds.text(l = 'Moving To :', h = iRowHeight, w = oUI.Div[0][0]),
		cmds.textField('oCalcMoveTo', tx = sDefault, h = iRowHeight, w = oUI.Div[0][1], bgc = UIColourControl.keywordColour('Tone2'), fn = 'fixedWidthFont', tcc = UICalcTool ),
		cmds.textField('oCalcDifference', tx = '0f', h = iRowHeight, w = oUI.Div[0][2], bgc = UIColourControl.keywordColour('Tone4'), ed = False ),
		cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][3]),
		cmds.textField('oCalcAdjFirstFrame', tx = sDefault, h = iRowHeight, w = oUI.Div[0][4], bgc = UIColourControl.keywordColour('Tone4'), fn = 'fixedWidthFont'),
		cmds.textField('oCalcRange', tx = '          ----- 0f -----', h = iRowHeight, w = oUI.Div[0][5], bgc = UIColourControl.keywordColour('Tone4')),
		cmds.textField('oCalcAdjLastFrame', tx = sDefault, h = iRowHeight, w = oUI.Div[0][6], bgc = UIColourControl.keywordColour('Tone4'), fn = 'fixedWidthFont'),
		cmds.separator(height = iRowHeight, style = 'none', w = oUI.Div[0][7]),
		] ; oUI.UIAddRow(aRow)

def	UIReBuild():
	global oUI
	oUI.UIPrepare()
	UILayout()
	oUI.UICreate()


### TOOL SETUP ###
def GlobalVar():
	global K, oUI, dShotInfo, aPBInfo, sSceneTool, dDict, sRvPath

	## Global Vars ##
	K = cmds.getModifiers()
	oUI = UIWindowControl.UIBuilder()
	dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)
	aPBInfo = StudioSettings.ProjectInfo('ABA')
	sSceneTool = 'PBTool' # Tool name node under 'Anim_Tool'
	dDict = StudioSettings.SceneInfoStorage(sSceneTool)

	# Importing Studio Settings
	iPBwidth = aPBInfo[0][0]
	iPBheight = aPBInfo[0][1]
	sRvPath = os.path.join(dShotInfo['sPlayBlastToolPath'], '%s_%s.rv'%(dShotInfo['sSeqNumber'],dShotInfo['sShotNumber']))

def UISetUp():
	global dDict
	## UI SetUp ##

	oUI.Width = 450 # Total Width of Window in pixel (Default 320)
	oUI.Height = 75 # Total Height of Window in pixel
	oUI.iRowHeight = 25
	oUI.sUI = 'PB_%s_%s' % (dShotInfo['sSeqNumber'], dShotInfo['sShotNumber']) # Watch out when this is only numbers, the tool fails.

	# Setting up SceneTool custom dictionary for storage
	if not dDict:
		 dDict = {  '1': '1',
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
		dDict[tool] = 0

	# Reset Convert tool
	dDict['ConvertToolFrom'] = [0,0,0,0,0]
	dDict['ConvertToolTo'] =[0,0,0,0,0]

	StudioSettings.SceneInfoStorage(sSceneTool, dDict) # Store dDict\


### TOOL FUNCTIONS ###

def UIConvertTool(sType, *args):
	dDict = StudioSettings.SceneInfoStorage(sSceneTool)
	iNukeConversion = 0

	sPickedFile = ''

	if sType == 'Pick': # Pick Button
		for i in range(5):
			dDict['ConvertToolFrom'][i] = 0
		dDict['PickedFile'] = ''

		sPickedFile = cmds.fileDialog2(ds = 1, cap = 'Title', fm = 1)
		if sPickedFile:
			dDict['ConvertToolFrom'][0] = 1
			dDict['PickedFile'] = sPickedFile
			StudioSettings.SceneInfoStorage(sSceneTool, dDict) # Store dDict


	elif sType.isdigit(): # From : 1-4, To : 5-8
		iIndex = int(sType)

		if iIndex <5: # From: 1-4
			sVar = 'ConvertToolFrom'
			#aShotInfo[7]
			iVal = 1

			dDict['ConvertToolTo'][iIndex] = 0

		else: # To : 5 - 8
			sVar = 'ConvertToolTo'
			iIndex = iIndex - 4
			iVal = 1
			if dDict['ConvertToolFrom'][iIndex] == 1:
				iVal = 0


		for i in range(5):
			dDict[sVar][i] = 0

		dDict[sVar][iIndex] = iVal


	else: # Convert
		if dDict['ConvertToolTo'][0]:

			# Empty destination Folder
			iTarget =  dDict['ConvertToolTo'][1:].index(1)+1
			#sTargetPath = aShotInfo[7] + '/%s/' % iTarget
			sTargetPath = dShotInfo['sPlayBlastSeqPath'] + '/%s/' % iTarget


			if os.path.exists(sTargetPath):
				shutil.rmtree(sTargetPath) # delete .../PB/3/

			if not os.path.exists(sTargetPath):
				os.makedirs(sTargetPath) # create .../PB/3/



			# Get SourcePath
			if dDict['ConvertToolFrom'][0]: #if user selecting files:

				dDict = StudioSettings.SceneInfoStorage(sSceneTool)
				if dDict['PickedFile']:
					if not dDict['PickedFile'][0].endswith('jpg'):
						iNukeConversion = 1
					else:
						aPickedPath = dDict['PickedFile'][0].split('/')
						sPickedFile = aPickedPath[-1]
						sSourcePath = '/'.join(aPickedPath[:-1])


			else: # if not picked ( if sSourcePath is none)
				iSource = dDict['ConvertToolFrom'].index(1)
				sSourcePath = dShotInfo['sPlayBlastSeqPath'] + '/%s/' % iSource



			# Get files to be copied over.
			aTransferFiles = []
			aFileName = [str(_) for _ in sPickedFile.split('.')]

			if not aFileName[-1].lower() == 'jpg':
				iNukeConversion = 1

			for  f in os.listdir(sSourcePath):
				if f.startswith(aFileName[0]):
					aTransferFiles.append(f)
			aTransferFiles.sort()


			sFileName = 'PlayBlast_%s'%iTarget
			for tf in aTransferFiles:
				aName = tf.split('.')
				aName[0] = sFileName

				shutil.copy(sSourcePath+'/' + tf, sTargetPath+'/'+'.'.join(aName))

			if iNukeConversion:
				print 'start nuke'


	iCheck = sum(dDict['ConvertToolFrom']) + sum(dDict['ConvertToolTo'][1:])
	if iCheck == 2:
		dDict['ConvertToolTo'][0] = 1
	else:
		dDict['ConvertToolTo'][0] = 0


	StudioSettings.SceneInfoStorage(sSceneTool, dDict)
	UIConvertTool_DisplayChecker()

def UIConvertTool_DisplayChecker():
	dDict = StudioSettings.SceneInfoStorage(sSceneTool)
	aList = ['oUIConvertPick','oUIConvert1','oUIConvert2','oUIConvert3','oUIConvert4']
	aList2 = ['oUIConvertIT','oUIConvert5','oUIConvert6','oUIConvert7','oUIConvert8']
	aColour = ['DarkGray', 'Tone5']
	aColour2 = ['DarkGray', 'Tone1']


	# run only if the tool is (UI is) extended. having the conv tools (on extra UI page) displaying
	if dDict['ConvertTool']:
		for i in range(5):

			iVal = dDict['ConvertToolTo'][i]
			cmds.button(aList2[i], e = True, bgc = UIColourControl.keywordColour(aColour[iVal]), en = True)
			if i == 0: # special colour for convert button
				cmds.button(aList2[i], e = True, bgc = UIColourControl.keywordColour(aColour2[iVal]), en = True)

			iVal = dDict['ConvertToolFrom'][i]
			cmds.button(aList[i], e = True, bgc = UIColourControl.keywordColour(aColour[iVal]))

			if iVal:
				if i:
					cmds.button(aList2[i], e = True, bgc = UIColourControl.keywordColour(aColour[0]), en = False)



			if i:
				iVal = dDict[str(i)]
				if iVal == '-':
					cmds.button(aList2[i], e = True, bgc = UIColourControl.keywordColour(aColour[0]), en = False)



		StudioSettings.SceneInfoStorage(sSceneTool, dDict)

def UIButton_OpenFolder( sFolder, *args):
	K = cmds.getModifiers()
	if sFolder == 'rv':
		sPath = dShotInfo['sPlayBlastToolPath']
	elif sFolder == 'seq':
		sPath = dShotInfo['sPlayBlastSeqPath']




	if K:
		StudioSettings.OSFileBrowserCommand(sPath)
		aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'Opening a FileBrowser.')

	else:
		StudioSettings.CopyToClipBoard(sPath)
		aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'Copied Path to Clipboard.')

	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def UICalcTool( *args):
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

def SoundCheck():
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

def UIButton_ExtraToolExpand(sTool, *args):


	dDict = StudioSettings.SceneInfoStorage(sSceneTool)


	# Set height of each custom tools.
	dTools = {  'CalcTool' : 62,
				'ConvertTool' : 62,
				'AnnotateTool' : 200,}

	# Change height accordingly
	for tool in dTools.keys():
		if tool == sTool:
			# Toggle and change height
			if dDict[tool]:
				dTools[tool] *= -1
			oUI.Height += dTools[tool]
			dDict[tool] = 1 - dDict[tool]

	StudioSettings.SceneInfoStorage(sSceneTool, dDict)
	UIReBuild()
	UIDisplayChecker()
	UIConvertTool_DisplayChecker()

def UIButton_SetRangeFromRV( *args):
	aContent = GetActiveRVinfo()
	iIn = aContent[1][0]
	iOut = aContent[1][1]

	dDict['currentStartFrame'] = iIn
	dDict['currentEndFrame'] = iOut
	cmds.button('oUIStartButton', e = True, label = iIn)
	cmds.button('oUIEndButton', e = True, label = iOut)

	StudioSettings.SceneInfoStorage(sSceneTool, dDict)
	UIDisplayChecker()

def UIButton_RVInfoToMaya( sType, *args):
	K = cmds.getModifiers()



	aContent = GetActiveRVinfo()
	# aContent[0] : Capture Frame Range
	# aContent[1] : RV Region
	# aContent[2] : RV Marked Frames
	# aContent[3] : Current Frame

	if aContent:
		if sType == 'Range':
			cmds.playbackOptions(min = aContent[1][0])

		elif sType == 'Current':
			cmds.currentTime(aContent[3][0])

		elif sType == 'Marked':

			oAnimTools = 'ANIM_TOOLS'
			sSceneTool = 'PBTool'
			if K:
				oTick = 'KeyPoseFrames'
			else:
				oTick = 'MarkedFrames'


			if aContent[2]:
				if cmds.objExists(oTick):
					cmds.delete(oTick)

				#dDict = StudioSettings.SceneInfoStorage(sSceneTool)
				dDict['markedFrames'] = aContent[2]



				cmds.group(name = oTick, em = True, p = sSceneTool)

				cmds.setKeyframe( oTick, attribute = 'translateX', t = dDict['markedFrames'])
				StudioSettings.SceneInfoStorage(sSceneTool, dDict)

def GetActiveRVinfo():

	oRvFile = open(sRvPath, 'r')
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

def UIDisplayChecker():
	dDict = StudioSettings.SceneInfoStorage(sSceneTool)

	# Frame Count
	iCurrentStart = dDict['currentStartFrame']
	iCurrentEnd = dDict['currentEndFrame']
	iProdStart = dDict['prodStartFrame']
	iProdEnd = dDict['prodEndFrame']

	cmds.text('oUIFrameCout', e = True, l = str(iCurrentEnd - iCurrentStart + 1)+ ' f')

	# Frames Section
	aTones = ['Tone5', 'Tone5']

	if iCurrentStart == iProdStart:
		aTones[0] = 'Tone1'
	if iCurrentEnd == iProdEnd:
		aTones[1] = 'Tone1'


	# if aTones[0]:
	cmds.button('oUIStartButton', e = True, bgc = UIColourControl.keywordColour(aTones[0]))
	# if aTones[1]:
	cmds.button('oUIEndButton', e = True, bgc = UIColourControl.keywordColour(aTones[1]))


	# Views Section
	aView = ['1', '2', '3', '4']

	for v in aView:
		if dDict[v] == '-':
			sBGC = 'CaptureTone3'
			sLabel = '-'
		else:
			sBGC = 'Tone4'
			sLabel = v
			if dDict['LastCapture'] == v:
				sBGC = 'Tone1'
		cmds.button('oUICapture%sButton'%v, e = True, bgc = UIColourControl.keywordColour(sBGC), label = sLabel)





	# Extra tools

	aTones = ['ConvertToolButtonOff', 'ConvertToolButtonOn']
	aTones2 = ['CalcToolButtonOff', 'CalcToolButtonOn']
	aTones3 = ['AnnotateToolButtonOff', 'AnnotateToolButtonOn']
	cmds.button('oUIConvert', e = True, bgc = UIColourControl.keywordColour(aTones[dDict['ConvertTool']]))
	cmds.button('oUICalc',    e = True, bgc = UIColourControl.keywordColour(aTones[dDict['CalcTool']]))
	cmds.button('oUIAnnotate',    e = True, bgc = UIColourControl.keywordColour(aTones[dDict['AnnotateTool']]))

def UIButton_ProdRange(*args):
	dDict = StudioSettings.SceneInfoStorage(sSceneTool)


	iRange = StudioSettings.StudioProductionFrameRange()
	iIn = int(cmds.playbackOptions(q = True, minTime = True))
	iOut = int(cmds.playbackOptions(q = True, maxTime = True))
	if iRange:
		cmds.button('oUIProdButton', e = True, bgc = UIColourControl.keywordColour('Tone2'))
	else:
		dDict = StudioSettings.SceneInfoStorage(sSceneTool)
		cmds.button('oUIProdButton', e = True, bgc = UIColourControl.keywordColour('Tone3'))

	dDict['currentStartFrame'] = iIn
	dDict['currentEndFrame'] = iOut
	cmds.button('oUIStartButton', e = True, label = str(iIn))
	cmds.button('oUIEndButton', e = True, label = str(iOut))

	dDict['prodStartFrame'] = iIn
	dDict['prodEndFrame'] = iOut



	StudioSettings.SceneInfoStorage(sSceneTool, dDict) # To update the info
	UIDisplayChecker()

def UIButton_InOut( sInOut, *args):
	dDict = StudioSettings.SceneInfoStorage(sSceneTool)

	iCurrent = int(cmds.currentTime(q = True))
	if sInOut == 'Start':
		dDict['currentStartFrame'] = iCurrent
		cmds.button('oUIStartButton', e = True, label = iCurrent)

		# if End frame is before current frame.
		if dDict['currentEndFrame'] <= iCurrent:
			dDict['currentEndFrame'] = iCurrent + 1
			cmds.button('oUIEndButton', e = True, label = iCurrent + 1)


	elif sInOut == 'End':
		dDict['currentEndFrame'] = iCurrent
		cmds.button('oUIEndButton', e = True, label = iCurrent)

		# if End frame is before current frame.
		if dDict['currentStartFrame'] >= iCurrent:
			dDict['currentStartFrame'] = iCurrent - 1
			cmds.button('oUIStartButton', e = True, label = iCurrent - 1)


	elif sInOut == 'Current':
		iIn = int(cmds.playbackOptions(q = True, minTime = True))
		iOut = int(cmds.playbackOptions(q = True, maxTime = True))
		dDict['currentStartFrame'] = iIn
		dDict['currentEndFrame'] = iOut
		cmds.button('oUIStartButton', e = True, label = iIn)
		cmds.button('oUIEndButton', e = True, label = iOut)

	else:
		pass

	StudioSettings.SceneInfoStorage(sSceneTool, dDict)

	UIDisplayChecker()

def UIButton_Open( sOpen, *args):
	global K, sRvPath
	# 'PB' for quad view, 'Anno' for opening Annotation.rv
	#sRvPath = os.path.join(sRvPath, dShotInfo['sSeqNumber'] + '_' +dShotInfo['sShotNumber'])

	if sOpen =='PB':
		if not os.path.exists(sRvPath):
			K = 100
		if K: # If with any Modifiers, Create a fresh Active.rv. (deletes all markings etc.)
			dInfo = StudioSettings.SceneInfoStorage(sSceneTool) # Check function for more info.

			sIn = dInfo['prodStartFrame']
			if sIn == None:
				sIn = dInfo['currentStartFrame']

			sOut = dInfo['prodEndFrame']
			if sOut == None:
				sOut = dInfo['currentEndFrame']


			aPath = [None, None, None, None, ]
			for i in range(0, len(aPath)):
				#aPath[i] = aShotInfo[7] + '/%s/PlayBlast_%s.%s-%s@@@@.jpg'%(str(i+1), str(i+1), sIn, sOut)
				aPath[i] = dShotInfo['sPlayBlastSeqPath'] + '/%s/PlayBlast_%s.%s-%s@@@@.jpg'%(str(i+1), str(i+1), sIn, sOut)



			sContent = CreateLatestQuadRvFile(aPath)

			if sContent:
				oRvFile = open(sRvPath, 'w')
				oRvFile.write(sContent)
				oRvFile.close()

			aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'Creating a New .rv')

		else:
			aPrint = UIColourControl.inViewMessageColourPreset('Blue', 'Opening Existing .rv')

		try:
			cmd = 'rv %s &' % (sRvPath)
			os.system(cmd)
		except Exception as e:
			print e

		print sRvPath

		PrintOnScreen(aPrint)

	UIDisplayChecker()

def UIButton_Capture( sView, *args):
	# Display Logic
	K = cmds.getModifiers()
	sGrayOut = 'DarkGray'

	dToolInfo = StudioSettings.SceneInfoStorage(sSceneTool)
	sLabel = dToolInfo[sView]


	iStartCapture = 0
	if K:

		if sLabel == '-':
			sLabel = sView
		else:
			sLabel = '-'

		dToolInfo[sView] = sLabel



		StudioSettings.SceneInfoStorage(sSceneTool, dToolInfo)

	else:
		if not sLabel == '-':
			iStartCapture = 1

	#UIDisplayChecker()

	# PlayBlast time!
	if iStartCapture:

		sCapturePath = dShotInfo['sPlayBlastSeqPath']+'/'+sView+'/PlayBlast_%s'%sView
		#sCapturePath = aShotInfo[7]+'/'+sView+'/PlayBlast_%s'%sView
		sIn = dToolInfo['currentStartFrame']
		sOut = dToolInfo['currentEndFrame']

		cmds.playblast(format = 'image', filename = sCapturePath, st = int(sIn), et = int(sOut), sequenceTime = 0, clearCache = 1, viewer = 0, showOrnaments = 1, offScreen = True, fp = 4, percent = 100, compression = "jpg", quality = 70, fo = True, wh = [iPBwidth, iPBheight])


		cmds.warning('Capture Process All Finished')
		#UIDisplayChecker()

		cmds.button('oUICapture%sButton'%sView, e = True, bgc = UIColourControl.keywordColour('Tone1'))
		#dDict['LastCapture'] = sView
		dToolInfo['LastCapture'] = sView

		PrintOnScreen(['a7a8af', 'Playblast done [%s]'%sView, 0x6b6c75])



	StudioSettings.SceneInfoStorage(sSceneTool, dToolInfo)

	UIConvertTool_DisplayChecker()
	UIDisplayChecker()

def CreateLatestQuadRvFile( aPath):
	sContent = None

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
