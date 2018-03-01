# Re-Number Sequenced files. v0.2.0
# 1) the Directory should only contain One Sequenced

import os
# Full path

aList = [   ['/mll/shots/ate/1320/motion/work/maya/dyabu/Images/Refs/001.Wrist/Take3/','PlayBlast_2', 0001],
            ['/mll/shots/ate/1320/motion/work/maya/dyabu/Images/Refs/001.Wrist/Take3/','PlayBlast_2', 0001],
            ['/mll/shots/ate/1320/motion/work/maya/dyabu/Images/Refs/001.Wrist/Take3/','PlayBlast_2', 0001],
            ]

i = 0

sPath = aList[i][0]
sFile = aList[i][1]
iStartFrame = aList[i][2]

aFiles = os.listdir(sPath)

aFiles.sort()
if aFiles:
    for f in aFiles[:]:
        aFileName = f.split('.')
        if len(aFileName) >= 4:
            aFileName = ['.'.join(aFileName[:-3]), aFileName[-2], aFileName[-1]]

        aFileName[0] = sFile + '_'
        sFileName = '.'.join(aFileName)
        os.rename(sPath + f, sPath + sFileName)

aFiles = os.listdir(sPath)
aFiles.sort()
if aFiles:
    for i, f in enumerate(aFiles[:]):
        aFileName = f.split('.')
        aFileName[0] = aFileName[0][:-1]
        aFileName[1] = str(i + iStartFrame).zfill(4)
        sFileName = '.'.join(aFileName)
        os.rename(sPath+f, sPath+sFileName)
