import maya.cmds as cmds
import subprocess
import os
import os.path
import imp
import base64
try:
	import cPickle as pickle
except ImportError:
	import pickle

# vvv 1/1

fNukeCreatorFile = os.path.join(os.path.dirname(__file__), "NukeCreator_Customizer.py")

# Getting Shot Number - StudioSettings.py
sScriptName = 'StudioSettings' # remove '.py'
sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts/%s.py' % sScriptName
StudioSettings = imp.load_source(sScriptName, sScriptPath)

# Getting info using StudioSettings
dShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)

# vvv paths 1/1
dShot = {
	"FilePath": "/%s/shots/%s/%s/motion/work/maya/dyabu/Images/Nuke/TheNukeFile.nk"%(dShotInfo['sProject'], dShotInfo['sSeqNumber'], dShotInfo['sShotNumber']),
	'ShotNumber': "  %s %s"%(dShotInfo['sSeqNumber'], dShotInfo['sShotNumber'])
	}

def main():
	if not os.path.exists(dShot['FilePath']):
		# Using sys.argv to pass info of shot number to NukeCreator2.py.
		command = 'nuke -t -- "%s" "%s"' % (fNukeCreatorFile, base64.b64encode(pickle.dumps(dShot))) # import pickle & base64
		# -t : runs in terminal mode
		# -- : tells nuke that not to pick up information from that point on.
		# anything after -- will be stored in sys.argv
		# pickle stores data into strings.
		# base64 combines info into one. (in this case, a dictionary(non string) to pass through to sys.argv)


		# For testing:
		#print sys.argv[1] # System variable cross softwares. List and String. sys.argv[0] is Self.


		try:
			process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			while True:
				line = process.stdout.readline()
				if not line:
					break
				print line,
			err = process.stderr.read()  # Collects "Standard errors" (incl. exceptions.)
			if process.returncode:  # gets code of what has returned. if 0, no errors. ohter, with error(s)of some kind.
				raise Exception(err)
			else:
				print err # includes "Warnings" Here.
		finally:
			pass


	if os.path.exists(dShot['FilePath']):
		os.system('nuke %s &' % dShot['FilePath'])
		aPrint = ['9bbcf2', 'Opening NUKE', 0x485872] # Blue
		cmds.inViewMessage(amg = '<text style="color:#%s";>%s</text>'%(aPrint[0], aPrint[1]), pos = 'topCenter', fade = True, fts = 12, ft = 'arial',bkc = aPrint[2] )
