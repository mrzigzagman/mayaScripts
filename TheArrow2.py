# Arrow Custom Rig v0.0.16
# W V
import maya.cmds as cmds
import maya.mel as mel

def ReStructure(fCurve, fName, fAtrList, fColour):
    global oCurve, sName, aParent
    cmds.setAttr("%s.overrideEnabled"%fCurve, 1)
    cmds.setAttr ("%s.overrideColor"%fCurve , fColour)
    cmds.rename(fCurve, fName)

    if fAtrList:
        for atr in fAtrList:
            cmds.setAttr(fName+atr, lock = True)

    aParent.append(fName)
    oCurve = None

def FindArrowNum(sSel):
    sNum = None
    if 'PUP' in sSel:
        if ':' in sSel:
            sNum = sSel.split('PUP')[1].split(':')[0]
    elif 'Arrow' in sSel:
        if '_' in sSel:
            sNum = sSel.split('Arrow')[1].split('_')[0]
    return sNum


### Start ###
oSel = [str(o) for o in cmds.ls(o = True, sl = True)]

K = cmds.getModifiers()
sMenu = '''
	----- ALT [8]
	----- CTL [4]
	----- SFT [1]
	----- CTL + SFT [5]
	----- ALT + SFT [9]
	----- CTL + ALT [12]
	----- CTL + ALT + SFT [13]'''

## PREP ##
aList = ['Curve']
for l in aList:
    if not cmds.objExists(l):
        cmds.createDisplayLayer(name = l, number = 1, nr = True)


## Start ##
if K == 8:
    sNum = FindArrowNum(oSel[0])
    if not sNum == None:
        sSelect = 'Arrow%s_PathFollow'%sNum
        if cmds.objExists(sSelect):
            cmds.select(sSelect)

    iFrame = cmds.keyframe('Arrow%s_MotionPath'%sNum, q=True,index=(1,1))[0]
    cmds.currentTime(iFrame)
if K == 12:
    sNum = FindArrowNum(oSel[0])
    if not sNum == None:
        cmds.select('PUP%s:hitJig_ctrl'%sNum)


elif K == 4:
    sNum = FindArrowNum(oSel[0])
    if not sNum == None:
        sSelect = 'Arrow%s_Custom'%sNum
        if cmds.objExists(sSelect):
            cmds.select(sSelect)

elif K == 1:
    sNum = FindArrowNum(oSel[0])
    if not sNum == None:
        sSelect = 'Arrow%s_Angle'%sNum
        if cmds.objExists(sSelect):
            cmds.select(sSelect)

elif K == 12:
    sNum = FindArrowNum(oSel[0])
    if not sNum == None:
        sSelect = 'Arrow%s_Anim'%sNum
        if cmds.objExists(sSelect):
            cmds.select(sSelect)

elif K == 13:
    if 'weaponsLongbowArrow' in oSel[0]:
        if 'PUP' in oSel[0]:
            sNum = oSel[0].split(':')[0].split('PUP')[1]


            aParent = []
            sName = 'Arrow%s_Root'%sNum
            oCurve = cmds.circle( c = (0, 0, 0), nr = (0, 1, 0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1)
            ReStructure(oCurve[0], sName, ['.tx','.ty','.tz','.rx','.ry','.rz'], 1)


            sName = 'Arrow%s_Custom'%sNum
            oCurve = cmds.circle( c = (0, 0, 0), nr = (0, 1, 0), sw = 360, r = 24, d = 3, ut = 0, tol = 0.01, s = 8, ch = 1)
            ReStructure(oCurve[0], sName, ['.rx','.rz'], 3)
            #cmds.editDisplayLayerMembers(aList[0], sName, noRecurse = True)


            sName = 'Arrow%s_Angle'%sNum
            oCurve = cmds.curve(d=1, p=[(0, -0.8, -4),(0, -0.8, -170),(0, 0.8, -170),(0, 0.8, -4),(0, 0.8, -2),(0, 2, -2),(0, 0, 0),(0, -2, -2),(0, -0.8, -2),(0, -0.8, -4)]);
            ReStructure(oCurve, sName, ['.tx','.ty','.tz','.ry','.rz'], 3)

            sName = 'Arrow%s_Curve'%sNum
            oCurve = mel.eval('curve -bezier -d 3 -p -0 0 0 -p 0 13.048 -279.503     -p 0 -74.966 -1366.459     -p 0 -184.085 -2037.556     -p 0 -286.395 -2666.774      -p 0 -620.206 -3815.093     -p 0 -907.357 -4517.515 -k 0 -k 0 -k 0 -k 1 -k 1 -k 1 -k 2 -k 2 -k 2 ;')
            ReStructure(oCurve, sName, [], 3)
            cmds.editDisplayLayerMembers('Curve',sName, noRecurse = True)

            sName = 'Arrow%s_PathFollow'%sNum
            oCurve = cmds.curve(d=1, p=[(-0.8, 0, -4),(-0.8, 0, -170),(0.8, 0, -170),(0.8, 0, -4),(0.8, 0, -2),(2, 0, -2),(0, 0, 0),(-2, 0, -2),(-0.8, 0, -2),(-0.8, 0, -4)]);
            ReStructure(oCurve, sName, [], 3)

            sName = 'Arrow%s_Anim'%sNum
            oCurve = cmds.curve(d=1, p=[(-0.9, 0, -4.1),(-0.9, 0, -170.1),(0.9, 0, -170.1),(0.9, 0, -4.1),(0.9, 0, -2.1),(2.1, 0, -2.1),(0, 0, 0),(-2.1, 0, -2.1),(-0.9, 0, -2),(-0.9, 0, -4.1)]);
            ReStructure(oCurve, sName, [], 4)


            sName = 'Arrow%s_Const'%sNum
            oCurve = cmds.curve(p = [(1,0,-1),(1,0,1),(-1,0,1),(-1,0,-1)]);
            cmds.setAttr("%s.translateZ"%oCurve, -172)
            ReStructure(oCurve, sName, ['.tx','.ty','.tz','.rx','.ry','.rz'], 4)


            print aParent
            for i in range(0, len(aParent)):
                if '_PathFollow' in aParent[-i-1]:
                    cmds.select('Arrow%s_PathFollow'%sNum, r = True)
                    cmds.select('Arrow%s_Curve'%sNum, tgl = True)
                    oMotionPath = mel.eval('pathAnimation -fractionMode true -follow true -followAxis z -upAxis y -worldUpType "vector" -worldUpVector 0 1 0 -inverseUp false -inverseFront true -bank false -endTimeU 1104 -startTimeU  1103;')
                    cmds.rename(oMotionPath, 'Arrow%s_MotionPath'%sNum)
                if not i == len(aParent)-1:
                    if i == 2:
                        cmds.parent(aParent[-i-1], aParent[0])
                    else:
                        cmds.parent(aParent[-i-1], aParent[-i-2])
                    print i, aParent[-i-1], aParent[-i-2]


            cmds.parentConstraint('Arrow%s_Const'%sNum, 'PUP%s:root_ctrl'%sNum)

            # FCurves
            iFrame = int(cmds.currentTime(q = True))
            cmds.keyframe('Arrow%s_MotionPath'%sNum, edit=True,index=(1,1),timeChange = iFrame)
            cmds.keyframe('Arrow%s_MotionPath'%sNum, edit=True,index=(0,0),timeChange = iFrame-1)
            cmds.keyTangent('Arrow%s_MotionPath'%sNum, itt='linear', time=(1000, 1500) )
            cmds.keyTangent('Arrow%s_MotionPath'%sNum, ott='linear', time=(1000, 1500) )

            # Pass Through
            #cmds.keyframe('Arrow%s_MotionPath'%sNum, edit=True,index=(0,0),valueChange = 0.127)
            #cmds.keyframe('Arrow%s_MotionPath'%sNum, edit=True,index=(1,1),valueChange = 0.0842)
            #cmds.setInfinity('Arrow%s_MotionPath.u'%sNum, pri='cycleRelative', poi='cycleRelative' )

            # HIT
            cmds.keyframe('Arrow%s_MotionPath'%sNum, edit=True,index=(0,0),valueChange = 0.0428)
            cmds.keyframe('Arrow%s_MotionPath'%sNum, edit=True,index=(1,1),valueChange = 0.0)
            cmds.setInfinity('Arrow%s_MotionPath.u'%sNum, pri='cycleRelative', poi='constant')
            cmds.setKeyframe('PUP%s:hitJig_ctrl.HitJiggle'%sNum)
            cmds.setAttr("PUP%s:hitJig_ctrl.HitJiggle"%sNum, 0)


            # Custom
            cmds.setAttr("Arrow%s_Angle.rotateX"%sNum, 45)
            cmds.setAttr("Arrow%s_Custom.rotateY"%sNum, 180)
            cmds.setAttr("Arrow%s_Custom.translate"%sNum,*[-136.769, 747.933, 2747.617])
            cmds.select("Arrow%s_Custom"%sNum, r = True)
