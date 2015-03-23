import maya.cmds as cmds
import os

imageFormats = { "tga":19, "tif":4, "png":32, "jpg":8 }

editor = 'renderView'
if not cmds.renderWindowEditor(editor, q=True, exists=True ):
	cmds.warning("No render window found!")

try:
	path, frmt = str( cmds.fileDialog2( dialogStyle=2)[0] ).split(".")
except TypeError:
	pass

if not path:
	maya.warning("Please provide a valid path.")

if frmt == "*" or frmt not in imageFormats.keys():
	cmds.warning("Please provide one of the formats in tga, tif, png, jpg.")
else:
	cmds.setAttr ('defaultRenderGlobals.imageFormat', imageFormats[frmt])

	editor = 'renderView'
	totalImages = cmds.renderWindowEditor(editor, q=True, nbImages=True ) + 1

	for i in range(0, int(totalImages)):
		cmds.renderWindowEditor(editor, e=True, displayImage=i-1)
		imgNumber = ( "00000" + str(i) )[-4:]
		imgPath = path + "_" + imgNumber
		cmds.renderWindowEditor(editor, e=True, writeImage= imgPath)

	cmds.setAttr('defaultRenderGlobals.imageFormat', 51)

