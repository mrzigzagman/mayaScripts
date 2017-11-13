
import nuke
#nuke.scriptNew()
#nuke.scriptSaveAs("/mll/shots/ate/2060/motion/work/maya/dyabu/Images/Nuke/TEMP/Temp.nk")


aBD_args = ['input', 'name', 'tile_color', 'label', 'note_font_size', 'note_font_color', 'xpos', 'ypos', 'bdwidth', 'bdheight']
aBD_info = [[0, '', 0x212121ff, 60, 'ate 1350/n', 60, 0xfefefeff, -951, -595, 1497, 805 ],
]

for list in aBD_info:
    oBD = nuke.createNode('BackdropNode')
    for i, item in enumerate(list[:]):
        oBD[aBD_args[i]].setValue(item)


#r = nuke.createNode('Read')
#r['colorspace'].value()
#w = nuke.createNode('Write')
#w.setInput(0,r)
#r['ypos'].setValue(-400)

nuke.scriptSaveAs("/mll/shots/ate/2060/motion/work/maya/dyabu/Images/Nuke/TEMP/Temp.nk")
nuke.scriptExit()
