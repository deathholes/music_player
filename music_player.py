'''
Documentation, License etc.

@package music_player
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
	
		self.currentFile = '/'
		self.player = QMediaPlayer()
		self.lastState = -1			#0- stopped, 1- playing 2-paused
		self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
		self.player.stateChanged.connect(self.qmp_stateChanged)
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
		centralWidget = QWidget(self)
		centralWidget.setLayout(controlBar)
		self.setCentralWidget(centralWidget)
		
		#Add Status bar
		self.statusBar().showMessage('Ready')
		
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
		controls = QHBoxLayout()
		playBtn = QPushButton('Play')
		pauseBtn = QPushButton('Pause')
		stopBtn = QPushButton('Stop')
		self.currentFile = '/home/deathholes/Music/jiya_jale.mp3'
		print(self.player.state())
		print(self.player.mediaStatus())
		playBtn.clicked.connect(self.playHandler)
		pauseBtn.clicked.connect(self.pauseHandler)
		stopBtn.clicked.connect(self.stopHandler)
		controls.addWidget(playBtn)
		controls.addWidget(pauseBtn)
		controls.addWidget(stopBtn)
		return controls
	
	def playHandler(self):
		self.presentState = 1
		print('playHandler')
		if self.player.state() == QMediaPlayer.StoppedState :
			if self.player.mediaStatus() == QMediaPlayer.NoMedia:
				self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.currentFile)))
			elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
				self.player.play()
			elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
				self.player.play()
			self.player.setVolume(60)
		if self.player.state() == QMediaPlayer.PlayingState:
			pass
		if self.player.state() == QMediaPlayer.PausedState:
			self.player.play()
			
	def pauseHandler(self):
		self.presentState = 2
		print('pauseHandler')
		self.player.pause()
			
	def stopHandler(self):
		self.presentState = 0
		print('stopHandler')
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
		print('media status changed signal catched, signal was : ',self.player.mediaStatus())
		if self.player.mediaStatus() == QMediaPlayer.LoadedMedia and self.presentState == 1:
			self.player.play()
			
	
	def qmp_stateChanged(self):
		print('QMediaPlayer state changed, new state :',self.player.state())
		if self.player.state() == QMediaPlayer.StoppedState:
			self.player.stop()
	
	def fileOpen(self):
		pass
		#fileAc = QAction('Open File',self)
		#fileAc.setShortcut('Ctrl+O')
	
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