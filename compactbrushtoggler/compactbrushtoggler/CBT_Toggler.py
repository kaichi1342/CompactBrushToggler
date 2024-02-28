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

from PyQt5.QtCore import (  QItemSelectionModel, QSize, QTimer, Qt, pyqtSignal, QLocale, qDebug, qWarning )
 
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
 
    theme_color = { } 

    property_list = {
        "Fade",
        "Size",
        "Opacity",
        "Flow",
        "Softness",
        "Rotation",
        "Scatter",
        "Color Rate",
        "Overlay Mode",
        "Ink depletion",
        "Painting Mode",
    }

 
    def __init__(self, parent, theme_preset = False): 
        self.parent = parent 
        self.cbt_icons     = CBT_Icons(self)  
        self.theme_color = theme_preset if theme_preset != False else self.theme_color

        translation   = CBT_Translation(self)  
        self.translation = translation.getTranslationTable()
        self.loadBrushSetting()

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

    def loadBrushSetting(self):
        self.brush_definition = {   "Fade"  : self.BrushSetting("Brush Tip", "Fade",  0, False) }
       
        self.property = { 
            "Size"          : self.BrushSetting("Size",          "PressureSize",               False,  False, "SizeUseCurve"),
            "Opacity"       : self.BrushSetting("Opacity",       "OpacityUseCurve",            False,  False),
            "Flow"          : self.BrushSetting("Flow",          "FlowUseCurve",               False,  False),
            "Softness"      : self.BrushSetting("Softness",      "PressureSoftness",           False,  False, "SoftnessUseCurve"),
            "Rotation"      : self.BrushSetting("Rotation",      "PressureRotation",           False,  False, "RotationUseCurve"),
            "Scatter"       : self.BrushSetting("Scatter",       "PressureScatter",            False,  False, "ScatterUseCurve"), 
            "Color Rate"    : self.BrushSetting("Color Rate",    "PressureColorRate",          False,  False, "ColorRateUseCurve"),
            "Overlay Mode"  : self.BrushSetting("Overlay Mode",  "MergedPaint",                False,  False),
            "Ink depletion" : self.BrushSetting("Ink depletion", "HairyInk/enabled",           False,  False, "HairyInk/soak"),
            "Painting Mode" : self.BrushSetting("Painting Mode", "PaintOpAction",              False,  False), 
        }

        self.property["Size"].setIcons("pressure_size", "pressure_size_off")
        self.property["Opacity"].setIcons("pressure_opacity", "pressure_opacity_off")

        self.property["Flow"].setIcons("pressure_flow", "pressure_off")
        self.property["Softness"].setIcons("pressure_softness", "pressure_softness_off")

        self.property["Rotation"].setIcons("pressure_rotation", "pressure_rotation_off")
        self.property["Scatter"].setIcons("pressure_scatter", "pressure_scatter_off")
          
        self.property["Color Rate"].setIcons( "pressure_colrate", "pressure_colrate_off")
        self.property["Overlay Mode"].setIcons("overlay_on", "overlay_off")

        self.property["Ink depletion"].setIcons("soak_ink", "soak_ink_off")
        self.property["Painting Mode"].setIcons("paint_wash", "paint_buildup")


    def resetBrushSetting(self):
        self.brush_definition["Fade"].setValueAndAvailability(0, False)

        self.property["Size"].setValueAndAvailability(False, False)
        self.property["Opacity"].setValueAndAvailability(False, False)
        self.property["Flow"].setValueAndAvailability(False, False)
        self.property["Softness"].setValueAndAvailability(False, False)
        self.property["Rotation"].setValueAndAvailability(False, False)
        self.property["Scatter"].setValueAndAvailability(False, False) 

        self.property["Color Rate"].setValueAndAvailability(False, False)
        self.property["Overlay Mode"].setValueAndAvailability(False, False)
        self.property["Ink depletion"].setValueAndAvailability(False, False)
        self.property["Painting Mode"].setValueAndAvailability(False, False)

 
    #----------------------------------------------------#
    # For Changing Info                                  #
    #                                                    #
    #----------------------------------------------------#

    def loadBrushInfo(self ): 
        cur_brush = Krita.instance().activeWindow().activeView().currentBrushPreset() 
        self.cur_size  = Krita.instance().activeWindow().activeView().brushSize()
 
        #self.get_palette_values() 
        if cur_brush.name() != self.last_brush :  
            self.resetBrushSetting()   
            self.last_brush = cur_brush.name()  
            self.loadState() 


    #----------------------------------------------------#
    # Toggle And Change Function                         #
    #                                                    #
    #----------------------------------------------------#
 
    def toggleOptions(self, prop):  
        cur_state = self.property[prop].value 

        if self.property[prop].is_available == False : return False
  
        if(cur_state == True):
            new_value = False #self.translatePropertyState(prop, False)
            self.property[prop].value = False
        else:
            new_value = True #self.translatePropertyState(prop, True)
            self.property[prop].value = True
           
        self.setOptions( prop , new_value ) 
        self.toggleIcon(prop)
        self.setBrushSize() 
 
    def translatePropertyState(self, prop, state):
        if prop in ["MergedPaint", "HairyInk/soak", "PaintOpAction"]:
            return True if state else False   
        else:
            return True if state else False


    def toggleIcon(self, prop): 
        state = self.property[prop].value  

        def_color  = self.theme_color[self.theme]["off"] if not state  else self.theme_color[self.theme]["on"]
        def_color  = def_color if self.property[prop].is_available else self.theme_color[self.theme]["disabled"]

        icon = self.property[prop].icon_off if not state else self.property[prop].icon_on
        
        self.BrushProperty[prop].setIcon(self.cbt_icons.icon(icon)) 
        self.BrushProperty[prop].setStyleSheet(def_color)
        


    #---------------------------------------------------------------------------#
    # TREE TRAVERSING    / BRUSH SETTING                                        # 
    #---------------------------------------------------------------------------#

    #----------------------------------------------------#
    # For Traversing nodes to get to Brush Editor Docker #
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
    def selectBrushContainer(self, prop):
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
        current_view = None
        selectedRow  = None 
 
        prop_key = self.property[prop].getKey(True) if prop != "Fade" else self.brush_definition["Fade"].getKey(True)
        
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
                if index.data() == prop_key: 
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
    # Load the current state of brush property toggles   #
    #                                                    #
    #----------------------------------------------------#
 
    def loadState(self): 
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
         
        current_view = self.findView(option_widget_container)

        for prop in self.property_list:  
            qDebug(prop)
            prop_key = self.property[prop].getKey(True) if prop != "Fade" else self.brush_definition["Fade"].getKey(True)
            current_settings_widget = current_view.parent()
            s_model = current_view.selectionModel()
            model = current_view.model()
            target_index = None
            for row in range(model.rowCount()):
                index = model.index(row)     
                if index.data() == prop_key: 
                    target_index = index
                    break

            self.evalTargetIndex(target_index, s_model, current_view, prop, current_settings_widget, option_widget_container)   

        self.isPropertyExist()     
        pass

    def findView(self, option_widget_container):
        current_view = None
        for view in option_widget_container.findChildren(QListView):
            if view.metaObject().className() == 'KisCategorizedListView':
                if view.isVisibleTo(option_widget_container):
                    current_view = view
                    break
        
        return current_view 

    def evalTargetIndex(self, target_index, s_model, current_view, prop, current_settings_widget, option_widget_container ):
        if target_index is None: return False

        s_model.clear()
        s_model.select(target_index, QItemSelectionModel.SelectCurrent)
        s_model.setCurrentIndex(target_index, QItemSelectionModel.SelectCurrent)
        current_view.setCurrentIndex(target_index)
        current_view.activated.emit(target_index)
        
        prop_key = self.property[prop].getKey(True) if prop != "Fade" else self.brush_definition["Fade"].getKey(True)
       
        if(prop_key != self.translate("Brush Tip")):    
            m_check = self.setOptionProperty(prop, target_index, current_settings_widget, option_widget_container)              
        else:  
            self.setOptionBrushTip(prop, current_settings_widget, option_widget_container)
    
    #-----------------------#
    # GET BRUSH VALUE       #
    #-----------------------#

    def setOptionBrushTip(self, prop, current_settings_widget, option_widget_container): 
        qDebug("tppppsss")      
        for spin_box in current_settings_widget.findChildren(QDoubleSpinBox, 'inputHFade'): 
            qDebug("fnd tipsss")      
            if spin_box.isVisibleTo(option_widget_container):  
                self.brush_definition[prop].value = int(spin_box.value()*100)
                self.brush_definition[prop].is_available = True 
                break
 

    def setOptionProperty(self, prop, target_index, current_settings_widget, option_widget_container):
        m_check = False

        prop_key = self.property[prop].getKey(True)
         
        if (prop_key != self.translate("Opacity") and prop_key != self.translate("Flow") and prop_key != self.translate("Painting Mode")) and target_index.flags() & Qt.ItemIsUserCheckable:
            self.property[prop].is_available = True
            self.property[prop].value = self.checkState(target_index.data(Qt.CheckStateRole), True)
            m_check = self.property[prop].value

        if prop_key == self.translate("Overlay Mode"):
            self.property[prop].is_available = True
            self.property[prop].value = self.checkState(target_index.data(Qt.CheckStateRole), True)
            m_check = self.property[prop].value
        
         
        if prop_key == self.translate("Ink depletion") :   
            self.loadSoakInk(prop, m_check, current_settings_widget, option_widget_container) 
        elif prop_key == self.translate("Painting Mode"):
            self.loadPaintMode(prop, m_check, current_settings_widget, option_widget_container) 
        else:
            self.loadUseCurve(prop, m_check, current_settings_widget, option_widget_container)
        
        
        return m_check

    def checkState(self,  check1 , check2):
        return True if(check1 and check2) else False
        
    def loadSoakInk(self, prop, m_check, current_settings_widget, option_widget_container ): 
        for check_box in current_settings_widget.findChildren(QCheckBox, 'soakInkCBox'):  
            self.property[prop].is_available = True 
            if check_box.isVisibleTo(option_widget_container) :    
                self.property[prop].value = self.checkState(check_box.isChecked(), m_check)
                break
            else: 
                if(check_box.isVisibleTo(option_widget_container)): 
                    self.property[prop].value = self.checkState(check_box.isChecked(), True) 
                    

 
    #For Paint Mode False => Build Up, True => Wash
    def loadPaintMode(self, prop, m_check, current_settings_widget, option_widget_container ): 
        for radio in current_settings_widget.findChildren(QRadioButton, 'radioWash'):  
            self.property[prop].is_available = True
            if radio.isVisibleTo(option_widget_container) :    
                self.property[prop].value = self.checkState(radio.isChecked(), True)


    def loadUseCurve(self, prop, m_check, current_settings_widget, option_widget_container ): 
        prop_key = self.property[prop].getKey(True)

        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):  
            self.property[prop].is_available = True
            if prop_key != self.translate("Opacity") and prop_key != self.translate("Flow")  and check_box.isVisibleTo(option_widget_container) :    
                self.property[prop].value = self.checkState(check_box.isChecked(), m_check)
                break
            else: 
                if(check_box.isVisibleTo(option_widget_container)): 
                    self.property[prop].value = self.checkState(check_box.isChecked(), True) 


    def isPropertyExist(self): 
        if self.brush_definition["Fade"].is_available :
            qDebug("heeeeer")  
            self.BrushFadeSlider.setValue( int( self.brush_definition["Fade"].value * 100 ) )  
            self.BrushFade.setValue( self.brush_definition["Fade"].value )
            self.BrushFadeSlider.setEnabled(True)
            self.BrushFade.setEnabled(True) 
        else: 
            qDebug("xxxsddd")  
            self.BrushFadeSlider.setValue( 0 )  
            self.BrushFade.setValue( 0 )
            self.BrushFadeSlider.setEnabled(False)
            self.BrushFade.setEnabled(False)  

        #TOGGLES
        for key in self.property.keys(): 
            prop = self.property[key]  
            if prop.is_available :  
                self.BrushProperty[key].setEnabled(True)
                self.toggleIcon(key)  
            else: 
                prop.value = False 
                self.toggleIcon(key)   
                self.BrushProperty[key].setStyleSheet(self.theme_color[self.theme]["disabled"])
                self.BrushProperty[key].setEnabled(False)


    
    #----------------------------------------------------#
    # Check Pressure Toggle Curve Check box of           #
    # Corresponding Property                             #
    #----------------------------------------------------#    
    def setOptions(self, prop, new_state): 
        container_info = self.selectBrushContainer(prop) 
        m_index = container_info["model_index"]
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        prop_key = self.property[prop].getKey(True)
         
        if current_view: 
            if prop_key == self.translate("Painting Mode"):
                self.setPaintMode(prop, new_state, m_index, current_view, current_settings_widget, option_widget_container)
            elif prop_key == self.translate("Ink depletion"):
                self.setSoakInk(prop, new_state, m_index, current_view, current_settings_widget, option_widget_container)
            else: 
                self.setCheckBoxUseCurve(prop, new_state, m_index, current_view, current_settings_widget, option_widget_container)
              


    #----------------------------------------------------#
    # Set the Value of Brush Toggles                     # 
    #----------------------------------------------------#
    def setCheckBoxUseCurve(self, prop, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model()
 
        prop_key = self.property[prop].getKey(True)
 
        for check_box in current_settings_widget.findChildren(QCheckBox, 'checkBoxUseCurve'):
            if prop_key == self.translate("Overlay Mode"):
                model.setData(m_index, Qt.Checked, Qt.CheckStateRole)  if new_state else model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)

            if check_box.isVisibleTo(option_widget_container):
                if prop_key != self.translate("Opacity") and prop_key != self.translate("Flow") :
                    model.setData(m_index, Qt.Checked, Qt.CheckStateRole) if new_state  else model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                            
                check_box.setChecked(new_state)  
                break  
 
              
    def setSoakInk(self, prop, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model()
        for check_box in current_settings_widget.findChildren(QCheckBox, 'soakInkCBox'): 
            if check_box.isVisibleTo(option_widget_container):
                model.setData(m_index, Qt.Checked, Qt.CheckStateRole) if new_state else  model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                check_box.setChecked(new_state)  
                break   
             
    def setPaintMode(self, prop, new_state, m_index, current_view, current_settings_widget, option_widget_container):
        model = current_view.model() 
        
        rbt = 'radioWash' if new_state else 'radioBuildup'

        for radio in current_settings_widget.findChildren(QRadioButton, rbt): 
            if radio.isVisibleTo(option_widget_container):  
                if radio.isChecked() == False: 
                    model.setData(m_index, Qt.Unchecked , Qt.CheckStateRole)
                    radio.setChecked(True) 
                break  
         
    #----------------------------------------------------#
    # Set the Value of Brush HFade in the Brush          #
    # Property Editor                                    #
    #----------------------------------------------------#
    def setBrushFadeValue(self):  
        container_info = self.selectBrushContainer("Fade")
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
        container_info = self.selectBrushContainer("Fade")
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  
        
        if current_view:   
            for spin_box in current_settings_widget.findChildren(QDoubleSpinBox):
               if spin_box.isVisibleTo(option_widget_container) and (spin_box.objectName() == "inputRadius" or spin_box.objectName() == "brushSizeSpinBox"):  
                    spin_box.setValue(self.cur_size)  
                    break 

 
    
    #-----------------------#
    # Classes               #
    #-----------------------#
    class BrushSetting(): 
        def __init__(self, key, name, value, is_available, sub_name = ""):
            self.key  = key
            self.name = name
            self.sub_name = sub_name
            self.value = value
            self.is_available = is_available
            self.icon_on = ""
            self.icon_off = ""

            translation   = CBT_Translation(self)  
            self.translation = translation.getTranslationTable()

        def setIcons(self, on, off):
            self.icon_on = on
            self.icon_off = off

        def setValueAndAvailability(self, value, is_available):
            self.value = value
            self.is_available = is_available

        def getKey(self, translate = False):
            return  self.key if not translate else self.translate(self.key)
            
        def translate(self, key):
            tn_table = self.translation
            prop = tn_table[key]

            return  prop["tr"] if prop["tr"] else prop["en"]

        def toString(self):
            return self.name + " : " + str(self.value) + " - " + str(self.is_available)
        
        