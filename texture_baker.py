from PySide import QtGui

import pymel.core as pm
import maya.cmds as cmds
import maya.mel

class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        
        self.setGeometry(400, 400, 400, 160)
        self.setWindowTitle("Projection Bakery")

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)        

        self.renderPathLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.renderPathLayout)
        self.renderPath = QtGui.QLineEdit()
        self.renderPath.setPlaceholderText("Set Render Path")
        self.renderPathLayout.addWidget(self.renderPath)

        self.browserButton = QtGui.QPushButton("Browse")
        self.browserButton.clicked.connect(lambda: self.getPath() )
        self.renderPathLayout.addWidget(self.browserButton)

        self.imageName = QtGui.QLineEdit()
        self.imageName.setPlaceholderText("Set Image Name")
        self.mainLayout.addWidget(self.imageName)

        self.frangeLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.frangeLayout)

        self.startFrame = QtGui.QLineEdit()
        self.startFrame.setPlaceholderText("Start Frame")
        self.frangeLayout.addWidget(self.startFrame)

        self.endFrame = QtGui.QLineEdit()
        self.endFrame.setPlaceholderText("End Frame")
        self.frangeLayout.addWidget(self.endFrame)

        self.incrFrame = QtGui.QLineEdit()
        self.incrFrame.setPlaceholderText("Increment")
        self.frangeLayout.addWidget(self.incrFrame)


        self.sizeLayout = QtGui.QHBoxLayout()  
        self.mainLayout.addLayout(self.sizeLayout)

        self.sizex = QtGui.QLineEdit()
        self.sizex.setPlaceholderText("X resolution")
        self.sizeLayout.addWidget(self.sizex)

        self.sizey = QtGui.QLineEdit()
        self.sizey.setPlaceholderText("Y resolution")
        self.sizeLayout.addWidget(self.sizey)

        self.formats = ["Format", "png", "jpg", "tga"]
        self.format = QtGui.QComboBox()
        self.format.addItems(self.formats)
        self.sizeLayout.addWidget(self.format)

        self.bakeButton = QtGui.QPushButton("Bake")
        self.bakeButton.clicked.connect(lambda: self.bake() )
        self.mainLayout.addWidget(self.bakeButton)

        self.mainLayout.addStretch(0)
        self.setFocus()
        self.show()


    def getPath(self):
        ''' get the folder path '''
        path = pm.windows.promptForFolder()
        self.renderPath.setText(str( path) )


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
        #print sel_geo
        # get shading groups from shapes:
        shadingGrps = cmds.listConnections(sel_shape,type='shadingEngine')
        #print shadingGrps
        # get the shaders:
        shader = cmds.ls(cmds.listConnections(shadingGrps),materials=1)[0]
        shader = shader + ".outColor"
        #print shader

        sizex = int ( self.sizex.text() )
        sizey = int ( self.sizey.text() )
        sel_format = self.formats[ self.format.currentIndex() ]

        renderPath = self.renderPath.text()
        imageName = self.imageName.text()

        startFrame = int( self.startFrame.text() )
        endFrame = int( self.endFrame.text() ) + 1

        if self.incrFrame.text() == "":
            incrFrame = 1
        else:
            incrFrame = int( self.incrFrame.text() )

        for currentFrame in range(startFrame, endFrame, incrFrame):
            cmds.currentTime(currentFrame)
            frameNumber = ("00000" + str(currentFrame) ) [-5:]
            #print incrFrame
            #print frameNumber
            fileNode = cmds.convertSolidTx(sel_geo, shader, 
                                        antiAlias=1, bm=1, fts=1, sp=0, sh=0, alpha=0, 
                                        doubleSided=0, componentRange=0, 
                                        resolutionX=sizex, resolutionY=sizey, 
                                        fileFormat=sel_format, 
                                        fin=renderPath+"/"+imageName+"."+frameNumber+"."+sel_format);

            cmds.delete(fileNode)


main = Window()
main()
