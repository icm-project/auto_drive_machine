#!/usr/bin/env python
# coding: utf-8

# **Importing Modules and Libraries :**
# 
# Before running the next section please be sure about connection of the control unit cable to the specified USB port of the PC
# 
# (this might take afew minutes) 

# In[1]:


from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QGridLayout, QTextEdit, QProgressBar, QFrame, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QSize, QDir
from PyQt5.QtGui import QPixmap, QFont, QMovie,QFontDatabase

import sys
import ip
import detection
#import control
import cv2
import numpy as np
import pickle
import keyboard
import time
path="Detected_Sign.png"
path_2="Frame.png"


# In[ ]:


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300 # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40) # x, y
        self.labelTitle.setText('AI Racing Cars')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Seaching for Ip of the car camera...</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')

        self.labelReference = QLabel(self.frame)
        self.labelReference.resize(self.width() - 10, 20)
        self.labelReference.move(15, self.progressBar.y() + 170)
        self.labelReference.setObjectName('LabelReference')
        self.labelReference.setAlignment(Qt.AlignBottom)
        self.labelReference.setText('Developed By AAILab, Univercity Of Tehran')

    def loading(self):
        self.progressBar.setValue(self.counter)
        if self.counter ==int(self.n * 0.1):##########################################################IP Finder####################################
            time.sleep(1)
            #global Ip
            #Ip = ip.ip_finder()

        if self.counter == int(self.n * 0.5):
            self.labelDescription.setText('<strong>Importning Aritficial Intelligence Models...</strong>')
            
        
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(0.5)

            self.myApp = MyApp()
            self.myApp.show()

        self.counter += 1

def write(sign):
    with open("sign.txt","wb") as f:
            pickle.dump(sign, f)
    
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    
    
    
    
    def run(self):
        # capture from web cam
        image=np.zeros((320,240,3),dtype="uint8")
        i=0
        flag=1
        start =0
        sign = "No Sign Detected"
        with open("sign.txt","wb") as f:
            pickle.dump(sign, f)
#########################################################################Control Loop#############################################################        
        #cap = cv2.VideoCapture(Ip + ":81/stream")
        #print(Ip )
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            
            if ret:
                #img= cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) for final version!!!
                self.change_pixmap_signal.emit(img)
            else:
                img=image
            
            if keyboard.is_pressed('s'):
                print("start")
                #control.force_start(control.ser)
            if flag:
                contours,cropped_img,area,w,h = detection.reqdetection(img)
                ratio=w/h
                c_id,c_27 = detection.detect(cropped_img,area,ratio)
            if(flag==0)and(time.time()-start<1):
                c_id=0
                c_27=0
            if(flag==0)and(time.time()-start>1):
                contours,cropped_img,area,w,h = detection.reqdetection(img)
                ratio=w/h
                c_id,c_27 = detection.detect(cropped_img,area,ratio)
                flag = 1
                
            if(c_id==5):
                sign = "Slow Down Sign Detected"
                write(sign)
                #control.slow_down(control.ser)
                cropped_img= cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(path, cropped_img)
                cv2.imwrite(path_2, img)
            if(c_id==6):
                sign = "Speed Up Sign Detected"
                write(sign)
                #control.speed_up(control.ser)
                cropped_img= cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(path, cropped_img)
                cv2.imwrite(path_2, img)
            if(c_27==27):
                sign = "Limited Stop Sign Detected"
                write(sign)
                #control.limited_stop(control.ser)
                cropped_img= cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(path, cropped_img)
                cv2.imwrite(path_2, img)
                start = time.time()
                flag=0
                
            if(c_id==35):
                sign = "Start Sign Detected"
                write(sign)
                #control.start(control.ser)
                cropped_img= cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(path, cropped_img)
                cv2.imwrite(path_2, img)
            if(c_id==14)and(c_27==14):
                
                sign = "Stop Sign Detected"
                write(sign)
                #control.stop(control.ser)
                cropped_img= cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(path, cropped_img)
                cv2.imwrite(path_2, img)
                start = time.time()
                flag=0
                '''
            if((c_id!=14)and(c_27!=14)and(c_id!=35)and(c_27!=27)and(c_id!=6)and(c_id!=5)):
                sign = "No Sign Detected"
                write(sign)
                '''
            
######################################################################################UI##########################################################
            
                


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Racing Cars")
        self.setStyleSheet("background-color: #2E4452")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.center()
        
        # create a image label
        
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("color: gray;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #64E1FA")
        self.disply_width = 185
        self.display_height = 236
        self.image_label.resize(self.disply_width, self.display_height)
        
        self.image_label_d = QLabel(self)
        self.image_label_d.setStyleSheet("color: gray;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #64E1FA")
        self.image_label_d.resize(self.disply_width, self.display_height)
        self.image_label_d.setPixmap(QPixmap('Frame.png').scaled(185, 236))
        
        self.image_label_c = QLabel(self)
        self.image_label_c.setStyleSheet("color: gray;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #64E1FA")
        self.image_label_c.resize(self.disply_width, self.display_height)
        self.image_label_c.setPixmap(QPixmap('Detected_Sign.png').scaled(276, 236))
        
        
        # create a text label
        Font = "Montserrat"
        Font_f_b = "Anjoman_b"
        Font_size = 16
        self.textLabel = QLabel("CAR'S CAMERA")
        self.textLabel.setFont(QFont(Font, Font_size))
        self.textLabel.setStyleSheet("color: #FFFFFF;")
        self.textLabel.setAlignment(Qt.AlignRight)

        self.textLabel_f = QLabel("دوربین ماشین")
        self.textLabel_f.setFont(QFont(Font_f_b, Font_size,QFont.Bold))
        self.textLabel_f.setStyleSheet("color: #FFFFFF;")
        
        self.textLabel_d = QLabel('SIGN DETECTING')
        self.textLabel_d.setFont(QFont(Font, Font_size))
        self.textLabel_d.setStyleSheet("color: #FFFFFF;")
        self.textLabel_d.setAlignment(Qt.AlignRight)
        
        self.textLabel_d_f = QLabel('تشخیص علامت')
        self.textLabel_d_f.setFont(QFont(Font_f_b, Font_size ,QFont.Bold))
        self.textLabel_d_f.setStyleSheet("color: #FFFFFF;")
        
        self.textLabel_c = QLabel('THE SIGN WAS DETECTED')
        self.textLabel_c.setFont(QFont(Font, Font_size))
        self.textLabel_c.setStyleSheet("color: #FFFFFF;")
        self.textLabel_c.setAlignment(Qt.AlignRight)

        self.textLabel_c_f = QLabel('علامت تشخیص داده شده')
        self.textLabel_c_f.setFont(QFont(Font_f_b, Font_size,QFont.Bold))
        self.textLabel_c_f.setStyleSheet("color: #FFFFFF;")


        self.textReference = QLabel('Developed By AAILab, Univercity Of Tehran')
        self.textReference.setFont(QFont(Font, 6))
        self.textReference.setStyleSheet("color: #C0C0C0;")

        self.spaceLabel = QLabel("                ")
        self.spaceLabel.setFont(QFont(Font, 20))
        self.spaceLabel.setStyleSheet("color: #FFFFFF;")
        self.hspaceLabel = QLabel("       ")
        self.hspaceLabel.setFont(QFont(Font, 20))
        self.hspaceLabel.setStyleSheet("color: #FFFFFF;")

        #self.gif_label = QLabel(self)
        #self.movie = QMovie("Gif/AI.gif")
        #self.movie.setScaledSize(QSize(100, 100))
        #self.gif_label.setMovie(self.movie)
        #self.gif_label.setAlignment(Qt.AlignCenter)
        #self.gif_label.resize(100, 100)
        #self.movie.start()

        self.flag_label = QLabel(self)
        self.flag_label.resize(180, 120)
        self.flag_label.setPixmap(QPixmap('pic/Ns.png').scaled(80, 80))
        self.flag_label.setAlignment(Qt.AlignCenter)


        self.signs_head = {"No Sign Detected" : "تابلویی شناسایی نشده",
                      "Limited Stop Sign Detected" :"تابلو توقف زمان‌دار:",
                      "Slow Down Sign Detected" : "تابلو کاهش سرعت:",
                      "Speed Up Sign Detected" : "تابلو افزایش سرعت:",
                      "Start Sign Detected" : "تابلو شروع :",
                      "Stop Sign Detected" : "تابلو توقف:"}


        self.signs = {"No Sign Detected" :" " ,
                      "Limited Stop Sign Detected": " ماشین با دیدن این تابلو به مدت ۱۰ ثانیه"+"\n"+" متوقف شده و دوباره شروع به حرکت"+"\n"+"می‌کند.",
                      "Slow Down Sign Detected" : " ماشین با دیدن این تابلو سرعت روتین"+"\n"+" خود را کاهش خواهد داد.",
                      "Speed Up Sign Detected" : "ماشین با دیدن این تابلو، سرعت خود"+"\n"+"را افزایش داده و به صورت معمول خود"+"\n"+"میرسد.",
                      "Start Sign Detected" : "ماشین با دیدن این تابلو شروع به حرکت"+"\n"+"خواهد کرد.",
                      "Stop Sign Detected" : " ماشین با مشاهده این تابلو کاملا متوقف"+"\n"+"می‌شود و تا دوباره تابلو شروع حرکت"+"\n"+"را مشاهده نکند حرکت نخواهد کرد."}

              

        
        
        
        
        with open("sign.txt", "rb") as f:
            self.sign = pickle.load(f)
        
        #print(self.sign)
        self.textEdit_h = QLabel(self.signs_head[self.sign])
        self.textEdit_h.setFont(QFont(Font_f_b, Font_size,QFont.Bold))
        self.textEdit_h.setStyleSheet("color: #FFFFFF;")
        self.textEdit_h.setAlignment(Qt.AlignLeft)
        
        self.textEdit = QLabel(self.signs[self.sign])
        self.textEdit.setFont(QFont(Font_f_b, 12))
        self.textEdit.setStyleSheet("color: #FFFFFF;")
        self.textEdit.setAlignment(Qt.AlignLeft)

        #self.textLabel_c = QLabel(sign)

        
        
        
        vbox = QGridLayout()
        vbox.addWidget(self.image_label,3,1)
        vbox.addWidget(self.textLabel,2,1)
        vbox.addWidget(self.textLabel_f,1,1)
        vbox.addWidget(self.hspaceLabel,3,0)
        vbox.addWidget(self.spaceLabel,0,2)
        vbox.addWidget(self.hspaceLabel,3,6)
        vbox.addWidget(self.spaceLabel,3,2)
        vbox.addWidget(self.spaceLabel,3,4)
        vbox.addWidget(self.image_label_d,3,3)
        vbox.addWidget(self.textLabel_d_f,1,3)
        vbox.addWidget(self.textLabel_d,2,3)
        vbox.addWidget(self.image_label_c,3,5)
        vbox.addWidget(self.textLabel_c,2,5)
        vbox.addWidget(self.textLabel_c_f,1,5)
        vbox.addWidget(self.textEdit_h,4,5)
        vbox.addWidget(self.textEdit,5,5)
        #vbox.addWidget(self.gif_label,3,0)
        vbox.addWidget(self.textReference,6,1)
        vbox.addWidget(self.flag_label,5,3)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        
        # create the label that holds the image
        
        # create a text label
        #self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot(np.ndarray)
    def update_image(self, img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(img)
        self.image_label.setPixmap(qt_img.scaled(185, 236))
        self.image_label_c.setPixmap(QPixmap('Detected_Sign.png').scaled(276, 236))
        self.image_label_d.setPixmap(QPixmap('Frame.png').scaled(185, 236))
        
        with open("sign.txt", "rb") as f:
            self.sign = pickle.load(f)
        #print(self.sign)
        self.textEdit.setText(self.signs[self.sign])
        self.textEdit.setAlignment(Qt.AlignLeft)
        self.textEdit_h.setText(self.signs_head[self.sign])
        self.textEdit.setAlignment(Qt.AlignLeft)
        self.flag_label.setPixmap(QPixmap('pic/'+self.sign+'.png').scaled(80, 80))
        self.flag_label.setAlignment(Qt.AlignCenter)

        
    
    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rgb_image = cv2.resize(rgb_image, (185, 236), interpolation = cv2.INTER_AREA)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

'''
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = myApp()
    a.show()
    sys.exit(app.exec_())
'''
if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        #LabelTitle {
            font-size: 60px;
            color: #93deed;
        }

        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }

        #LabelLoading {
            font-size: 30px;
            color: #e8e8eb;
        }

        QFrame {
            background-color: #2F4454;
            color: rgb(220, 220, 220);
        }

        QProgressBar {
            background-color: #DA7B93;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    ''')
    dir_ = QDir("Montserrat")
    _id = QFontDatabase.addApplicationFont("Fonts/Montserrat-Light.ttf")
    dir_ = QDir("Anjoman_b")
    _id = QFontDatabase.addApplicationFont("Fonts/Anjoman-Bold.ttf")
    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')



# **The Next Section Will Find The Ip of The Car Camera**
# 
# Before running the next section please be sure about these:
# 
# 1) just one of the cars be on and turn off another car
# 
# 2) check the modem, it should be on
# 
# 3) check pc wifi, it should be connected to the modem
# 
# (Next part run time might be a few minutes)

# In[ ]:


#Ip = ip.ip_finder()


# **This is the main loop:**
# 
# please before running the next section put the car on the rail in front of the flag
# 
# During the loop is running:
# 
# 1) pressing "S" button to activate "force start" command.
# 
# 2) preesing "Q" buttumn break the loop.

# In[ ]:




