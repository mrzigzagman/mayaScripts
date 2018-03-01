# Plot Controllers v005.2.5
# On Custom Nulls
import maya.cmds as cmds

K = cmds.getModifiers()
iIn = int(cmds.playbackOptions(q = True, minTime = True))
iOut = int(cmds.playbackOptions(q = True, maxTime = True))

def MessageBox(Message):
	'''Displaying Entered Message as Popup '''
	window = cmds.window(title = 'Message Box')
	cmds.columnLayout(adjustableColumn = True)
	cmds.text('\n\t%s\t\n' % Message)
	cmds.button(label = 'Close', command = ('cmds.deleteUI(\"'+window+'\",window = True)'))
	cmds.setParent('..')
	cmds.showWindow(window)


def CustomParentConstraint(oSrc, oFollow, sConst = 'TempConst'):
	''' Apply parent constraint on keyable axis only.'''

	aSkipTrans = ['x','y','z']
	aSkipRot = ['x','y','z']
	# To be added : feature that supports only one axis to constraint.
	aList = [ 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']


	aConstList = [str(c) for c in cmds.listAttr(oFollow, keyable = True)]

	for c in aConstList:
		for l in aList:
			if l == c:
				if 'translate' in c:
					aSkipTrans.remove(c[-1].lower())
				else:
					aSkipRot.remove(c[-1].lower())


	cmds.parentConstraint(oSrc, oFollow, weight = 1, n = sConst, st=aSkipTrans, sr = aSkipRot)


# Get Shape Node of a DAG obj
def getShapeNodes(obj):
	howManyShapes = 0
	getShape = cmds.listRelatives(obj, shapes=True)
	if(getShape == None):
		print 'ERROR:: getShapeNodes : No Shape Nodes Connected to ' + obj + ' /n'
	else:
		howManyShapes = len(getShape[0])
	return (getShape, howManyShapes)


def ChangeColour(oSel, aColour):
	for o in oSel:
		cmds.setAttr("%s.overrideEnabled"%o, 1)
		cmds.setAttr ("%s.overrideColor"%o , aColour)

		if cmds.objExists("%sShape.overrideEnabled"%o):
			cmds.setAttr("%sShape.overrideEnabled"%o, 1)
			cmds.setAttr("%sShape.overrideColor"%o , aColour)

		if cmds.objExists("%s_CRVShape.overrideEnabled"%o):
			cmds.setAttr("%s_CRVShape.overrideEnabled"%o, 1)
			cmds.setAttr("%s_CRVShape.overrideColor"%o , aColour)


def ApplyConst(oSrc, oFollow):

	if 'Plot' in oFollow:
		sConst = oFollow+'Const'
	else:
		sConst = NamespaceToggle(oFollow)+'Const'

	aSkipTrans = ['x','y','z']
	aSkipRot = ['x','y','z']
	# To be added : feature that supports only one axis to constraint.
	aList = [ 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']


	aConstList = [str(c) for c in cmds.listAttr(oFollow, keyable = True)]

	for c in aConstList:
		for l in aList:
			if l == c:
				if 'translate' in c:
					aSkipTrans.remove(c[-1].lower())
				else:
					aSkipRot.remove(c[-1].lower())


	cmds.parentConstraint(oSrc, oFollow, weight = 1, n = sConst, st=aSkipTrans, sr = aSkipRot)



def NamespaceToggle(sCtl):
	# Switches colon to underscore and vice versa
	if '__' in sCtl:
		sNew = sCtl.replace('__', '_:')[:-5]
	else:
		sNew = sCtl.replace(':', '_')+'_Plot'
	return sNew


oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
if K == 0:
	sString = '''
	- SELECTION -
	Toggle Selection Between Plot Null / CTL ----- ALT [8]
	Filter Constrained CTL ----------- SHIFT + CTL [5]
	Filter Non Constrained CTL ----- SHIFT + ALT [9]


	- CONSTRAINT -
	Apply '_PlotConst' to '_Plot' ----- CTL [4]
	Delete '_PlotConst' ------------- SHIFT [1]


	- PLOT -
	Apply Plot and Constraint ----- CTL + ALT [12]

	Create Camera Aimed Control ------ SHIFT CTL ALT [13]  '''
	MessageBox(sString)





elif K == 5: # S + C
	aList = []
	for o in oSel:
		sConst = NamespaceToggle(o)
		if 'Plot' in o:
			sConst = o+'Const'
		else:
			sConst = o+'_PlotConst'

		if cmds.objExists(sConst):
			aList.append(o)
	cmds.select(cl = True)
	if aList:
		cmds.select(aList, r = True)
elif K == 9: # S + A
	aList = []
	for o in oSel:
		sConst = NamespaceToggle(o)
		if 'Plot' in o:
			sConst = o+'Const'
		else:
			sNull = o+'_Plot'
			if cmds.objExists(sNull):
				sConst = o+'_PlotConst'
			else:
				sConst = 'DoNotFindThis'

		if not cmds.objExists(sConst):
			aList.append(o)

	cmds.select(cl = True)
	if aList:
		cmds.select(aList, r = True)

elif K == 8: # Alt
	aSelList = []
	aSel = oSel[:]
	# Create Plot Nulls
	for o in aSel:
		if not '__' in o:
			if not '_Plot' in o:
				oObj = NamespaceToggle(o)
		if not cmds.objExists(oObj):
			cmds.spaceLocator(name = oObj)
			cmds.parentConstraint(o, oObj, weight = 1, n = 'TempConst')
			cmds.delete('TempConst')




	for o in aSel:
		sObj = NamespaceToggle(o)
		if cmds.objExists(sObj):
			aSelList.append(sObj)
	cmds.select(aSelList, replace = True)
elif K == 4: # Ctrl # Apply Constraint
	aSelList = []
	for o in oSel:

		if not '__' in o:
			if not '_Plot' in o:
				oObj = NamespaceToggle(o)
		if not cmds.objExists(oObj):
			cmds.spaceLocator(name = oObj)
			cmds.parentConstraint(o, oObj, weight = 1, n = 'TempConst')
			cmds.delete('TempConst')


		if '_Plot' in o:
			oObj =NamespaceToggle(o)
		else:
			if cmds.objExists(NamespaceToggle(o)):
				oObj = o

		if not oObj in aSelList:
			aSelList.append(oObj)

	for l in aSelList:
		ApplyConst(NamespaceToggle(l),l)


elif K == 1: # Shift # Remove COnstraints
	aSelList = []
	for o in oSel:
		if '_Plot' in o:
			sConst = o+'Const'
		else:
			sConst = NamespaceToggle(o)+'Const'

		if cmds.objExists(sConst):
			cmds.delete(sConst)
elif K == 12: # Ctl + Alt


	aPlotList = []
	# Create Plot Nulls
	for o in oSel:

		if '__' in o:
			sCtl = NamespaceToggle(o)
			if not sCtl in aPlotList:
				aPlotList.append(sCtl)

		else:
			if not o in aPlotList:
				aPlotList.append(o)
			if not '_Plot' in o:
				sNull = NamespaceToggle(o)

				if not cmds.objExists(sNull):
					cmds.spaceLocator(name = sNull)


	for s in aPlotList:

		sNull = NamespaceToggle(s)
		sConst = sNull+'Const'

		cmds.parentConstraint(s, sNull, weight = 1, n = 'TempConst')


		cmds.refresh(su = True)

		cmds.bakeResults(sNull, t = (iIn,iOut), simulation = True )
		cmds.delete('TempConst')

		cmds.refresh(su = False)

		ApplyConst(sNull, s)


	cmds.select(cl = True)
	restoreLayout('Custom_AnimWithCam')

elif K == 13: # Ctl + Alt + Shift # Special Plot
	if not oSel:
		cmds.warning(' Please Select an obj first.')
	else:
		oCamera = ''
		oPanel = cmds.getPanel(wf = True)

		if 'modelPanel' in oPanel:
			oCamera = cmds.modelEditor(oPanel, q = True, camera = True).split('Shape')[0]
			if not cmds.objExists(oCamera):
				cmds.warning('View not selected!!')

		print 'Camera : ', oCamera
		if oCamera:
			aPlotList = []
			# Create Plot Nulls
			for o in oSel:
				if '_Plot' in o:
					aPlotList.append(o)
				else:
					o = NamespaceToggle(o)
					if not cmds.objExists(o):
						cmds.spaceLocator(name = o)
					if not o in aPlotList:
						aPlotList.append(o)


			for p in aPlotList[:]:
				oPlot = p
				oPlotZ = p+'_Zero'
				oPlotR = p+'_Root'
				oCamAim = p+'_CamAim_Anim'
				oCamAimZ = p+'_CamAim'

				s = NamespaceToggle(p)

				cmds.rename(oPlot , oPlotR)
				# Set Look and Hiearachy.
				aHiearachy  = [oPlot, oPlotZ, oCamAim, oCamAimZ, oPlotR]
				aVisibility = [1,0,1,0,0]
				aColourList = [13, 1, 22, 1, 1]

				for n in [oPlot, oPlotZ, oCamAimZ]:
					if cmds.objExists(n):
						cmds.delete(n)
					cmds.spaceLocator(name = n)

				if cmds.objExists(oCamAim):
					cms.delete(oCamAim)
				cmds.curve(n = oCamAim, d=1, p=[(-0.5, 0, 0),(-0.5, 0, 2),(-2, 0, 2),(0, 0, 4),(2, 0, 2),(0.5, 0, 2),(0.5, 0, 0),(0.5, 0, -2),(2, 0, -2),(0, 0, -4),(-2, 0, -2),(-0.5, 0, -2),(-0.5, 0, 0)])

				sShape = getShapeNodes(oCamAim)[0][0]
				cmds.rename(sShape, oCamAim+'Shape')

				print aHiearachy
				for i in range (0, len(aHiearachy)):
					if not i == len(aHiearachy)-1:
						cmds.parent(aHiearachy[i], aHiearachy[i+1])
						cmds.setAttr(aHiearachy[i]+'.rotate', *[0,0,0])
						cmds.setAttr(aHiearachy[i]+'.translate', *[0,0,0])
					cmds.setAttr("%sShape.visibility"%aHiearachy[i], aVisibility[i])

					ChangeColour([aHiearachy[i]], aColourList[i])


				aPlotList = [oCamAimZ, oPlotZ, oPlotR]



				# Original Plot and Const
				sNull = NamespaceToggle(s)

				aConstraints = ['TempConst', 'TempCamAimConst', 'TempCounterConst']
				for c in aConstraints:
					if cmds.objExists(c):
						cmds.delete(c)


				CustomParentConstraint(s, oPlotR, aConstraints[0])
				cmds.aimConstraint(oCamera, oCamAimZ, weight = 1, n = aConstraints[1], aimVector = (0, 0, 1,))
				CustomParentConstraint(oPlotR, oPlotZ, aConstraints[2])

				cmds.refresh(su = True)
				cmds.bakeResults(aPlotList, t = (iIn,iOut), simulation = True, at =  [ 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ'])
				cmds.refresh(su = False)


				for c in aConstraints:
					cmds.delete(c)

				ApplyConst(sNull, s)


			cmds.select(cl = True)
			#restoreLayout('Custom_AnimWithCam')
