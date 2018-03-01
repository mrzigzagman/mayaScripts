# Cycle through existing Sound. v0.0.3
import maya.cmds as cmds
import maya.mel as mel
def main():
	# Get List of Audios in the scene.
	aAudio = [str(a) for a in cmds.ls(typ = 'audio')]

	# Get Currently Active Sound
	aPlayBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
	sAudio = cmds.timeControl(aPlayBackSlider, q = True, s = True)

	aSetting = []
	if aAudio:
		if sAudio:
			iIndex = aAudio.index(sAudio)
			if len(aAudio) > iIndex+1:
				aSetting = [aAudio[iIndex+1], True, aAudio[iIndex+1]]
			else:
				aSetting = [sAudio, False, 'OFF']
		else:
			aSetting = [aAudio[0], True, aAudio[0]]

		cmds.timeControl(aPlayBackSlider, e = True, sound = aSetting[0], displaySound = aSetting[1] )
		cmds.warning(' 	[Audio]	%s'%aSetting[2])
