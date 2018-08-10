# This script runs second. (First : NukeCreator_FileCreator.py)

import nuke
import sys


# Modules to pass info from NukeCreator_Creator.py
import base64
try:
	import cPickle as pickle
except ImportError:
	import pickle
dShotInfo = pickle.loads(base64.b64decode(sys.argv[1]))


sScript = '/proj/uap/shots/0571gr/0140/motion/work/maya/dyabu/Images/PB/1/TEMP.nk'

inputSeq = '/proj/uap/shots/0571gr/0140/render/motion/images/s0571gr_0140_previewRender_v2/s0571gr_0140_previewRender_v2.####.exr '
outSeq =   '/proj/uap/shots/0571gr/0140/motion/work/maya/dyabu/Images/PB/1/PlayBlast_1.####.jpg'
startFrame = 1009
endFrame = 1049
fGamma = 1.0

nuke.scriptClear()


oRead = nuke.createNode('Read')
oRead["file"].fromUserText("{} {}-{}".format(inputSeq, startFrame, endFrame))


#oGrade = nuke.createNode("Grade")
#oGrade['gamma'].setValue(float(fGamma))
#oColourSpace = nuke.createNode('Colorspace')
#oColourSpace['colorspace_out'].setValue('sRGB')
oWrite = nuke.createNode('Write')
#oWrite = ['file'].fromUserText('{} {}-{}'.format(outSeq, startFrame, endFrame))
oWrite['file'].fromUserText(outSeq)
oWrite['file_type'].setValue('jpg')
#oWrite['jpg_quality'].setValue(1)

# if video is loaded.
startFrame = oRead['origfirst'].value()
endFrame = oRead['origlast'].value()

#find and get 1st view
view = (oWrite['views'].value() or '').split(' ')[:1]

nuke.execute(oWrite, int(startFrame), int(endFrame), views = view)

#oGrade.setInput(0, oRead)
#oColourSpace.setInput(0, oGrade)
oWrite.setInput(0,oRead)
#oWrite.setInput(0,oColourSpace)


nuke.scriptSaveAs(dShotInfo['FilePath'])
nuke.scriptExit()



sys.exit(0) # Stops running from this point on.




##################
sScript = '/proj/uap/shots/0571gr/0140/motion/work/maya/dyabu/Images/PB/1/TEMP.nk'

inputSeq = '/proj/uap/shots/0571gr/0140/motion/work/maya/dyabu/Images/PB/3/PlayBlast_3.####.jpg'
outSeq =   '/proj/uap/shots/0571gr/0140/motion/work/maya/dyabu/Images/PB/1/PlayBlast_1.####.jpg'
startFrame = 1009
endFrame = 1009
gamma = 1


sAll ='''
#import os
import re
#import sys
#import os.path
#import argparse
import nuke


nuke.scriptClear()

oRead = nuke.createNode('Read')


oRead["file"].fromUserText("{} {}-{}")


oGrade = nuke.createNode("Grade")
oGrade['gamma'].setValue(1)
oColourSpace = nuke.createNode('Colorspace')
oColourSpace['colorspace_out'].setValue('sRGB')
oWrite = nuke.createNode('Write')
oWrite = ['file'].fromUserText({})

# connect nodes
oGrade.setInput(0, oRead)
oColourSpace.setInput(0, oGrade)
oWrite.setInput(0,oColourSpace)

#find and get 1st view
view = (oWrite['views'].value() or '').split(' ')[:1]

# just for when loading video
startFrame = oRead['origfirst'].value()
endFrame = oRead['origlast'].value()

nuke.execute(oWrite, int(startFrame), int(endFrame), views = view)
	'''.format(inputSeq, inputSeq, startFrame, endFrame, inputSeq, outSeq)
