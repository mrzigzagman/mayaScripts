# Camera Ghosting Tool v015 Wip 012
# comment out ColourOverride


# To Be Done
'''
#- Set Target button - reset offset on ghost null
#- Checkbox / Move frame creates a ghost.
#- Button, Change colour to all black
#- Set Colour. create null with that colour
#- All in Nurbs Surface
#- Not able to create ghost after timeline zone
- Test Region tools.
# - Size - Ctl and not - reverse it.
#- Able to plot in Orthographic views.
'''



import maya.cmds as cmds
import maya.mel as mel
from functools import partial




### Global Variables

# Main UI Var
oUI = 'CameraGhostingUI'

# Rig Elements
oColourUI = 'ColourPicker'
oAnimTools   = 'ANIM_TOOLS'
oCameraGhost = 'CameraGhost'
oCameraConst = 'CameraConst'
oFrames = 'Frames'
oFrameZero = 'FrameZero'
oTarget = 'TargetFollow'
oTargetOffset = 'TargetFollowOffset'
oUpV = 'UpV'
oDirConst = 'DirConst'
oCurrentFrame = 'CurrentFrame'
oOrthoFrames = 'OrthoAdjFrames'
oOrthoCursor = 'OrthoAdjCursor'





sAimConst	= 'TargetAim_Const'
sCamConst = 'CameraFollow_Const'
sTargetConst = 'TargetFollow_Const'
sOrthoConst = 'Ortho_PointConst'
sCameraGhost = 'CameraGhost'

# Used for Storage as attributes on 'Anim_Tools' Null
aInfoStorage = [
'CamGhostCamera',
'CamGhostCamShape',
'CamGhostTarget',
'CamGhostDepth',
'CamGhostSize',
'CamGhostStart',
'CamGhostEnd',
'CamGhostInc',
'CamGhostColour',]

# In/Out
iIn = int(cmds.playbackOptions(q = True, minTime = True))
iOut = int(cmds.playbackOptions(q = True, maxTime = True))

# Colour

aColourList = [	[22 ,[1.0 , 1.0 , 0.39]],
	[18 ,[ 0.39 , 0.86 , 1.0 ]],
	[19 ,[ 0.26 , 1.0 , 0.64 ]],
	[20 ,[ 1.0 , 0.69 , 0.69 ]],
	[28 ,[ 0.19 , 0.63 , 0.63 ]],
	[21 ,[ 0.89 , 0.67 , 0.47 ]],
	[26 ,[ 0.41 , 0.63 , 0.19 ]],
	[23 ,[ 0 , 0.6 , 0.33 ]],
	[13 ,[ 1.0 , 0 , 0 ]],
	[14 ,[ 0 , 1.0 , 0 ]],
	[00 ,[ 0 , 0 , 0 ]],   ]

### Class Assignment###

class CreateUI:

	def __init__(self):
		### Pre-Setup ###
		self.Width  = 400	# Total  Width of Window in pixel
		self.Height = 200	# Total Height of Window in pixel

		self.iBoarderW = 10  # Default Empty Pixels around window for Width
		self.iBoarderH = 10  # Default Empty Pixels around window for Height



		### Initial Setup ###

		# Delete UI if exists.
		if cmds.window(oUI, exists=True):
			cmds.deleteUI(oUI, window=True)

		# Create Window as formLayout
		self.oWindow = cmds.window(oUI, w = self.Width, h = self.Height, mnb = False, mxb = False, title = oUI, sizeable = False)
		self.oForm = cmds.formLayout()

		self.Div = [] # [  [iP, iP, iP, iP] ,  iGapBetweenCells, iHeightBetweenRows]
		self.Row = [] # Stores All creation for window separated by rows.


	def AddRow(self, Entry):
		self.Row.append([Entry, self.Div[1], self.Div[2]])


	def Division(self, aList, iGap = None, iVerticalSpace = None):

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
		for l in range (len(aList)):
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


	def Create(self):
		'''

		Takes the entered oAnyVar.Row info to Create the UI.
		'''
		# Logic #
		aAP = []
		aAC = []
		for r in range(len(self.Row)):
			for i in range(len(self.Row[r][0])):
				if r == 0:
					if i == 0:
						aAP.append( (self.Row[r][0][i], 'top' , self.iBoarderH, 0)  )
						aAP.append( (self.Row[r][0][i], 'left', self.iBoarderW, 0)  )

					else:
						aAP.append( (self.Row[r][0][i], 'top' , self.iBoarderH, 0)  )
						aAC.append( (self.Row[r][0][i], 'left', self.Row[r][1], self.Row[r][0][i-1]) )


				else:
					if i == 0:
						aAC.append( (self.Row[r][0][i], 'top' , self.Row[r][2], self.Row[r-1][0][0]) )
						aAP.append( (self.Row[r][0][i], 'left', self.iBoarderW, 0) )

					else:
						aAC.append( (self.Row[r][0][i], 'top' , self.Row[r][2], self.Row[r-1][0][0]) )
						aAC.append( (self.Row[r][0][i], 'left', self.Row[r][1], self.Row[r][0][i-1]) )

		cmds.formLayout(self.oForm, edit = True, attachPosition = aAP)

		if aAC:
			cmds.formLayout(self.oForm, edit = True, attachControl = aAC)

		cmds.showWindow( self.oWindow )




### General Function ###

def ListSelection():
	'''
	List section into an array of strings
	'''
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	return oSel

def MessageBox(Message):
	'''
	Displaying Entered Message as Popup
	'''
	window = cmds.window(title = 'Message Box')
	cmds.columnLayout(adjustableColumn = True, )
	cmds.text('\n\t%s\t\n' % Message)
	cmds.button(label = 'Close', command = ('cmds.deleteUI(\"'+window+'\",window = True)'))
	cmds.setParent('..')
	cmds.showWindow(window)


# Speed up Bake
def makeHiddenLayout(name):

	# store a temporary panel configuration.
	layout = cmds.panelConfiguration(l=name, sc=0)
	evalStr = 'updatePanelLayoutFromCurrent "'+name+'"'
	mel.eval(evalStr)

	# switch to fast "hidden" layout
	evalStr = 'setNamedPanelLayout "Single Perspective View"'
	mel.eval(evalStr)
	perspPane = cmds.getPanel(vis=1)
	cmds.scriptedPanel('graphEditor1',e=1,rp=perspPane[0])
	return name

def restoreLayout(name):
	# restore the layout returned from makeHiddenLayout.
	evalStr = 'setNamedPanelLayout "'+name+'"'
	mel.eval(evalStr)
	# now delete the old layout.
	killMe = cmds.getPanel(cwl=name)
	cmds.deleteUI(killMe,pc=1)





### Storage Functions ###

def StoreInfo(*args):
	'''
	Get Info on UI and store on oCameraGhost attributes
	'''
	if cmds.objExists(oCameraGhost):

		# Get Info if Exists.
		if cmds.objExists(oCameraGhost):
			sCameraVal   = cmds.textField('SelectedCamera'  , q = True, tx =True)
			sCamShapeVal = cmds.textField('SelectedCamShape', q = True, tx =True)
			sTargetVal   = cmds.textField('SelectedTarget'  , q = True, tx =True)

			sDepthVal   	= cmds.textField('Depth'   	, q = True, tx =True)
			sSizeVal    	= cmds.textField('Size'    	, q = True, tx =True)
			sStartVal   	= cmds.textField('Start'   	, q = True, tx =True)
			sEndVal     	= cmds.textField('End'     	, q = True, tx =True)


			# Store Info
			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[0], sCameraVal   , typ = 'string')
			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[1], sCamShapeVal , typ = 'string')
			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[2], sTargetVal   , typ = 'string')

			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[3], sDepthVal	, typ = 'string')

			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[4], sSizeVal 	, typ = 'string')
			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[5], sStartVal	, typ = 'string')
			cmds.setAttr(oCameraGhost+'.'+aInfoStorage[6], sEndVal  	, typ = 'string')

def ApplyInfo():
	'''
	Get Info from oCameraGhost attributes and store on UI boxes
	'''
	# Get Info if Exists.
	if cmds.objExists(oCameraGhost+'.'+aInfoStorage[0]):
		# Get From
		sCameraVal	= cmds.getAttr(oCameraGhost+'.'+aInfoStorage[0])
		sCamShapeVal  = cmds.getAttr(oCameraGhost+'.'+aInfoStorage[1])
		sTargetVal	= cmds.getAttr(oCameraGhost+'.'+aInfoStorage[2])

		sDepthVal 	= cmds.getAttr(oCameraGhost+'.'+aInfoStorage[3])
		sSizeVal  	= cmds.getAttr(oCameraGhost+'.'+aInfoStorage[4])
		sStartVal 	= cmds.getAttr(oCameraGhost+'.'+aInfoStorage[5])
		sEndVal   	= cmds.getAttr(oCameraGhost+'.'+aInfoStorage[6])

		# Store Info
		cmds.textField('SelectedCamera'  , tx = sCameraVal  , e = True)
		cmds.textField('SelectedCamShape', tx = sCamShapeVal, e = True)
		cmds.textField('SelectedTarget'  , tx = sTargetVal  , e = True)

		cmds.textField('Depth'	, tx = sDepthVal	, e = True)
		cmds.textField('Size' 	, tx = sSizeVal 	, e = True)
		cmds.textField('Start'	, tx = sStartVal	, e = True)
		cmds.textField('End'  	, tx = sEndVal  	, e = True)


def AddInfo():
	'''
	Creates Extra attributes on oCameraGhost
	'''
	if not cmds.objExists(oCameraGhost+'.'+aInfoStorage[0]):
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[0], dt = "string")
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[1], dt = "string")
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[2], dt = "string")

		cmds.addAttr(oCameraGhost, ln = aInfoStorage[3], dt = "string")
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[4], dt = "string")

		cmds.addAttr(oCameraGhost, ln = aInfoStorage[5], dt = "string")
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[6], dt = "string")
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[7], dt = "string")
		cmds.addAttr(oCameraGhost, ln = aInfoStorage[8], dt = "string")

def DefaultInfo():
	'''
	Sets the Default Values on oCameraGhost. ApplyInfo() Left out on purpose.
	'''

	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[0], ' - '  , typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[1], ' - ', typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[2], ' - '  , typ = 'string')

	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[3], '5'	, typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[4], '5' 	, typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[5], str(iIn)	, typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[6], str(iOut)  	, typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[7], '1', typ = 'string')
	cmds.setAttr(oCameraGhost+'.'+aInfoStorage[8], '13', typ = 'string')



### Tool Related Function ###

def getCamera():
	'''
	Get Currently Selected 3D View
	'''
	oCamera = ''
	oPanel = cmds.getPanel(wf = True)

	if 'modelPanel' in oPanel:
		oCamera = cmds.modelEditor(oPanel, q = True, camera = True)

		if not cmds.objExists(oCamera+'tx'):
			if oCamera.endswith('Shape'):
				if cmds.objExists(oCamera[:-5]+'.tx'):
					oCamera = oCamera[:-5]

	return str(oCamera)




def CreateRig():

	CreateShaders()

	cmds.select(cl = True)

	### Create Hierarchy ###
	cmds.group(name = oCameraGhost, em = True, p = oAnimTools)
	cmds.group(name = oOrthoFrames, em = True, p = oCameraGhost)

	cmds.group(name = oOrthoCursor, em = True, p = oCameraGhost)
	cmds.setAttr(oOrthoCursor+ ".scale", *(0.02, 0.02, 0.02) )

	cmds.group(name = oCameraConst, em = True, p = oCameraGhost)

	cmds.group(name = oTarget, em = True, p = oCameraGhost)

	cmds.spaceLocator(name = oTargetOffset)
	cmds.parent(oTargetOffset, oTarget)
	cmds.setAttr(oTargetOffset+'.visibility',0)

	cmds.group(name = oFrames, em = True, p = oCameraConst)
	cmds.setAttr(oFrames+'.scale', *[1, 1, 1])

	cmds.group(name = oUpV, em = True, p = oCameraConst)
	cmds.setAttr('%s.translateY'%oUpV, 60)

	cmds.group(name = oDirConst, em = True, p = oCameraConst)

	cmds.group(name = oFrameZero, em = True, p = oDirConst)
	cmds.setAttr(oFrameZero+'.scale', *[1, 1, 1])

	cmds.torus(n = oCurrentFrame, p = (0, 0, 0) , ax = (0 ,0 ,1), ssw = 0, esw = 360, msw = 360, r = 0.3, hr  = 0.15, d = 3, ut = 0, tol = 0.01, s = 8, nsp = 4, ch = 1)
	cmds.parent(oCurrentFrame, oFrameZero)
	cmds.setAttr(oCurrentFrame+'.scale', *[.5, .5, .5])
	# Apply Default Colour
	cmds.sets(oCurrentFrame,  fe = 'CamGhost_13_SDR' , e = True)


	### Apply Constraints ###
	cmds.aimConstraint(oTargetOffset, oDirConst, n = sAimConst, weight = 1, aimVector =  (0, 0, 1), upVector = (0, 1, 0), worldUpType = "object", worldUpObject = 'UpV')
	cmds.parentConstraint(oCameraGhost, oCameraConst, weight = 1, n = sCamConst)
	cmds.parentConstraint(oCameraGhost, oTarget, n = sTargetConst, weight = 1)
	cmds.pointConstraint(oTargetOffset, oOrthoCursor, n = sOrthoConst, offset =  (0, 0, 0) , weight = 1)


	AddInfo()
	DefaultInfo()

def CreateShaders():
	for colour in aColourList:
		oMaterial = 'CamGhost_%s' % colour[0]
		oShader = oMaterial+'_SDR'
		if not cmds.objExists(oMaterial):
			cmds.shadingNode('lambert', n = oMaterial, asShader = 1, )
			cmds.sets(oMaterial, renderable = True, noSurfaceShader = True, empty = True, name = oShader)
			cmds.connectAttr(oMaterial+'.outColor', oShader+'.surfaceShader', f = True)

			cmds.setAttr( "%s.color"%oMaterial, type = 'double3', *colour[1])
			cmds.setAttr( "%s.incandescence"%oMaterial, type = 'double3', *colour[1])
			cmds.setAttr( "%s.ambientColor"%oMaterial, type = 'double3', *colour[1])


def SetCamera(sCamera, sCamShape):
	iNear = 0
	try:
		iNear = cmds.getAttr("%s.nearClipPlane"%sCamShape)
	except:
		MessageBox( 'Please Manually Find Node with ".nearPlane" attribute.')

	cmds.textField('Depth', e = True, tx = iNear)

	### Set Transform Values ###
	cmds.setAttr("%s.translateZ"%oFrameZero, iNear + 1)
	aNear = [iNear * 0.01, iNear * 0.01, iNear * 0.01]
	cmds.setAttr("%s.scale"%oFrameZero, *aNear)

	### Apply Constraint
	cmds.delete(sCamConst)
	cmds.parentConstraint(sCamera, oCameraConst, weight = 1, n = sCamConst)



def SetTarget(sTarget):
	if cmds.objExists(sTargetConst):
		cmds.delete(sTargetConst)
	cmds.parentConstraint(sTarget, oTarget, n = sTargetConst, weight = 1)

	cmds.setAttr("%s.translate"%oTargetOffset , *[0,0,0] )
	cmds.setAttr("%s.rotate"%oTargetOffset , *[0,0,0] )


def NullSize(val = 10):
	sSizeVal = str(float(cmds.textField('Size', q = True, tx =True)))
	iScale = round(float(sSizeVal)/val,2)
	aScale = [iScale, iScale, iScale]
	return aScale



### Button Functions ###


def Button_CreateRig(*args):
	if cmds.objExists(oAnimTools+'|'+oCameraGhost):
		cmds.delete(oAnimTools+'|'+oCameraGhost)
	CreateRig()
	if cmds.objExists(oAnimTools+'.'+aInfoStorage[0]):
		DefaultInfo()
		ApplyInfo()
	ResetRange()

def FindCamShape(sCamera):
	# From Selected Camera, will try to return 'Shape' Node with NearClipPlane parameter.
	sNearObj = None

	# General Search assignment
	sShape =  sCamera+'Shape'

	# Project-Specific Search assignments
	sAYNIK =  	sCamera.split('_')[0]+'_:camera_:rig_:render_:camera'

	sPaddington = sCamera.split('_')[0]+'_:geo_:rig_:renderCamera_:camera'

	# Search Logic
	if cmds.objExists(sShape+'.nearClipPlane'):
		sNearObj = sShape
	elif cmds.objExists(sAYNIK+'.nearClipPlane'):
		sNearObj = sAYNIK
	elif cmds.objExists(sPaddington+'.nearClipPlane'):
		sNearObj = sPaddington
	else:
		for c in cmds.listRelatives(sCamera):
			if 'Shape' in c:
				if cmds.objExists(c+'.nearClipPlane'):
					sNearObj = c
					break


	# Update info on UI
	if sNearObj:
		cmds.textField('SelectedCamShape', e = True, text = sNearObj)
	else:
		cmds.textField('SelectedCamShape', e = True, text = '-')


	return sNearObj


### Button_Set....







def Button_SetCamera(*args):
	sCamera = getCamera()
	if sCamera:
		cmds.textField('SelectedCamera', e = True, text = sCamera)

		sNearObj = FindCamShape(sCamera)
		SetCamera(sCamera, sNearObj)



		if sNearObj:
			cmds.setAttr('%s.tz'%oFrameZero, float(cmds.getAttr(sNearObj+'.nearClipPlane'))+ 0.1)
			cmds.textField('Depth'	, tx = cmds.getAttr(sNearObj+'.nearClipPlane')+0.1	, e = True)

		sSizeVal = str(float(cmds.textField('Depth'    	, q = True, tx =True)))
		SizeFrameZero(sSizeVal)

		StoreInfo()

		# Variation for Orthographic Camera
		if sCamera in ['front', 'side', 'top']:
			print True
			print str(cmds.listRelatives(oCurrentFrame, p = True))[3:-2]

			if str(cmds.listRelatives(oCurrentFrame, p = True))[3:-2] == oFrameZero:
				cmds.parent(oFrames, oOrthoFrames)
				cmds.setAttr(oFrames+ ".rotate", *(0,0,0))
				cmds.setAttr(oFrames+ ".translate", *(0,0,0))
				cmds.setAttr(oFrames+ ".scale", *(10, 10, 10) )


				cmds.parent(oCurrentFrame, oOrthoCursor)

				cmds.setAttr(oCurrentFrame+ ".rotate", *(0,0,0))
				cmds.setAttr(oCurrentFrame+ ".translate", *(0,0,0))
				cmds.setAttr(oCurrentFrame+ ".scale", *(1, 1, 1) )


		else:
			print False
			if str(cmds.listRelatives(oCurrentFrame, p = True))[3:-2] == oOrthoCursor:
				cmds.parent(oFrames, oCameraConst)
				cmds.setAttr(oFrames+ ".rotate", *(0,0,0))
				cmds.setAttr(oFrames+ ".translate", *(0,0,0))
				cmds.setAttr(oFrames+ ".scale", *(0.02, 0.02, 0.02) )


				cmds.parent(oCurrentFrame, oFrameZero)
				cmds.setAttr(oCurrentFrame+ ".rotate", *(0,0,0))
				cmds.setAttr(oCurrentFrame+ ".translate", *(0,0,0))
				cmds.setAttr(oCurrentFrame+ ".scale", *(1, 1, 1) )


	ApplyInfo()
	StoreInfo()

























def Button_SetCamShape(*args):
	oSel = ListSelection()
	if oSel:
		SetTarget(oSel[0])
		cmds.textField('SelectedCamShape', e = True, text = oSel[0])
		StoreInfo()
		ApplyInfo()


		sSizeVal = str(float(cmds.textField('Depth'    	, q = True, tx =True)))
		SizeFrameZero(sSizeVal)

	StoreInfo()
	ApplyInfo()


def Button_SetTarget(*args):
	oSel = ListSelection()
	if oSel:
		SetTarget(oSel[0])
		cmds.textField('SelectedTarget', e = True, text = oSel[0])
		StoreInfo()
		ApplyInfo()


### Button_Select...
def Button_SelectRoot(*args):
	if cmds.objExists(oCameraGhost):
		cmds.select(oCameraGhost, r = True)


def Button_SelectCamera(*args):
	sCameraVal = cmds.getAttr(oCameraGhost+'.'+aInfoStorage[0])
	if cmds.objExists(sCameraVal):
		cmds.select(sCameraVal, r = True)

	ApplyInfo()

def Button_SelectCamShape(*args):
	sCamShapeVal = cmds.getAttr(oCameraGhost+'.'+aInfoStorage[1])

	if cmds.objExists(sCamShapeVal):
		cmds.select(sCamShapeVal, r = True)

	ApplyInfo()

def Button_SelectTarget(*args):
	sTargetVal = cmds.getAttr(oCameraGhost+'.'+aInfoStorage[2])

	if cmds.objExists(sTargetVal):
		cmds.select(sTargetVal, r = True)

	ApplyInfo()

def Button_SelectAim(*args):

	if cmds.objExists(oTarget):
		cmds.select(oTarget, r = True)


### Button_Plot....
def Button_PlotOneFrame(frame, *args): #
	PlotOne()
	cmds.currentTime(cmds.currentTime(q = True) + frame)

def Button_PlotRange(*args): #
	iCurrent = int(cmds.currentTime(q = True))
	StoreInfo()
	oSel = ListSelection()

	sIn = int(cmds.textField('Start' , q = True, tx =True))
	sOut = int(cmds.textField('End' , q = True, tx =True))
	aRange = [sIn, sOut]


	makeHiddenLayout('tempLayout')
	try:
		for i in range(aRange[0],aRange[1]+1):
			PlotOne()
			cmds.currentTime(i)
	finally:
		restoreLayout('tempLayout')

	if oSel:
		cmds.select(oSel)

def Button_PlotBetKeys(*args): #
	StoreInfo()
	iExecuteTime = int(cmds.currentTime(q = True))

	# Find the key frames between current frame.
	oSel = ListSelection()

	if oSel:
		sIn =  int(cmds.textField('Start' , q = True, tx =True))
		sOut = int(cmds.textField('End'   , q = True, tx =True))

		aFrames = list(set(cmds.keyframe(oSel[0], q = True)))
		aFrames.extend([sIn, sOut])
		aFrames = [int(t) for t in aFrames]
		aFrames = sorted(aFrames)

		iCurrent = int(cmds.currentTime(q = True))

		aRange = [0,0]
		iStart = 0
		iEnd = 0
		if iCurrent in aFrames:
			iIndex = aFrames.index(iCurrent)
			aRange =[aFrames[iIndex-1], aFrames[iIndex+1]]
		else:
			for i in aFrames:
				if i > iCurrent:
					iStart = iEnd
					iEnd = i
					break
				else:

					iStart = iEnd
					iEnd = i
			aRange = [iStart, iEnd]


		# Stert Plotting
		makeHiddenLayout('tempLayout')

		try:
			for i in range(aRange[0],aRange[1]+1):
				PlotOne()
				cmds.currentTime(i)
		finally:
			restoreLayout('tempLayout')

		cmds.select(oSel)
		cmds.currentTime(iExecuteTime)

### Plot Functions
def PlotOne():
	print 'PlotOne'
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	sIn = int(cmds.textField('Start' , q = True, tx =True))
	sOut = int(cmds.textField('End' , q = True, tx =True))

	iCurrent = cmds.currentTime(q = True)

	print sOut
	print iCurrent
	print sIn



	if sOut > iCurrent > sIn:


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


def Button_PlotKey(amount = -1, *args):
	StoreInfo()

	oSel = ListSelection()

	aFrames = list(set(cmds.keyframe(oSel[0], q = True)))
	aFrames.extend([iIn, iOut])
	aFrames = [int(t) for t in aFrames]
	aFrames = sorted(aFrames)

	iCurrent = int(cmds.currentTime(q = True))

	if amount == 1:
		aRange = [iCurrent,iCurrent+1]
	else:
		aRange = [iCurrent - 1, iCurrent]

	for i in aFrames:
		if i > iCurrent:
			aRange[1] = i
			break

		else:
			if amount == -1:
				aRange[0] = i

	makeHiddenLayout('tempLayout')
	try:
		for i in range(aRange[0],aRange[1]+1):
			PlotOne()
			cmds.currentTime(i)
	finally:
		restoreLayout('tempLayout')

	cmds.select(oSel)





### Misc Buttons
def Button_Size(amount = -1 , *args): #
	K = cmds.getModifiers()

	if K == 0:
		iInc = 0.1 * amount
	else:
		iInc = 1.0 * amount
	print iInc
	iSizeVal = float(cmds.textField('Size', q = True, tx =True)) + iInc
	if iSizeVal < 0:
		iSizeVal = 0.1
	sSizeVal = str(iSizeVal)


	cmds.textField('Size', tx = sSizeVal , e = True)

	# Change Circle Size
	aScale = NullSize()
	cmds.setAttr('CurrentFrame.scale',*aScale)

	# Change Null Size
	aScale = NullSize(100)
	if cmds.objExists("Frames|frame_*_"):
		cmds.select("Frames|frame_*_", r = True)
	else:
		cmds.select(cl = True)

	oNulls = cmds.ls(sl = True)
	if oNulls:
		for o in oNulls:
			cmds.setAttr('%s.scale'%o, *aScale)

	cmds.select(cl = True)
	StoreInfo()
	ApplyInfo()



def Button_Near(amount = -1 , *args): #
	ApplyInfo()
	K = cmds.getModifiers()

	if K == 4:
		iInc = 0.1
	else:
		iInc = 1.0

	iSizeVal = float(cmds.textField('Depth'    	, q = True, tx =True)) + amount
	if iSizeVal < 0:
		iSizeVal = 0.1
	sSizeVal = str(round(iSizeVal,2))

	SizeFrameZero(sSizeVal)
	StoreInfo()


def SizeFrameZero(sSizeVal):
	cmds.textField('Depth' 	, tx = sSizeVal 	, e = True)
	cmds.setAttr('%s.tz'%oFrameZero, float(sSizeVal))

	iScale = float(sSizeVal)/100
	aScale = [iScale, iScale, iScale]
	cmds.setAttr('%s.scale'%oFrameZero, *aScale)
	cmds.setAttr('Frames.scale', *aScale)


def Button_SelectGhost(*args): #
	oObj = 'TargetFollowOffset'
	if cmds.objExists(oObj):

		cmds.select(oObj, r = True)
	StoreInfo()


def Button_ResetRange(*args): #
	ResetRange()
def ResetRange():
	iIn = int(cmds.playbackOptions(q = True, minTime = True))
	iOut = int(cmds.playbackOptions(q = True, maxTime = True))
	cmds.textField('Start'	, tx = iIn	, e = True)
	cmds.textField('End'  	, tx = iOut  	, e = True)

	StoreInfo()


def Button_ToggleVis(*args): #
	try:
		cmds.select("Frames|frame_*_")
		oNulls = cmds.ls(sl = True)

		if cmds.getAttr('%s.visibility'%oNulls[0]): iVis = 0
		else: iVis = 1

		for o in oNulls:  cmds.setAttr( "%s.visibility" % o, iVis)

		cmds.select(cl = True)
	except:
		pass

def Button_DeleteNulls(*args): #
	try:
		cmds.delete('Frames|frame_*_')
	except:
		pass



## Colour
def Button_Black(*args): #
	for oChild in cmds.listRelatives('Frames', c = True):
		cmds.sets(oChild,  fe = 'CamGhost_0_SDR' , e = True)

def Button_Colour(sNum, *args): #
	cmds.setAttr('CameraGhost.CamGhostColour', sNum, type = 'string')


def main():
	###################
	### Pre Execute ###
	if not cmds.objExists(oAnimTools):
		cmds.group(name = oAnimTools, em = True)

	if cmds.objExists(oAnimTools+'|'+oCameraGhost) == False:
		CreateRig()


	### Execute ###

	oCamGhost = CreateUI()  # Assigning class to a var.


	### Layout ###

	oColour1  = ( 0.8, 0.8, 0.8 )
	oColour2  = ( 0.5, 0.5, 0.5 )
	oColourBG = ( 0.3, 0.3, 0.3 )
	oColour3  = ( 0.2, 0.2, 0.2 )


	## Row 1
	oCamGhost.Division([10,1,1,1,1,1,1,1,1,1,1],None, 0)
	iHeight = 20
	aRow1 = [cmds.button(l = 'Re-Generate Structure', w = oCamGhost.Div[0][0], h = iHeight, command = Button_CreateRig, bgc = (0.2, 0.2, 0.2), enableBackground = False)]

	for colour in aColourList[:-1]:
		aRow1.append(cmds.button(l = colour[0], w = oCamGhost.Div[0][1], h = iHeight, command = partial(Button_Colour, colour[0]), bgc = colour[1], enableBackground = False))

	oCamGhost.AddRow(aRow1)



	## Row 2
	oCamGhost.Division([5,3,15,1,3,3,3], None ,5)
	iHeight = 20
	aRow2 = [
	cmds.button(l = 'Set Cam'  	, h = iHeight, w = oCamGhost.Div[0][0] , bgc = (0.8, 0.4, 0.4), command = Button_SetCamera, enableBackground = False),
	cmds.button(l = 'Select'   	, h = iHeight, w = oCamGhost.Div[0][1] , command = Button_SelectCamera, bgc = oColourBG ,enableBackground = False),
	cmds.textField('SelectedCamera', h = iHeight, w = oCamGhost.Div[0][2] , text = 'Camera01_:camera_:rig_:render_:cameraLeft',ed = False, bgc = oColour3, enableBackground = False),
	cmds.text(label = ' ' , h = iHeight, w = oCamGhost.Div[0][3] ),
	cmds.button(l = 'Reset'	, h = iHeight, w = oCamGhost.Div[0][4], command = Button_ResetRange, bgc = oColour1 ,enableBackground = False),
	cmds.textField('Start'       	, h = iHeight, w = oCamGhost.Div[0][5] , text = '0', bgc = oColour1, enableBackground = False),
	cmds.textField('End'         	, h = iHeight, w = oCamGhost.Div[0][6] , text = '0', bgc = oColour1, enableBackground = False),
	]
	oCamGhost.AddRow(aRow2)



	## Row 3

	aRow3 = [

	cmds.button(l = 'SetShape'   , h = iHeight, w = oCamGhost.Div[0][0]  , command = Button_SetCamShape, bgc = oColourBG ,enableBackground = False) ,
	cmds.button(l = 'Select'   	, h = iHeight, w = oCamGhost.Div[0][1] , command = Button_SelectCamShape, bgc = oColourBG ,enableBackground = False),
	cmds.textField('SelectedCamShape', h = iHeight, w = oCamGhost.Div[0][2]  , text = ' - ', ed = False),
	cmds.text(label = ' ' , h = iHeight, w = oCamGhost.Div[0][3] ),
	cmds.button(l = 'Ghost', h = iHeight, w = oCamGhost.Div[0][4], command = Button_SelectGhost, bgc = (0.4, 0.4, 0.4 ) ,enableBackground = False),
	cmds.button(l = 'Root'  	, h = iHeight, w = oCamGhost.Div[0][5], command = Button_SelectRoot, bgc = [0.4,0.4, 0.4], enableBackground = False),

	cmds.button(l = 'Aim'  	, h = iHeight, w = oCamGhost.Div[0][6], command = Button_SelectAim, bgc = [0.4,0.4, 0.4], enableBackground = False),
	]
	oCamGhost.AddRow(aRow3)



	## Row 4
	aRow3 = [
	cmds.button(l = 'Set Target'   , h = iHeight, w = oCamGhost.Div[0][0]  , bgc = (0.8, 0.4, 0.4), command = Button_SetTarget, enableBackground = False) ,
	cmds.button(l = 'Select'   	, h = iHeight, w = oCamGhost.Div[0][1]  , command = Button_SelectTarget, bgc = oColourBG ,enableBackground = False),
	cmds.textField('SelectedTarget', h = iHeight, w = oCamGhost.Div[0][2]  , text = ' - ',ed = False, bgc = oColour3, enableBackground = False),
	cmds.text(label = ' ' , h = iHeight, w = oCamGhost.Div[0][3] ),
	cmds.button(l = 'Vis' , h = iHeight , w = oCamGhost.Div[0][4], command = Button_ToggleVis  , bgc = (0.4, 0.4, 0.4 ) ,enableBackground = False),
	cmds.button(l = 'Delete', h = iHeight , w = oCamGhost.Div[0][5], command = Button_DeleteNulls, bgc = (0.4, 0.4, 0.4 ) ,enableBackground = False),
	cmds.button(l = 'Black', h = iHeight , w = oCamGhost.Div[0][6], command = Button_Black, bgc = (0.4, 0.4, 0.4 ) ,enableBackground = False),

	]
	oCamGhost.AddRow(aRow3)



	## Row 5
	oCamGhost.Division([ 5, 3, 3, 4, 5, 3, 3, 4, 1, 10], 0, 14)
	aRow4 = [
	cmds.text(label = 'Depth : '  , h = iHeight, w = oCamGhost.Div[0][0]),
	cmds.button(l = '-'       	, h = iHeight, w = oCamGhost.Div[0][1], command = partial(Button_Near,-1) , bgc = (0.4, 0.4, 0.4 ) ,enableBackground = False),
	cmds.button(l = '+'       	, h = iHeight, w = oCamGhost.Div[0][2], command = partial(Button_Near, 1), bgc = (0.5, 0.5, 0.5 ) ,enableBackground = False),
	cmds.textField('Depth'    	, h = iHeight, w = oCamGhost.Div[0][3] , text = '0', ed = False),
	cmds.text(label = 'Size : '   , h = iHeight, w = oCamGhost.Div[0][4]),
	cmds.button(l = '-'       	, h = iHeight, w = oCamGhost.Div[0][5], command = partial(Button_Size, -1), bgc = (0.4, 0.4, 0.4 ) ,enableBackground = False),

	cmds.button(l = '+'       	, h = iHeight, w = oCamGhost.Div[0][6], command = partial(Button_Size,  1), bgc = (0.5, 0.5, 0.5 ) ,enableBackground = False),
	cmds.textField('Size'     	, h = iHeight, w = oCamGhost.Div[0][7], text = '1', ed = False),
	cmds.text(label = ' '     	, h = iHeight, w = oCamGhost.Div[0][8]),
	cmds.checkBox('NextFrameCreation', label = 'Plot Creation'  , h = iHeight, w = oCamGhost.Div[0][9], v = 1 ),

	]
	oCamGhost.AddRow(aRow4)




	## Row
	oCamGhost.Division([1,2,5,2,1],0, 6)
	iHeight = 25
	aRow8 = [
	cmds.button(l = '<'            	,h = iHeight, w = oCamGhost.Div[0][0], command = partial(Button_PlotOneFrame, -1) ),
	cmds.button(l = '<<'           	,h = iHeight, w = oCamGhost.Div[0][1], command = partial(Button_PlotKey, -1), bgc = oColour2 ,enableBackground = False)  ,
	cmds.button(l = 'Plot Between Keys',h = iHeight, w = oCamGhost.Div[0][2], command = Button_PlotBetKeys   , bgc = oColour1 , enableBackground = False),
	cmds.button(l = '>>'           	,h = iHeight, w = oCamGhost.Div[0][3], command = partial(Button_PlotKey,  1), bgc = oColour2 ,enableBackground = False)  ,
	cmds.button(l = '>'            	,h = iHeight, w = oCamGhost.Div[0][4], command = partial(Button_PlotOneFrame,  1) ),
	]
	oCamGhost.AddRow(aRow8)

	## Row
	oCamGhost.Division([1],0,0)

	aRow6 = [
	cmds.button(l = 'Plot Range'  , h = iHeight , w = oCamGhost.Div[0][0], command = Button_PlotRange  , bgc = oColour1 ,enableBackground = False),
	]
	oCamGhost.AddRow(aRow6)

	ApplyInfo()

	oCamGhost.Create()
