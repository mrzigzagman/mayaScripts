# Select CTL from fCurve selection Tool v003
import maya.cmds as cmds

aObjList = [str(s) for s in cmds.selectionConnection('graphEditor1FromOutliner', q = True, object = True)]
aCurveList = [str(s) for s in cmds.keyframe(query = True, name = True)]

aSelectList = []
for o in aObjList:
    if not o in aSelectList:
        for c in aCurveList:
            sObj = '_'.join(c.split('_')[:-1])

            if sObj in o:
                aSelectList.append(o)

cmds.select(aSelectList, r = True)
