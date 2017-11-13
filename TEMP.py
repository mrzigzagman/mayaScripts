# Camera space Manipultor
import maya.cmds as cmds



def main():
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
