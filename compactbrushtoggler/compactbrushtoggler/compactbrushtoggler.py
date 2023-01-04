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
 

from faulthandler import disable
from operator import truediv
from traceback import format_exc
from webbrowser import get
from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase

import krita, time
 
from PyQt5.QtCore import (
        QItemSelectionModel,QSize,QTimer,Qt,pyqtSignal)

from PyQt5.QtWidgets import (
        QApplication, QCheckBox, QListView,
        QFrame,QWidget, QLabel, QSlider,
        QVBoxLayout,  QGridLayout, QTextEdit,
        QPushButton,QDoubleSpinBox,QMainWindow,
        QComboBox, QMessageBox, QRadioButton
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
    
    property = [ 
        "Size","Opacity","Flow","Softness","Rotation",
        "Scatter","Overlay Mode","Color Rate","Ink depletion","Painting Mode", "Brush Tip" 
    ] 
    property_fn = { 
        "Size" : 0,"Opacity" : 0,"Flow": 0,"Softness": 0,"Rotation": 0,
        "Scatter": 0,"Overlay Mode": 0,"Color Rate": 0,
        "Ink depletion": 0,"Painting Mode": 0 , "Brush Tip": 0,
    } 
    #Painting Mode : 0 => Build Up , 1 => Wash
  
    toggleState = {}

    br_values = {"Size:" : None, "Opacity:" : None, "Color Rate:" : None, "Smudge Length:" : None, "Angle:" : None, "Smudge mode:" : "Dulling"}

    for_set = {}
    last_brush = ""
    cur_size = 1
    count = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compact Brush Toggler") 

        self.baseWidget = QWidget()
         
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(2, 2, 2, 2)

        self.baseWidget.setLayout(self.vbox)
        self.setWidget(self.baseWidget)

        for br_prop in self.property:
            if(br_prop != "Brush Tip") : self.toggleState[br_prop] = True; 
    
        self.setUI_H()

    # UI LAYOUT
    def setUI_H(self):

        self.baseWidget.setMinimumSize(QSize(60,100))
        self.baseWidget.setMaximumSize(QSize(280,340))

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
        self.lbl_test            = QLabel(self)
        self.BrushFadeSlider     = QSlider(Qt.Horizontal)
        self.BrushFade           = CBTDoubleSpinBox()

        self.BrushProperty       = { 
            "Size"      : QPushButton("Sze "),
            "Opacity"   : QPushButton("Opc "),
            "Flow"      : QPushButton("Flw "),
            "Softness"  : QPushButton("Sft "), 
            "Rotation"  : QPushButton("Rot "),
            "Scatter"   : QPushButton("Sct "), 
            "Overlay Mode"    : QPushButton("Ovl "), 
            "Color Rate"      : QPushButton("Col "), 
            "Ink depletion"   : QPushButton("Sok "), 
            "Painting Mode"   : QPushButton("PtM ") 

        }
        
        self.lbl_BrushFade.setText("Fade")
        self.BrushFade.setRange(0, 1.0)
        self.BrushFade.setSingleStep(.01) 

        self.BrushFadeSlider.setRange(0,100)  
        self.BrushFadeSlider.setTickPosition(QSlider.NoTicks)
        self.BrushFadeSlider.setTickInterval(1)
       
        self.toolGrid1.addWidget(self.lbl_test, 0, 0)
        self.toolGrid1.addWidget(self.lbl_BrushFade, 0, 0)
        self.toolGrid1.addWidget(self.BrushFadeSlider, 0, 1, 0, 5)
        self.toolGrid1.addWidget(self.BrushFade, 0, 6)
 

        i = 0 
        for prop in self.BrushProperty:   
            self.toolGrid2.addWidget(self.BrushProperty[prop], i // 2, i % 2)
            i += 1
      
      
        self.brushPropertyConnect()

        self.BrushFadeSlider.valueChanged.connect(lambda:  self.sliderChange()) 
        self.BrushFadeSlider.sliderReleased.connect(lambda:  self.changeFadeValue()) 
        self.BrushFade.stepChanged.connect(lambda:  self.spinnerChangedValue())  

        self.setNames()
        for prop in self.toggleState.keys():
            self.toggleIcon(prop, True)
    
        self.timer.timeout.connect(self.loadBrushInfo)

    
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
        else:
            self.timer.stop() 

    def brushPropertyConnect(self):
        self.BrushProperty["Size"].clicked.connect(lambda: self.toggleOptions("Size"))
        self.BrushProperty["Opacity"].clicked.connect(lambda: self.toggleOptions("Opacity"))
        self.BrushProperty["Flow"].clicked.connect(lambda: self.toggleOptions("Flow"))
        self.BrushProperty["Softness"].clicked.connect(lambda: self.toggleOptions("Softness"))
        self.BrushProperty["Rotation"].clicked.connect(lambda: self.toggleOptions("Rotation"))
        self.BrushProperty["Scatter"].clicked.connect(lambda: self.toggleOptions("Scatter"))
        self.BrushProperty["Overlay Mode"].clicked.connect(lambda: self.toggleOptions("Overlay Mode"))
        self.BrushProperty["Color Rate"].clicked.connect(lambda: self.toggleOptions("Color Rate"))
        self.BrushProperty["Ink depletion"].clicked.connect(lambda: self.toggleOptions("Ink depletion"))
        self.BrushProperty["Painting Mode"].clicked.connect(lambda: self.toggleOptions("Painting Mode")) 
    
    #----------------------------------------------------#
    # Connect Functions                                  #
    #                                                    #
    #----------------------------------------------------#
    def setNames(self):
        if(self.baseWidget.width() > 200):
            self.BrushProperty["Size"].setText("Size")
            self.BrushProperty["Opacity"].setText("Opacity")
            self.BrushProperty["Flow"].setText("Flow")
            self.BrushProperty["Softness"].setText("Softness")
            self.BrushProperty["Rotation"].setText("Rotation")
            self.BrushProperty["Scatter"].setText("Scatter")
            self.BrushProperty["Overlay Mode"].setText("Overlay Mode")
            self.BrushProperty["Color Rate"].setText("Color Rate")
            self.BrushProperty["Ink depletion"].setText("Soak Ink")
            self.BrushProperty["Painting Mode"].setText("Paint Mode")
        else:
            self.BrushProperty["Size"].setText("Sze")
            self.BrushProperty["Opacity"].setText("Opc")
            self.BrushProperty["Flow"].setText("Flw")
            self.BrushProperty["Softness"].setText("Sft")
            self.BrushProperty["Rotation"].setText("Rot")
            self.BrushProperty["Scatter"].setText("Sct")
            self.BrushProperty["Overlay Mode"].setText("Ovl")
            self.BrushProperty["Color Rate"].setText("Col")
            self.BrushProperty["Ink depletion"].setText("Sok")
            self.BrushProperty["Painting Mode"].setText("PtM")

    #----------------------------------------------------#
    # For Changing Info                                  #
    #                                                    #
    #----------------------------------------------------#
    
    def loadBrushInfo(self): 
        cur_brush = Krita.instance().activeWindow().activeView().currentBrushPreset() 
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()
 
        #self.get_palette_values() 

        if(cur_brush.name() != self.last_brush):   
            self.last_brush = cur_brush.name()  
            self.loadState()
        
        
    def toggleIcon(self, prop, state):
        if prop == "Painting Mode" or prop == "Ink depletion": 
            icon = 'showColoring' if(state) else 'showColoringOff' 
            self.BrushProperty[prop].setIcon( Krita.instance().icon(icon) ) 
            return True 

        icon = 'transform_icons_penPressure'
        def_color = "background-color : #305475"

        if(not state):
            icon = 'transform_icons_penPressure_locked'
            def_color = "background-color : #383838"

        self.BrushProperty[prop].setIcon( Krita.instance().icon(icon) )
        self.BrushProperty[prop].setStyleSheet(def_color)
        return True
        
    #----------------------------------------------------#
    # Toggle And Change Function                         #
    #                                                    #
    #----------------------------------------------------#
 
    def toggleOptions(self, prop):  
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()
           
        if(self.toggleState[prop] == True):
            self.setOptions(prop, False)
            self.toggleState[prop] = False 
            self.toggleIcon(prop,False)
        else:
            self.setOptions(prop, True)
            self.toggleState[prop] = True 
            self.toggleIcon(prop,True) 

         
        #self.set_PaletteValue(self.br_values)
             

    def sliderChange(self):    
        self.BrushFade.setValue(self.BrushFadeSlider.value()/100)  
 
    def spinnerChangedValue(self): 
        self.BrushFadeSlider.setValue(self.BrushFade.value()*100)
        self.changeFadeValue()
    
    def changeFadeValue(self): 
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()    
        self.set_brushFadeValue()
        self.set_brushSize()

    
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
    def setOptions(self, br_property, new_state): 
        container_info = self.selectBrushContainer(br_property) 
        m_index = container_info["model_index"]
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        if current_view:
            if br_property == "Painting Mode":
                self.setPaintMode(br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container)
            elif br_property == "Ink depletion":
                self.setSoakInk(br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container)
            else: 
                self.setCheckBoxUseCurve(br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container)
        self.set_brushSize()  

    def setCheckBoxUseCurve(self, br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model()
        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):
            if br_property == "Overlay Mode":
                model.setData(m_index, Qt.Checked, Qt.CheckStateRole)  if new_state else model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)

            if check_box.isVisibleTo(option_widget_container):
                if (br_property != "Opacity" and br_property != "Flow"):
                    model.setData(m_index, Qt.Checked, Qt.CheckStateRole) if new_state  else model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                            
                check_box.setChecked(new_state)  
                break  
              
    
    def setSoakInk(self, br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model()
        for check_box in current_settings_widget.findChildren(QCheckBox, 'soakInkCBox'): 
            if check_box.isVisibleTo(option_widget_container):
                model.setData(m_index, Qt.Checked, Qt.CheckStateRole) if new_state else  model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                        
                check_box.setChecked(new_state)  
                break  
             
    def setPaintMode(self, br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model() 
        
        rbt = 'radioWash' if new_state else 'radioBuildup'

        for radio in current_settings_widget.findChildren(QRadioButton, rbt): 
            if radio.isVisibleTo(option_widget_container):  
                if radio.isChecked() == False: 
                    model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                    radio.setChecked(True) 
                break   
 
        self.set_brushSize()   
    #----------------------------------------------------#
    # Toggle Other option                                #
    # [Painting Mode / Ink depleteion]                   #
    #----------------------------------------------------#

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
                    self.BrushFade.setEnabled(True) 
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
    # Check Palette Value                                #
    #                                                    #
    #----------------------------------------------------#

    def get_palette(self):
        for window in QApplication.topLevelWidgets():
            if isinstance(window, QMainWindow) and window.metaObject().className() == 'KisMainWindow':
                for widget, _ in self.walk_widgets(window):
                    real_cls_name = widget.metaObject().className()
                    #obj_name = widget.objectName() 
                    if real_cls_name == 'KisPopupPalette':             
                        return widget



    def get_palette_values(self):    
        palette = self.get_palette()  
        if(palette.isVisible()): 
            for view in palette.findChildren(QWidget): 
                if(view.metaObject().className() == 'KisBrushHud'): 
                    for spin in view.findChildren(QDoubleSpinBox):
                        key = spin.prefix().rstrip()
                        self.br_values[key] = spin.value() 
                    for combo in view.findChildren(QComboBox): 
                        self.br_values["Smudge mode:"] = combo.currentText() 

                if(len(self.br_values) == 4):
                    break
 
        return self.br_values             
    


    def set_PaletteValue(self,values):
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
        current_view = None  
        
        for view in option_widget_container.findChildren(QListView):
            if view.metaObject().className() == 'KisCategorizedListView':
                if view.isVisibleTo(option_widget_container):
                    current_view = view
                    break

        props = ["Opacity", "Color Rate", "Smudge Length", "Brush Tip"]
 
        #disable option here 
        if current_view :
            current_settings_widget = current_view.parent()
            s_model = current_view.selectionModel()
            model = current_view.model()
            target_index = None
            for br_property in props:
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
                    
                    if(target_index.data() in props ): 
                        for combo in current_settings_widget.findChildren(QComboBox):   
                            if(combo.isVisibleTo(option_widget_container) and combo.metaObject().className() == "QComboBox"): 
                                if(combo.currentText() == "Dulling" or combo.currentText() == "Smearing"): 
                                    if(values["Smudge mode:"] != None):
                                        index = combo.findText(values["Smudge mode:"], Qt.MatchFixedString)
                                        if index >= 0:
                                                combo.setCurrentIndex(index) 
                                            
                                        
                        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox):    
                            if(spin_box.isVisibleTo(option_widget_container) and spin_box.metaObject().className() == "KisAngleSelectorSpinBox"): 
                                if(br_property == "Brush Tip"):
                                    if(values["Angle:"] != None):
                                        spin_box.setValue(values["Angle:"])
                                        break
                                        
                        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'strengthSlider'):    
                            if(spin_box.isVisibleTo(option_widget_container)):   
                                if(br_property == "Color Rate"):
                                    if(values["Color Rate:"] != None):
                                        spin_box.setValue(values["Color Rate:"] * 100) 
                                elif(br_property == "Opacity"): 
                                    if(values["Opacity:"] != None):
                                        spin_box.setValue(values["Opacity:"] * 100)
                                else:
                                    if(values["Smudge Length:"] != None): 
                                        spin_box.setValue(values["Smudge Length:" ] * 100)

                        
                        
                                        
    #----------------------------------------------------#
    # Check Pressure Toggle Curve Check box of           #
    # Corresponding Property                             #
    #----------------------------------------------------#
    
        
        

    #----------------------------------------------------#
    # Load the current state of brush property toggles   #
    #                                                    #
    #----------------------------------------------------#
   
    def loadState(self): 
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
        
        
        current_view = self.findView(option_widget_container)
          
        #disable option here
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

                self.evalTargetIndex(target_index, s_model, current_view, br_property, current_settings_widget, option_widget_container)   
                

        self.isPropertyExist(br_property)

    
    def findView(self, option_widget_container):
        current_view = None
        for view in option_widget_container.findChildren(QListView):
            if view.metaObject().className() == 'KisCategorizedListView':
                if view.isVisibleTo(option_widget_container):
                    current_view = view
                    break
        
        return current_view 
  

    def evalTargetIndex(self, target_index, s_model, current_view, br_property, current_settings_widget, option_widget_container ):
        if target_index is None: return False

        s_model.clear()
        s_model.select(target_index, QItemSelectionModel.SelectCurrent)
        s_model.setCurrentIndex(target_index, QItemSelectionModel.SelectCurrent)
        current_view.setCurrentIndex(target_index)
        current_view.activated.emit(target_index)
        
        if(br_property != "Brush Tip"): 
            m_check = self.setOptionProperty(br_property, target_index, current_settings_widget, option_widget_container)              
        else:  
            self.setOptionBrushTip(current_settings_widget, option_widget_container)
            
    #toggling is done here

    def setOptionBrushTip(self, current_settings_widget, option_widget_container): 
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

    def setOptionProperty(self, br_property, target_index, current_settings_widget, option_widget_container):
        m_check = False

        if (br_property != "Opacity" and br_property != "Flow" and br_property != 'Painting Mode') and target_index.flags() & Qt.ItemIsUserCheckable:
            self.property_fn[br_property] = 1 
            m_check = True if target_index.data(Qt.CheckStateRole) else False 

        if br_property == "Overlay Mode":
            self.property_fn[br_property] = 1
            self.checkState(br_property, target_index.data(Qt.CheckStateRole), True)
        
        if br_property == "Ink depletion" :  
            self.loadSoakInk(br_property, m_check, current_settings_widget, option_widget_container)
        elif br_property == "Painting Mode":
            self.loadPaintMode(br_property, m_check, current_settings_widget, option_widget_container)
        else:
            self.loadUseCurve(br_property, m_check, current_settings_widget, option_widget_container)
        
        return m_check

    def loadUseCurve(self, br_property, m_check, current_settings_widget, option_widget_container ):
        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):  
            self.property_fn[br_property] = 1
            if br_property != "Opacity" and br_property != "Flow"  and check_box.isVisibleTo(option_widget_container) :    
                self.checkState(br_property, check_box.isChecked(), m_check)
                break
            else: 
                if(check_box.isVisibleTo(option_widget_container)): 
                    self.checkState(br_property, check_box.isChecked(), True) 

    def loadSoakInk(self, br_property, m_check, current_settings_widget, option_widget_container ): 
        for check_box in current_settings_widget.findChildren(QCheckBox, 'soakInkCBox'):  
            self.property_fn[br_property] = 1
            if check_box.isVisibleTo(option_widget_container) :    
                self.checkState(br_property, check_box.isChecked(), m_check)
                break
            else: 
                if(check_box.isVisibleTo(option_widget_container)): 
                    self.checkState(br_property, check_box.isChecked(), True) 

    #For Paint Mode False => Build Up, True => Wash
    def loadPaintMode(self, br_property, m_check, current_settings_widget, option_widget_container ): 
        for radio in current_settings_widget.findChildren(QRadioButton, 'radioWash'):  
            self.property_fn[br_property] = 1
            if radio.isVisibleTo(option_widget_container) :    
                self.checkState(br_property, radio.isChecked(), True)

    def checkState(self, br_property, check1 , check2):
        if(check1 and check2): 
            self.toggleState[br_property] = True
            self.toggleIcon(br_property,True)
        else:
            self.toggleState[br_property] = False
            self.toggleIcon(br_property,False)
 

    def isPropertyExist(self,br_property): 
        for br_property in self.property: 
            if(br_property != "Brush Tip"): 
                if(self.property_fn[br_property] == 1):
                    self.BrushProperty[br_property].setEnabled(True)
                else: 
                    self.BrushProperty[br_property].setEnabled(False)
                    self.toggleState[br_property] = False
                    self.toggleIcon(br_property,False) 
            self.property_fn[br_property] = 0


instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        Compactbrushtoggler)

instance.addDockWidgetFactory(dock_widget_factory)