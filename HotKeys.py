# Hotkeys - Consolidated v0.0.1
# need a few cleanups.

import maya.cmds as cmds
import maya.mel as mel

sScriptPath = '/usr/home/dyabu/Personal/MayaScripts/'

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

def Execute(skey = 'j', iModifier = 0, sPress = 'P'):
    sKey = skey.upper()
    sModifier = str(iModifier)
    sPress = sPress.upper()
    aModifier = [   0, 'N',
                    1, 'SHIFT',
                    4, 'CTRL',
                    8, 'ALT',
                    5, 'S+C',
                    9, 'S+A',
                    12, 'A+C',
                    13, 'C+A+S',]
    for i in range(0, len(aModifier), 2):
        if aModifier[i] == iModifier:
            sModifier = aModifier[i+1]

    dHotKeys = {
                    'B_ALT_P': NOT,
                    'B_N_P': HotKey_PreviousKey,
                    # 'C_ALT_P': C_ALT_P,
                    'D_ALT_P': HotKey_ToggleVisCurves,
                    # 'E_ALT_P': E_ALT_P,


                    'F_ALT_P': HotKey_AttrIncrement_n001,
                    'F_N_P': Hotkey_SelectAll_P,
                    'F_N_R': Hotkey_SelectAll_R,

                    'G_ALT_P': HotKey_AttrIncrement_n01,
                    'G_N_P': Hotkey_SetKey,

                    'H_ALT_P': HotKey_AttrIncrement_p01,
                    'H_N_P': HotKey_Playback_P,
                    'H_N_R': HotKey_Playback_R,

                    'I_ALT_P': HotKey_OpenOutliner,
                    'I_N_P': I_N_P,
                    'I_N_R': I_N_R,

                    'J_ALT_P': HotKey_AttrIncrement_p001,
                    'J_N_P': HotKey_Focus,
                    # 'K_ALT_P': K_ALT_P,
                    # 'L_ALT_P': L_ALT_P,
                    'M_ALT_P': HotKey_Paste,
                    'M_N_P': HotKey_NextFrame,

                    'N_ALT_P': HotKey_Copy,
                    'N_N_P': HotKey_NextKey,
                    # 'O_ALT_P': O_ALT_P

                    # 'R_ALT_P' : NOT,
                    'R_N_P': HotKey_SelectTool_P,
                    'R_N_R': HotKey_SelectTool_R,
                    #'T_ALT_P': NOT,
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

                    'SPACE_N_P': HotKey_PanePoP,
                    }
    #print sKey, sModifier, sPress
    dHotKeys['%s_%s_%s' % (sKey, sModifier, sPress)]()


#### Shortcut Functions ####
# 1. All Caps

##### NON HotKey_ Fuctions #####
def NOT():
    print 'Hotkey Not Assigned.'
    aPrint = ['d8766c', 'HotKey Not Assigned', 0x756b6b, 'topCenter']
    cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = aPrint[3], fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def ATT_INCREMENT(iAmount):
    aSel = [str(o) for o in cmds.ls(sl = True, o = True)]
    if aSel:
        oChannel = cmds.channelBox('mainChannelBox', q = True, sma = True)
        if oChannel:
            aChannel = [str(s) for s in oChannel]
            aVal = []
            for s in aSel:
                for c in aChannel:
                    sAxis = '%s.%s'%(s,c)
                    iVal = cmds.getAttr(sAxis)
                    cmds.setAttr(sAxis, iVal + iAmount)
            if iAmount >= 0.01:
                aPrint = ['a7a8af', '+'+str(iAmount), 0x6b6c75, 'botCenter']
            else:
                aPrint = ['d8766c', '+'+str(iAmount), 0x756b6b, 'botCenter']
        else:
            aPrint = ['d8766c', 'No Attr Selected', 0x756b6b, 'topCenter']
    else:
        aPrint = ['d8766c', 'No Object Selected', 0x756b6b, 'topCenter']
    cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = aPrint[3], fade = True, fts = 10, ft = 'arial',bkc = aPrint[2] )


##### HotKey_ Fuctions #####

def HotKey_PanePoP():
    mel.eval('panePop;')

def HotKey_AttrIncrement_n01():
    ATT_INCREMENT(-0.1)


def HotKey_ToggleVisCurves():
    # Need to revise. make it active editor.
    # Toggle nurbsCurve in modelPanel4
    bSwitch = cmds.modelEditor('modelPanel4', q = True, nurbsCurves = True)
    bSwitchReverse = bSwitch*-1-1
    #print bSwitch
    cmds.modelEditor('modelPanel4', e = True, nurbsCurves = bSwitchReverse, handles = bSwitchReverse)
    cmds.modelEditor('modelPanel1', e = True, nurbsCurves = bSwitch, handles = bSwitch)



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
    cmds.undoInfo(swf = 1)
def Hotkey_SelectAll_P():
    mel.eval('buildSelectAllMM')
def Hotkey_SelectAll_R():
    mel.eval('buildSelectAllMM_release')


def HotKey_PreviousKey():
    # PrevKey v2.0.1
    cmds.undoInfo(swf = 0)
    cmds.currentTime(cmds.findKeyframe(timeSlider = True, which = 'previous'))
    cmds.undoInfo(swf = 1)
def Hotkey_SetKey():
    mel.eval('performSetKeyframeArgList 1 {"0", "animationList"}')


def HotKey_NextKey():
    # NextKey v2.0.1
    cmds.undoInfo(swf = 0)
    cmds.currentTime(cmds.findKeyframe(timeSlider = True, which = 'next'))
    cmds.undoInfo(swf = 1)
def HotKey_Playback_P():
    mel.eval('togglePlayback')
def HotKey_Playback_R():
    mel.eval('togglePlayback')


def HotKey_OpenOutliner():
    # Weta zeus window
    from ShotsToolbar import zeus_window; zeus_window.main(workflows=["lighting"])
def I_N_P():
    mel.eval('storeLastAction( "restoreLastContext " + `currentCtx`); setToolTo insertKeySuperContext')
def I_N_R():
    mel.eval('invokeLastAction')


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
    cmds.undoInfo(swf = 1)
def HotKey_Focus():
    mel.eval('fitPanel -selected')


def HotKey_AttrIncrement_p001():
    ATT_INCREMENT(0.01)

def HotKey_Paste():
    mel.eval('cutCopyPaste "paste"')


def HotKey_AttrIncrement_p01():
    ATT_INCREMENT(0.1)
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
        aPrint = ['6bad64', 'WORLD', 0x6c756b]
    elif iVal == 2:
        cmds.manipMoveContext('Move', e = True, mode = 0)
        cmds.manipRotateContext('Rotate', e = True, mode = 0)
        aPrint = ['d8766c', 'OBJECT', 0x756b6b]
    elif iVal == 0:
        # Camera space Manipultor
        aCoordinate = cmds.xform(oCamera, q = True, a = True, ws = True, t = True)

        cmds.manipMoveContext('Move', e = True, mode = 6, activeHandle = 0, orientTowards = aCoordinate)
        cmds.manipRotateContext('Rotate', e = True, mode = 3)
        aPrint = ['9bbcf2', 'CAMERA', 0x485872]
    else:
        cmds.manipMoveContext('Move', e = True, mode = 1)
        cmds.manipRotateContext('Rotate', e = True, mode = 2)
        aPrint = ['a7a8af', 'LOCAL ', 0x6b6c75]

    cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'botCenter', fade = True, fts = 7, ft = 'arial',bkc = aPrint[2] )

def HotKey_ScaleTool_P():
    mel.eval('buildScaleMM')
def HotKey_ScaleTool_R():
    mel.eval('destroySTRSMarkingMenu ScaleTool')


def HotKey_AttrIncrement_n001():
    ATT_INCREMENT(-0.01)
def HotKey_Undo():
    cmds.undo()


def HotKey_BreakConnections():
    # Break Connection of Selected Attributes v2.0.1
    oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
    oChannel = [str(s) for s in cmds.channelBox('mainChannelBox', q = True, sma = True)]
    if oSel:
        for o in oSel:
            for c in oChannel:
                cmds.delete(o, at = c, c = True)
def HotKey_RotationTool_P():
    mel.eval('buildRotateMM')
def HotKey_RotationTool_R():
    mel.eval('destroySTRSMarkingMenu RotateTool')
