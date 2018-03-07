import imp
import json
import maya.cmds as cmds


def main():

	sScriptName = 'StudioSettings' # state the filename without '.py'
	sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts/%s.py'%sScriptName
	StudioSettings = imp.load_source(sScriptName, sScriptPath)
	aShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)

	sShotNumber = aShotInfo[4]+aShotInfo[3]
	sProjectConfigFile = aShotInfo[12]

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

	print 'MayaBGColour - Write'
	print dDict
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


def getBGColour():
	sScriptName = 'StudioSettings' # state the filename without '.py'
	sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts/%s.py'%sScriptName
	StudioSettings = imp.load_source(sScriptName, sScriptPath)
	aShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)

	sShotNumber = aShotInfo[4]+aShotInfo[3]
	sProjectConfigFile = aShotInfo[12]

	with open(sProjectConfigFile, 'r') as oFile:
		dDict = json.load(oFile)

	for keyA, valueA in dDict['MayaBGColourAssign'].iteritems(): # find the Tone of current shotnumber.
		if valueA == sShotNumber:
			sColourAssign = keyA # Current Tone assigned to sShotNumber

	sBGC = dDict['MayaBGColourPalette'][sColourAssign]
	return sBGC
