# ALL Custom Settings to be created here.
# Version 0.2.2
# Adding MAYA UI BG colour tool. Creating setting folder and text.
import json
import maya.cmds as cmds
import getpass
import os.path
import os

def ProjectInfo(sProj = ''):
	# Project base settings

	### CUSTOMIZE - Playblast Size ###
	dPlayBlastSize = {	''   :[0, 0],
						'ABA':[1092, 576],}

	aProjectInfo = [[0,0], # Playblast Width & Height (int has to be able to divide by 4.)
					]

	aProjectInfo[0] = dPlayBlastSize[sProj]

	return aProjectInfo


def ShotInfo(iFolder = 0, iPrint = 0):
	''' Adjusting Studio differences of Folder Hiearchy to get Shot Numbers and Paths and etc.

	Returns a List, containing all info.

	iFolder # Switch this on to create folder structure.
	iPrint # Switch this on when setting up. Displays what gets returned.'''


	### CUSTOMIZE - Setting ###
	iAvoidRunFromNewScene = 0 # Studio Dependant : Switch this on if os.getcwd does not return. Proj Seq Shot info.
	###

	aReturn = [] # The main var to collect info.
	SSV_sUser = getpass.getuser() # get username

	## Checking Scene Paths
	# The goal is to prepare SSV_sScenePath with or without having a scene opened.
	# sScenePath should be the Folder where the Custom folders to be populated. Not where the .ma files are.
	# SSV_sScenePath shold be the folder where scene files to be saved.


	## Getting the environment.
	# Essential to get [Proj] [Seq] [Shot] in order for tools to run in a freshly opened maya.
	sScenePath = os.path.realpath(os.getcwd()) # vvv ?/?
	#sScenePath = os.path.realpath(cmds.file(q = True, sn = True)) # Getting ScenePath if new scene, returns null.


	aScenePath = sScenePath.split('/')
	SSV_sProject = aScenePath[2]
	SSV_sSeqNumber = aScenePath[4]
	SSV_sShotNumber = aScenePath[5]


	### CUSTOMIZE - set path to where custom folders to be populated. [Scenes] [Images] [Export] ###
	sScenePath = os.path.join(sScenePath, 'motion/work/maya' ,SSV_sUser)
	###
	aScenePath = sScenePath.split('/')

	### CUSTOMIZE - Personal Folder path (where .rv files are saved under project folders.) ###
	SSV_sPersonalFolder = '/usr/home/%s'%SSV_sUser # Initial Path to the folder.
	###


	## Tool setting all across other tools. # Shoun't Have to Modiy...
	SSV_sPlayBlastToolPath = os.path.join(SSV_sPersonalFolder, 'Project/%s/RV/%s_%s'%(SSV_sProject, SSV_sSeqNumber, SSV_sShotNumber))
	SSV_sSceneConfigFile = os.path.join(SSV_sPersonalFolder, 'Project/%s/Setting'%(SSV_sProject))

	aCreateFolder = []
	aCreateFolder.append(SSV_sPlayBlastToolPath)
	aCreateFolder.append(SSV_sSceneConfigFile)

	#SSV_sProjectConfigFile = SSV_sPersonalFolder+aPersonalFolder[1]+'ProjectConfig.json'
	SSV_sProjectConfigFile = os.path.join(SSV_sSceneConfigFile,'ProjectConfig.json')


	## PRODUCTION PATHS
	# ex '/proj/mll/shots/ata/1600/motion/work/maya/dyabu/....'
	aProductionPath = [ 'Scenes',      # [0] # DO NOT CHANGE the index of these entries. (Can add more)
						'Scenes/Old',  # [1]
						'Exports',     # [2]
						'Images/Refs', # [3]
						'Images/PB',   # [4]
						'Images/PB/1', # [5]
						'Images/PB/2', # [6]
						'Images/PB/3', # [7]
						'Images/PB/4', # [8]
						'Images/Nuke', # [9]
						'cf',] # marked as [-1] do not change this.

	for a in aProductionPath:
		#print sScenePath, a
		aCreateFolder.append(os.path.join(sScenePath, a))

	SSV_sSceneConfigFile = os.path.join(sScenePath, aProductionPath[-1] , 'SceneConfig.json')

	## Folder Creation
	if iAvoidRunFromNewScene:
		print 'This will only work from a saved scene.'
	else:
		# Create Folder structure
		if iFolder:
			# Check Folders existance for folders
			for a in aCreateFolder:
				if not os.path.isdir(a):
					os.makedirs(a)
					if iPrint: print 'Directory CREATED : %s '%(a)
				else:
					if iPrint: print 'Directory exists : %s '%(a)

			# Create PROJECT config files.



		dContent = {'MayaBGColourPalette' : {	'MayaBGtone1': (0.3254,0.3490,0.2627),
												'MayaBGtone2': (0.2627,0.3490,0.2627),
												'MayaBGtone3': (0.2627,0.3490,0.3411),
												'MayaBGtone4': (0.2627,0.3058,0.3490),
												'MayaBGtone5': (0.3215,0.2627,0.3490),
												'MayaBGtone6': (0.3490,0.2627,0.3137),
												'MayaBGtone7': (0.3490,0.2745,0.2627),
												'MayaBGtone8': (0.3490,0.3476,0.2627),
												},
					'MayaBGColourAssign' : {	'MayaBGtone1': '-',
												'MayaBGtone2': '-',
												'MayaBGtone3': '-',
												'MayaBGtone4': '-',
												'MayaBGtone5': '-',
												'MayaBGtone6': '-',
												'MayaBGtone7': '-',
												'MayaBGtone8': '-',
												},
					'MayaBGColourFrequency' : {	'MayaBGtone1': 0,
												'MayaBGtone2': 1,
												'MayaBGtone3': 2,
												'MayaBGtone4': 3,
												'MayaBGtone5': 4,
												'MayaBGtone6': 5,
												'MayaBGtone7': 6,
												'MayaBGtone8': 7,
												},
					}

		print SSV_sProjectConfigFile

		if not os.path.isfile(SSV_sProjectConfigFile):
			with open(SSV_sProjectConfigFile, 'w') as oFile:
				#json.dumps(dContent, oFile, indent = 4) # This does not work
				json.dump(dContent, oFile, indent = 4)

		# Create SCENE config files.
		dContent = {}
		if not os.path.isfile(SSV_sSceneConfigFile):
			with open(SSV_sSceneConfigFile, 'w') as oFile:
				json.dump(dContent, oFile, indent = 4)


	# Othere Paths
	SSV_sPlayBlastSeqPath = os.path.join(sScenePath, aProductionPath[4])
	SSV_sEnvFolder = os.path.realpath(os.path.split(cmds.about(env = True))[0])

	#Scripts Folders
	SSV_sGlobalScriptFolder = '- Not Specified'
	SSV_sLocalScriptFolder = '/vol/transfer/dyabu/Scripts/mayaScripts'
	SSV_sMayaEnvScriptFolder = os.path.join(SSV_sEnvFolder, 'scripts')
	SSV_sNukeFileFolder = os.path.join(sScenePath, aProductionPath[4])

	# Scene Path
	SSV_sScenePath = os.path.join(sScenePath, aProductionPath[0])

	# Collect all Variables.
	aReturn.extend([SSV_sUser,
					SSV_sScenePath,
					SSV_sProject,
					SSV_sShotNumber,
					SSV_sSeqNumber,
					SSV_sPersonalFolder,
					SSV_sPlayBlastToolPath,
					SSV_sPlayBlastSeqPath,
					SSV_sEnvFolder,
					SSV_sGlobalScriptFolder,
					SSV_sLocalScriptFolder,
					SSV_sMayaEnvScriptFolder,
					SSV_sProjectConfigFile,
					SSV_sSceneConfigFile,
					SSV_sNukeFileFolder
					])

	# Path Existance Check
	for i, path in enumerate(aReturn[:]):
		if '/' in path:
			if not os.path.exists(path):
				aReturn[i] = 'Path Does Not Exist'


	if iPrint:
		print '-------------------------------------'
		print '### SSV : STUDIO SETTING VARIABLES ###'
		print '[0] = SSV_sUser : ', aReturn[0]
		print '[1] = SSV_sScenePath : ', aReturn[1]
		print '[2] = SSV_sProject : ', aReturn[2]
		print '[3] = SSV_sShotNumber : ', aReturn[3]
		print '[4] = SSV_sSeqNumber : ', aReturn[4]
		print '[5] = SSV_sPersonalFolder : ', aReturn[5]
		print '[6] = SSV_sPlayBlastToolPath : ', aReturn[6]
		print '[7] = SSV_sPlayBlastSeqPath : ', aReturn[7]
		print '[8] = SSV_sEnvFolder : ', aReturn[8]
		print '[9] = SSV_sGlobalScriptFolder : ', aReturn[9]
		print '[10] = SSV_sLocalScriptFolder : ', aReturn[10]
		print '[11] = SSV_sMayaEnvScriptFolder : ', aReturn[11]
		print '[12] = SSV_sProjectConfigFile : ', aReturn[12]
		print '[13] = SSV_sSceneConfigFile : ', aReturn[13]
		print '[14] = SSV_sNukeFileFolder: ', aReturn[14]
		print '-------------------------------------'

	return aReturn

def OSFileBrowserCommand(sPath):
	# FileBrowser command
	import os
	iOption = 0

	if iOption == 0:
		sBrowserCommand = 'dolphin'
	elif iOption == 1:
		sBrowserCommand = 'nautilus'

	os.system('%s %s &'%(sBrowserCommand, sPath))

def StudioProductionFrameRange():
	# IF studio Range Tool don't exist, set to 0:
	iStudioTool = 1
	if iStudioTool:
		from mo.wm.utils.sceneRange import setSceneRange; setSceneRange(handles = True)

	return iStudioTool

def OpenSceneCommand(sPath, bForce = False):
	# Load Scene command
	iOption = 1
	if iOption == 0: # Maya Default
		cmds.file(sPath, o = True, f = bForse)
	elif iOption == 1: # W V
		import mo.wm.tools.updateAssets.ui.updateUI
		mo.wm.tools.updateAssets.ui.updateUI.launch(sPath)

def CopyToClipBoard(sString):
	import pygtk ; pygtk.require('2.0')
	import gtk

	clipboard = gtk.clipboard_get()
	clipboard.set_text(sString)
	clipboard.store()

def AnimToolAttributes(sTool, dDict = None):
	# This funciton...
	# 1. Sets Custom Animation Nodes for different custom tools. With Attributes Note activated (if they don't exist.)
	# 2. Rewirtes (if dDict is entered.)
	# 3. Returns dictionary. (if no dDict is specified.)


	oAnimTools = 'ANIM_TOOLS'
	if not cmds.objExists(oAnimTools):
		cmds.group(em = True, name = oAnimTools)
		cmds.addAttr(oAnimTools, shortName = 'notes', dataType = 'string') # Activate Notes Attributes to store json
		cmds.setAttr('%s.notes'%oAnimTools, json.dumps(None, indent = 4) , type = 'string')


	if not cmds.objExists(sTool):
		cmds.group( em = True, name = sTool, p = oAnimTools)
		cmds.addAttr(sTool, shortName = 'notes', dataType = 'string')
		cmds.setAttr('%s.notes'%sTool, json.dumps(None, indent = 4), type = 'string')


	if dDict:
		cmds.setAttr('%s.notes'%sTool, json.dumps(dDict, indent = 4), type = 'string')


	dDict = json.loads(cmds.getAttr('%s.notes' % sTool))
	return dDict

def MayaBGColourAdjustment():
	pass
