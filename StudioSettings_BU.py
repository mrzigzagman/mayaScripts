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



    iAvoidRunFromNewScene = 0 # Studio Dependant : Switch this on if os.getcwd does not return. Proj/Seq/Shot numbers.

    #-----

    aReturn = []

    sUser = getpass.getuser()

    # Scene Paths
    sShotPath = os.getcwd() # Getting environment. Essential to get this including Proj, Seq, Shot numbers.
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

    # Weta structure 2/2 : fixing error : doesn't read /Proj
    aScenePath = sScenePath.split('/')
    if not aScenePath[1] == 'proj':
        aScenePath.insert(1, 'proj')
        sScenePath = '/'.join(aScenePath)

    # Custom Scene Folder structure
    aPath = [   '/Scenes', # Do not change the index of aPath[0]
                '/Scenes/Old',
                '/Exports',
                '/Images/Refs',
                '/Images/PB',
                '/Images/PB/1',
                '/Images/PB/2',
                '/Images/PB/3',
                '/Images/PB/4',
                '/Images/Nuke',]


    if iAvoidRunFromNewScene:
        aReturn = []
        print 'This will only work from a saved scene.'
    else:
        # Create Folder structure
        if iFolder:
            # Check Folders existance


            for a in aPath:
                if not os.path.isdir(sScenePath + a):
                    os.makedirs(sScenePath + a)
                    if iPrint: print 'Directory Created : %s '%(sScenePath + a)
                else:
                    if iPrint: print 'Directory Existed : %s '%(sScenePath + a)


        # Shot / Seq Numbers
        sProject = sScenePath.split('/')[2]
        sSeqNumber = sScenePath.split('/')[4]
        sShotNumber = sScenePath.split('/')[5]

        # Personal Folder
        sPersonalFolder = '/usr/home/%s'%sUser

        # Playblast Folders
        sPlayBlastToolPath = sPersonalFolder + '/Project/%s/RV/%s%s/'%(sProject, sSeqNumber, sShotNumber) # where .rv files go
        sPlayBlastSeqPath = sScenePath + aPath[4] # where the actual playblast files go.

        sScenePath += aPath[0] # Keep this at the very end to have '/Scenes' added at the end

        if iFolder:
            if not os.path.isdir(sPlayBlastToolPath):
                os.makedirs(sPlayBlastToolPath)
                if iPrint: print 'Directory Created : %s '%(sPlayBlastToolPath)
            else:
                if iPrint: print 'Directory Existed : %s '%(sPlayBlastToolPath)


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
                        sMayaScriptFolder,])


        # Path Existance Check
        for i, path in enumerate(aReturn[:]):
            if '/' in path:
                if not os.path.exists(path):
                    print path
                    aReturn[i] = 'Path Does Not Exists'



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
            print '-------------------------------------'

        sShotgunPage = ''
        sShotWebPage = ''

    return aReturn

def OSFileBrowserCommand(sPath):
    import os
    # FileBrowser command
    sBrowserCommand = 'dolphin'
    #sBrowserCommand = 'nautilus'

    os.system('%s %s &'%(sBrowserCommand, sPath))

def StudioProductionFrameRange():
    # IF studio Range Tool don't exist, set to 0:
    iStudioTool = 1
    if iStudioTool:
        from mo.wm.utils.sceneRange import setSceneRange; setSceneRange(handles = True)

    return iStudioTool


def OpenSceneCommand(sPath, bForce = False):
    # Load Scene command

    # [ Option 1 ] Maya Default
    #cmds.file(sPath, o = True, f = bForse)

    # [ Option 2 ] W
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
    # 2. Re0wirtes (if dDict is entered.)
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
