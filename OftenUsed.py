## [Often used] v1.3.1
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

#TO STUDY
cmds.fileDialog2()
lines = [line.rstrip().rstrip('\n') for line in open(srcPath)]
cmds.scriptJob()
cmds.refresh(su = True) # No Refresh


aPlayBackSliderPython=mel.eval('$tmpVar=$gPlayBackSlider')
v1= int(mc.timeControl(aPlayBackSliderPython, q=1, rng=1).split(":")[0][1:])
v2= int(mc.timeControl(aPlayBackSliderPython, q=1, rng=1).split(":")[1][:-1])
if v2 - v1 > 1:

# Grammer

# cmds.setKeyframe( oSel[0], breakdown = 0, at = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'])

# Similar to try:/ finally. this will close the file no matter what. Safer way to open a file.
with open(sProjectConfigFile, 'r') as oFile:
	dDict = json.load(oFile)

#################

s = 'a' if i == 100 else ('b' if i == 10 else 'c')
print s

# Same as:
i = 10
if i == 100:
	s = 'a'
else:
	if i == 10:
		s = 'b'
	else:
		s = 'c'
##############
import collections
pos = collections.namedtuple('Position', ['name', 'xpos', 'ypos'])

v = pos('one', 232, 323)
print v
print v.name





x = 1 if z else 2

for iIndex, x in enumerate(oSel[:]): # [:] makes it run a copy of oSel so you can modify oSel in the loop.
	print iIndex
	print x
	oSel.remove(x)



# Pring all attributes selected. (Regardless of shape, transform node..)
print [str(c+'.'+cmds.attributeName(c+'.'+b, l=True)) for a in 'msho' for b in cmds.channelBox('mainChannelBox', **{'q':True, 's%sa'%a:True}) or [] for c in cmds.channelBox('mainChannelBox', q = True, **{'%sol'%a:True})]


# Toggle Trick
sphere.visibility = False == sphere.visibility
# s.v = False == True (returns False)
# s.v = False == False (returns True)

or
iVal = abs(iVal-1)
iVal = iVal * -1 + 1



# And & Or
var1 = var2 and var3
# if Var 2 is true, var3 is returned.
# if Var 2 is False, var2 is returned. (because it fails at var2)

var1 = var2 or var3
# if Var 2 is true, var2 is returned. (because the statement is already true)
# if Var2 is False, var3 is returned.

# all()
bBool = all([1,1,1,1]) # True
bBool = all([1,1,0,1]) # False


# Swap Variables
iVal1, iVal2 = iVal2, iVal1




# Run external python file
# Option 1
import imp
IncrementSaveWindow = imp.load_source('IncrementSaveWindow', '/weta/prod/motion/work/dpretorius/python/share/IncrementSaveWondow.py')
IncrementSaveWindow.main();

# Option 2
import sys; p = '/weta/prod/moiton/work/dpretorius/python/share/'
if p not in sys.path: sys.path.append(p)

import shot_notes

shot_notes.main()

#json
with open(sSceneConfigFile, 'w') as oFile:
	json.dumps(dContent, indent = 4)) # dump STRING. returns

with open(sProjectConfigFile, 'w') as oFile:
	json.dump(dDict, oFile, indent = 4) # dump w/o returns nothing.

# List all unde scene root
ls(assembly = True)

# Run external .py
import sys; p = '/vol/transfer/dyabu/Scripts/mayaScripts/'
if p not in sys.path: sys.path.append(p)
import PlayBlastTool
reload(PlayBlastTool)
PlayBlastTool.main()



# parent constraint only keyable.
def CustomParentConst(oSrc, oFollow, sConst = 'TempConst'):
	''' Apply parent constraint on keyable axis only.'''

	aSkipTrans = ['x','y','z']
	aSkipRot = ['x','y','z']
	# To be added : feature that supports only one axis to constraint.
	aList = [ 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']


	aConstList = [str(c) for c in cmds.listAttr(oFollow, keyable = True)]

	for c in aConstList:
    	for l in aList:
        	if l == c:
            	if 'translate' in c:
                	print c[-1].lower()
                	aSkipTrans.remove(c[-1].lower())
            	else:
                	aSkipRot.remove(c[-1].lower())


	cmds.parentConstraint(oSrc, oFollow, weight = 1, n = sConst, st=aSkipTrans, sr = aSkipRot)


# Get variety of info
print cmds.about(os = True) # OS version
print cmds.about(env = True) # Pref folder
print cmds.about(cd = True) # Date
print cmds.about(ct = True) # Time


# Get Shape Node of a DAG obj
def getShapeNodes(obj):
	howManyShapes = 0
	getShape = maya.cmds.listRelatives(obj, shapes=True)
	if(getShape == None):
    	print 'ERROR:: getShapeNodes : No Shape Nodes Connected to ' + obj + ' /n'
	else:
    	howManyShapes = len(getShape[0])
	return (getShape, howManyShapes)

print getShapeNodes('Plumette01__geo__rig__puppet__C_body_CTL_Plot_CamAim_Anim')[0][0]



# Arrow Shapes
maya.cmds.curve(d=1, p=[(-0.5, 0, 0),(-0.5, 0, 2),(-2, 0, 2),(0, 0, 4),(2, 0, 2),(0.5, 0, 2),(0.5, 0, 0),(0.5, 0, -2),(2, 0, -2),(0, 0, -4),(-2, 0, -2),(-0.5, 0, -2),(-0.5, 0, 0)]);
maya.cmds.curve(d=1, p=[(-4, 0, 0),(-2, 0, -1.5),(-2, 0, -0.5),(-0.5, 0, -0.5),(-0.5, 0, -2),(-1.5, 0, -2),(0, 0, -4),(1.5, 0, -2),(0.5, 0, -2),(0.5, 0, -0.5),(2, 0, -0.5),(2, 0, -1.5),(4, 0, 0),(2, 0, 1.5),(2, 0, 0.5),(0.5, 0, 0.5),(0.5, 0, 2),(1.5, 0, 2),(0, 0, 4),(-1.5, 0, 2),(-0.5, 0, 2),(-0.5, 0, 0.5),(-2, 0, 0.5),(-2, 0, 1.5),(-4, 0, 0)]);
maya.cmds.curve(d=1, p=[(-0.5, 2.5, 0),(-0.5, 2.449, 2),(-2, 2.25, 2),(0, 0, 4),(2, 2.25, 2),(0.5, 2.449, 2),(0.5, 2.5, 0),(0.5, 2.449, -2),(2, 2.25, -2),(0, 0, -4),(-2, 2.25, -2),(-0.5, 2.449, -2),(-0.5, 2.5, 0)]);
maya.cmds.curve(d=1, p=[(-4, 0, 0),(-2, 3.146, -1.5),(-2, 3.464, -0.5),(-0.5, 3.9680, -0.5),(-0.5, 3.464, -2),(-1.5, 3.146, -2),(0, 0, -4),(1.5, 3.146, -2),(0.5, 3.464, -2),(0.5, 3.968, -0.5),(2, 3.464, -0.5),(2, 3.146, -1.5),(4, 0, 0),(2, 3.146, 1.5),(2, 3.464, 0.5),(0.5, 3.968, 0.5),(0.5, 3.464, 2),(1.5, 3.146, 2),(0, 0, 4),(-1.5, 3.146, 2),(-0.5, 3.464, 2),(-0.5, 3.968, 0.5),(-2, 3.464, 0.5),(-2, 3.146, 1.5),(-4, 0, 0)]);




## Re-Ordering
    	for p in aPreferenceOrder:
        	if p in aKeys:
            	aReorder[aKeys.index(p)] = iReorder
            	iReorder +=1

    	for i in range(0, len(aReorder)):
        	if aReorder[i] == -1:
            	aReorder[i] = iReorder
            	iReorder +=1

    	aKeys = [x for (y,x) in sorted(zip(aReorder, aKeys))]

# Sound
setSoundDisplay Audio01_:main_:audioTrack 1;
setAttr "Audio01_:main_:audioTrack.offset" 1001;



# ClipBoard
import pygtk
pygtk.require('2.0')
import gtk

clipboard = gtk.clipboard_get()

clipboard.set_text('Shit!')
clipboard.store()


# Filter objects
aKeyWords = ['*nose*','*lip*']
aList = cmds.listAttr(r = True, st = aKeyWords) or []
oFilter = cmds.itemFilterAttr(bns = aList)
cmds.channelBox('mainChannelBox', e = True, attrFilter = oFilter)

# Apply list to translation
cmds.setAttr("TargetFollowOffset.rotate" , *[1,1,0] )


### Get Selection as a list
def ListSelection():
	''' List section into an array of strings'''
	return [str(o) for o in cmds.ls(sl = True, o = True)]

oSel = ListSelection()

# Get Current Selected Curve
aObjList = [str(s) for s in cmds.selectionConnection('graphEditor1FromOutliner', q = True, object = True)]
aCurveList = [str(s) for s in cmds.keyframe(query = True, name = True)]

# Get Children
oChildren = [str(o) for o in cmds.listRelatives('XXXXXX', c = True)]
cmds.rename()



# Split example
print 'test:ttt:zzz:ccc'.split(':', 2 )[2]

# Apply transform
cmds.setAttr('%s.translate'%sPivotAni, *[0,0,0])
cmds.setAttr('%s.rotate'%sPivotAni, *[0,0,0])

# Get Keyable channels
cmds.listAttr(oSel[0], k = True)

# List all windows
oWindows = cmds.lsUI( windows=True )

# Apply Const on Non Locked Tx~Rz
def Custom_2Const(oSel,sConstName, iMo = False, aSkipTrans = [], aSkipRot = []):
	aAxis = ['tx','ty','tz','rx','ry','rz']
	for i in range(0,6):
    	v = cmds.getAttr(str(oSel[0])+'.%s'%aAxis[i], l = True)
    	if v:
        	if i < 3:
            	if not aAxis[i][-1] in aSkipTrans:
                	aSkipTrans.append(aAxis[i][-1])
        	else:
            	if not aAxis[i][-1] in aSkipRot:
                	aSkipRot.append(aAxis[i][-1])
	cmds.parentConstraint(oSel[-1], oSel[0], st = aSkipTrans, sr = aSkipRot, n = sConstName, mo = iMo)

	# Returns Non Locked Axis
	aAdj = ['z','y','x']
	for i in range(0,3):
    	if aSkipRot:
        	if aAdj[i] in aSkipRot:
            	aAxis.remove('r%s'%aAdj[i])
    	if aSkipTrans:

        	if aAdj[i] in aSkipTrans:
            	aAxis.remove('t%s'%aAdj[i])
	return aAxis

# List files and directories
aSceneFiles = os.listdir(sFullPath)

# Find keyable attributes
print cmds.listAttr(oSel[0], keyable = True)


# Check if path exists
import os
def CreateTxtFilePath(sPath = '/net/homes/dyabu/Personal/TimeStamp/TimeStamp.txt'):
	if os.path.exists(sPath):
    	print 'yes'

# Get Local Transform Values
aTrans = cmds.xform(oSel, q = True,  translation = True)
aRot = cmds.xform(oSel, q = True,  ro = True, os = True)


### To get Scene File Path
cmds.file( q = True, sn = True)


### In view Message
self.PrintOnScreen = ['a7a8af', 'Playblast done [%s]'%sView, 0x6b6c75]
cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 10, ft = 'arial', bkc = aPrint[2])

### Display Message Box
def MessageBox(Message):
	'''Displaying Entered Message as Popup '''
	oWindow = cmds.window(title = 'Message Box', s = False)
	if cmds.windowPref(oWindow, exists = True):
    	cmds.windowPref(oWindow, remove = True)
	cmds.columnLayout(adjustableColumn = True)
	cmds.text('\n\t%s\t\n' % Message, bgc = (.25,.25,.25),enableBackground = False)
	cmds.button(label = 'Close', command = ('cmds.deleteUI(\"'+oWindow+'\",window = True)'), bgc = (.2,.2,.2),enableBackground = False)
	cmds.setParent('..')
	cmds.showWindow(oWindow)


# Print Methods
import maya.mel as mel
dir(mel)

# To Get the creation time of a file
from datetime import datetime
import os

tCreateTime = os.path.getmtime('/job/nysm2/film/bt163/bt163_0485/work/dyabu/maya/scenes/bt163_0485_DY.v001.01.Ohoh.0002.mb')
print datetime.fromtimestamp(tCreateTime).strftime('%Y-%m-%d %H:%M:%S')



### Modifiers
K = cmds.getModifiers()
sMenu = '''
	----- ALT [8]
	----- CTL [4]
	----- SFT [1]
	----- CTL + SFT [5]
	----- ALT + SFT [9]
	----- CTL + ALT [12]
	----- CTL + ALT + SFT [13]'''

### fill with 0 in a string. ex "003"
'1'.zfill(3)


### Prompt Dialog Box

o = cmds.confirmDialog( title='Confirm', message='Are you sure?', button=['Yes','No','Maybe','Not Sure'], defaultButton='Yes', cancelButton='No', dismissString='No' , bgc = [1.2,1.2,1.2])

### Prompt Enter Box
def EnterBox():
	oResult = cmds.promptDialog(
   		 title='Rename Object',
   		 message='Enter Name:',
   		 button=['OK', 'Cancel'],
   		 defaultButton='OK',
   		 cancelButton='Cancel',
   		 dismissString='Cancel')

	if oResult == 'OK':
   	 sText = cmds.promptDialog(query=True, text=True)
    	return sText
	else:
    	return None



### Change all non alpha numeric to '_'
def Underscore(sString):
	if sString[0].isdigit():
    	sString = '_'+sString

	sNewString =''
	for s in sString:
    	if s.isalnum():
        	sNewString += s
    	else:
        	sNewString += '_'

	print sNewString
Underscore('a#$^fgg1')



### Current Frame
iFrame = int(cmds.currentTime(q = True))



### In/Out Range
iIn = int(cmds.playbackOptions(q = True, minTime = True))
iOut = int(cmds.playbackOptions(q = True, maxTime = True))


# Get List of Audios in the scene.
aAudio = [str(a) for a in cmds.ls(typ = 'audio')]

# Get Currently Active Sound
aPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
sAudio = cmds.timeControl(aPlayBackSlider, q = True, s = True)


### Date Examples
from datetime import datetime
from datetime import timedelta
# String to daytime
def MondayFinder(sYear, sMonth, sDate):
	#date_object = datetime.strptime('05 12 2015  1:33PM', '%b %d %Y %I:%M%p')
	oEntered = datetime.strptime('%s %s %s'%(sMonth, sD), '%m %d %Y')
	#print date_object.weekday()
	oMonday = date_object - timedelta(days = date_object.weekday())
	print newDate.weekday()


### Get Current SoundTrack
aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')
sSound = cmds.timeControl( aPlayBackSliderPython, q = True, sound = True)
print sSound
if sSound:
	iOffset = cmds.getAttr(sSound+'.offset')
	print cmds.sound( sSound, q = True, f = True )
	print iOffset


### Open Fold
	[pasted text truncated for security]

cmd1 ='nautilus /net/homes/dyabu/Desktop/Shots/tu125250/Rv'
os.system(cmd1)



### User Define Enter Box
oClick = cmds.promptDialog(
   	 title='Rename Object',
   	 message='Enter Shot : ( ex.  fs150 )',
   	 button=['OK', 'Cancel'],
   	 defaultButton='OK',
   	 cancelButton='Cancel',
   	 dismissString='Cancel')

if oClick == 'OK':
    sShot = cmds.promptDialog(query=True, text=True)



### Get Current Camera ###
def getCamera():
	oCamera = ''
	oPanel = cmds.getPanel(wf = True)

	if 'modelPanel' in oPanel:
    	oCamera = cmds.modelEditor(oPanel, q = True, camera = True)

	return str(oCamera)


### Warning Message
cmds.warning( 'Enter something here' )




### Rename objects
cmds.rename(o, sName)

### Get User Name
import getpass
print getpass.getuser()


### Write File
oRvFile = open(sPath, 'w')
oRvFile.write(sContent)
oRvFile.close()

### Read File
oRvFile = open(sPath, 'r')
aLines = oRvFile.readlines()
oRvFile.close()
for line in aLines:
	sLine = line.strip()


### Get Active Panel
sCurrentPanel = cmds.getPanel(underPointer = True)
if sCurrentPanel == None:
	sCurrentPanel = cmds.getPanel(withFocus = True)

tCurrentPanel = cmds.getPanel(typeOf = sCurrentPanel)
if tCurrentPanel == 'modelPanel':
	print tCurrentPanel


# Execute Python File
#import sys
#sys.path.append('/home/ericb/GIT_DEV/ebLabs-workshop/whisKEY2')
import ebLabs_whisKEY
reload(ebLabs_whisKEY)
ebLabs_whisKEY.window.load()

# Execute External Python file
import sys
import  os

def ExecuteExternal(Mod):
	sFile  = os.path.basename( Mod )
	aFiles = sFile.split( '.' )

	sDir   = os.path.dirname( Mod )

	if( os.path.exists( sDir ) ):

    	aPaths = sys.path
    	iCheck = 0
    	for p in aPaths:
        	if(sDir == p):
            	iCheck = 1

    	if not iCheck:
        	print iCheck
        	sys.path.append( sDir )

	exec( 'import  ' + aFiles[0]    	) in globals()
	exec( 'reload( ' + aFiles[0] + ' )' ) in globals()


ExecuteExternal('/net/homes/dyabu/maya/2013.5-x64/scripts/HelloWorld.py')


### Linux Run Command
def Execute(cmd2):
	global aMainPath

	if cmd2:
    	if aMainPath[2] == 'homes':
        	MessageBox('Please open your scene first.')
    	else:
        	cmd1 ='go %s'%aMainPath[2]
        	os.system(cmd1)

        	os.system(cmd2)


### Partial Usage ###
from functools import partial

cmds.button( .... command = partial(defFunction, arg1, arg2) ...) # in a button
# and/or
oCMD = cmds.optionMenu( "CustomOptionMenu", label = "Version ", w = fWidth, cc = partial(self.defFunction))

def defFunction(arg1, arg2, *args):
	print 1


### Create Hotkey ###
def createHotkey(command, name, description=''):
	'''
	Open up the hotkey editor to create a hotkey from the specified command
	'''

	mel.eval('hotkeyEditor')
	cmds.textScrollList('HotkeyEditorCategoryTextScrollList', edit=True, selectItem='User')
	mel.eval('hotkeyEditorCategoryTextScrollListSelect')
	mel.eval('hotkeyEditorCreateCommand')

	cmds.textField('HotkeyEditorNameField', edit=True, text=name)
	cmds.textField('HotkeyEditorDescriptionField', edit=True, text=description)
	cmds.scrollField('HotkeyEditorCommandField', edit=True, text=command)
	mel.eval('hotkeyEditorAcceptCommand')
	mel.eval('hotkeyEditorSave')


### Create Shaders and assign to an object.
def Colour_The_Balls():
# Create Shaders
	aColourList = [
    	[0 ,[ 0.39 , 0.86 , 1.0 ]],
    	[1 ,[ 0.26 , 1.0 , 0.64 ]],
    	[2 ,[ 1.0 , 0.69 , 0.69 ]],
    	[3 ,[ 0.19 , 0.63 , 0.63 ]],
    	[4 ,[ 0.89 , 0.67 , 0.47 ]],
    	[5 ,[ 0.41 , 0.63 , 0.19 ]],
    	[6 ,[ 0 , 0.6 , 0.33 ]],
    	[7 ,[ 1.0 , 0 , 0 ]],
    	[8 ,[ 0 , 1.0 , 0 ]],
    	[9 ,[ 0 , 0 , 0 ]],   ]


	for colour in aColourList:
    	oMaterial = 'PivotColour_%s' % colour[0]

    	oShader = oMaterial+'_SDR'
    	if not cmds.objExists(oMaterial):
        	cmds.shadingNode('lambert', n = oMaterial, asShader = 1, )
        	cmds.sets(oMaterial, renderable = True, noSurfaceShader = True, empty = True, name = oShader)
        	cmds.connectAttr(oMaterial+'.outColor', oShader+'.surfaceShader', f = True)

        	cmds.setAttr( "%s.color"%oMaterial, type = 'double3', *colour[1])
        	cmds.setAttr( "%s.incandescence"%oMaterial, type = 'double3', *colour[1])
        	cmds.setAttr( "%s.ambientColor"%oMaterial, type = 'double3', *colour[1])


	# Change the color of the Spheres.

	for i in range(0,len(GetExistingPivots())):
    	sBall = 'PivotSphere_%s_Pivot' % i # Object Name
    	print sBall
    	cmds.sets( sBall, fe = 'PivotColour_%s_SDR' % i,  e = True)


### Copy files in Python
from shutil import copyfile

copyfile(src, dst)

### Bake Animation ###
import maya.mel as mel
def SpeedUpBake_1_Store(sName):
	# store a temporary panel configuration.
	layout = cmds.panelConfiguration(l=sName, sc=0)
	evalStr = 'updatePanelLayoutFromCurrent "'+name+'"'
	mel.eval(evalStr)

	# switch to fast "hidden" layout
	evalStr = 'setNamedPanelLayout "Single Perspective View"'
	mel.eval(evalStr)
	perspPane = cmds.getPanel(vis=1)
	cmds.scriptedPanel('graphEditor1',e=1,rp=perspPane[0])
	return sName

def SpeedUpBake_2_Restore(sName):
	# restore the layout returned from makeHiddenLayout.
	evalStr = 'setNamedPanelLayout "'+sName+'"'
	mel.eval(evalStr)
	# now delete the old layout.
	killMe = cmds.getPanel(cwl=sName)
	cmds.deleteUI(killMe,pc=1)

SpeedUpBake_1_Store('tempLayout')

try:
	print 'do something'

	cmds.bakeResults(aFirst, t = (aRange[0],aRange[1]), simulation = True )
finally:
	SpeedUpBake_2_Restore('tempLayout')

#ScriptJob example (ScriptJob : script must fishish executing completely in order for maya to respond.)
def CB(callback):
	trans = set(cmds.ls(sl = True, type = 'transform'))
	if trans:
		cb = cmds.channelBox('mainChannelBox', q = True, sma = True) or []
		if cb:
			callback([a+'.' +b for a in trans for b in cb])
		else:
			objs = set(cmds.ls(sl = True)) - trans
			if objs:
				cmds.select(list(objs))
				def temp():
					res = [a+'.'+b for a in objs for b in cmds.channelBox('mainChannelBox', q = True, sma = True)or[]]
					cmds.select(list(trans))
					callback(res)
				cmds.scriptJob(e = ('idle', temp), ro = True)

def main():
	def p(val):
		print val
	CB(p)
	print 'test'
#ScriptJob example - End
