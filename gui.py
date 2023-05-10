import sys
import os
from pathlib import Path
import pandas as pd
# Pqt5
from PyQt5.QtWidgets import QDialog,QApplication, QMainWindow, QHeaderView, QFileDialog, QColorDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor, QPixmap, QFont, QFontDatabase
from PyQt5 import QtCore, QtWidgets

import functions as fn
from classes import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('gui/CV-creator.ui', self)

        self.templates = [
            'plantilla1',
            'plantilla2'
        ]
            
        

        # Menu animation
        self.bt_menu.clicked.connect(self.move_menu)

        # Hide buttons
        self.bt_normalsize.hide()

        # Bar buttons
        self.bt_quit.clicked.connect(lambda: self.close())
        self.bt_maximize.clicked.connect(self.maximize)
        self.bt_normalsize.clicked.connect(self.normalsize)
        self.bt_minimize.clicked.connect(self.minimize)
        # Page buttons
        self.bt_data.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_data))
        self.bt_filepath.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_files))
        self.bt_config.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_config))
        # Create button
        
        self.bt_create.clicked.connect(self.create_cv)
        # Clear buttons
        data_lines = [self.le_name,self.le_phone,self.le_page,self.le_email,self.le_carge,self.te_social]
        files_lines = [self.le_photo,self.le_description,self.le_education,self.le_works,
            self.le_skills, self.le_output
        ]
        self.bt_clear_data.clicked.connect(lambda: self.clear_data(data_lines))
        self.bt_clear_filepath.clicked.connect(lambda: self.clear_data(files_lines))
        # charge buttons
        self.bt_photo.clicked.connect(lambda: self.charge_file((self.le_photo, 'Images (*.jpg, *.png *.jpeg)')))
        self.bt_description.clicked.connect(lambda: self.charge_file((self.le_description, 'text files (*.txt)')))
        self.bt_education.clicked.connect(lambda: self.charge_file((self.le_education, '(*.csv)')))
        self.bt_work.clicked.connect(lambda: self.charge_file((self.le_works, '(*.csv)')))
        self.bt_skills.clicked.connect(lambda: self.charge_file((self.le_skills, '(*.csv)')))
        self.bt_output.clicked.connect(self.charge_dir)
        # Colors pick
        self.col_1 = QColor (95,193,171)
        self.col_2 = QColor (119,138,178)
        self.fr_color1.setStyleSheet('QWidget {Background-color: %s}' % self.col_1.name())
        self.fr_color2.setStyleSheet('QWidget {Background-color: %s}' % self.col_2.name())
        self.bt_color1.clicked.connect(lambda: self.show_color_dialog(self.col_1, self.fr_color1))
        self.bt_color2.clicked.connect(lambda: self.show_color_dialog(self.col_2, self.fr_color2))
        # Combobox
        self.fonts_dict = {'Courier': 'Adobe Courier',
        'Helvetica': 'Adobe Helvetica', 
        'Times': 'Adobe Times',
        'Times San Serif': 'Times Sans Serif',
        'Iosevka': 'Iosevka',
        }
        #fonts = ['Courier','Helvetica', 'Times', 'Times San Serif','Iosevka']
        self.comboTem.addItems(i for i in self.templates)
        self.comboFont.addItems(self.fonts_dict.keys())
        self.comboFont.currentTextChanged.connect(self.change_font)

        # Templates view
        template_path = 'gui/src/templates/'
        self.comboTem.currentTextChanged.connect(lambda : self.lb_image.setPixmap(QPixmap(template_path + self.comboTem.currentText() + '.jpg')))


        # Hide title bar (opacity)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Move window
        self.top_frame.mouseMoveEvent = self.move_window

    # Move menu method

    def move_menu(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extend = 200
            else:
                extend = normal
            self.animation = QPropertyAnimation(self.frame_control, b'minimumWidth')
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    
    def maximize(self):
        self.showMaximized()
        self.bt_maximize.hide()
        self.bt_normalsize.show()

    def normalsize(self):
        self.showNormal()
        self.bt_normalsize.hide()
        self.bt_maximize.show()
    
    def minimize(self):
        self.showMinimized()

    ## SizeGrip

    def resize_evet(self,event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
    
    def create_cv(self):
        
        study_colums = ['title','state', 'date','institute']
        works_colums = ['job','date','company','description']
        skills_colums = ['skill','description']

        if self.le_education.text():
            study_dict = pd.read_csv(self.le_education.text(),names=study_colums).to_dict()
        else:
            study_dict={}

        if self.le_works.text():
            works_dict = pd.read_csv(self.le_works.text(),names=works_colums).to_dict()
        else:
            works_dict = {}
        if self.le_skills.text():
            skills_dict = pd.read_csv(self.le_skills.text(),names=skills_colums).to_dict()
        else:
            skills_dict = {}

        if self.rbt_work_description.isChecked():
            use_work_description = True
        else:
            use_work_description = False

        color1 = self.fr_color1.palette().window().color().name().lstrip('#')
        color2 = self.fr_color2.palette().window().color().name().lstrip('#')

        colors_dict= {
            'color1': tuple(int(color1[i:i+2], 16) for i in (0, 2, 4)),
            'color2': tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
        }

        social = self.te_social.toPlainText().split('\n')

        context_dict = {
            'use_work_desc': use_work_description,
            'name' :self.le_name.text(),
            'phone': self.le_phone.text(),
            'description_file': self.le_description.text(),
            'photo': self.le_photo.text(),
            'page': self.le_page.text(),
            'email': self.le_email.text(),
            'carge': self.le_carge.text(),
            'social': social,
            'study': study_dict,
            'works': works_dict,
            'skills': skills_dict
        }
        if self.le_output.text():
            output = self.le_output.text() + '/' + self.le_filename.text() + '.pdf'
        else:
            output = self.le_filename.text() + '.pdf'

        font = self.comboFont.currentText()
        
        if self.le_filename.text():
            self.lb_signal.setText('')
            

            if self.comboTem.currentText() == 'plantilla1':
                pdf = PDF1()
            elif self.comboTem.currentText() == 'plantilla2':
                pdf = PDF2()
        
            fn.create_CV(pdf,context=context_dict,
                output=output,selected_font=font,colors=colors_dict)
            self.lb_done.setText('Archivo creado')
            
        else:
            self.lb_signal.setText('Ponle nombre al archivo')
            self.lb_done.setText('')

    def clear_data(self, list):
        for i in list:
            i.clear()
    
    def charge_file(self,tuple):
        fname = QFileDialog.getOpenFileName(self, 'Open file', str(Path.home()),tuple[1])
        tuple[0].setText(fname[0])

    def charge_dir(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open Directory', str(Path.home()))
        self.le_output.setText(fname)
    
    # Move window
    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def move_window(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()
        if event.globalPos().y() <=10:
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normalsize.show()
        else:
            self.showNormal()
            self.bt_normalsize.hide()
            self.bt_maximize.show()

    def show_color_dialog(self,col,fr_color):
        col = QColorDialog.getColor()
        if col.isValid():
            fr_color.setStyleSheet('QWidget {Background-color: %s}' % col.name())

    
    def change_font(self):
        
        if self.comboFont.currentText() in self.fonts_dict.keys():
            self.lb_font.setStyleSheet('QWidget {font: 18pt "%s";}' % self.fonts_dict[self.comboFont.currentText()])
        
    def test_data(self):
        # variables set to test
        path = Path.home() / 'programing/python/documents_create/pdf/CV'

        self.le_name.setText('Nombre completo')
        self.le_phone.setText('Telefono')
        self.le_page.setText('Pagina')
        self.le_email.setText('Correo')
        self.le_carge.setText('Cargo')

        self.le_education.setText(str(path / 'data/learning.csv'))
        self.le_works.setText(str(path / 'data/works.csv'))
        self.le_skills.setText(str(path / 'data/skills.csv'))
        self.le_output.setText(str(path))
        self.le_photo.setText(str(path / 'src/foto.jpg'))
        self.le_description.setText(str(path / 'data/description.txt'))
        self.le_filename.setText('gui_cv')


