# -*- coding: utf-8 -*-
import sys
import os 
from PySide import QtGui, QtCore
import subprocess

global info
info = []


class TestListView(QtGui.QTableWidget):
    fileDropped = QtCore.Signal(list)

    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)  #
        self.setIconSize(QtCore.QSize(300, 300))


        
        self.resizeColumnsToContents()

        self.setSortingEnabled(False)

        self.setColumnCount(6)
        rowPosition = self.rowCount()
        self.setItem(rowPosition, 0, QtGui.QTableWidgetItem("text1"))
        self.setItem(rowPosition, 1, QtGui.QTableWidgetItem("text2"))
        self.setItem(rowPosition, 2, QtGui.QTableWidgetItem("text3"))
        self.insertRow(rowPosition)  # insertRow
        self.setHorizontalHeaderLabels(["NAME", "CONTAINER", "CODEC", "RESOLUTION", "FRAME RATE", "BITRATE, Mb/s"])

        #header.setSectionsMovable(True)

        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(False)

        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)





    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                try:
                    links.append(str(url.toLocalFile()))
                except UnicodeEncodeError:
                    msg = QtGui.QMessageBox()
                    msg.setIcon(QtGui.QMessageBox.Critical)
                    msg.setText("Don't feed me with some weird files")
                    msg.setInformativeText('Check if there is a Russian name in {}'.format(str(url).split('///')[1]))
                    msg.setWindowTitle("Wait a second")
                    msg.exec_()

            self.fileDropped.emit(links)
        else:
            event.ignore()


#################
#################

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestListView(self)

        self.view.fileDropped.connect(self.ffprobe)  # connection to the main function ffprobe

        self.setCentralWidget(self.view)
        #self.move(QtGui.QApplication.desktop().screen().rect().center() - self.rect().center())  ### lastchange centre
        # Title
        self.setWindowTitle("FFmpeg Application")
        # logo
        self.setWindowIcon(QtGui.QIcon('Sila_sveta_new logo.jpg'))
        # Resize Main Window
        self.resize(920, 800)
        self.setStyleSheet('background: silver;')
        self.view.setStyleSheet('font: bold 16px;')

        #  self.view.setSortingEnabled(False)

        self.view.setMouseTracking(True)

        #while self.view.grabMouse()


        # ComboBoxes

        self.menu = QtGui.QWidget()

        #self.raw = QtGui.QWidget()

        self.listwidget = QtGui.QListWidget(self)    #raw.
        self.listwidget.setStyleSheet('background: white;font:bold 14px;') #raw.


        #self.bottomlayout = QtGui.QVBoxLayout(self.raw)
        #self.bottomlayout.addWidget(self.listwidget,stretch=1) # (.raw)

        #self.raw.addWidget(self.listwidget)

        #############################################
        
        self.menu.cmbox1 = QtGui.QComboBox(self)
        self.menu.cmbox2 = QtGui.QComboBox(self)
        self.menu.cmbox3 = QtGui.QComboBox(self)
        self.menu.cmbox4 = QtGui.QComboBox(self)
        self.menu.cmbox5 = QtGui.QComboBox(self)

        self.menu.textDrop = QtGui.QLabel()
        self.menu.textDrop.setText("\nDrop files below")

        self.menu.cmbox1.addItem("Container")    
        self.menu.cmbox1.addItem(".mp4")
        self.menu.cmbox1.addItem(".mov")
        self.menu.cmbox1.addItem(".jpg")
        self.menu.cmbox1.addItem(".png")

        self.menu.cmbox2.addItem("Frame Rate")    
        self.menu.cmbox2.addItem("24")
        self.menu.cmbox2.addItem("25")
        self.menu.cmbox2.addItem("30")
        self.menu.cmbox2.addItem("50")
        self.menu.cmbox2.addItem("60")
        self.menu.cmbox2.addItem("1")
        
        self.menu.cmbox3.setEditable(True) # 



        self.menu.cmbox3.addItem("Resolution")    
        self.menu.cmbox3.addItem("1920x1080")
        self.menu.cmbox3.addItem("1280x720")
        self.menu.cmbox3.addItem("3840x2160")
        self.menu.cmbox3.setEditable(True)

        self.menu.cmbox4.addItem("Codec")    
        self.menu.cmbox4.addItem("H.264")
        self.menu.cmbox4.addItem("Hap")
        self.menu.cmbox4.addItem("H.265(HEVC)")
        self.menu.cmbox4.addItem("DXV3")
        self.menu.cmbox4.addItem("mjpeg")
        self.menu.cmbox4.addItem("png")

        self.menu.cmbox5.addItem("Bit rate")
        self.menu.cmbox5.addItem("0")
        self.menu.cmbox5.addItem("7")
        self.menu.cmbox5.addItem("9")
        self.menu.cmbox5.addItem("10")
        self.menu.cmbox5.addItem("11")
        self.menu.cmbox5.addItem("12")
        self.menu.cmbox5.addItem("13")
        self.menu.cmbox5.setEditable(True)


        # Buttons

        self.menu.buttonex = QtGui.QPushButton('Exit', self)
        self.menu.buttonclear = QtGui.QPushButton('Restart', self)

        
        global cmbox1
        global cmbox2
        global cmbox3
        global cmbox4
        global buttonex

        # Layouts

        self.menu.h2Box = QtGui.QHBoxLayout()
        self.menu.vbox = QtGui.QVBoxLayout()
        self.menu.hbox = QtGui.QVBoxLayout()


        """self.bottomlayout = QtGui.QVBoxLayout(self.view)
        self.bottomlayout.addStretch(1)
        self.bottomlayout.addWidget(self.listwidget, alignment=QtCore.Qt.AlignVCenter)"""
        
        

        

        self.menu.hbox.addWidget(self.menu.textDrop)

        self.menu.h2Box.addWidget(self.menu.cmbox1)
        self.menu.h2Box.addWidget(self.menu.cmbox2)
        self.menu.h2Box.addWidget(self.menu.cmbox3)
        self.menu.h2Box.addWidget(self.menu.cmbox4)
        self.menu.h2Box.addWidget(self.menu.cmbox5)

        self.menu.vbox.addWidget(self.menu.buttonex)
        #self.menu.vbox.addWidget(self.menu.buttonclear)

        self.menu.vbox.addLayout(self.menu.h2Box, stretch=True)
        self.menu.vbox.addLayout(self.menu.hbox, stretch=True)
        # self.menu.h2Box.addLayout(self.menu.vbox)

        self.menu.setLayout(self.menu.vbox)
        # self.setLayout(self.menu.h2Box)

        self.setMenuWidget(self.menu)
        self.menu.move(0, 500)

        self.dockWidget = QtGui.QDockWidget(str("Raw output from FFprobe"), self)
        self.dockWidget.setStyleSheet("font:bold 14px;")
        self.dockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.dockWidget.setWidget(self.listwidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockWidget)


        #self.area=QtCore.Qt.ToolBarArea()
        #self.addToolBar(self.listwidget)
        ##########
        #self.setStatusBar(self.raw)
        ##########
        

        self.menu.cmbox1.setStyleSheet('font: bold 14px;')
        self.menu.cmbox2.setStyleSheet('font: bold 14px;')
        self.menu.cmbox3.setStyleSheet('font: bold 14px;')
        self.menu.cmbox4.setStyleSheet('font: bold 14px;')
        self.menu.cmbox5.setStyleSheet('font: bold 14px;')

        self.menu.buttonex.setStyleSheet('font: bold 30px;')

        self.menu.buttonclear.setStyleSheet('font: bold 30px;')

        self.menu.textDrop.setStyleSheet('font: bold 30px;color:white;')


        



        # Events processing (Buttons clicked, comboboxes changed)

        self.menu.buttonclear.clicked.connect(self.cleartable)
        self.menu.buttonex.clicked.connect(self.ButtonEx)  # Exit button

        self.menu.cmbox1.currentIndexChanged.connect(self.finder1)
        self.menu.cmbox2.currentIndexChanged.connect(self.finder2)
        self.menu.cmbox3.currentIndexChanged.connect(self.finder3)
        self.menu.cmbox4.currentIndexChanged.connect(self.finder4)
        self.menu.cmbox5.currentIndexChanged.connect(self.finder5)


    # Clear the table function (works through restarting for cleaning the cash of values)
    # if the is a better idea for doing that, please, proceed
    
    def cleartable(self):
        info=[]
        information=[]
        self.view.clearContents()
        self.view.setRowCount(1)
        self.listwidget.clear ()
        #self.close()
        #subprocess.call("python" + " App.py", shell=False)
       

    # Apply settings given in comboboxes


    def finder1(self):
        self.view.setSortingEnabled(False)

        items = self.view.findItems(self.menu.cmbox1.currentText(), QtCore.Qt.MatchExactly)
        for item in items:
            if item.column() == 1:
                item.setBackground(QtGui.QColor(20, 255, 0, 50))
        self.view.setSortingEnabled(False)
    def finder2(self):
        self.view.setSortingEnabled(False)
        items = self.view.findItems(self.menu.cmbox2.currentText(), QtCore.Qt.MatchExactly)
        for item in items:
            if item.column() == 4:
                item.setBackground(QtGui.QColor(20, 255, 0, 50))

        self.view.setSortingEnabled(False)


    def finder3(self):
        self.view.setSortingEnabled(False)

        items = self.view.findItems(self.menu.cmbox3.currentText(), QtCore.Qt.MatchContains)
        for item in items:
            if item.column() == 3:
                item.setBackground(QtGui.QColor(20, 255, 0, 50))
        self.view.setSortingEnabled(False)


    def finder4(self):
        self.view.setSortingEnabled(False)

        items = self.view.findItems(self.menu.cmbox4.currentText(), QtCore.Qt.MatchExactly)
        for item in items:
            if item.column() == 2:
                item.setBackground(QtGui.QColor(20, 255, 0, 50))
        self.view.setSortingEnabled(False)

    def finder5(self):
        self.view.setSortingEnabled(False)
        itemsmatch = self.view.findItems(self.menu.cmbox5.currentText(), QtCore.Qt.MatchExactly)
        for item in itemsmatch:
            if item.column() == 5:
                item.setBackground(QtGui.QColor(20, 255, 0, 50))
        self.view.setSortingEnabled(False)


    # Exit function
    def ButtonEx(self):
        app.exit()
    
    
    def ffprobe(self, f):
        self.view.setSortingEnabled(False)
        for url in f:
    
            if os.path.exists(url):
                # print url
                global base_name
                global ext
                global videofps
                global videocodec
                global size
                global bitrateMBSfloat
                base_name, ext = os.path.splitext(url)  # exctracting .mp4
                if ext == '.jpg' or ext == '.jpeg' or ext == '.png':
                    filename = 'THIS IS A PICTURE'

                path = url

                cmd = 'ffprobe -i "{}" -show_streams -hide_banner'.format(path)  # FFprobe command here

                # cmdNEW='ffmpeg -i {} -f null -'.format(path)

                x = subprocess.check_output(cmd, shell=False)
                #print x
                global information
                information = []
                base_name, ext = os.path.splitext(url)
                name_of_file = base_name.split('/')[-1]
                
                # y = subprocess.check_output(cmdNEW,shell=False)
                # print x
                splited = x.splitlines()
                #print splited

                # print y

                codec_name = splited[2]
                widthh = splited[9]
                heightt = splited[10]
                frame_rate = splited[29]
                #print frame_rate
                

                videopartSTREAM = x.split('[STREAM]')[1]

                # data VIDEO
                videopart = videopartSTREAM.splitlines()
                videocodecRAW = videopart[2]
                videocodec = videocodecRAW.split('=')[1]

                if videocodec=="h264":
                    videocodec="H.264"
                elif videocodec=="dxv":
                    videocodec="DXV3"
                elif videocodec=="hap":
                    videocodec="Hap"
                elif videocodec=="hevc":
                    videocodec="H.265(HEVC)"






                

                for i in videopart:
                    if "r_frame_rate" in i:
                        videofps = i.split('=')[1]
                        print videofps
                    elif ext ==".jpg" or ext==".png":
                        videofps= "/"
                        
                            
                #videofpsRAW = videopart[29]
                #videofps = videofpsRAW.split('=')[1]
                videofps=videofps.split('/')[0]




                

                #video_bit_rate = videopart[36]

                for i in videopart:
                    
                    if "bit_rate" in i and "max_bit_rate" not in i:
                        print i
                        video_bit_rate = i
                        try:
                            video_bit_rate = float(video_bit_rate.split('=')[1])
                        except Exception:
                            video_bit_rate =video_bit_rate

                    elif ext ==".jpg" or ext==".png":
                        video_bit_rate= i
                        





                

                width = widthh.split('=')[1]
                height = heightt.split('=')[1]
                size = width + 'x' + height

                """try:
                    video_bit_rate = float(video_bit_rate.split('=')[1])
                except Exception:
                    video_bit_rate =video_bit_rate"""

                #print video_bit_rate
                try:
                    bitrateMBSfloat = video_bit_rate / (1000000)
                    bitrateMBSfloat =round(bitrateMBSfloat)
                    bitrateMBSfloat=int(bitrateMBSfloat)
                except Exception:
                    bitrateMBSfloat = video_bit_rate
                    try:
                       bitrateMBSfloat= round(bitrateMBSfloat)
                    except Exception:
                        bitrateMBSfloat="N/A"
                bitrateMBS = str(bitrateMBSfloat)

                print bitrateMBSfloat

                ############
                # check if there is any AUDIO stream, process if yes
                """try:
                    audiopartSTREAM = x.split('[STREAM]')[2]
                    audiopart = audiopartSTREAM.splitlines()
                    # data AUDIO
                    audiocodec = audiopart[2]
                    audio_sample_rate = audiopart[10]
                    audio_bit_rate = audiopart[22]
                    ##########
                except Exception:
                    audiocodec = ''
                    audio_sample_rate = 'NO AUDIO'
                    audio_bit_rate = ''

                try:
                    #print audiocodec
                    #print audio_sample_rate
                    #print audio_bit_
                    rate
                except Exception:
                    pass #print 'No AUDIO'

                if audio_sample_rate == 'NO AUDIO':
                    spacing = ''
                else:
                    spacing = ',       '       """

                numrows = self.view.rowCount()
                numcolumns = self.view.columnCount()

                information.append(name_of_file)
                information.append(ext)
                information.append(videocodec)
                information.append(size)
                information.append(videofps)
                information.append(bitrateMBS)

                info.append(information)
                
                self.view.setItem(numrows - 1, 0, QtGui.QTableWidgetItem(name_of_file+ext))
                self.view.item(numrows - 1, 0).setBackground(QtGui.QColor(255, 100, 0, 50))

                self.view.setItem(numrows - 1, 1, QtGui.QTableWidgetItem(ext))
                if self.menu.cmbox1.currentText() == ext:
                    self.view.item(numrows - 1, 1).setBackground(QtGui.QColor(20, 255, 0, 50))
                    self.view.item(numrows - 1, 0).setBackground(QtGui.QColor(255, 100, 0, 50))

                    
                if videofps=="1/25":
                    self.view.setItem(numrows - 1, 4, QtGui.QTableWidgetItem("It is an image"))
                else:
                    self.view.setItem(numrows - 1, 4, QtGui.QTableWidgetItem(videofps))
                    if self.menu.cmbox2.currentText() == videofps:
                        self.view.item(numrows - 1, 4).setBackground(QtGui.QColor(20, 255, 0, 50))
                        self.view.item(numrows - 1, 0).setBackground(QtGui.QColor(255, 100, 0, 50))
                        # self.view.item(numrows-1,1).setBackground(QtGui.QColor(20,255,0,50))
                
                    

                self.view.setItem(numrows - 1, 3, QtGui.QTableWidgetItem(size))
                if self.menu.cmbox3.currentText() == size:
                    self.view.item(numrows - 1, 3).setBackground(QtGui.QColor(20, 255, 0, 50))

                self.view.setItem(numrows - 1, 2, QtGui.QTableWidgetItem(videocodec))
                if self.menu.cmbox4.currentText() == videocodec:
                    self.view.item(numrows - 1, 2).setBackground(QtGui.QColor(20, 255, 0, 50))
                    self.view.item(numrows - 1, 0).setBackground(QtGui.QColor(255, 100, 0, 50))
                    
                print type(bitrateMBSfloat)
                print bitrateMBSfloat
                
                if bitrateMBSfloat <=0.001:
                    bitrateKbs=bitrateMBSfloat*1000
                    bitrateMBS=str(bitrateMBSfloat)
                    self.view.setItem(numrows - 1, 5, QtGui.QTableWidgetItem(bitrateMBS))
                    #self.view.item(numrows - 1, 5).setBackground(QtGui.QColor(20, 255, 0, 50))

                else:
                    self.view.setItem(numrows - 1, 5, QtGui.QTableWidgetItem(bitrateMBS))
                    if self.menu.cmbox5.currentText() == bitrateMBS:
                        self.view.item(numrows - 1, 5).setBackground(QtGui.QColor(20, 255, 0, 50))

                self.view.insertRow(numrows)  # add an empty row in the end
                
                item = QtGui.QListWidgetItem(str(name_of_file)+': '+str(splited)+'\n'+'---'*1000, self.listwidget) #raw.

                self.view.resizeColumnsToContents()
                
                #self.updateTable()
                app.processEvents()
                self.view.setSortingEnabled(True)

                '''
                except Exception:
                    print Exception
                    print '---------\n----------\n--------'
                    print path
                    
                    print 'VIDEO STREAM'
                    print size
                    print videocodec
                    print videofps
                    print video_bit_rate
                    print '-------------'
                    print 'AUDIO STREAM'

                    try:
                        print audiocodec
                        print audio_sample_rate
                        print audio_bit_rate
                    except Exception:
                        print 'No AUDIO'
                        base_name,ext=os.path.splitext(url)
                        name_of_file=base_name.split('/')[-1]

                        file_info='\nVIDEO_STREAM\n' + size+''+ videocodec + ', '+videofps + ', '+video_bit_rate + '\nAUDIO_STREAM\n' + audiocodec + ', ' +audio_sample_rate + ', ' +audio_bit_rate                    
                        filename=name_of_file+ext+'\n'+file_info+'\n\n\n'
                        item = QtGui.QListWidgetItem(filename, self.view) 
                    #print Exception'''

def main():
    global app
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
