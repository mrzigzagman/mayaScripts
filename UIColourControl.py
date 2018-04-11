import imp
import json
import maya.cmds as cmds

# Custom
import StudioSettings


dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)
sShotNumber = dShotInfo['sSeqNumber']+dShotInfo['sShotNumber']
sProjectConfigFile = dShotInfo['sProjectConfigFile']

def faceColour(sColour = 'default'):

	dColour = {
	'eyeBalls':[102, 0, 0],
	'eyeLids':[170, 0, 0],
	'brows':[170, 170, 0],
	'cheeks':[0, 85, 0],
	'nose':[170, 85, 0],
	'lipSticky':[71, 71, 71],
	'lipZipper':[151, 151, 151],
	'jaw':[255, 255, 255],
	'lipCorners':[0, 75, 110],
	'lipsPart':[0, 125, 178],
	'lipsFold':[84, 218, 255],
	'puff':[38, 0, 59],
	'throat':[96, 48, 0],
	'tongue':[255, 85, 0],
	'ears':[0, 28, 0],
	'neck':[85, 85, 0],
	'gravity':[0, 0, 0],
	'eyeLidTweaks':[170, 93, 93],
	'browTweaks':[255, 255, 127],
	'cheekTweaks':[120, 120, 120],
	'noseTweak':[255, 170, 0],
	'lipTweaks':[174, 108, 255],
	'default':[68, 68, 68] # 68/ 2.6666 # text 0.8
	}

	if sColour == 'getDict':
		return dColour
	else:
		return getRGBvalues(dColour[sColour])

def offsetRGBvalues(aRGB = [0.0, 0.0, 0.0], R = 0.1, G = 0.1, B = 0.1):
	aRGB[0] += R
	aRGB[1] += G
	aRGB[2] += B
	return aRGB


def getRGBvalues(aRGB):
	aValues = []
	for v in aRGB:
		aValues.append(round(v/255.0, 4))

	return aValues
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
				'red':(1, 0, 0),
				'lightgray':(0.7, 0.7, 0.7),
				'mayabg':oRGB,}

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
