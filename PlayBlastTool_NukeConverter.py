# This script runs second. (First : NukeCreator_FileCreator.py)

import nuke
import sys

 
# Modules to pass info from NukeCreator_Creator.py
import base64
try:
	import cPickle as pickle
except ImportError:
	import pickle
dConvertInfo = pickle.loads(base64.b64decode(sys.argv[1]))




inputSeq = dConvertInfo[0]
outSeq =  dConvertInfo[1]
startFrame = dConvertInfo[2]
endFrame = dConvertInfo[3]
fGamma = dConvertInfo[4]

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


#nuke.scriptSaveAs('FilePath')
nuke.scriptExit()



sys.exit(0) # Stops running from this point on.
