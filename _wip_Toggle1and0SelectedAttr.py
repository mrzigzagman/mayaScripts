import maya.cmds as cmds

oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
oChannel = [str(s) for s in cmds.channelBox('mainChannelBox', q = True, sma = True)]


if oSel:
    for o in oSel:
        if oChannel:
            iVal = cmds.getAttr('%s.%s'%(o, oChannel[0]))
            iVal = 0 if int(iVal) else 1

            for c in oChannel:
                cmds.setAttr('%s.%s' % (o,c) , iVal)
