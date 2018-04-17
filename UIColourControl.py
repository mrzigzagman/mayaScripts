import imp
import json
import colorsys
import maya.cmds as cmds

# Custom
import StudioSettings


dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)
sShotNumber = dShotInfo['sSeqNumber']+dShotInfo['sShotNumber']
sProjectConfigFile = dShotInfo['sProjectConfigFile']

def faceColour(sColour = 'default'):

	dColour = {
	'eyeBalls':[[102, 0, 0], [230, 184, 184]],
	'eyeLids':[[170, 0, 0],[255, 218, 218]],
	'brows':[[170, 170, 0], [50, 50, 0]],
	'cheeks':[[0, 85, 0], [178, 255, 178]],
	'nose':[[170, 85, 0], [255, 221, 186]],
	'lipSticky':[[71, 71, 71], [169, 169, 169]],
	'lipZipper':[[151, 151, 151], [40, 40, 40]],
	'jaw':[[255, 255, 255], [65, 65, 65]],
	'lipCorners':[[0, 75, 110], [141, 230, 255]],
	'lipsPart':[[0, 125, 178], [203, 239, 255]],
	'lipsFold':[[84, 218, 255], [0, 45, 64]],
	'puff':[[38, 0, 59], [155, 108, 181]],
	'throat':[[96, 48, 0], [221, 186, 152]],
	'tongue':[[255, 85, 0], [255, 228, 215]],
	'ears':[[0, 28, 0], [95, 161, 95]],
	'neck':[[85, 85, 0], [191, 191, 0]],
	'gravity':[[0, 0, 0], [79, 79, 79]],
	'eyeLidTweaks':[[170, 93, 93], [255, 220, 220]],
	'browTweaks':[[255, 255, 127], [70, 70, 0]],
	'cheekTweaks':[[120, 120, 120], [226, 226, 226]],
	'noseTweak':[[255, 170, 0], [50, 34, 0]],
	'lipTweaks':[[174, 108, 255], [245, 237, 255]],
	'default':[[68, 68, 68], [255, 255, 255]], # 68/ 2.6666 # text 0.8
	}


	if sColour == 'getDict':
		return dColour
	else:
		if sColour in dColour.keys():
			return getRGBvalues(dColour[sColour])
		else:
			return getRGBvalues(dColour['default'])


def offsetRGBvalues(aRGB = [0.0, 0.0, 0.0], R = 0.0, G = 0.0, B = 0.0):
	aRGB[0] += R
	aRGB[1] += G
	aRGB[2] += B
	return aRGB


def getRGBvalues(aRGB): # from 255 to 1.0 USE convertRGBvaluesToScaleOF instead.
	pass



def convertRGBvaluesToScaleOf(iType = 1, aRGB = []): # iType is 1 or 255
	aValues = []

	if iType == 1:
		for v in aRGB:
			aValues.append(round(v/255.0, 4))

	elif iType == 255:
		for v in aRGB:
			aValues.append(int(v*255))
	else:
		print 'convertRGBvaluesTo : error: enter only 1 or 255'

	return aValues

def RGBHSVconverter(sType = 'ToRGB', aColour = [1, 1, 1]):
	aNew = []
	if sType == 'ToHSV':
		aNew = list(colorsys.rgb_to_hsv(aColour[0],aColour[1],aColour[2]))
	else:
		aNew = list(colorsys.hsv_to_rgb(aColour[0],aColour[1],aColour[2]))

	return aNew

def inViewMessageColourPreset(keyword = 'Blue', text = 'TEST'):
	dColour = {
	'Green': ['6bad64', text, 0x6c756b],
	'Red': ['d8766c', text, 0x756b6b],
	'Blue': ['9bbcf2', text, 0x485872],
	'Gray': ['a7a8af', text, 0x6b6c75],
	}
	return dColour[keyword]


def keywordColour(sColour = 'Red'):
	# Get Maya BG Colour from pallette.
	#sScriptName = 'MayaBGColour' # state the filename without '.py'
	#MayaBGColour = imp.load_source(sScriptName, '%s/MayaBGColour.py'%self.sScriptPath)

	#oRGB = MayaBGColour.getBGColour()
	oRGB = getMayaBGColour()

	# List all keys in lowerCase
	dColour = { 'MayaBG':oRGB,

				'Tone1':(0.822, 0.967, 1.000),
				'Tone2':(0.349, 0.447, 0.537),
				'Tone3':(0.231, 0.384, 0.525),
				'Tone4':(0.188, 0.231, 0.271),
				'Tone5':(0.224, 0.420, 0.502),
				'Tone6':(0.224, 0.369, 0.502),
				'Tone7':(0.224, 0.298, 0.502),


				# PlayBlastTool Colours
				'CaptureTone1':(0.8196, 0.9020, 1.000),
				'CaptureTone2':(0.6471, 0.7608, 0.8941),
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

				'SeqButton' : (0.1882, 0.2627, 0.2706),
				'RvButton' : (0.1216, 0.2471, 0.2706),


				# General
				'LightGray':(0.6, 0.6, 0.6),
				'WhiteGray':(0.8, 0.8, 0.8),
				'White':(1,1,1),
				'DarkGray':(0.3,0.3,0.3),
				'Gray':(0.4, 0.4, 0.4),
				'Blue':(0.8, 0.8, 0.8),
				'Yellow':(1.0, 1.0, 0.8),
				'Red':(1, 0, 0),
				'LightGray':(0.7, 0.7, 0.7),}

	return dColour[sColour]




def setMayaBGColour():

	##sScriptName = 'StudioSettings' # state the filename without '.py'
	##sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts/%s.py'%sScriptName
	##StudioSettings = imp.load_source(sScriptName, sScriptPath)
	#dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)

	##sShotNumber = aShotInfo[4]+aShotInfo[3]
	#sShotNumber = dShotInfo['sSeqNumber']+dShotInfo['sShotNumber']
	##sProjectConfigFile = aShotInfo[12]
	#sProjectConfigFile = dShotInfo['sProjectConfigFile']

	with open(sProjectConfigFile, 'r') as oFile:
		dDict = json.load(oFile)



	# Frequency Logic
	aColourOrder = []

	if sShotNumber in dDict['MayaBGColourAssign'].values(): # if sShotNumber exist in the Assign list.
		for keyA, valueA in dDict['MayaBGColourAssign'].iteritems(): # find the Tone of current shotnumber.
			if valueA == sShotNumber:
				sColourAssign = keyA # Current Tone assigned to sShotNumber
			aColourOrder.append('') # This is just to help create an empty array

		for keyF, valueF in dDict['MayaBGColourFrequency'].iteritems(): # Create a list with the current frequency order
			if not keyF == sColourAssign: # Except for the current assign. (leaving one entry empty as '')
				aColourOrder[valueF] = keyF

		aColourOrder.remove('') # Remove and...
		aColourOrder.append(sColourAssign) # add the current assign to the end.

		for i, v in enumerate(aColourOrder[:]):
			dDict['MayaBGColourFrequency'][v] = i # Reorder using the index

	else: # if a new shot is about to be worked on. (not listed on the Assign List)
		for keyA, valueA in dDict['MayaBGColourFrequency'].iteritems(): # Find the frequency of 0 in the list.
			if valueA == 0:
				sColourAssign = keyA
			aColourOrder.append('') # This is just to help create an empty array

		dDict['MayaBGColourAssign'][sColourAssign] = sShotNumber

		for keyA in dDict['MayaBGColourFrequency'].keys(): # subtract all frequency -1 and re-assign current to max.
			dDict['MayaBGColourFrequency'][keyA] -= 1
		dDict['MayaBGColourFrequency'][sColourAssign] = 4 # max number of colour index

	#print 'MayaBGColour - Write'
	#print dDict
	# Logic is done. Write to file
	with open(sProjectConfigFile, 'w') as oFile:
		#json.dumps(dDict, indent = 4) #This Does not work
		json.dump(dDict, oFile, indent = 4)

	# Apply in Maya
	sBGC = dDict['MayaBGColourPalette'][sColourAssign]
	for ctrl in cmds.lsUI(type = 'control'):
		try:
			cmds.layout(ctrl, e = True, bgc = sBGC)
		except RuntimeError:
			pass
	cmds.refresh(f = True)


def getMayaBGColour():
	##sScriptName = 'StudioSettings' # state the filename without '.py'
	##sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts/%s.py'%sScriptName
	##StudioSettings = imp.load_source(sScriptName, sScriptPath)
	#dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)

	#sShotNumber = aShotInfo[4]+aShotInfo[3]
	#sProjectConfigFile = aShotInfo[12]


	with open(sProjectConfigFile, 'r') as oFile:
		dDict = json.load(oFile)


	for keyA, valueA in dDict['MayaBGColourAssign'].iteritems(): # find the Tone of current shotnumber.
		if valueA == sShotNumber:
			sColourAssign = keyA # Current Tone assigned to sShotNumber

	sBGC = dDict['MayaBGColourPalette'][sColourAssign]
	return sBGC
