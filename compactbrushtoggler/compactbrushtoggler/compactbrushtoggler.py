#-----------------------------------------------------------------------------#
# Compact Brush Toggler - Copyright (c) 2021 - kaichi1342                     #
# ----------------------------------------------------------------------------#
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
# ----------------------------------------------------------------------------#
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                        #
# See the GNU General Public License for more details.                        #
#-----------------------------------------------------------------------------#
# You should have received a copy of the GNU General Public License           #
# along with this program.                                                    #
# If not, see https://www.gnu.org/licenses/                                   #
# ----------------------------------------------------------------------------#
# Thank you to: AkiR , Grum999, KnowZero                                      #
# Who provided much of the base code and helped me making this.               #
# -----------------------------------------------------------------------------
# This is docker that  toggle pen pressure on/off of 6 brush property         #
# [Size, Opacity, Flow, Softness, Scatter, Rotation ] and adjust              #
# brush hfade without opening the Brush Editor.                               #
# -----------------------------------------------------------------------------
  
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase

import krita, time, os
 
from PyQt5.QtCore import (
    QSize, QTimer, Qt, pyqtSignal
)
from PyQt5.QtGui import (
    QPalette
)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget, QLabel, QSlider,
    QVBoxLayout,  QHBoxLayout,  QGridLayout,  
    QPushButton,QDoubleSpinBox,  
    QToolButton, QSizePolicy
        
)


from .CBT_Icons import * 
from .CBT_Toggler import * 


DOCKER_NAME = 'CompactBrushToggler'
DOCKER_ID = 'pykrita_compactbrushtoggler'


class CBTDoubleSpinBox(QDoubleSpinBox):
    stepChanged = pyqtSignal() 

    def stepBy(self, step):
        value = self.value()
        super(CBTDoubleSpinBox, self).stepBy(step)
        if self.value() != value:
            self.stepChanged.emit()

    def focusOutEvent(self, e):
        value = self.value() 
        super(CBTDoubleSpinBox, self).focusOutEvent(e)
        self.stepChanged.emit()


class CompactBrushToggler(DockWidget):
    
    theme_color = {
        "dark"  : {"on" :  "background-color : #305475; color : #D2D2D2;", "off" : "background-color : #383838 : color : #D2D2D2;", "disabled" : "background-color : #1a1a1a; color : #9A9A9A;"},
        "light" : {"on" :  "background-color : #8BD5F0; color : #9A9A9A;", "off" : "background-color : #1a1a1a : color : #373737;", "disabled" : "background-color : #9A9A9A; color : #2a2a2a;"}
    } 
    

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compact Brush Toggler") 

        self.baseWidget = QWidget()
         
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(2, 2, 2, 2)

        self.baseWidget.setLayout(self.vbox)
        self.setWidget(self.baseWidget)
        
        self.theme      = "dark"
        self.theme_signal  = False 

        self.toggler    = CBT_Toggler(self, self.theme_color) 
        self.toggler.setTheme(self.theme)
        
        for br_prop in self.toggler.property:
            if(br_prop != "Brush Tip") : self.toggler.toggleState[br_prop] = True; 
    
        self.setUI_H() 

    # UI LAYOUT
    def setUI_H(self):

        self.baseWidget.setMinimumSize(QSize(60,100))
        self.baseWidget.setMaximumSize(QSize(350,650)) 

        self.timer = QTimer() 

        self.hRow1 = QWidget()
        self.toolGrid1 = QGridLayout()
        self.toolGrid1.setContentsMargins(1, 1, 1, 0) 
        self.hRow1.setLayout(self.toolGrid1)
          
        self.hRow2 = QWidget()
        self.toolGrid2 = QGridLayout()
        self.toolGrid2.setContentsMargins(1, 1, 1, 2)  
        self.hRow2.setLayout(self.toolGrid2)

        self.hRow3 = QWidget()
        self.toolGrid3 = QHBoxLayout()
        self.toolGrid3.setContentsMargins(1, 1, 1, 2) 
        self.toolGrid3.setAlignment(Qt.AlignRight)
        self.hRow3.setLayout(self.toolGrid3)


        self.lbl_test            = QLabel()
        self.lbl_BrushFade       = QLabel("Softness")
        self.BrushFadeSlider     = QSlider(Qt.Horizontal)
        self.BrushFade           = CBTDoubleSpinBox()
 

        self.lbl_Toggle       = QLabel("Toggles")
  
        self.vbox.addWidget(self.hRow1)    
        self.vbox.addWidget(self.hRow2)   
        #self.vbox.addWidget(self.lbl_test)  


        self.BrushProperty       = { }

        for prop in self.toggler.toggleState.keys(): 
            self.BrushProperty[prop] =  QPushButton() 
            self.BrushProperty[prop].setToolTip("Toggle Brush " + self.toggler.brush_text["full"][prop])
         
        self.BrushFade.setRange(0, 1.0)
        self.BrushFade.setSingleStep(.01) 

        self.BrushFadeSlider.setRange(0,100)  
        self.BrushFadeSlider.setTickPosition(QSlider.NoTicks)
        self.BrushFadeSlider.setTickInterval(1)
  
       
        #self.toolGrid1.addWidget(self.lbl_BrushFade, 0, 0)
        self.toolGrid1.addWidget(self.BrushFadeSlider, 0, 0, 0, 5)
        self.toolGrid1.addWidget(self.BrushFade, 0, 6)
      
  
        i = 0 
        for prop in self.BrushProperty.keys():   
            self.BrushProperty[prop].setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Expanding )
            self.toolGrid2.addWidget(self.BrushProperty[prop], i // 2, i % 2) 
            i += 1
      
        self.brushPropertyConnect()

        self.BrushFadeSlider.valueChanged.connect(lambda:  self.sliderFadeChange()) 
        self.BrushFadeSlider.sliderReleased.connect(lambda:  self.changeFadeValue()) 
        self.BrushFade.stepChanged.connect(lambda:  self.spinnerChangedFadeValue())  
   
 
        self.toggler.setInputItems(self.BrushProperty, self.BrushFade, self.BrushFadeSlider)
         
        for prop in self.toggler.toggleState.keys(): 
            self.toggler.toggleIcon(prop, True)
 
        self.timer.timeout.connect(self.toggler.loadBrushInfo)
        self.resize(self.sizeHint())  
   
    
    #----------------------------------------------------#
    # Events and Connection                              #
    #                                                    #
    #----------------------------------------------------#
        

    def resizeEvent(self, event):    
        self.setNames()

    
    def canvasChanged(self, canvas):    
        if canvas:       
            if canvas.view():
                self.timer.start(300)  
                
                if self.theme_signal == False:
                    self.Window_Connect()
                
        else:
            self.timer.stop() 


    def brushPropertyConnect(self):
        self.BrushProperty["Size"].clicked.connect(lambda: self.toggler.toggleOptions("Size"))
        self.BrushProperty["Opacity"].clicked.connect(lambda: self.toggler.toggleOptions("Opacity"))
        self.BrushProperty["Flow"].clicked.connect(lambda: self.toggler.toggleOptions("Flow"))
        self.BrushProperty["Softness"].clicked.connect(lambda: self.toggler.toggleOptions("Softness"))
        self.BrushProperty["Rotation"].clicked.connect(lambda: self.toggler.toggleOptions("Rotation"))
        self.BrushProperty["Scatter"].clicked.connect(lambda: self.toggler.toggleOptions("Scatter"))
        self.BrushProperty["Color Rate"].clicked.connect(lambda: self.toggler.toggleOptions("Color Rate"))
        self.BrushProperty["Overlay Mode"].clicked.connect(lambda: self.toggler.toggleOptions("Overlay Mode"))
        self.BrushProperty["Ink depletion"].clicked.connect(lambda: self.toggler.toggleOptions("Ink depletion"))
        self.BrushProperty["Painting Mode"].clicked.connect(lambda: self.toggler.toggleOptions("Painting Mode")) 
    
    def showEvent(self, event):
        # Window 
        self.setNames()
        self.Theme_Changed()  
        self.Window_Connect()


    def Window_Connect(self):
        # Window
        self.window = Krita.instance().activeWindow() 
        
        if self.window != None:  
            self.window.themeChanged.connect(self.Theme_Changed)  
            self.theme_signal = True
            
         

    def Theme_Changed(self):
        theme = QApplication.palette().color(QPalette.Window).value()
        
        if theme > 128: 
            self.theme  = "light"
            self.toggler.setTheme(self.theme)
            self.toggler.cbt_icons.setTheme("dark")   
        else: 
            self.theme  = "dark"
            self.toggler.setTheme(self.theme)
            self.toggler.cbt_icons.setTheme("light") 

        for prop in self.toggler.toggleState.keys():  
            self.toggler.toggleIcon(prop, self.toggler.toggleState[prop])

    #----------------------------------------------------#
    # Connect Functions                                  #
    #                                                    #
    #----------------------------------------------------#
    def setNames(self):
        #self.Theme_Changed()
        ratio =  self.BrushProperty["Size"].width() / self.BrushProperty["Size"].height() 
        self.lbl_test.setText("")
        if ratio > 4:
            for prop in self.toggler.toggleState.keys():    
                self.BrushProperty[prop].setText( self.toggler.brush_text["full"][prop]) 
        elif ratio > 2:
            for prop in self.toggler.toggleState.keys():    
                self.BrushProperty[prop].setText( self.toggler.brush_text["short"][prop]) 
        else:  
            for prop in self.toggler.toggleState.keys():    
                self.BrushProperty[prop].setText("")
        
        for prop in self.toggler.toggleState.keys():   
            ico_size = QSize(
                int(self.BrushProperty[prop].height() - ( self.BrushProperty[prop].height() * .20)),
                int(self.BrushProperty[prop].width() - ( self.BrushProperty[prop].width() * .20)),
            )
             
            self.BrushProperty[prop].setIconSize( ico_size )

    def reloadPreset(self):
        Krita.instance().action('reload_preset_action').trigger()
        self.lbl_test.setText("")  
        self.toggler.loadState()
        
            
    def loadBrushState(self):  
        self.lbl_test.setText("")
        self.toggler.loadState()

    #----------------------------------------------------#
    # Toggle And Change Function                         #
    #                                                    #
    #----------------------------------------------------#
 
    
    def sliderFadeChange(self):    
        self.BrushFade.setValue(self.BrushFadeSlider.value()/100)  
 
    def spinnerChangedFadeValue(self): 
        self.BrushFadeSlider.setValue(self.BrushFade.value()*100)
        self.changeFadeValue()
    
    def changeFadeValue(self): 
        self.toggler.cur_size  = Krita.instance().activeWindow().activeView().brushSize()    
        self.toggler.setBrushFadeValue()
        self.toggler.setBrushSize()
 
     

instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        CompactBrushToggler)

instance.addDockWidgetFactory(dock_widget_factory)