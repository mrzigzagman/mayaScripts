# ALL Custom Settings to be created here.
# Version 0.1.1
# Adding MAYA UI BG colour tool. Creating setting folder and text.
import json
import maya.cmds as cmds

def ShotInfo(iFolder = 0, iPrint = 0):
	''' Adjusting Studio differences of Folder Hiearchy to get Shot Numbers and Paths and etc.

	Returns a List, containing all info.

	iFolder # Switch this on to create folder structure.
	iPrint # Switch this on when setting up. Displays what gets returned.'''
	import maya.cmds as cmds
	import getpass
	import os
	#-----


	### Setting ###
	iAvoidRunFromNewScene = 0 # Studio Dependant : Switch this on if os.getcwd does not return. Proj/Seq/Shot numbers.

	#-----

	aReturn = [] # The main var to collect info.
	sUser = getpass.getuser() # get username

	### Checking Scene Paths ###
	# The goal is to prepare sScenePath with or without having a scene opened.
	sShotPath = os.getcwd() # Getting the environment. Essential to get this including Proj, Seq, Shot numbers.
	sScenePath = cmds.file(q = True, sn = True) # Getting ScenePath if new scene, returns null.

	if sScenePath: # If run from a saved sScenePath
		sScenePath = '/'.join(sScenePath.split('/')[:-2])
	else: # If run in a new scene:
		if not iAvoidRunFromNewScene:
			# Try to match the result of sScenePath to cmds.file(q = True, sn = True) to have all customization in one place. (here)

			# Weta structure 1/2
			aShotPath = sShotPath.split('/')
			sShotPath = '/'.join(aShotPath)
			sScenePath = '%s/motion/work/maya/%s'%(sShotPath, sUser)
		else:
			print 'Might cause an error. havnt test this condition.'

	# Weta structure 2/2 : fixing error : doesn't read /Proj
	aScenePath = sScenePath.split('/')
	if not aScenePath[1] == 'proj':
		aScenePath.insert(1, 'proj')
		sScenePath = '/'.join(aScenePath)
	### Ready : sScenePath

	# Variable Assignments
	# Shot / Seq Numbers : Adjust the index for studio specific
	sProject = sScenePath.split('/')[2]
	sSeqNumber = sScenePath.split('/')[4]
	sShotNumber = sScenePath.split('/')[5]

	aCreateFolder = []
	### PERSONAL FOLDER PATHS #
	# Adjust the Personal folder structure here.
	sPersonalFolder = '/usr/home/%s'%sUser # Initial Path to the folder.
	# Personal folder contains...
	# *Personal Folder*/Project/*Project Name*/RV/*Shot Number*/
	# *Personal Folder*/Project/*Project Name*/Setting/
	aPersonalFolder = [ '/Project/%s/RV/%s%s/'%(sProject, sSeqNumber, sShotNumber),
						'/Project/%s/Setting/'%(sProject)]
	sPlayBlastToolPath = sPersonalFolder + aPersonalFolder[0]
	sSceneConfigFile = sPersonalFolder + aPersonalFolder[1]

	for a in aPersonalFolder:
		aCreateFolder.append(sPersonalFolder + a)

	sProjectConfigFile = sPersonalFolder+aPersonalFolder[1]+'ProjectConfig.json'


	# ## PRODUCTION PATHS ###
	# Adjust Here : Custom Scene Folder structure under PRODUCTION folder.
	# ex '/proj/mll/shots/ata/1600/motion/work/maya/dyabu/....'
	aProductionPath = [ '/Scenes', # Do not change the index of aProductionPath[0]
						'/Scenes/Old',
						'/Exports',
						'/Images/Refs',
						'/Images/PB',
						'/Images/PB/1',
						'/Images/PB/2',
						'/Images/PB/3',
						'/Images/PB/4',
						'/Images/Nuke',
						'/cf',] # marked as [-1] do not change this.

	for a in aProductionPath:
		aCreateFolder.append(sScenePath + a)

	sSceneConfigFile = sScenePath + aProductionPath[-1] + "/" + 'SceneConfig.json'

	### Folder Creation ###
	if iAvoidRunFromNewScene:
		print 'This will only work from a saved scene.'
	else:
		# Create Folder structure
		if iFolder:
			# Check Folders existance for folders
			for a in aCreateFolder:
				if not os.path.isdir(a):
					os.makedirs(a)
					if iPrint: print 'Directory Created : %s '%(a)
				else:
					if iPrint: print 'Directory Existed : %s '%(a)

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


		if not os.path.isfile(sProjectConfigFile):
			with open(sProjectConfigFile, 'w') as oFile:
				#json.dumps(dContent, oFile, indent = 4) # This does not work
				json.dump(dContent, oFile, indent = 4)

		# Create SCENE config files.

		dContent = {}
		if not os.path.isfile(sSceneConfigFile):
			with open(sSceneConfigFile, 'w') as oFile:
				json.dump(dContent, oFile, indent = 4)



	# More variables assignment.
	sPlayBlastSeqPath = sScenePath + aProductionPath[4] # where the actual playblast files go.
	sScenePath += aProductionPath[0] # Keep this at the very end to have '/Scenes' added at the end

	# Environment Folder
	sEnvFolder = '/'.join(cmds.about(env = True).split('/')[:-1])
	#Scripts Folders
	sGlobalScriptFolder = ''
	sLocalScriptFolder = ''
	sMayaScriptFolder = '/vol/transfer/dyabu/Scripts/mayaScrips/'


	# Collect all Variables.
	aReturn.extend([sUser,
					sScenePath,
					sProject,
					sShotNumber,
					sSeqNumber,
					sPersonalFolder,
					sPlayBlastToolPath,
					sPlayBlastSeqPath,
					sEnvFolder,
					sGlobalScriptFolder,
					sLocalScriptFolder,
					sMayaScriptFolder,
					sProjectConfigFile,
					sSceneConfigFile,
					])


	# Path Existance Check
	for i, path in enumerate(aReturn[:]):
		if '/' in path:
			if not os.path.exists(path):
				aReturn[i] = 'Path Does Not Exist'



	if iPrint:
		print '-------------------------------------'
		print 'STUDIO SETTING VARIABLES'; print
		print '[0] = sUser : ', aReturn[0]
		print '[1] = sScenePath : ', aReturn[1]
		print '[2] = sProject : ', aReturn[2]
		print '[3] = sShotNumber : ', aReturn[3]
		print '[4] = sSeqNumber : ', aReturn[4]
		print '[5] = sPersonalFolder : ', aReturn[5]
		print '[6] = sPlayBlastToolPath : ', aReturn[6]
		print '[7] = sPlayBlastSeqPath : ', aReturn[7]
		print '[8] = sEnvFolder : ', aReturn[8]
		print '[9] = sGlobalScriptFolder : ', aReturn[9]
		print '[10] = sLocalScriptFolder : ', aReturn[10]
		print '[11] = sMayaScriptFolder : ', aReturn[11]
		print '[12] = sProjectConfigFile : ', aReturn[12]
		print '[13] = sSceneConfigFile : ', aReturn[13]
		print '-------------------------------------'

	sShotgunPage = ''
	sShotWebPage = ''

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
