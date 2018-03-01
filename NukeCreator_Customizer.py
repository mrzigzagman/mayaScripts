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


#### Creating BackdropNode ###
sNodeParent = 'colNodeParent'

# iWidth = 100
# iHeight = 100
# iPad = 10

# def p(col, row, width, height, pad=0):
# 	return [
# 		col*iWidth-pad*iPad,
# 		row*iHeight-pad*iPad,
# 		width*iWidth+pad*iPad*2,
# 		height*iHeight+pad*iPad*2]
#
# def stuff(col, row):
# 	return [
# 		col*iWidth,
# 		row*iHeight]

aNodes = [  ['BackdropNode',
				['z_order', 'name', 'tile_color', 'label', 'note_font_size', 'note_font_color', 'xpos', 'ypos', 'bdwidth', 'bdheight'],
				# [   [0, '', 0x212121ff, dShotInfo['ShotNumber'],    60, 0xfefefeff, 0, 0, 9*iWidth, 8*iHeight ],
				# 	[0, '', 0x3d505bff, 'FACIAL',      43, 0xaaffffff] + p(6,0,3,8),
				# 	[0, '', 0x7ea5bcff, '1',            43, 0xaaffffff, -816, 291, 270, 180 ],
				# 	[0, '', 0x365147ff, '2',            43, 0xaaffffff] + p(0,4,3,4),
				# 	[0, '', 0x81c1a9ff, '3',            43, 0xaaffffff, -1660, 770, 180, 130 ],
				# 	[0, '', 0x7ea5bcff, '4',            43, 0xaaffffff, -883, 770, 180, 130 ],
				# 	[0, '', 0x7ea5bcff, '5',            43, 0xaaffffff, -671, 770, 180, 130 ],
				# 	[3, '', 0x604800ff, 'MAIN PLATE',  43, 0xffe9aaff,] + p(3,0,3,8),
				# 	[5, '', 0xc19100ff, '6',            43, 0xffe9aaff, -1356, 768, 180, 130 ],
				# 	[5, '', 0xc19100ff, '7',            43, 0xffe9aaff, -1132, 768, 180, 130 ],
				# 	[5, '', 0xc19100ff, '8',            43, 0xffe9aaff, -1284, 289, 270, 180 ],
				#	],],
				[   [0, '', 0x212121ff, dShotInfo['ShotNumber'],    60, 0xfefefeff, -1767, 173, 1320, 781 ],
					[0, '', 0x3d505bff, 'FACIAL',      43, 0xaaffffff, -913, 218, 440, 710 ],
					[0, '', 0x7ea5bcff, '',            43, 0xaaffffff, -816, 291, 270, 180 ],
					[0, '', 0x365147ff, '',            43, 0xaaffffff, -1746, 531, 349, 398 ],
					[0, '', 0x81c1a9ff, '',            43, 0xaaffffff, -1660, 770, 180, 130 ],
					[0, '', 0x7ea5bcff, '',            43, 0xaaffffff, -883, 770, 180, 130 ],
					[0, '', 0x7ea5bcff, '',            43, 0xaaffffff, -671, 770, 180, 130 ],
					[3, '', 0x604800ff, 'MAIN PLATE',  43, 0xffe9aaff, -1379, 218, 440, 710 ],
					[5, '', 0xc19100ff, '',            43, 0xffe9aaff, -1356, 768, 180, 130 ],
					[5, '', 0xc19100ff, '',            43, 0xffe9aaff, -1132, 768, 180, 130 ],
					[5, '', 0xc19100ff, '',            43, 0xffe9aaff, -1284, 289, 270, 180 ],],],
			['ColorCorrect',
					['name', 'unpremult', 'xpos', 'ypos'],
					[   ['ColorCorrect1', '-rgba.alpah', -1189, 420],
						['ColorCorrect2', '-rgba.alpah', -716, 420],],],
			['Dot',
					['name', 'xpos', 'ypos'],
					[   ['Dot3', -1155, 500],
						['Dot4', -1047, 500],
						['Dot5', -799, 500],
						['Dot6', -682, 500],
						['Dot7', -586, 500],
						['Dot2', -1274, 500],
						['Dot1', -1576, 500],],],
			['Read',
					['name', 'xpos', 'ypos'],
					[   ['Read1', -1189, 320],
						['Read2', -716, 320],],],
			['Transform',
					['name', 'xpos', 'ypos'],
					[   ['Transform1', -833, 675],
						['Transform2', -620, 675],
						['Transform3', -1079, 675],],],
			['Reformat',
					['name', 'xpos', 'ypos'],
					[   ['Reformat1', -833, 710],
						['Reformat4', -620, 710],
						['Reformat5', -1079, 710],
						['Reformat2', -1610, 710],
						['Reformat3', -1308, 710],],],
			['Write',
					['name', 'xpos', 'ypos'],
					[   ['Write1', -833, 810],
						['Write2', -620, 810],
						['Write3', -1079, 810],
						['Write4', -1610, 810],
						['Write5', -1308, 810],],],
			['Roto',
					['name', 'xpos', 'ypos'],
					[   ['Roto1', -1610, 610],],],
			['Premult',
					['name', 'xpos', 'ypos'],
					[   ['Premult1', -1610, 640],],],
			['Viewer',
					['name', 'xpos', 'ypos'],
					[   ['Viewer1', -1159, 1113],],],

		]


# 1. Create Nodes Listed above.
# 2. Create a dictionary of nodes as objects. with Keys being the name of the node in string.
dNode = {}
for x in range(0, len(aNodes)):
	for list in aNodes[x][2]:
		oNode = nuke.createNode(aNodes[x][0])
		for i, item in enumerate(list[:]):
			if not aNodes[x][1][i].startswith(sNodeParent):
				oNode[aNodes[x][1][i]].setValue(item)
				dNode.update({list[0]: oNode})



#                Node, Node, Node, ... int (connection input) ]
aConnection = [ ['Read1', 'ColorCorrect1', 'Dot3', 'Dot2', 'Dot1', 'Roto1', 'Premult1', 'Reformat2', 'Write4', 0],
				['Dot2', 'Reformat3', 'Write5', 0],
				['Dot4', 'Transform3', 'Reformat5', 'Write3',0],
				['Read2','ColorCorrect2','Dot6','Dot5', 'Transform1', 'Reformat1', 'Write1', 0],
				['Dot7', 'Transform2', 'Reformat4', 'Write2' ,0],
				]


# Connect the nodes based on the entries of aConnection
for connection in aConnection:
	for i in range(1,len(connection)-1):
		dNode[connection[i]].setInput(connection[-1], dNode[connection[i-1]] )


# TODO: Deleting file to create a new file. un comment when modifying nuke tree.
import os
try:
	os.unlink(dShotInfo['FilePath'])
except:
	pass


nuke.scriptSaveAs(dShotInfo['FilePath'])
nuke.scriptExit()



sys.exit(0) # Stops running from this point on.
