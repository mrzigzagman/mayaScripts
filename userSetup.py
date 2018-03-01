# Start Up Template - Maya Startup Execution
import maya.utils
import imp
import sys
import maya.cmds as cmds

'Core Items to import on startup. Place this under maya/2016/scripts'

def Startup():
	print '''
	Custom Startup
	'''

	sScriptPath = '/usr/home//dyabu/Personal/MayaScripts'


	# Custom Tool : MayaBGColour
	MayaBGColour = imp.load_source('MayaBGColour', '%s/MayaBGColour.v8.0.0.py'%sScriptPath)
	MayaBGColour.main()


	# Custom Tool : OpenTool
	OpenSaveTool = imp.load_source('OpenSaveTool', '%s/OpenSaveTool.v8.0.0.py'%sScriptPath)
	OpenSaveTool.main()






	# print 'Execution StartUp Procedure'

	#try:
	#    import todo
	#    todo.MainWindow()
	#except Exception as e:
	#    print e


	# Custom Tool : TimeLogger
	try:
		import os.path
		import timetrack
		mon = timetrack.ctrl.Monitor()
		mon.set_note(os.path.expandvars("/$FILM/$TREE/$SCENE/$SHOT"))
		mon.start()
	except Exception as e:
		print e

	# Move timeline to provided frame range.
	#try:
	#    from mo.vm.utils.sceneRange import setSceneRange
	#    setSceneRange(handles = True)
	#except Exception as e:
	#    print e


sys.path.append('/weta/prod/motion/work/jdixon/python')
cmds.scriptJob(ie = Startup, ro = True)
