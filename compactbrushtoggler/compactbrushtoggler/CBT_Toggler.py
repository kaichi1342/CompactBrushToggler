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
        
import os, math, json

from PyQt5.QtCore import (  QItemSelectionModel, QSize, QTimer, Qt, pyqtSignal, QLocale )
 
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QListView,
    QFrame,QWidget, QDoubleSpinBox,QMainWindow,
    QComboBox, QMessageBox, QRadioButton  
)
 
from .CBT_Icons import * 
from .CBT_Translation import * 

class CBT_Toggler():
    language    = [] 
    
    last_brush  = ""
    cur_size    = 1 

    toggleState = {}
    
    theme_color = {
        "dark"  : {"on" :  "background-color : #305475; color : #D2D2D2;", "off" : "background-color : #383838 ; color : #D2D2D2;", "disabled" : "background-color : #1a1a1a; color : #9A9A9A;"},
        "light" : {"on" :  "background-color : #8BD5F0; color : #9A9A9A;", "off" : "background-color : #1a1a1a ; color : #373737;", "disabled" : "background-color : #9A9A9A; color : #2a2a2a;"}
    } 

    br_values = {"Size:" : None, "Opacity:" : None, "Color Rate:" : None, "Smudge Length:" : None, "Angle:" : None, "Smudge mode:" : "Dulling"}

    property = [ 
        "Size","Opacity","Flow","Softness","Rotation",
        "Scatter","Color Rate","Overlay Mode", "Ink depletion","Painting Mode", "Brush Tip" 
    ] 
 
    
    #Painting Mode : 0 => Build Up , 1 => Wash
    
    property_fn = { 
        "Size"          : 0,
        "Opacity"       : 0,
        "Flow"          : 0,
        "Softness"      : 0,
        "Rotation"      : 0,
        "Scatter"       : 0, 
        "Color Rate"    : 0, 
        "Overlay Mode"  : 0,
        "Ink depletion" : 0,
        "Painting Mode" : 0, 
        "Brush Tip"     : 0,
    } 

    brush_text = {
        "short" : { 
            "Size"              : "Sze",            "Opacity"       : "Opc",
            "Flow"              : "Flw",            "Softness"      : "Sft",
            "Rotation"          : "Rot",            "Scatter"       : "Sct",    
            "Color Rate"        : "Col",            "Overlay Mode"  : "Ovl", 
            "Ink depletion"     : "Sok",            "Painting Mode" : "PtM"  
        },
        "full"  : { 
            "Size"              : "Size",           "Opacity"       : "Opacity",
            "Flow"              : "Flow",           "Softness"      : "Softness",
            "Rotation"          : "Rotation",       "Scatter"       : "Scatter",    
            "Color Rate"        : "Color Rate",     "Overlay Mode"  : "Overlay Mode",  
            "Ink depletion"     : "Soak Ink",       "Painting Mode" : "Painting Mode"  
        }
    }

    def __init__(self, parent, theme_preset = False): 
        self.parent = parent 
        self.cbt_icons     = CBT_Icons(self)  
        self.theme_color = theme_preset if theme_preset != False else self.theme_color

        translation   = CBT_Translation(self)  
        self.translation = translation.getTranslationTable()
        #self.lang = translation.getLanguage()
        
 
    def setInputItems(self, brush_property, fade_spinner, fade_slider):
        self.BrushProperty = brush_property
        self.BrushFadeSlider = fade_slider
        self.BrushFade = fade_spinner
    
    def setTheme(self, theme):
        self.theme = theme 
     

    def translate(self, key):
        tn_table = self.translation
        prop = tn_table[key]

        return  prop["tr"] if prop["tr"] else prop["en"]

    def translateEn(self, key):
        tn_table = self.translation
        prop = tn_table[key]

        return  prop["en"]


    def setTestLabel(self, text, append = False):
        if append:
            self.parent.lbl_test.setText(self.parent.lbl_test.text() + text)
        else:
            self.parent.lbl_test.setText(text)

    
    #----------------------------------------------------#
    # For Changing Info                                  #
    #                                                    #
    #----------------------------------------------------#
    
    def loadBrushInfo(self ): 
        cur_brush = Krita.instance().activeWindow().activeView().currentBrushPreset() 
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()
 
        #self.get_palette_values() 
        if cur_brush.name() != self.last_brush :  
            self.resetPropertyFn()   
            self.last_brush = cur_brush.name()  
            self.loadState() 
            
              
    #----------------------------------------------------#
    # Toggle And Change Function                         #
    #                                                    #
    #----------------------------------------------------#
 
    def toggleOptions(self, prop):  
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()
        
        if(self.toggleState[prop] == True):
            self.setOptions( prop , False)
            self.toggleState[prop] = False 
            self.toggleIcon(prop,False)
        else:
            self.setOptions(prop, True)
            self.toggleState[prop] = True 
            self.toggleIcon(prop,True) 
 
        self.setBrushSize() 
    
     
           
    def toggleIcon(self, prop, state):  
 
        def_color  = self.theme_color[self.theme]["off"] if not state  else self.theme_color[self.theme]["on"]    
        def_color  = def_color if self.property_fn[prop] == 1 else self.theme_color[self.theme]["disabled"]


        if prop == "Painting Mode": 
            icon = 'paint_wash' if state else 'paint_buildup' 
            self.BrushProperty[prop].setIcon(self.cbt_icons.icon(icon)) 
            self.BrushProperty[prop].setStyleSheet(def_color)
            return True 

        if prop == "Ink depletion":
            icon = 'soak_ink' if state else 'soak_ink_off' 
            self.BrushProperty[prop].setIcon( self.cbt_icons.icon(icon)) 
            self.BrushProperty[prop].setStyleSheet(def_color)
            return True 

        if prop == "Overlay Mode":
            icon = 'overlay_on' if state else 'overlay_off' 
            self.BrushProperty[prop].setIcon( self.cbt_icons.icon(icon)) 
            self.BrushProperty[prop].setStyleSheet(def_color)
            return True 
  
        icon = 'pressure_'+prop.lower() if prop != "Color Rate" else 'pressure_colrate' 
        icon = 'pressure_off' if not state else icon



        self.BrushProperty[prop].setIcon(self.cbt_icons.icon(icon))
        self.BrushProperty[prop].setStyleSheet(def_color)      

        return True
           

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
            if isinstance(window, QFrame) and (window.objectName() == 'popup frame' or window.objectName() == 'KisPopupButtonFrame' ):
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

        tra_property = self.translate(br_property)

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
                if index.data() == tra_property: 
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
        
        tra_property = self.translate(br_property)
         
        if current_view: 

            if tra_property == self.translate("Painting Mode"):
                self.setPaintMode(br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container)
            elif tra_property == self.translate("Ink depletion"):
                self.setSoakInk(br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container)
            else: 
                self.setCheckBoxUseCurve(br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container)
    


    def setCheckBoxUseCurve(self, br_property, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model()

        tra_property = self.translate(br_property)
 
        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):
            if tra_property == self.translate("Overlay Mode"):
                model.setData(m_index, Qt.Checked, Qt.CheckStateRole)  if new_state else model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)

            if check_box.isVisibleTo(option_widget_container):
                if tra_property != self.translate("Opacity") and tra_property != self.translate("Flow") :
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
         
  
    #----------------------------------------------------#
    # Toggle Other option                                #
    # [Painting Mode / Ink depleteion]                   #
    #----------------------------------------------------#

    #----------------------------------------------------#
    # Set the Value of Brush HFade in the Brush          #
    # Property Editor                                    #
    #----------------------------------------------------#
    def setBrushFadeValue(self):  
        container_info = self.selectBrushContainer("Brush Tip")
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        if current_view:   
            for spin_box in current_settings_widget.findChildren(QDoubleSpinBox):
                if spin_box.isVisibleTo(option_widget_container) and (spin_box.objectName() == "inputRadius" or spin_box.objectName() == "brushSizeSpinBox"):  
                    spin_box.setValue(self.cur_size)  

                if spin_box.isVisibleTo(option_widget_container) and spin_box.objectName() == "inputHFade":  
                    spin_box.setValue(self.BrushFade.value()) 
                    self.BrushFade.setEnabled(True) 
                    break 
 
    def setBrushSize(self):
        container_info = self.selectBrushContainer("Brush Tip")
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        if current_view:   
            for spin_box in current_settings_widget.findChildren(QDoubleSpinBox):
               if spin_box.isVisibleTo(option_widget_container) and (spin_box.objectName() == "inputRadius" or spin_box.objectName() == "brushSizeSpinBox"):  
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
                tra_property = self.translate(br_property)
                for row in range(model.rowCount()):
                    index = model.index(row)   
                    if index.data() == tra_property: 
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
                                if combo.currentText() == self.translate("Dulling") or combo.currentText() == self.translate("Smearing"): 
                                    if values["Smudge mode:"] != None:
                                        index = combo.findText(values["Smudge mode:"], Qt.MatchFixedString)
                                        if index >= 0:
                                                combo.setCurrentIndex(index) 
                                            
                                        
                        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox):    
                            if(spin_box.isVisibleTo(option_widget_container) and spin_box.metaObject().className() == "KisAngleSelectorSpinBox"): 
                                if tra_property == self.translate("Brush Tip"):
                                    if values["Angle:"] != None:
                                        spin_box.setValue(values["Angle:"])
                                        break
                                        
                        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'strengthSlider'):    
                            if(spin_box.isVisibleTo(option_widget_container)):   
                                if tra_property == self.translate("Color Rate"):
                                    if(values["Color Rate:"] != None):
                                        spin_box.setValue(values["Color Rate:"] * 100) 
                                elif tra_property == self.translate("Opacity"): 
                                    if values["Opacity:"] != None:
                                        spin_box.setValue(values["Opacity:"] * 100)
                                else:
                                    if values["Smudge Length:"] != None: 
                                        spin_box.setValue(values["Smudge Length:" ] * 100)

                        
                        
                                        
    #----------------------------------------------------#
    # Check Pressure Toggle Curve Check box of           #
    # Corresponding Property                             #
    #----------------------------------------------------#
    
        
        

    #----------------------------------------------------#
    # Load the current state of brush property toggles   #
    #                                                    #
    #----------------------------------------------------#
   
    def loadState(self ): 
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
         
        current_view = self.findView(option_widget_container)
          
        #disable option here
        for br_property in self.property: 
            tra_property = self.translate(br_property)

            if current_view:
                current_settings_widget = current_view.parent()
                s_model = current_view.selectionModel()
                model = current_view.model()
                target_index = None
                for row in range(model.rowCount()):
                    index = model.index(row)   
                    if index.data() == tra_property: 
                        target_index = index
                        break

                self.evalTargetIndex(target_index, s_model, current_view, br_property, current_settings_widget, option_widget_container)   
                 
        self.isPropertyExist()

    
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
        
        tra_property = self.translate(br_property)
       
        if(tra_property != self.translate("Brush Tip")):   
            m_check = self.setOptionProperty(br_property, target_index, current_settings_widget, option_widget_container)              
        else:  
            self.setOptionBrushTip(current_settings_widget, option_widget_container)
    
    #-----------------------#
    # toggling is done here #
    #-----------------------#

    def setOptionBrushTip(self, current_settings_widget, option_widget_container): 
        ft = 0  
          
        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'inputHFade'): 
            if spin_box.isVisibleTo(option_widget_container): 
                ft = 1
                self.BrushFade.setEnabled(True)
                self.BrushFadeSlider.setEnabled(True) 
                self.BrushFadeSlider.setValue(int(spin_box.value()*100))  
                break

        if ft == 0:
            self.BrushFadeSlider.setValue(0)
            self.BrushFade.setEnabled(False)
            self.BrushFadeSlider.setEnabled(False)

    def setOptionProperty(self, br_property, target_index, current_settings_widget, option_widget_container):
        m_check = False

        tra_property = self.translate(br_property)
        
        self.property_fn[br_property] = 0   
        #found = False

        if (tra_property != self.translate("Opacity") and tra_property != self.translate("Flow") and tra_property != self.translate("Painting Mode")) and target_index.flags() & Qt.ItemIsUserCheckable:
            self.property_fn[br_property] = 1 
            m_check = True if target_index.data(Qt.CheckStateRole) else False 

        if tra_property == self.translate("Overlay Mode"):
            self.property_fn[br_property] = 1
            self.checkState(br_property, target_index.data(Qt.CheckStateRole), True)
       
        
        if tra_property == self.translate("Ink depletion") :  
            self.loadSoakInk(br_property, m_check, current_settings_widget, option_widget_container)
        elif tra_property == self.translate("Painting Mode"):
            self.loadPaintMode(br_property, m_check, current_settings_widget, option_widget_container)
        else:
            self.loadUseCurve(br_property, m_check, current_settings_widget, option_widget_container)
        
        
        return m_check

    def loadUseCurve(self, br_property, m_check, current_settings_widget, option_widget_container ):
        tra_property = self.translate(br_property)

        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):  
            self.property_fn[br_property] = 1
            if tra_property != self.translate("Opacity") and tra_property != self.translate("Flow")  and check_box.isVisibleTo(option_widget_container) :    
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
 

    def isPropertyExist(self): 
        for br_property in self.property_fn.keys(): 
            tra_property = self.translate(br_property)
            if(br_property == "Brush Tip"): continue    

            if(self.property_fn[br_property] == 1): 
                self.BrushProperty[br_property].setEnabled(True)
            else:  
                self.toggleState[br_property] = False
                self.toggleIcon(br_property,False)  
                self.BrushProperty[br_property].setStyleSheet(self.theme_color[self.theme]["disabled"])
                self.BrushProperty[br_property].setEnabled(False)
        
             
    def resetPropertyFn(self, text = ""):  
        for property in self.property_fn.keys(): 
            if(property == "Brush Tip"): continue    
            self.property_fn[property] = 0   
     
    def printPropertyFn(self, text = ""): 
        for property in self.property_fn.keys(): 
            if(property == "Brush Tip"): continue    
            self.setTestLabel(property + " : " + str( self.property_fn[property] ) + ",", True)
  