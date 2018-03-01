import subprocess
import os
import os.path


import base64
try:
	import cPickle as pickle
except ImportError:
	import pickle



fNukeCreatorFile = os.path.join(os.path.dirname(__file__), "NukeCreator_Customizer.py")

# Getting Shot Number - StudioSettings.py
import imp
sScriptName = 'StudioSettings' # remove '.py'
sScriptPath = '/vol/transfer/dyabu/Scripts/mayaScripts/%s.py' % sScriptName
StudioSettings = imp.load_source(sScriptName, sScriptPath)

# Getting info using StudioSettings
aShotInfo = StudioSettings.ShotInfo(1,0) # (1,1) = (Folder Creation, Print paths.)


def main():

	# Weta paths 1/1
	dShotInfo = {
		"FilePath": "/%s/shots/%s/%s/motion/work/maya/dyabu/Images/Nuke/TheNukeFile.nk"%(aShotInfo[2], aShotInfo[4], aShotInfo[3]),
		'ShotNumber': "  %s %s"%(aShotInfo[4], aShotInfo[3])
		}

	# Using sys.argv to pass info of shot number to NukeCreator2.py.
	command = 'nuke -t -- "%s" "%s"' % (fNukeCreatorFile, base64.b64encode(pickle.dumps(dShotInfo))) # import pickle & base64
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
		# os.system('nuke %s &' % dShotInfo['FilePath'])

		print 'Processed',
