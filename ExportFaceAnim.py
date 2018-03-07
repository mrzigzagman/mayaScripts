# Export face anim. v0.1.0
# Able to COpy anim 0 = target / -1 = source
import maya.cmds as cmds
import maya.mel as mel

def main():
	oSel = [str(o) for o in cmds.ls(sl = True, o = True)]
	# Creating AnimTool Group Node
	sAnimToolsGrp = 'ANIM_TOOLS'
	if not cmds.objExists(sAnimToolsGrp):
		cmds.createNode('transform', n = sAnimToolsGrp)

	sFaceCtlGrp = 'FaceControls'
	if not cmds.objExists(sFaceCtlGrp):
		cmds.createNode('transform', n = sFaceCtlGrp, p = sAnimToolsGrp)

	K = cmds.getModifiers()

	if not K:

		aCtlList = []
		if oSel:
			print 1
			for sel in oSel:

				sModel = sel.rpartition(':')[0]
				if sModel[-2:-1].isdigit():
					sNum = sModel[-2:-1]
				elif sModel[-1].isdigit():
					sNum = sModel[-1]
				else:
					sNum = ''
				sFace = 'FACE%s:FacialActionControl'%sNum
				if cmds.objExists(sFace):

					aAttrList = cmds.listAttr(sFace, v = True, k = True)

					sFaceNull = sFace + '_Export'

					# Delete previous Copy Null

					if cmds.objExists(sFaceNull):
						cmds.delete(sFaceNull)
					# Hide transforms
					cmds.createNode('transform', n = sFaceNull, p = sFaceCtlGrp)
					for b in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v', ]:
						print '%s.%s'%(sFace,b)
						cmds.setAttr('%s.%s'%(sFaceNull,b), keyable = False, channelBox = False)

					#Logic starts Here
					for a in aAttrList:
						# separate all Locked attr with "Fr..."
						iLock = 0
						if a[:2] == 'fr':
							iLock = 1

						# Create Attr on Copy Null
						cmds.addAttr(sFaceNull, longName = a, attributeType = 'float', w = True, r = True, k = True)
						cmds.setAttr(sFaceNull+'.'+a, cb = True, l = iLock)


						if not iLock:
							# If animated:
							if cmds.keyframe(sFace, attribute = a, sl = False, q = True, tc = True):
								cmds.copyKey(sFace, at = a)
								cmds.pasteKey(sFaceNull, connect = True, at = a)

							# Copy Value if not.
							else:
								iVal = cmds.getAttr('%s.%s'%(sFace, a))
								cmds.setAttr('%s.%s'%(sFaceNull, a ), iVal)

					print aAttrList
		else:
			print "Select a Controller"

	else:
		sSource = sSel[-1]
		sTarget = oSel[0]

		for a in cmds.listAttr(sSource, v = True, u = True):
			# If animated:
			if cmds.keyframe(sSource, attribute = a, sl = False, q = True, tc = True):
				if cmds.listAttr(sTarget, v = True, k = True, c = True):
					print a
					cmds.copyKey(sSource, at = a)
					cmds.pasteKey(sTarget, connect = True, at = a)
