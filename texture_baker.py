
from multiprocessing import Process
import os

from PySide import QtGui, QtCore

import maya.cmds as cmds
import pymel.core as pm
import maya.mel


class TextureBaker(QtGui.QWidget):
	
	def __init__(self):
		super(TextureBaker, self).__init__()

		self.setGeometry(400, 400, 400, 160)
		self.setWindowTitle("Texture Bakery")

		self.mainLayout = QtGui.QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.renderPathLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.renderPathLayout)

		self.renderPathLabel = QtGui.QLabel("Render Path:  ")
		self.renderPathLayout.addWidget(self.renderPathLabel)

		self.renderPath = QtGui.QLineEdit()
		self.renderPath.setPlaceholderText("Set Render Path")
		self.renderPathLayout.addWidget(self.renderPath)

		self.browserButton = QtGui.QPushButton("Browse")
		self.browserButton.clicked.connect(lambda: self.getPath() )
		self.renderPathLayout.addWidget(self.browserButton)

		self.imageNameLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.imageNameLayout)

		self.renderPathLabel = QtGui.QLabel("Image Name:  ")
		self.imageNameLayout.addWidget(self.renderPathLabel)

		self.imageName = QtGui.QLineEdit()
		self.imageName.setPlaceholderText("Set Image Name")
		self.imageNameLayout.addWidget(self.imageName)

		self.fileNameDotLabel = QtGui.QLabel(".")
		self.imageNameLayout.addWidget(self.fileNameDotLabel)

		self.framePadding = QtGui.QSpinBox()
		self.framePadding.setMinimum(1)
		self.framePadding.setToolTip("set Frame Padding")
		self.imageNameLayout.addWidget(self.framePadding)

		self.formatDotLabel = QtGui.QLabel(".")
		self.imageNameLayout.addWidget(self.formatDotLabel)

		self.formats = ["Format", "png", "jpg", "tga"]
		self.format = QtGui.QComboBox()
		self.format.addItems(self.formats)
		self.imageNameLayout.addWidget(self.format)

		self.sizeLayout = QtGui.QHBoxLayout()  
		self.mainLayout.addLayout(self.sizeLayout)

		self.sizeLabel = QtGui.QLabel("Resolution:     ")
		self.sizeLayout.addWidget(self.sizeLabel)

		self.sizex = QtGui.QLineEdit()
		self.sizex.setPlaceholderText("X resolution")
		self.sizex.setInputMask("000000")
		self.sizeLayout.addWidget(self.sizex)

		self.sizeXLabel = QtGui.QLabel("X")
		self.sizeLayout.addWidget(self.sizeXLabel)

		self.sizey = QtGui.QLineEdit()
		self.sizey.setPlaceholderText("Y resolution")
		self.sizey.setInputMask("000000")
		self.sizeLayout.addWidget(self.sizey)

		self.frangeLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.frangeLayout)

		self.frangeLabel = QtGui.QLabel("Frame Range:")
		self.frangeLayout.addWidget(self.frangeLabel)

		self.startFrame = QtGui.QLineEdit()
		self.startFrame.setPlaceholderText("Start Frame")
		self.startFrame.setInputMask("000000")
		self.frangeLayout.addWidget(self.startFrame)

		self.frameConectorLabel = QtGui.QLabel("-")
		self.frangeLayout.addWidget(self.frameConectorLabel)

		self.endFrame = QtGui.QLineEdit()
		self.endFrame.setPlaceholderText("End Frame")
		self.endFrame.setInputMask("000000")
		self.frangeLayout.addWidget(self.endFrame)

		self.frameByLabel = QtGui.QLabel("increment by")
		self.frangeLayout.addWidget(self.frameByLabel)

		self.incrFrame = QtGui.QSpinBox()
		self.incrFrame.setMinimum(1)
		self.frangeLayout.addWidget(self.incrFrame)

		self.buttonLayout = QtGui.QHBoxLayout()  
		self.mainLayout.addLayout(self.buttonLayout)

		self.bakeButton = QtGui.QPushButton("Bake")
		self.bakeButton.clicked.connect(lambda: self.bake() )
		self.buttonLayout.addWidget(self.bakeButton)

		self.bakeButton = QtGui.QPushButton("Reset")
		self.bakeButton.clicked.connect(lambda: self.resetUi() )	
		self.buttonLayout.addWidget(self.bakeButton)

		self.progress = QtGui.QProgressDialog("Copying files...", "Cancel", 0, 1, self)
		self.progress.setWindowModality(QtCore.Qt.WindowModal)
		self.progress.setAutoClose(True)

		self.setFocus()
		self.show()
		self.resetUi()

		
	def resetUi(self):
		''' reset the ui '''

		imgFolder = cmds.workspace( q=True, rd=True )+"images"
		self.renderPath.setText(imgFolder)
		self.imageName.clear()
		startFrame = str( int( cmds.playbackOptions(q=True, minTime=True) ) )
		self.startFrame.setText(startFrame)
		endFrame = str( int( cmds.playbackOptions(q=True, maxTime=True) ) )
		self.endFrame.setText(endFrame)
		defSizex = str( cmds.getAttr("defaultResolution.width") )
		self.sizex.setText(defSizex)
		defSizey = str( cmds.getAttr("defaultResolution.height") )
		self.sizey.setText(defSizey)
		self.framePadding.setValue(4)
		self.incrFrame.setValue(1)
		self.format.setCurrentIndex(3)

	def getPath(self):
		''' get the folder path '''
		path = pm.windows.promptForFolder()
		self.renderPath.setText(str( path) )


	def bakeIt(self, sel_geo, shader, sizex, sizey, sel_format, renderPath, imageName, frameNumber ):
		''' bake the image '''

		fileNode = cmds.convertSolidTx(sel_geo, shader, 
									antiAlias=1, bm=1, fts=1, sp=0, sh=0, alpha=0, 
									doubleSided=0, componentRange=0, 
									resolutionX=sizex, resolutionY=sizey, 
									fileFormat=sel_format, 
									fin=renderPath+"/"+imageName+"."+frameNumber+"."+sel_format);

		cmds.clearCache(fileNode)
		cmds.delete(fileNode)


	def bake(self):
		''' bakes the image to the given path '''

		selection = cmds.ls(sl = True)

		if len(selection) != 1:
			message = 'Select one object to bake.' 
			pm.windows.informBox('Erorr', message)
			return

		# get shapes of selection:
		sel_shape = cmds.ls(dag=1,o=1,s=1,sl=1)[0]
		sel_geo = selection[0]

		# get shading groups from shapes:
		shadingGrps = cmds.listConnections(sel_shape,type='shadingEngine')

		# get the shaders:
		shader = cmds.ls(cmds.listConnections(shadingGrps),materials=1)[0]
		if not shader:
			message = 'No shader assgned.' 
			pm.windows.informBox('Error', message)
			return

		shader = shader + ".outColor"

		renderPath = self.renderPath.text()
		if not renderPath or renderPath == "None" or not os.path.exists(renderPath):
			message = 'Render path not defined.' 
			pm.windows.informBox('Erorr', message)
			return

		imageName = self.imageName.text()
		if not imageName:
			message = 'image Name not defined.' 
			pm.windows.informBox('Erorr', message)
			return

		startFrame = self.startFrame.text()
		if not startFrame:
			message = 'start Frame defined.' 
			pm.windows.informBox('Erorr', message)
			return
		else:
			startFrame = int( startFrame )

		endFrame = self.endFrame.text()
		if not endFrame:
			message = 'EndFrame  not defined.' 
			pm.windows.informBox('Erorr', message)
			return
		else:
			endFrame = int( endFrame ) + 1

		if self.incrFrame.value() == "":
			incrFrame = 1
		else:
			incrFrame = int( self.incrFrame.text() )

		sizex = self.sizex.text()
		if not sizex:
			message = 'X resolution not defined.' 
			pm.windows.informBox('Error', message)
			return
		else:
			sizex = int( sizex )

		sizey = self.sizey.text()
		if not sizey:
			message = 'Y resolution not defined.' 
			pm.windows.informBox('Error', message)
			return
		else:
			sizey = int( sizey )

		sel_format = self.formats[ self.format.currentIndex() ]
		maxStep = len( range(startFrame, endFrame, incrFrame ) )
		self.progress.setMaximum(maxStep)

		step = 0
		
		for currentFrame in range(startFrame, endFrame, incrFrame):	
			self.progress.setValue(step)
			if self.progress.wasCanceled():
				break
			step += 1
			cmds.currentTime(currentFrame)
			padding =  self.framePadding.value()
			frameNumber = ("0000000" + str(currentFrame) ) [-padding:]
			self.bakeIt(sel_geo, shader, sizex, sizey, sel_format, renderPath, imageName, frameNumber)

		self.progress.setValue(maxStep)
