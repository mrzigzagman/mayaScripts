# Pivot Tool v013

# Set the length of bones for Female02 v002
from functools import partial

K = cmds.getModifiers()

### Class Assignment###
sCustomUI = 'Custom_Pivot_v012'
class CreateUI:


	def __init__(self):

    	### Pre-Setup ###

    	# Custom Setup To Refresh UI depends on the count of nulls under CustomPivots.
    	iExtend = 0
    	oPivots = GetExistingPivots()
    	if oPivots:
        	iExtend = len(oPivots) * 27 + 25

    	# Setup Body
    	self.oUI = sCustomUI
    	self.Width  = 320   # Total  Width of Window in pixel
    	self.Height = 95 + iExtend  # Total Height of Window in pixel

    	self.iBoarderW = 10  # Default Empty Pixels around window for Width
    	self.iBoarderH = 10  # Default Empty Pixels around window for Height

    	self.PreDefine()

	def PreDefine(self):
    	# Delete UI if exists.
    	if cmds.window(self.oUI, exists=True):
        	cmds.deleteUI(self.oUI, window=True)

    	# Create Window as formLayout
    	self.oWindow = cmds.window(self.oUI, w = self.Width, h = self.Height, mnb = False, mxb = False, title = self.oUI, sizeable = False)
    	self.oForm = cmds.formLayout()

    	self.Div = [] # [  [iP, iP, iP, iP] ,  iGapBetweenCells, iHeightBetweenRows]
    	self.Row = [] # Stores All creation for window separated by rows.

	def DeleteWindow(self):
    	if cmds.window(self.oUI, exists=True):
        	cmds.deleteUI(self.oUI, window=True)
	def AddRow(self, Entry):
    	'''
    	Collects list of maya commands for each entry in 'self.Row'. (Buttons, Boxes, Text Fields, etc. )
    	'''
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
    	Takes the entered oUIWindow.Row info to Create the UI.
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

	def Refresh(self):
    	self.PreDefine()


### General Functions
def ReCreateUI(aCode = None):
	# Refresh UI with colour code of a List[4]
	sText = cmds.textField('enterbox', tx = True, q = True)
	cmds.deleteUI(sCustomUI, window = True)
	CreateWindow(aCode)
	cmds.textField('enterbox', tx = sText, e = True)


def GetExistingPivots():
	# Return the count of custom pivots. Excluding the Pivot Rig. "Pivot_Root"
	oPivots = []
	if cmds.listRelatives(oAnimTools+'|'+oAnimPivots, c = True):
    	oPivots = [str(o) for o in cmds.listRelatives(oAnimTools+'|'+oAnimPivots, c = True)]
    	sPivotRoot = 'Pivot_Root'
    	if sPivotRoot in oPivots:
        	oPivots.remove(sPivotRoot)
	return oPivots


def ListSelection():
	''' List section into an array of strings'''
	return [str(o) for o in cmds.ls(sl = True, o = True)]


def ChangeColour(oObj, iColour):
	# Changing Colour of an object.
	if cmds.objExists("%s.overrideEnabled"%oObj):
    	cmds.setAttr("%s.overrideEnabled"%oObj, 1)
    	cmds.setAttr ("%s.overrideColor"%oObj , iColour)
	if cmds.objExists('%sShape'%oObj):
    	cmds.setAttr("%sShape.overrideEnabled"%oObj, 1)
    	cmds.setAttr ("%sShape.overrideColor"%oObj , iColour)


def SetColour(oObj):
	# Change Colour of pivot nulls all in Brown, then the selected one to be Red.
	oPivots = GetExistingPivots()
	if oPivots:
    	for obj in oPivots:
        	ChangeColour(obj, 24)
	ChangeColour(oObj, 13)


### Button Functions
def ButtonHidePivot(*args):
	# Toggle visibility of Custom Pivots.
	global oAnimPivots

	if cmds.objExists(oAnimPivots):
    	iVis = cmds.getAttr('{}.visibility'.format(oAnimPivots))
    	if iVis:
        	iVis = 0

    	else:
        	iVis = 1
    	cmds.setAttr('{}.visibility'.format(oAnimPivots), iVis)


def ButtonSetGuide(sGuide, *args):
	# Set the picked CustomPivot as the New Pivot.
	SetColour(sGuide)
#	ReCreateUI([5, 3, 3, 1])
	cmds.textField('enterbox', tx = sGuide, e = True)
	Colour_The_UI()




def ButtonDeleteGuide(sGuide, *args):
	# Deletes the picked CustomPivot.
	cmds.delete(sGuide)

	# Rename the PivotSpheres to fit the list in UI. 0 = first entry.
	oPivots = GetExistingPivots()

	aBalls = [Get_ChildBall(o) for o in oPivots]

	for i in range(0,len(aBalls)):
    	iNum = int(aBalls[i].split('_')[1])
    	if not iNum == i:
        	cmds.rename(aBalls[i], 'PivotSphere_%s_Pivot'%i)


	# Change the color of the Spheres.
	Colour_The_Balls()


	sText = cmds.textField('enterbox', tx = True, q = True)

	if not cmds.objExists(sText):
    	oPivots = GetExistingPivots()

    	if oPivots:
        	sText = oPivots[0]
        	ReCreateUI([5, 3, 3, 1])
    	else:
        	sText = 'Create Your Target Pivot First.'
        	ReCreateUI([0, 4, 1, 1])
	else:
    	ReCreateUI([5, 3, 3, 1])

	cmds.textField('enterbox', tx = sText, e = True)




def Colour_The_Balls():
# Create Shaders
	aColourList = [
	[0 ,( 1.00 , 1.00 , 0.39 )],
	[1 ,( 0.39 , 0.86 , 1.00 )],
	[2 ,( 0.26 , 1.00 , 0.64 )],
	[3 ,( 0.80 , 0.70 , 0.80 )],
	[4 ,( 0.19 , 0.63 , 0.63 )],
	[5 ,( 0.89 , 0.67 , 0.47 )],
	[6 ,( 0.41 , 0.63 , 0.19 )],
	[7 ,( 0.00 , 0.60 , 0.33 )],
	[8 ,( 0.19 , 0.40 , 0.63 )],
	[9 ,( 0.44 , 0.19 , 0.63 )], ]


	for colour in aColourList:
    	oMaterial = 'PivotColour_%s' % colour[0]
    	oShader = oMaterial+'_SDR'
    	if not cmds.objExists(oMaterial):
        	cmds.shadingNode('lambert', n = oMaterial, asShader = 1, )

        	cmds.sets(oMaterial, renderable = True, noSurfaceShader = True, empty = True, name = oShader)
        	cmds.connectAttr(oMaterial+'.outColor', oShader+'.surfaceShader', f = True)

        	cmds.setAttr( "%s.color"%oMaterial, type = 'double3', *colour[1])
#        	cmds.setAttr( "%s.incandescence"%oMaterial, type = 'double3', *colour[1])
#        	cmds.setAttr( "%s.ambientColor"%oMaterial, type = 'double3', *colour[1])




	# Change the color of the Spheres.

	for i in range(0,len(GetExistingPivots())):
    	sBall = 'PivotSphere_%s_Pivot' % i # Object Name

    	s = str(i)[-1]

    	cmds.sets( sBall, fe = 'PivotColour_%s_SDR' % s,  e = True)





def ButtonSelectGuide(sGuide, *args):
	# Deletes the picked CustomPivot.
	sText = cmds.textField('enterbox', tx = True, q = True)
	if cmds.objExists(sGuide):
    	cmds.select(sGuide, r = True)


def Get_ChildBall(sGuide):
	sSphere = ''
	oChildren = [str(p) for p in cmds.listRelatives(sGuide, c = True)]
	for e in oChildren:
    	if 'PivotSphere_' in e:
        	sSphere = e
	return sSphere

def ButtonSizeUp(sParent, *args):
	sBall = Get_ChildBall(sParent)

	iSize = cmds.getAttr('%s.scaleX'%sBall)

	if K:
    	iSize *= 1.5
	else:
    	iSize *= 1.1

	cmds.setAttr('%s.scale'%sBall, *[iSize, iSize, iSize])




def ButtonSizeDown(sParent, *args):
	sBall = Get_ChildBall(sParent)

	iSize = cmds.getAttr('%s.scaleX'%sBall)

	if K:
    	iSize *= 0.5

	else:
    	iSize *= 0.9

	if iSize < 0.01:
    	iSize = 0.01

	cmds.setAttr('%s.scale'%sBall, *[iSize, iSize, iSize])


def ButtonCreateGuide(*args):
	# Sets and creates the selected object as a new Pivot, if exists already, set only.
	oSel = ListSelection()
	iAdd = 0
	if oSel == []:
    	cmds.warning('Nothing is selected.')
	else:
    	if '|' in oSel[0]:
        	cmds.warning('An object with same name already exists..')
    	else:

        	if '_Pivot' in oSel[0]: # if CustomPivot is selected for creation,
            	cmds.textField('enterbox', tx = oSel[0], e = True)
            	sName = oSel[0]
            	#SetColour(oSel[0])

        	else:
            	sName = '{}_Pivot'.format(oSel[0])
            	if not cmds.objExists(sName): # if a selected object has already a CustomPivot,

                	sPivName = "PivotSphere_"+str(len(GetExistingPivots())) + "_Pivot"
                	cmds.sphere(name = sPivName)


                	oConst = oSel[0]+'_FollowConst'
                	cmds.spaceLocator(n = sName)
                	cmds.parent(sPivName, sName)
                	cmds.parent(sName, oAnimTools+'|'+oAnimPivots)
                	cmds.parentConstraint(oSel[0], sName, n = oConst)





            	cmds.textField('enterbox', tx = sName, e = True)

    	cmds.select(oSel[0])
    	Colour_The_Balls()
    	Colour_The_UI()


def Colour_The_UI():
	sPivot = cmds.textField('enterbox', tx = True, q = True)
	oChildren = [str(o) for o in cmds.listRelatives(sPivot, c = True)]
	i = 0
	for o in oChildren:
    	if 'PivotSphere_' in o:
        	print o.split('_')
        	i = int(str(o.split('_')[1])[-1])

	print i
	ReCreateUI([5, i+7, i+7, 1])

def ButtonApplyPivot(*args):
	## The Core Feature of this tool

	oSel = ListSelection()
	iMode = 0
	sPivot = cmds.textField('enterbox', tx = True, q = True)
	sPivotRoot = 'Root_Pivot'
	sPivotAni =  'Ani_Pivot'
	aObjList = []
	sTempC = 'TempConstraint'

	if cmds.objExists(sPivotAni):
    	iMode = 2
	else:
    	iMode = 1

	# Filter out any Pivot related selection / Flag error if nothing is selected.
	if oSel:
    	for o in oSel:
        	if not '_Pivot' in o:
            	aObjList.append(o)
	else:
    	if iMode == 1:
        	print 'Please select something.'
        	iMode = 0


	# Idle Mode to Active Mode
	if iMode == 1:
    	cmds.spaceLocator(n = sPivotRoot)
    	cmds.spaceLocator(n = sPivotAni)
    	cmds.parent(sPivotAni, sPivotRoot)
    	cmds.parent(sPivotRoot, 'CustomPivots')
#    	cmds.setAttr( "%sShape.visibility"%sPivotRoot ,0)
    	cmds.parentConstraint(sPivot, sPivotRoot,  n = sTempC, mo = False)
    	cmds.delete(sTempC)


    	for o in aObjList:
        	sConstNull = o + '_PivotConstNull'
        	sZero = o + '_PivotConstNull_zero'
        	cmds.spaceLocator(n = sConstNull)
        	cmds.spaceLocator(n = sZero)

        	cmds.parent(sConstNull, sZero)

        	cmds.parentConstraint(o, sZero, n = sTempC, mo = False)
        	cmds.delete(sTempC)


        	cmds.parent(sZero, sPivotAni)

        	sConst = o +'_PivotConstraint'
        	cmds.parentConstraint(sZero, o, n = sConst, mo = False)


    	cmds.select(sPivotAni, r = True)
    	cmds.setToolTo('RotateSuperContext')
    	ReCreateUI([0, 0, 4, 0])

	# Active Mode to Idle Mode
	elif iMode == 2:
    	oTargets = [str(o)[:-20] for o in cmds.listRelatives(sPivotAni, c = True) if not 'Shape' in o]


    	aTransform = []
    	for t in oTargets:
        	aTrans = cmds.xform(t , q = True,  translation = True )
        	aRot = cmds.xform( t , q = True,  ro = True, os = True )
        	aTransform.append([aTrans, aRot])



        	# Delete Constraints
        	# Try set the Pivot Constraint blend to 0
        	oConst = "{}_PivotConstraint.{}_PivotConstNull_zeroW0".format(t,t)


        	if cmds.objExists(oConst):
            	cmds.setAttr(oConst, 0)
            	cmds.delete(oConst)


    	cmds.delete(sPivotRoot)


    	cmds.select(oTargets, r = True)



    	for i in range(0,len(oTargets)):
        	cmds.xform(oTargets[i], translation = aTransform[i][0] )

        	cmds.xform(oTargets[i], ro = aTransform[i][1], os = True )

    	Colour_The_UI()


def ButtonKeyFrame(aAxis, *args):
	oChildren = None
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	if oSel:
    	oPivot = cmds.textField('enterbox', tx = True, q = True)
    	if cmds.objExists('{}Follow'.format(oPivot) ):
        	oChildren = [str(o) for o in cmds.listRelatives('{}Follow'.format(oPivot), c = True)]

    	if oChildren:
        	for o in oChildren:
            	if 'Target_' in o:
                	oSel[0] = o[7:]

    	for a in aAxis:
        	cmds.setKeyframe(oSel[0], attribute = a)

def ButtonReset(*args):
	global oUIWindow
	if cmds.objExists(oAnimPivots):
    	cmds.delete(oAnimPivots)

	oUIWindow.DeleteWindow()

def CreateWindow(aCode = [4, 3, 0, 3]):
	global oUIWindow
	### Execute ###
	oUIWindow = CreateUI()  # Assigning class to a var. ButtonCreateGuide




	### Layout ###
	iHeight = 25

	aPivotColour = [
	( 1.00 , 1.00 , 0.39 ),
	( 0.39 , 0.86 , 1.00 ),
	( 0.26 , 1.00 , 0.64 ),
	( 0.80 , 0.70 , 0.80 ),
	( 0.19 , 0.63 , 0.63 ),
	( 0.89 , 0.67 , 0.47 ),
	( 0.41 , 0.63 , 0.19 ),
	( 0.00 , 0.60 , 0.33 ),
	( 0.19 , 0.40 , 0.63 ),
	( 0.44 , 0.19 , 0.63 ),
	]

	aColourCode = [ (0.3, 0.3, 0.3),  # DarkGray
                	(0.4, 0.4, 0.4),  # Gray
                	(0.8, 0.8, 1.0),  # Blue
                	(1.0, 1.0, 0.8),  # Yellow
                	(0.9, 0.4, 0.4),  # Red
                	(0.7, 0.7, 0.7),  # Light Gray
                	(1.0, 1.0, 1.0),] # White
	aColourCode.extend(aPivotColour)





	# Change Colour of UI if any of the CustomPivot exists.
	oPivots = GetExistingPivots()
	if not oPivots:
    	aCode = [4, 3, 0, 1]

	iHeight = 25
	## Row
	oUIWindow.Division([1,8], None ,0)
	aRow = [

	cmds.text(label = 'Pivot', h = iHeight, w = oUIWindow.Div[0][0], enableBackground = False),
	cmds.textField('enterbox',h = iHeight, w = oUIWindow.Div[0][1] , bgc = aColourCode[0],text = 'Create/Set Target From Selection', ed = False),
	]
	oUIWindow.AddRow(aRow)






	## Row
	oUIWindow.Division([1], None ,10)
	aRow = [
	cmds.button(label = 'Apply/Remove', h = 38, w = oUIWindow.Div[0][0], bgc = aColourCode[aCode[2]], enableBackground = False, command = ButtonApplyPivot),
	]
	oUIWindow.AddRow(aRow)


	## Row
	oUIWindow.Division([1,1], None ,0)
	aRow = [
	cmds.button(label = 'Key Translation', h = iHeight, w = oUIWindow.Div[0][0],bgc = aColourCode[aCode[2]], enableBackground = False, command = partial(ButtonKeyFrame, ['tx', 'ty', 'tz'] )),
	cmds.button(label = 'Key Rotation',	h = iHeight, w = oUIWindow.Div[0][1],bgc = aColourCode[aCode[2]], enableBackground = False, command = partial(ButtonKeyFrame, ['rx', 'ry', 'rz'] )),
	]
	oUIWindow.AddRow(aRow)




	iHeight = 20
	# Series of Rows
	oPivots = GetExistingPivots()
	if oPivots:



    	## Row
    	oUIWindow.Division([1], None ,5)
    	aRow = [
    	cmds.text(label = '--- Pivots List ---', h = 20, w = oUIWindow.Div[0][0], enableBackground = False),
    	]
    	oUIWindow.AddRow(aRow)



    	## Row
    	oUIWindow.Division([1], None ,0)
    	aRow = [
    	cmds.text(label = '', h = 5, w = oUIWindow.Div[0][0], enableBackground = False)
    	]
    	oUIWindow.AddRow(aRow)

    	for i in range(len(oPivots)):
        	## Row

        	oUIWindow.Division([3,1,1,1], None ,0)
        	aRow = [
        	#cmds.textField(h = iHeight, w = oUIWindow.Div[0][0] , text = oPivots[i], ed = False),
        	cmds.button(label = 'SET', h = iHeight, w = oUIWindow.Div[0][0],bgc = aPivotColour[int(str(i)[-1])], enableBackground = False, command = partial(ButtonSetGuide, oPivots[i]) ),

        	cmds.button(label = '+', h = iHeight, w = oUIWindow.Div[0][1],bgc = aColourCode[0], enableBackground = False, command = partial(ButtonSizeUp, oPivots[i]) ),
    	cmds.button(label = '-', h = iHeight, w = oUIWindow.Div[0][2],bgc = aColourCode[0], enableBackground = False, command = partial(ButtonSizeDown, oPivots[i]) ),
        	cmds.button(label = 'Del', h = iHeight, w = oUIWindow.Div[0][3],bgc = aColourCode[0], enableBackground = False, command = partial(ButtonDeleteGuide, oPivots[i]) ),
        	]
        	oUIWindow.AddRow(aRow)


	iHeight = 35
	## Row
	oUIWindow.Division([4, 1, 1], None ,5)
	aRow = [
	cmds.button(label = 'Create/Set', h = iHeight, w = oUIWindow.Div[0][0],bgc = aColourCode[6], enableBackground = False, command = ButtonCreateGuide),
	cmds.button(label = 'Visibility', h = iHeight, w = oUIWindow.Div[0][1], bgc = aColourCode[1], enableBackground = False, command = ButtonHidePivot),
	cmds.button(label = 'Reset', h = iHeight, w = oUIWindow.Div[0][2],bgc = aColourCode[1], enableBackground = False, command = ButtonReset),
	]
	oUIWindow.AddRow(aRow)



	## Row
	oUIWindow.Division([1], None ,0)
	aRow = [
	cmds.text(label = '', h = 10, w = oUIWindow.Div[0][0], enableBackground = False)
	]
	oUIWindow.AddRow(aRow)

	# Create UI
	oUIWindow.Create()


### Global Variables
oAnimTools   = 'ANIM_TOOLS'
oAnimPivots   = 'CustomPivots'
#oSel = ListSelection()

# Create Root Groups
if not cmds.objExists(oAnimTools):
	cmds.group( em = True, name = oAnimTools )
if not cmds.objExists(oAnimPivots):
	cmds.group( em = True, name = oAnimPivots, p = oAnimTools)


oCustomUI = CreateWindow()
