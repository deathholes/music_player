'''
Documentation, License etc.

@package music_player
'''
import sys
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
	
		self.currentFile = '/'
		self.player = QMediaPlayer()
		self.userAction = -1			#0- stopped, 1- playing 2-paused
		self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.volumeChanged.connect(self.qmp_volumeChanged)
		self.player.setVolume(60)
		#Add Status bar
		self.statusBar().showMessage('No Media :: %d'%self.player.volume())
		self.homeScreen()
		
	def homeScreen(self):
		print('homeScreen')
		#Set title of the MainWindow
		self.setWindowTitle('Music Player by deathholes')
		
		#Create Menubar
		self.createMenubar()
		
		#Create Toolbar
		self.createToolbar()
		
		#Add info screen
		#infoscreen = self.createInfoScreen()
		
		#Add Control Bar
		controlBar = self.addControls()
		
		#need to add both infoscreen and control bar to the central widget.
		centralWidget = QWidget()
		centralWidget.setLayout(controlBar)
		self.setCentralWidget(centralWidget)
		
		#Set Dimensions of the MainWindow
		self.resize(400,300)
		
		#show everything.
		self.show()
		
	def createMenubar(self):
		print('createMenubar')
		menubar = self.menuBar()
		filemenu = menubar.addMenu('File')
		filemenu.addAction(self.fileOpen())
		filemenu.addAction(self.folderOpen())
		filemenu.addAction(self.exitAction())
		
	
	def createToolbar(self):
		pass
	
	def createInfoScreen(self):
		#it will be new window with all information about the song being played.
		#the shortcut will be Ctrl+I
		infoS = QLabel('Info',self)
		return infoS
		
	def addControls(self):
		print('addControls')
		#Creating layouts
		controlArea = QVBoxLayout()		#centralWidget
		controls = QHBoxLayout()
		
		#creating buttons
		playBtn = QPushButton('Play')		#play button
		pauseBtn = QPushButton('Pause')		#pause button
		stopBtn = QPushButton('Stop')		#stop button
		volumeDescBtn = QPushButton('V (-)')#Decrease Volume
		volumeIncBtn = QPushButton('V (+)')	#Increase Volume
		
		#creating seek slider
		seekSlider = QSlider()
		seekSlider.setMinimum(0)
		seekSlider.setMaximum(100)
		seekSlider.setOrientation(Qt.Horizontal)
		seekSlider.setTracking(False)
		seekSlider.sliderMoved.connect(self.seekPosition)
		#seekSlider.valueChanged.connect(self.seekPosition)
		
		seekSliderLabel1 = QLabel('0.00')
		seekSliderLabel2 = QLabel('0.00')
		seekSliderLayout = QHBoxLayout()
		seekSliderLayout.addWidget(seekSliderLabel1)
		seekSliderLayout.addWidget(seekSlider)
		seekSliderLayout.addWidget(seekSliderLabel2)
		
		self.currentFile = '/home/deathholes/Music/jiya_jale.mp3'
		
		#Add handler for each button. Not using the default slots.
		playBtn.clicked.connect(self.playHandler)
		pauseBtn.clicked.connect(self.pauseHandler)
		stopBtn.clicked.connect(self.stopHandler)
		volumeDescBtn.clicked.connect(self.decreaseVolume)
		volumeIncBtn.clicked.connect(self.increaseVolume)
		
		#Adding to the horizontal layout
		controls.addWidget(volumeDescBtn)
		controls.addWidget(playBtn)
		controls.addWidget(pauseBtn)
		controls.addWidget(stopBtn)
		controls.addWidget(volumeIncBtn)
		
		#Adding to the vertical layout
		controlArea.addLayout(seekSliderLayout)
		controlArea.addLayout(controls)
		return controlArea
	
	def playHandler(self):
		self.userAction = 1
		#print('playHandler')
		self.statusBar().showMessage('Playing at Volume %d'%self.player.volume())
		if self.player.state() == QMediaPlayer.StoppedState :
			if self.player.mediaStatus() == QMediaPlayer.NoMedia:
				self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.currentFile)))
			elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
				self.player.play()
			elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
				self.player.play()
		elif self.player.state() == QMediaPlayer.PlayingState:
			pass
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.play()
			
	def pauseHandler(self):
		self.userAction = 2
		print('pauseHandler')
		self.statusBar().showMessage('Paused %s at position %s at Volume %d'%\
			(self.player.metaData(QMediaMetaData.Title),\
				self.centralWidget().layout().itemAt(0).layout().itemAt(0).widget().text(),\
					self.player.volume()))
		self.player.pause()
			
	def stopHandler(self):
		self.userAction = 0
		print('stopHandler')
		self.statusBar().showMessage('Stopped at Volume %d'%(self.player.volume()))
		if self.player.state() == QMediaPlayer.PlayingState:
			print('already playing, so stopping')
			self.stopState = True
			self.player.stop()
			print('player stopped')
		elif self.player.state() == QMediaPlayer.PausedState:
			print('in pause state')
			self.player.stop()
			print('player stopped from paused state')
		elif self.player.state() == QMediaPlayer.StoppedState:
			print('already in stopped state')
			
	def playFile(self):
		print('playFile')
		self.loadFile()
	
	def loadFile(self):
		print('loadFile')
		self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.currentFile)))
		self.player.setVolume(40)
		
	def qmp_mediaStatusChanged(self):
		if self.player.mediaStatus() == QMediaPlayer.LoadedMedia and self.userAction == 1:
			durationT = self.player.duration()
			self.centralWidget().layout().itemAt(0).layout().itemAt(1).widget().setRange(0,durationT)
			self.centralWidget().layout().itemAt(0).layout().itemAt(2).widget().setText('%d:%02d'%(int(durationT/60000),int((durationT/1000)%60)))
			self.player.play()
			
	
	def qmp_stateChanged(self):
		print('QMediaPlayer state changed, new state :',self.player.state())
		if self.player.state() == QMediaPlayer.StoppedState:
			self.player.stop()
			
	def qmp_positionChanged(self, position,senderType=False):
		sliderLayout = self.centralWidget().layout().itemAt(0).layout()
		if senderType == False:
			sliderLayout.itemAt(1).widget().setValue(position)
		#update the text label
		sliderLayout.itemAt(0).widget().setText('%d:%02d'%(int(position/60000),int((position/1000)%60)))
	
	def seekPosition(self, position,isQMP=1):
		print(position)
		sender = self.sender()
		#print('type of sender : ',type(sender))
		if isinstance(sender,QSlider):
			if self.player.isSeekable():
				self.player.setPosition(position)
				#self.qmp_positionChanged(position,True)
				
	def qmp_volumeChanged(self):
		print('volumeChanged')
		msg = self.statusBar().currentMessage()
		msg = msg[:-2] + str(self.player.volume())
		self.statusBar().showMessage(msg)
		
	def increaseVolume(self):
		vol = self.player.volume()
		vol = min(vol+5,100)
		self.player.setVolume(vol)
		
	def decreaseVolume(self):
		vol = self.player.volume()
		vol = max(vol-5,0)
		self.player.setVolume(vol)
	
	def fileOpen(self):
		fileAc = QAction('Open File',self)
		fileAc.setShortcut('Ctrl+O')
		fileAc.setStatusTip('Open File')
		fileAc.triggered.connect(self.openFile)
		return fileAc
		
	def openFile(self):
		fileChoosen = QFileDialog.getOpenFileName(self,'Open Music File',expanduser('~'),'*.mp3 *.ogg *.wav')
		print(fileChoosen)
		if fileChoosen != None:
			self.currentFile = fileChoosen[0]
	
	def folderOpen(self):
		pass
		#folderAc = QAction('Open Folder',self)
	
	def exitAction(self):
		exitAc = QAction('&Exit',self)
		exitAc.setShortcut('Ctrl+Q')
		exitAc.setStatusTip('Exit App')
		exitAc.triggered.connect(self.closeEvent)
		return exitAc
	
	def closeEvent(self,event):
		reply = QMessageBox.question(self,'Message','Pres Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
		
		if reply == QMessageBox.Yes :
			qApp.quit()
		else :
			try:
				event.ignore()
			except AttributeError:
				pass
			
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())