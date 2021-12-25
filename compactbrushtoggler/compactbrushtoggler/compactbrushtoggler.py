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

import krita, time
 
from PyQt5.QtCore import (
        QItemSelectionModel,QSize,QTimer,Qt,pyqtSignal)

from PyQt5.QtWidgets import (
        QApplication, QCheckBox, QListView,
        QFrame,QWidget, QLabel, QSlider,
        QVBoxLayout,  QGridLayout,
        QPushButton,QDoubleSpinBox,
         )

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


class Compactbrushtoggler(DockWidget):
    
    property = [ "Size","Opacity","Flow","Softness","Rotation","Scatter","Brush Tip" ]
    toggleState = {}
    last_brush = ""
    cur_size = 1

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compact Brush Toggler")

        self.baseWidget = QWidget()
        self.baseWidget.setMinimumSize(QSize(120,80))
        self.baseWidget.setMaximumSize(QSize(280,90))

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(2, 2, 2, 2)

        self.baseWidget.setLayout(self.vbox)
        self.setWidget(self.baseWidget)

        for br_prop in self.property:
            if(br_prop != "Brush Tip") : self.toggleState[br_prop] = True; 
    
        self.setUi()

    # UI LAYOUT
    def setUi(self):
 
        self.timer=QTimer() 

        self.hRow1 = QWidget()
        self.toolGrid1 = QGridLayout()
        self.toolGrid1.setContentsMargins(1, 1, 1, 0) 
        self.hRow1.setLayout(self.toolGrid1)
        
        self.hRow2 = QWidget()
        self.toolGrid2 = QGridLayout()
        self.toolGrid2.setContentsMargins(1, 1, 1, 2) 
        self.hRow2.setLayout(self.toolGrid2)
 
  
        self.vbox.addWidget(self.hRow1)  
        self.vbox.addWidget(self.hRow2)  
 
        self.lbl_BrushFade       = QLabel(self)
        self.BrushFadeSlider     = QSlider(Qt.Horizontal)
        self.BrushFade           = CBTDoubleSpinBox()
        self.BrushProperty       = {
                
                "Size"      : QPushButton(" Sze"),
                "Opacity"   : QPushButton(" Opc"),
                "Flow"      : QPushButton(" Flw"),
                "Softness"  : QPushButton(" Sft"), 
                "Rotation"  : QPushButton(" Rot"),
                "Scatter"   : QPushButton(" Sct") 

        }
        self.lbl_BrushFade.setText("Br.Fade")
        self.BrushFade.setRange(0, 1.0)
        self.BrushFade.setSingleStep(.01) 

        self.BrushFadeSlider.setRange(0,100)  
        self.BrushFadeSlider.setTickPosition(QSlider.NoTicks)
        self.BrushFadeSlider.setTickInterval(1)
       
        self.toolGrid1.addWidget(self.lbl_BrushFade, 0, 0)
        self.toolGrid1.addWidget(self.BrushFadeSlider, 0, 1, 0, 5)
        self.toolGrid1.addWidget(self.BrushFade, 0, 6)
 
        self.toolGrid2.addWidget(self.BrushProperty["Size"], 0, 1)
        self.toolGrid2.addWidget(self.BrushProperty["Opacity"], 0, 2) 
        self.toolGrid2.addWidget(self.BrushProperty["Flow"], 0, 3)
        self.toolGrid2.addWidget(self.BrushProperty["Softness"], 1, 1)
        self.toolGrid2.addWidget(self.BrushProperty["Rotation"], 1, 2) 
        self.toolGrid2.addWidget(self.BrushProperty["Scatter"], 1, 3)

        self.BrushProperty["Size"].clicked.connect(lambda: self.toggleBrushPressure("Size"))
        self.BrushProperty["Opacity"].clicked.connect(lambda: self.toggleBrushPressure("Opacity"))
        self.BrushProperty["Flow"].clicked.connect(lambda: self.toggleBrushPressure("Flow"))
        self.BrushProperty["Softness"].clicked.connect(lambda: self.toggleBrushPressure("Softness"))
        self.BrushProperty["Rotation"].clicked.connect(lambda: self.toggleBrushPressure("Rotation"))
        self.BrushProperty["Scatter"].clicked.connect(lambda: self.toggleBrushPressure("Scatter"))
         
        self.BrushFadeSlider.valueChanged.connect(lambda:  self.sliderChange()) 
        self.BrushFadeSlider.sliderReleased.connect(lambda:  self.changeFadeValue()) 
        self.BrushFade.stepChanged.connect(lambda:  self.spinnerChangedValue())  

        for prop in self.toggleState.keys():
            self.toggleIcon(prop, True)
           
        self.timer.timeout.connect(self.loadBrushInfo)
         

    def canvasChanged(self, canvas):
        if canvas:       
            if canvas.view():
                self.timer.start(400)
        else:
            self.timer.stop() 

    
    #----------------------------------------------------#
    # For Changing Info                                  #
    #                                                    #
    #----------------------------------------------------#
    
    def loadBrushInfo(self): 
        cur_brush = Krita.instance().activeWindow().activeView().currentBrushPreset() 
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()

        if(cur_brush.name() != self.last_brush):   
            self.last_brush = cur_brush.name()  
            self.loadState() 

        
    def toggleIcon(self,prop,state):
        icon = 'transform_icons_penPressure'
        def_color = "background-color : #305475"

        if(not state):
            icon = 'transform_icons_penPressure_locked'
            def_color = "background-color : #383838"

        self.BrushProperty[prop].setIcon( Krita.instance().icon(icon) )
        self.BrushProperty[prop].setStyleSheet(def_color)
    

    #----------------------------------------------------#
    # Connect Functions                                  #
    #                                                    #
    #----------------------------------------------------#

    def toggleBrushPressure(self, prop):  
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()
         
        if(self.toggleState[prop] == True):
            self.set_checkBoxUseCurve(prop, False)
            self.toggleState[prop] = False 
            self.toggleIcon(prop,False)
        else:
            self.set_checkBoxUseCurve(prop, True)
            self.toggleState[prop] = True 
            self.toggleIcon(prop,True) 
             

    def sliderChange(self):    
        self.BrushFade.setValue(self.BrushFadeSlider.value()/100)  
 
    def changeFadeValue(self): 
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()    
         
        self.set_brushSize()
        
    def spinnerChangedValue(self): 
        self.BrushFadeSlider.setValue(self.BrushFade.value()*100)
        self.changeFadeValue()
         
    #----------------------------------------------------#
    # For Traversing nodes to get to Brush Editor Docker #
    #                                                    #
    #----------------------------------------------------#
    
    def walk_widgets(self,start):
        stack = [(start, 0)]
        while stack:
            cursor, depth = stack.pop(-1)
            yield cursor, depth
            stack.extend((c, depth + 1) for c in reversed(cursor.children()))


    def get_brush_editor(self):
        for window in QApplication.topLevelWidgets():
            if isinstance(window, QFrame) and window.objectName() == 'popup frame':
                for widget, _ in self.walk_widgets(window):
                    real_cls_name = widget.metaObject().className()
                    obj_name = widget.objectName()
                    if real_cls_name == 'KisPaintOpPresetsEditor' and obj_name == 'KisPaintOpPresetsEditor':
                        return widget

 
    #----------------------------------------------------#
    # Get the corresponding container of the             #
    # brush property selected on the list view           #
    #----------------------------------------------------#
    def selectBrushContainer(self,br_property):
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
        current_view = None
        selectedRow  = None 
        for view in option_widget_container.findChildren(QListView):
            if view.metaObject().className() == 'KisCategorizedListView':
                if view.isVisibleTo(option_widget_container):
                    current_view = view
                    break
                
        if current_view:
            current_settings_widget = current_view.parent()
            s_model = current_view.selectionModel()
            model = current_view.model()
            target_index = None
            for row in range(model.rowCount()):
                index = model.index(row,0)   
                if index.data() == br_property: 
                    target_index = index
                    selectedRow = row
                    break
                    
            if target_index is not None: 
                s_model.clear()
                s_model.select(target_index, QItemSelectionModel.SelectCurrent)
                s_model.setCurrentIndex(target_index, QItemSelectionModel.SelectCurrent)
                current_view.setCurrentIndex(target_index)
                current_view.activated.emit(target_index)
                
        
        container_info = dict()
        container_info["model_index"]  = target_index
        container_info["current_view"] = current_view
        container_info["row_count"]    = selectedRow
        container_info["option_widget_container"] = option_widget_container
        container_info["current_settings_widget"] = current_settings_widget

        return container_info  
    

    #----------------------------------------------------#
    # Check Pressure Toggle Curve Check box of           #
    # Corresponding Property                             #
    #----------------------------------------------------#
    def set_checkBoxUseCurve(self, br_property, new_state):
        container_info = self.selectBrushContainer(br_property) 
        m_index = container_info["model_index"]
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  

        if current_view:  
            model = current_view.model()
            for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):
                if check_box.isVisibleTo(option_widget_container):
                    if  (br_property != "Opacity" and br_property != "Flow"):
                        if new_state:
                           model.setData(m_index, Qt.Checked, Qt.CheckStateRole)
                        else: 
                           model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                #ask something for this
                    check_box.setChecked(new_state)  
                    break  
        
        self.set_brushSize()            

    #----------------------------------------------------#
    # Set the Value of Brush HFade in the Brush          #
    # Property Editor                                    #
    #----------------------------------------------------#
    def set_brushFadeValue(self):  
        container_info = self.selectBrushContainer("Brush Tip")
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        if current_view:   
            for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'inputHFade'):
                if spin_box.isVisibleTo(option_widget_container):  
                    spin_box.setValue(self.BrushFade.value()) 
                    #self.BrushFade.setEnabled(True) 
                    break 

    
        
    def set_brushSize(self):
        container_info = self.selectBrushContainer("Brush Tip")
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        if current_view:   
            for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'inputRadius'):
                if spin_box.isVisibleTo(option_widget_container):  
                    spin_box.setValue(self.cur_size)  
                    break 
    
    #----------------------------------------------------#
    # Load the current state of brush property toggles   #
    #                                                    #
    #----------------------------------------------------#
    def loadState(self): 
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
        current_view = None
         
        for view in option_widget_container.findChildren(QListView):
            if view.metaObject().className() == 'KisCategorizedListView':
                if view.isVisibleTo(option_widget_container):
                    current_view = view
                    break

        for br_property in self.property: 
            if current_view:
                current_settings_widget = current_view.parent()
                s_model = current_view.selectionModel()
                model = current_view.model()
                target_index = None
                for row in range(model.rowCount()):
                    index = model.index(row)   
                    if index.data() == br_property: 
                        target_index = index
                        break
                        
                if target_index is not None: 
                    s_model.clear()
                    s_model.select(target_index, QItemSelectionModel.SelectCurrent)
                    s_model.setCurrentIndex(target_index, QItemSelectionModel.SelectCurrent)
                    current_view.setCurrentIndex(target_index)
                    current_view.activated.emit(target_index)

                    if(br_property != "Brush Tip"): 
                        m_check = False
                        if (br_property != "Opacity" and br_property != "Flow") and target_index.flags()&Qt.ItemIsUserCheckable:
                            if target_index.data(Qt.CheckStateRole):
                                m_check = True
                            else:
                                m_check = False
                        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'): 
                            if check_box.isVisibleTo(option_widget_container):    
                                if(check_box.isChecked() and m_check): 
                                    self.toggleState[br_property] = True
                                    self.toggleIcon(br_property,True)
                                else:
                                    self.toggleState[br_property] = False
                                    self.toggleIcon(br_property,False)
                                break
                    else:  
                        ft = 0
                        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'inputHFade'): 
                            if spin_box.isVisibleTo(option_widget_container): 
                                ft = 1
                                self.BrushFade.setEnabled(True)
                                self.BrushFadeSlider.setEnabled(True) 
                                self.BrushFadeSlider.setValue(spin_box.value()*100)  
                                break
                        if ft == 0:
                            self.BrushFadeSlider.setValue(0)
                            self.BrushFade.setEnabled(False)
                            self.BrushFadeSlider.setEnabled(False)

                
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        Compactbrushtoggler)

instance.addDockWidgetFactory(dock_widget_factory)