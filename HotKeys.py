# Hotkeys - Consolidated v0.1.1
# Adjusting Custom Camera for aba
# Hotkeys - Consolidated v0.1.0
# new feature. a button to create custom scripts in Script editor.
# Hotkeys - Consolidated v0.0.3
# Focus Button Custom
# Hotkeys - Consolidated v0.0.2
# need a few cleanups.
# - camera creation R_ALT

# vvv 3/3


import maya.cmds as cmds
import maya.mel as mel
import imp
import sys
import redbox as rb #vvv 1/2

# Custom
import StudioSettings
import UIColourControl



sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScrips/'
if sScriptPath not in sys.path: sys.path.append(sScriptPath)


# Rule number 1 : ALL CAPS
# Dictionary Keys are in this format:
'''
S_S+C_P

S- Key in Caps
S+C - Modifier number
P - Pressed / Released
'''

# How to create hot keys in Maya
# - Copy and Paset Below to HotKey Editor
# 1. In Maya Hotkey Editor, Create a whole bunch of shortcuts with correct script names ex(F_ALT_P) with temp script in it.
# 2. Change the path in the below script
# 3. Then, paste to all script you made.
# 4. Then, change the Key and Press/Released
# Tip Set the release first before assign a pressed key.

'''
# Custom Hotkey - Consolidated - v0.0.1

# CUSTOMIZE HERE:
p = '/usr/home/dyabu/Personal/MayaScripts/' # Path to HotKeys.py
sChar = 'u' # Key on Keyboard. not case sensitive.
sPress = 'p' # 'P' or 'R' Pressed or Release

# -- Start --
import maya.cmds as cmds
import sys
if p not in sys.path: sys.path.append(p)
import Hotkeys # Hotkeys.py

#reload(HotKeys) #Use reload when testing. Comment out when in actual use.

iModifier = cmds.getModifiers()
HotKeys.Execute(sChar, iModifier, sPress)
'''


def KeyList():
	dHotKeys = {
	'B_ALT_P': HotKey_PreviousGreenKey,
	'B_N_P': HotKey_PreviousKey,
	# 'C_ALT_P': C_ALT_P,

	'D_ALT_P': HotKey_ToggleVisCurves,
	# 'E_ALT_P': E_ALT_P,


	'F_ALT_P': HotKey_AttrIncrement_n001,
	'F_N_P': HotKey_SelectAll_P,
	'F_N_R': HotKey_SelectAll_R,

	'G_ALT_P': HotKey_AttrIncrement_n01,
	'G_N_P': HotKey_SetKey,

	'H_ALT_P': HotKey_AttrIncrement_p01,
	'H_N_P': HotKey_Playback_P,
	'H_N_R': HotKey_Playback_R,

	#'I_ALT_P': HotKey_OpenOutliner,
	'I_ALT_P': I_ALT_P,
	'I_N_P': I_N_P,
	'I_N_R': I_N_R,

	'J_ALT_P': HotKey_AttrIncrement_p001,

	# Remember to modify Focus in OUtliner and GraphEditor to J also.
	'J_N_P': HotKey_Focus,

	'K_N_P': K_N_P,
	'K_N_R': K_N_R,

	#'K_ALT_P': K_ALT_P,
	#'K_ALT_P': K_ALT_R,
	# 'L_ALT_P': L_ALT_P,
	'M_ALT_P': HotKey_Copy,
	'M_N_P': HotKey_NextFrame,

	'N_ALT_P': HotKey_NextGreenKey,
	'N_N_P': HotKey_NextKey,
	# 'O_ALT_P': O_ALT_P

	'R_ALT_P' :HotKey_SetUI,
	'R_N_P': HotKey_SelectTool_P,
	'R_N_R': HotKey_SelectTool_R,
	'T_ALT_P': HotKey_PlayBlastTool,
	'T_N_P': HotKey_MoveTool_P,
	'T_N_R': HotKey_MoveTool_R,

	'U_ALT_P': HotKey_AxisSwitcher,
	'U_N_P': HotKey_ScaleTool_P,
	'U_N_R': HotKey_ScaleTool_R,

	'V_ALT_P': HotKey_Undo,
	'V_N_P': HotKey_PreviousFrame,

	'Y_ALT_P': HotKey_BreakConnections,
	'Y_N_P': HotKey_RotationTool_P,
	'Y_N_R': HotKey_RotationTool_R,

	'COMMA_ALT_P': HotKey_Paste,
	'SPACE_N_P': HotKey_PanePoP,
	}
	return dHotKeys

def Execute(skey = 'j', iModifier = 0, sPress = 'P'):
	sKey = skey.upper()
	sModifier = str(iModifier)
	sPress = sPress.upper()
	aModifier = [   0, 'N',
					1, 'SFT',
					4, 'CTR',
					8, 'ALT',
					5, 'S+C',
					9, 'S+A',
					12, 'A+C',
					13, 'C+A+S',
					9999,'CMD']
	for i in range(0, len(aModifier), 2):
		if aModifier[i] == iModifier:
			sModifier = aModifier[i+1]

	dHotKeys = KeyList()


	dHotKeys['%s_%s_%s' % (sKey, sModifier, sPress)]()


#### Shortcut Functions ####
# 1. All Caps

##### NOT HotKey_ Fuctions #####
def NOT():
	print 'Hotkey Not Assigned.'
	aPrint = ['d8766c', 'HotKey Not Assigned', 0x756b6b, 'topCenter']
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = aPrint[3], fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def DisplayFaceValues():
	iStop = 0
	iNegative = False

	oChannel = [str(c+'.'+cmds.attributeName(c+'.'+b, l=True)) for a in 'msho' for b in cmds.channelBox('mainChannelBox', **{'q':True, 's%sa'%a:True}) or [] for c in cmds.channelBox('mainChannelBox', q = True, **{'%sol'%a:True})]
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]

	if len(oSel) == 1:
		if 0 < len(oChannel) <= 2:
			for c in oChannel:
				if cmds.attributeQuery(c.split('.')[-1], node = oSel[0], minExists = True):
					if cmds.attributeQuery(c.split('.')[-1], node = oSel[0], min = True)[0] == -1.0:
						iNegative = True
				else:
					iStop = 2
				if cmds.attributeQuery(c.split('.')[-1], node = oSel[0], maxExists = True):
					if not cmds.attributeQuery(c.split('.')[-1], node = oSel[0], max = True)[0] == 1.0:
						iStop = 3
				else:
					iStop = 5

			if len(oChannel) == 2:
				if not oChannel[1].split('.')[-1] == oChannel[0].split('.')[-1][:-1]+'R':
					iStop = 6
		else:
			iStop = 7
	else:
		iStop = 8

	if iStop:
		#print iStop
		pass

	else:
		# Initial Bar Colours
		aBar = []
		aColour = []
		for i in range(201):
			aBar.append('-')
			aColour.append('#85929E')
		for i in range(0, 201, 10):
			aBar[i] = ':'
			aColour[i] = '#AEB6BF'
		for i in range(0, 201, 50):
			aBar[i] = '|'
			aColour[i] = '#D6DBDF'
		for i in range(0, 100):
			aColour[i] = '#808B96'

		# Logic to split markings
		for i, c in enumerate(oChannel):
			iVal = int(cmds.getAttr(c)*100.0)+100
			aColour[iVal] = '#D4AC0D'
			if len(oChannel) == 1:
				if c[-1] == 'L':
					aBar[iVal] = ')'
				elif c[-1] == 'R':
					aBar[iVal] = '('
				else:
					aBar[iVal] = '|'
					#aColour[iVal] = '#FEF9E7'
			else:
				if i == 0:
					aBar[iVal] = ')'
				else:
					if aBar[iVal] == ')':
						aBar[iVal] = 'O'
					else:
						aBar[iVal] = '('

		aText = []
		for i, v in enumerate(aBar[:]):
			aText.append('<text style="color:%s";>%s</text>'%(aColour[i], v ) )

		if not iNegative:
			aText = aText[100:]
		sText = ''.join(aText)

		cmds.inViewMessage(amg = sText, pos = 'botCenter', fade = False, fts = 7, ft = 'arial',bkc = 0x5D6D7E, dragKill = 1)

def ATT_INCREMENT(iAmount):
	# Attribute Increment v4.0.0
	oChannel = [str(c+'.'+cmds.attributeName(c+'.'+b, l=True)) for a in 'msho' for b in cmds.channelBox('mainChannelBox', **{'q':True, 's%sa'%a:True}) or [] for c in cmds.channelBox('mainChannelBox', q = True, **{'%sol'%a:True})]

	iNewValue = None

	if oChannel:
		for c in oChannel:
			iVal = cmds.getAttr(c) + iAmount

			if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], minExists = True):
				if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], min = True)[0] >= iVal :
					iNewValue = cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], min = True)[0]

			if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], maxExists = True):
				if cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], max = True)[0] <= iVal:
					iNewValue = cmds.attributeQuery(c.split('.')[-1], node = c.split('.')[0], max = True)[0]

			if not iNewValue == None:
				cmds.setAttr(c, iNewValue)
			else:
				cmds.setAttr(c, iVal)

	else:
		aPrint = ['d8766c', 'No Attr Selected', 0x756b6b, 'midCenterBot']
		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = aPrint[3], fade = True, fts = 10, ft = 'arial',bkc = aPrint[2] )

	DisplayFaceValues()

def PrintOnScreen(aPrint):
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = aPrint[2])

def GreenTickKeys(iAllFrame = 0):

	oKeyPoseFrames = 'KeyPoseFrames'
	aKeyFrames= []
	if cmds.objExists(oKeyPoseFrames):
		for i in range(cmds.keyframe(oKeyPoseFrames+'.tx', kc = True, q = True)):
			aKeyFrames.extend(cmds.keyframe(oKeyPoseFrames+'.tx', index = (i,i), q = True))


		aObjList = [str(s) for s in cmds.selectionConnection('graphEditor1FromOutliner', q = True, object = True)  or [] ]
		#aCurveList = [str(s) for s in cmds.keyframe(q = True, name = True)]

		# Store Selected Keys
		aSelection = []
		for o in aObjList:
			aName = cmds.keyframe(o, query = True, name = True)
			aKeys = cmds.keyframe(o, sl = True, q = True)

			if aName and aKeys:
				aSelection.append([str(aName[0]), aKeys])

		if cmds.ls(sl = True):
			cmds.selectKey( clear = True)

		# DO
		fTime = cmds.currentTime(q = True)
		if fTime in aKeyFrames:
			cmds.keyframe(t = (fTime, fTime), tds = True)

		# Select Stored keys
		if aSelection:
			for a in aSelection:
				sName = a[0]
				for t in a[1]:
					cmds.selectKey(sName, t = (t,t), tgl = True)

		# Update All Frames red/green.
		if iAllFrame:
			iIn = int(cmds.playbackOptions(q = True, minTime = True))
			iOut = int(cmds.playbackOptions(q = True, maxTime = True))
			for i in range(iIn, iOut+1):
				if i in aKeyFrames:
					cmds.keyframe(t = (i, i), tds = True)
				else:
					cmds.keyframe(t = (i, i), tds = False)

##### HotKey_ Fuctions #####

def HotKey_PreviousGreenKey():
	oKeyPoseFrames = 'KeyPoseFrames'
	aKeyFrames= []
	if cmds.objExists(oKeyPoseFrames):
		for i in range(cmds.keyframe(oKeyPoseFrames+'.tx', kc = True, q = True)):
			aKeyFrames.extend(cmds.keyframe(oKeyPoseFrames+'.tx', index = (i,i), q = True))

		iIn = int(cmds.playbackOptions(q = True, minTime = True))
		iOut = int(cmds.playbackOptions(q = True, maxTime = True))

		iCurrent = cmds.currentTime(q = True)

		iFrame = aKeyFrames[0]

		for v in aKeyFrames[:]:
			if v >= iCurrent:
				aKeyFrames.remove(v)
		if aKeyFrames:
			iFrame = aKeyFrames[-1]


		cmds.undoInfo(swf = 0)
		cmds.currentTime(iFrame)
		GreenTickKeys()
		cmds.undoInfo(swf = 1)


def HotKey_NextGreenKey():
	oKeyPoseFrames = 'KeyPoseFrames'
	aKeyFrames= []
	if cmds.objExists(oKeyPoseFrames):
		for i in range(cmds.keyframe(oKeyPoseFrames+'.tx', kc = True, q = True)):
			aKeyFrames.extend(cmds.keyframe(oKeyPoseFrames+'.tx', index = (i,i), q = True))

		iIn = int(cmds.playbackOptions(q = True, minTime = True))
		iOut = int(cmds.playbackOptions(q = True, maxTime = True))

		iCurrent = cmds.currentTime(q = True)

		iFrame = aKeyFrames[-1]

		for v in aKeyFrames[:]:
			if v <= iCurrent:
				aKeyFrames.remove(v)
		if aKeyFrames:
			iFrame = aKeyFrames[0]



		cmds.undoInfo(swf = 0)
		cmds.currentTime(iFrame)
		GreenTickKeys()
		cmds.undoInfo(swf = 1)


def HotKey_PanePoP():
	mel.eval('panePop;')

def HotKey_AttrIncrement_n01():
	ATT_INCREMENT(-0.1)
	DisplayFaceValues()

def HotKey_ToggleVisCurves():
	print 'test'
	# Toggle nurbsCurve in modelPanel4 (top Left)
	bSwitch = cmds.modelEditor('modelPanel4', q = True, nurbsCurves = True)
	print bSwitch
	#bSwitch = bSwitch * -1 +1
	bSwitch = False == bSwitch
	print bSwitch

	cmds.modelEditor('modelPanel4', e = True, nurbsCurves = bSwitch, handles = bSwitch, locators = bSwitch)
	cmds.modelEditor('modelPanel1', e = True, nurbsCurves = bSwitch, handles = bSwitch, locators = bSwitch)

	### Toggle vis atlas Lights vvv 1/2
	def walk(parent):
		for child in parent.getChildElements():
			yield child
			for ch in walk(child):
				yield ch

	ws = rb.Workspace.getShared()
	for child in walk(ws):
		if 'IBL' in child.name:
			child.visible = False == bSwitch
	### end

	aLight = ['all', 'default']
	cmds.modelEditor('modelPanel4', e = True, dl = aLight[bSwitch])
	#cmds.modelEditor('modelPanel1', e = True, dl = aLight[bSwitch])



def HotKey_PreviousFrame():
	# Need to revise here. need to clean.
	# [Hot Key] Alt_f_PrevFrame v2.0.1
	def PlotOne():
		oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
		iIn = int(cmds.textField('Start' , q = True, tx =True))
		iOut = int(cmds.textField('End' , q = True, tx =True))

		iCurrent = cmds.currentTime(q = True)

		if iOut > iCurrent > iIn:
			sName = 'frame_%s_'%str(int(iCurrent)).zfill(3)
			if not cmds.objExists(sName):
				cmds.sphere(n = sName, r = .5,  d = 3)
				#cmds.spaceLocator(n = sName)
				##
				cmds.parent(sName, oFrames )
			oCurrentFrame = 'CurrentFrame'
			cmds.parentConstraint(oCurrentFrame, sName, n = 'Temp_Par', mo = False)
			cmds.delete('Temp_Par')

			# Change Null Size
			aScale = NullSize(100)
			cmds.setAttr( "%s.scale"%sName, *aScale )

			iColour = cmds.getAttr('CameraGhost.CamGhostColour')
			cmds.sets(sName,  fe = 'CamGhost_%s_SDR'%iColour , e = True)

		else:
			cmds.warning( 'Ghost not created.' )
		cmds.select(oSel)



		if cmds.checkBox('NextFrameCreation', ex = True):
			if cmds.checkBox('NextFrameCreation', q = True, v = True):
				pass
				# PlotOne()

	cmds.undoInfo(swf = 0)
	cmds.currentTime(cmds.currentTime(q = True) - 1)
	GreenTickKeys()
	cmds.undoInfo(swf = 1)
	DisplayFaceValues()


def HotKey_SelectAll_P():

	mel.eval('buildSelectAllMM')
def HotKey_SelectAll_R():
	mel.eval('buildSelectAllMM_release')


def HotKey_PreviousKey():
	# PrevKey v2.0.1
	cmds.undoInfo(swf = 0)
	cmds.currentTime(cmds.findKeyframe(timeSlider = True, which = 'previous'))
	GreenTickKeys()
	cmds.undoInfo(swf = 1)
	DisplayFaceValues()


def HotKey_SetKey():
	mel.eval('performSetKeyframeArgList 1 {"0", "animationList"}')
	GreenTickKeys(1)



def HotKey_NextKey():
	# NextKey v2.0.1
	cmds.undoInfo(swf = 0)
	cmds.currentTime(cmds.findKeyframe(timeSlider = True, which = 'next'))
	GreenTickKeys()
	cmds.undoInfo(swf = 1)
	DisplayFaceValues()


def HotKey_Playback_P():
	mel.eval('togglePlayback')
def HotKey_Playback_R():
	mel.eval('togglePlayback')



def HotKey_PlayBlastTool():
	import sys; p = sScriptPath
	if p not in sys.path: sys.path.append(p)
	import PlayBlastTool
	#reload(PlayBlastTool)
	PlayBlastTool.main()

def I_ALT_P():
	if 'graphEditor' in cmds.getPanel(wf = True):
		# Jason's elastic tool. (fcurve peak scale tool)
		print 'test'
		__import__('imp').load_source("_", "/weta/prod/motion/work/jdixon/python/scaler.py").main()
	else:
		# Weta zeus window
		from ShotsToolbar import zeus_window; zeus_window.main(workflows=["lighting"])

def I_N_P():
		if 'graphEditor' in cmds.getPanel(wf = True):
			mel.eval('setToolTo regionSelectKeySuperContext;')
		else:
			pass
def I_N_R():
	pass

def K_N_P():
	oPanel = cmds.getPanel(wf = True)

	if 'graphEditor' in oPanel:
		mel.eval('storeLastAction( "restoreLastContext " + `currentCtx`);setToolTo TimeDragger')

	else:
		import AttrTool
		reload(AttrTool)
		AttrTool.main()


def K_N_R():
	oPanel = cmds.getPanel(wf = True)

	if 'graphEditor' in oPanel:
		mel.eval('invokeLastAction')

	else:
		pass
		#print 'else tool',
def HotKey_NextFrame():
	# Need to revise. optimize this part
	# Next Frame v2.0.1

	def PlotOne():
		oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
		iIn = int(cmds.textField('Start' , q = True, tx =True))
		iOut = int(cmds.textField('End' , q = True, tx =True))
		iCurrent = cmds.currentTime(q = True)
		if iOut > iCurrent > iIn:
			sName = 'frame_%s_'%str(int(iCurrent)).zfill(3)
			if not cmds.objExists(sName):
				cmds.sphere(n = sName, r = .5,  d = 3)
				#cmds.spaceLocator(n = sName)
				##
				cmds.parent(sName, oFrames )
			oCurrentFrame = 'CurrentFrame'
			cmds.parentConstraint(oCurrentFrame, sName, n = 'Temp_Par', mo = False)
			cmds.delete('Temp_Par')
			# Change Null Size
			aScale = NullSize(100)
			cmds.setAttr( "%s.scale"%sName, *aScale )
			iColour = cmds.getAttr('CameraGhost.CamGhostColour')
			cmds.sets(sName,  fe = 'CamGhost_%s_SDR'%iColour , e = True)
		else:
			cmds.warning( 'Ghost not created.' )
		cmds.select(oSel)
	cmds.undoInfo(swf = 0)
	cmds.currentTime(cmds.currentTime(q = True) +1 )
	GreenTickKeys()
	cmds.undoInfo(swf = 1)
	DisplayFaceValues()



def HotKey_Focus():
	mel.eval('fitPanel -selectedNoChildren')
	#mel.eval('fitPanel -selected')

	# or

	'''sBox = 'Focus_BoundingBox'
	oObj = [str(o) for o in cmds.ls(sl = True, o = True)]
	aBoundingBox = [round(b, 4) for b in cmds.xform(oObj[-1], q = True, bb =True)]

	# Create a boundin box according to the seleciton.
	cmds.polyCube(n = sBox)
	aList = [   [0,1,5,0],
				[3,1,5,1],
				[0,4,5,2],
				[3,4,5,3],
				[0,4,2,4],
				[3,4,2,5],
				[0,1,2,6],
				[3,1,2,7],]
	for a in aList:
		cmds.move(aBoundingBox[a[0]], aBoundingBox[a[1]], aBoundingBox[a[2]], '%s.vtx[%s]'%(sBox, a[3]), a = True, ws = True)

	oCamera =''
	oPanel = cmds.getPanel(wf = True)

	if 'modelPanel' in oPanel:
		oCamera = cmds.modelEditor(oPanel, q = True, camera = True)

	cmds.viewFit(oCamera)

	if cmds.objExists(sBox):
		cmds.delete(sBox)

	cmds.select(oObj, r = True)'''



def HotKey_SetUI():

	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]

	# Timeline setting : Display Key Ticks to : 'selected'
	oPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
	cmds.timeControl(oPlayBackSlider, edit = True, animLayerFilterOptions = 'selected')

	# ANIM camera creation
	iRecreateAnimCam = 0 # 1 = Re-create ANIM_CAM everytime. 0 = Only create when there is no cam.
	sCamName = 'ANIM_CAM'
	if iRecreateAnimCam:
		aList = ['focalLength', 'focusDistance', 'centerOfInterest', 'locatorScale', 'nearClipPlane', 'farClipPlane']

		aTransform = []
		aAttr = []
		if cmds.objExists(sCamName):
			aTransform.append(cmds.xform(sCamName, q = True, ws = True, t = True))
			aTransform.append(cmds.xform(sCamName, q = True, ws = True, ro = True))
			for a in aList:
				aAttr.append(cmds.getAttr('%sShape.%s'%(sCamName,a)))
			cmds.delete(sCamName)

		oCamera = cmds.camera()
		cmds.rename(oCamera[0], '%s'%sCamName)

		if aTransform:
			cmds.xform(sCamName, ws = True, t = aTransform[0])
			cmds.xform(sCamName, ws = True, ro = aTransform[1])

			for i, v in enumerate(aAttr):
				cmds.setAttr('%sShape.%s'%(sCamName,aList[i]),v)
	else:
		if not cmds.objExists(sCamName):
			oCamera = cmds.camera()
			cmds.rename(oCamera[0], '%s'%sCamName)


	# Visibility Layer creation
	aLayer = ['Hidden', 'NonSelect']
	aLayerSetting = [	[28,2,False, True],
						[28,2,True, False],]
	for i, a in enumerate(aLayer):
		if not cmds.objExists(a):
			cmds.createDisplayLayer(e = True, name = a)
			for v, s in enumerate(['color', 'displayType', 'visibility', 'hideOnPlayback']):
				cmds.setAttr('%s.%s'%(aLayer[i], s),aLayerSetting[i][v])


	# Set panel to custom.
	mel.eval('setNamedPanelLayout "Custom_Anim";')


	# CUSTOM TOOL - project based
	ProjectCustom_SetUI() # Custom tool for this proj

	# Selection - Back to what was selected first.
	cmds.select(oSel, r = True)

def ProjectCustom_SetUI(): # vvv 2/3 # Completely Custom tool for current proj.

	sSideCamera = 'SIDE_CAM'
	if not cmds.objExists(sSideCamera):
		oSideCamera = cmds.camera()
		cmds.rename(oSideCamera[0], '%s'%sSideCamera)



	oSel = [str(s) for s in cmds.ls(sl = True, o = True)]

	# Creation of  SideCam
	sSideCamera = 'SIDE_CAM'
	if not cmds.objExists(sSideCamera):
		oSideCamera = cmds.camera()
		cmds.rename(oSideCamera[0], '%s'%sSideCamera)


	# Scene Storage. StudioSetting.SceneInfoStorage()
	dSceneInfo = {	'CustomCamViews':0,
				'CustomCamViewList':[]}

	# Node Structure Creation
	aGroup = [	'lllllllllllllllll__CAMERAs__lllllllllllllllll',
				'CardRig___',
				'SideCam___',
				'FaceCam___',
				'RenderCam___',
				'lllllllllllllllll__Main_Puppet__lllllllllllll',
				'lllllllllllllllll__Sub_Puppet__llllllllllllll',
				'lllllllllllllllll__Lights__llllllllllllllllll'] # Do not change the list order. Possible to add more.
	cmds.select(clear = True)

	iError = 0

	# Parent Nodes
	for g in aGroup:
		if not cmds.objExists(g):
			if '___' in g: cmds.group( em = True, name = g, p = aGroup[0])
			else: cmds.group( em = True, name = g)
			if g == aGroup[0]:
				cmds.addAttr(aGroup[0], shortName = 'notes', dataType = 'string') # Activate Notes Attributes to store json
				StudioSettings.SceneInfoStorage(aGroup[0], dSceneInfo) # Store dSceneInfo
		if 'lllll' in g:
			vColour = UIColourControl.keywordColour('MayaBG')
			vColour = UIColourControl.offsetRGBvalues(vColour, R = 0.3, G = 0.3, B = 0.3)
			for i, v in enumerate('RGB'): 
				cmds.setAttr('%s.useOutlinerColor'%g, True)
				cmds.setAttr('%s.outlinerColor%s'%(g, v), vColour[i])


	## Logic to find available cameras. (find children for camera)
	dSceneInfo = StudioSettings.SceneInfoStorage(aGroup[0]) # Get dSceneInfo

	dSceneInfo['CustomCamViewList']  = []
	for cam in aGroup[2:5]: # Using aGroup[2 to 4]
		if cmds.listRelatives(cam, c = True, ad = True, type = 'camera'):
			dSceneInfo['CustomCamViewList'].append(cam)

	dSceneInfo = StudioSettings.SceneInfoStorage(aGroup[0], dSceneInfo) # Store dSceneInfo (update)
	print dSceneInfo


	# Find Next Camera to Display

	if len(dSceneInfo['CustomCamViewList']) == 0: # If no camera is found. (not sorted under cam groups)
		iError = 1 # No camera found.
		aPrint = UIColourControl.inViewMessageColourPreset('Red', 'No Cameras found')
		iIndex = 0

	elif dSceneInfo['CustomCamViews'] >= len(dSceneInfo['CustomCamViewList'])-1:
		iIndex = 0
	else:
		iIndex = dSceneInfo['CustomCamViews'] + 1


	if not iError: # If cameras are found...
		sCamera = dSceneInfo['CustomCamViewList'][iIndex]
		aCamera = cmds.listRelatives(sCamera, c = True, ad = True, type = 'camera')

		if sCamera == aGroup[4]:
			aPrint = UIColourControl.inViewMessageColourPreset('Green', 'RENDER cam')
			aVis = [1, 1, 0, 0, 1, None, None, 1]
			aCamKeyword = ['Left', 'render', 'legalCam']
		elif sCamera == aGroup[3]:
			aPrint = UIColourControl.inViewMessageColourPreset('Blue',  ' FACE cam ')
			aVis = [1, 0, 0, 1, 0, None, None, 0]
			aCamKeyword = ['Shape1', 'FACE']
		elif sCamera == aGroup[2]:
			aPrint = UIColourControl.inViewMessageColourPreset('Gray',  ' SIDE cam ')
			aVis = [1, 0, 1, 0, 1, None, None, 1]
			aCamKeyword = ['SIDE_CAM']

		# Hide unnecessary Groups of camera.
		for i, v in enumerate(aVis):
			if not v == None:
				cmds.setAttr('%s.visibility'%aGroup[i], v)


		# Pick camera of the first match in the keyword.
		sCamera = None
		sTCamera = None # This is needed if keyword search fails. (Just to have something selected.)
		for c in aCamera:
			sCamera = c
			for k in aCamKeyword:
				if k in c:
					sTCamera = c
					break
		if sTCamera:
			sCamera = sCamera
		if sCamera:
			cmds.modelEditor('modelPanel4', e = True, camera = sCamera)
		cmds.modelEditor('modelPanel1', e = True, camera = 'ANIM_CAM', activeView = True)


	# Print Statement
	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 10, ft = 'arial',bkc = aPrint[2] )

	# Store Scene Info.
	dSceneInfo['CustomCamViews'] = iIndex
	StudioSettings.SceneInfoStorage(aGroup[0], dSceneInfo) # Store dSceneInfo

	cmds.select(oSel, r = True)


def HotKey_AttrIncrement_p001():
	ATT_INCREMENT(0.01)
	DisplayFaceValues()
	GreenTickKeys()

def HotKey_Paste():
	mel.eval('cutCopyPaste "paste"')


def HotKey_AttrIncrement_p01():
	ATT_INCREMENT(0.1)
	DisplayFaceValues()
	GreenTickKeys()
def HotKey_Copy():
	mel.eval('cutCopyPaste "copy"')


def HotKey_SelectTool_P():
	mel.eval('buildSelectMM')
def HotKey_SelectTool_R():
	mel.eval('MarkingMenuPopDown')


def HotKey_MoveTool_P():
	mel.eval('buildTranslateMM')
def HotKey_MoveTool_R():
	mel.eval('destroySTRSMarkingMenu MoveTool')


def HotKey_AxisSwitcher():
	# AxisSwitcher v2.1.0

	oPanel = cmds.getPanel(wf = True)
	if 'modelPanel' in oPanel: # if a viewport is acitve (Not graphEditor1/etc)
		oCamera = cmds.modelPanel(oPanel, query=True, camera=True).replace('Shape', '')


		iVal = cmds.manipMoveContext('Move', q = True, mode = True)

	if iVal == 1:
		cmds.manipMoveContext('Move', e = True, mode = 2)
		cmds.manipRotateContext('Rotate', e = True, mode = 1)
		aPrint = ['6bad64', 'WORLD', 0x6c756b] # Green
	elif iVal == 2:
		cmds.manipMoveContext('Move', e = True, mode = 0)
		cmds.manipRotateContext('Rotate', e = True, mode = 0)
		aPrint = ['d8766c', 'OBJECT', 0x756b6b] # Red
	elif iVal == 0:
		# Camera space Manipultor
		aCoordinate = cmds.xform(oCamera, q = True, a = True, ws = True, t = True)

		cmds.manipMoveContext('Move', e = True, mode = 6, activeHandle = 0, orientTowards = aCoordinate)
		cmds.manipRotateContext('Rotate', e = True, mode = 3)
		aPrint = ['9bbcf2', 'CAMERA', 0x485872] # Blue
	else:
		cmds.manipMoveContext('Move', e = True, mode = 1)
		cmds.manipRotateContext('Rotate', e = True, mode = 2)
		aPrint = ['a7a8af', 'LOCAL ', 0x6b6c75] # Gray

	cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def HotKey_ScaleTool_P():
	mel.eval('buildScaleMM')
def HotKey_ScaleTool_R():
	mel.eval('destroySTRSMarkingMenu ScaleTool')


def HotKey_AttrIncrement_n001():
	ATT_INCREMENT(-0.01)
	DisplayFaceValues()
	GreenTickKeys()
def HotKey_Undo():
	cmds.undo()


def HotKey_BreakConnections():
	# Break Connection of Selected Attributes v3.0.0
	oChannel = [str(c+'.'+cmds.attributeName(c+'.'+b, l=True)) for a in 'msho' for b in cmds.channelBox('mainChannelBox', **{'q':True, 's%sa'%a:True}) or [] for c in cmds.channelBox('mainChannelBox', q = True, **{'%sol'%a:True})]

	for c in oChannel:
		aObj = c.split('.')
		cmds.delete(aObj[0], at = aObj[1], c = True)


def HotKey_RotationTool_P():
	mel.eval('buildRotateMM')
def HotKey_RotationTool_R():
	mel.eval('destroySTRSMarkingMenu RotateTool')
