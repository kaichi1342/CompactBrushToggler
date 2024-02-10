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
# This is docker that  toggle pen pressure on/off of 12 brush property        #
# [Size, Opacity, Flow, Softness, Scatter, Smudge Lenght, Smudge Mode,        #
#  Color Rage, Overlay Moad, Soak Ink, Painting Mode]                         #
# and adjust brush hfade without opening the Brush Editor.                    #
# -----------------------------------------------------------------------------
         
import os, math, json
import xml.etree.ElementTree as ET

from krita import *
from PyQt5.QtCore import (  QItemSelectionModel, QSize, QTimer, Qt, pyqtSignal, QLocale, qDebug, qWarning )
 
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QListView,
    QFrame,QWidget, QDoubleSpinBox,QMainWindow,
    QComboBox, QMessageBox, QRadioButton  
)
 
import xml.etree.ElementTree as ET

from .CBT_Icons import * 
from .CBT_Translation import * 



class CBT_Toggler():
    language    = [] 
    
    last_brush  = ""
    cur_size    = 1  
    
    theme_color = { } 

    property_list = {
        "PressureSize"                   : "Size",
        "OpacityUseCurve"                : "Opacity",
        "FlowUseCurve"                   : "Flow",
        "PressureSoftness"               : "Softness",
        "PressureRotation"               : "Rotation",
        "PressureScatter"                : "Scatter",
        "PressureSmudgeRate"             : "Smudge Length",
        "SmudgeRateMode"                 : "Smudge Mode",
        "PressureColorRate"              : "Color Rate",
        "MergedPaint"                    : "Overlay Mode",
        "HairyInk/soak"                  : "Ink depletion",
        "PaintOpAction"                  : "Painting Mode",
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
        self.brush_definition = {   "Fade"  : self.BrushSetting("Fade",  0, False) }
       
        self.property = { 
            "Size"          : self.BrushSetting("PressureSize",               False,  False, "SizeUseCurve"),
            "Opacity"       : self.BrushSetting("OpacityUseCurve",            False,  False),
            "Flow"          : self.BrushSetting("FlowUseCurve",               False,  False),
            "Softness"      : self.BrushSetting("PressureSoftness",           False,  False, "SoftnessUseCurve"),
            "Rotation"      : self.BrushSetting("PressureRotation",           False,  False, "RotationUseCurve"),
            "Scatter"       : self.BrushSetting("PressureScatter",            False,  False, "ScatterUseCurve"),
            "Smudge Length" : self.BrushSetting("PressureSmudgeRate",         False,  False, "SmudgeRateUseCurve"),
            "Smudge Mode"   : self.BrushSetting("SmudgeRateMode",             False,  False), 
            "Color Rate"    : self.BrushSetting("PressureColorRate",          False,  False, "ColorRateUseCurve"),
            "Overlay Mode"  : self.BrushSetting("MergedPaint",                False,  False),
            "Ink depletion" : self.BrushSetting("HairyInk/enabled",           False,  False, "HairyInk/soak"),
            "Painting Mode" : self.BrushSetting("PaintOpAction",              False,  False), 
        }

        self.property["Size"].setIcons("pressure_size", "pressure_size_off")
        self.property["Opacity"].setIcons("pressure_opacity", "pressure_opacity_off")

        self.property["Flow"].setIcons("pressure_flow", "pressure_off")
        self.property["Softness"].setIcons("pressure_softness", "pressure_softness_off")

        self.property["Rotation"].setIcons("pressure_rotation", "pressure_rotation_off")
        self.property["Scatter"].setIcons("pressure_scatter", "pressure_scatter_off")
         
        self.property["Smudge Length"].setIcons("pressure_smudlen", "pressure_smudlen_off")
        self.property["Smudge Mode"].setIcons("smudge_smearing", "smudge_dulling")

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
        self.property["Smudge Length"].setValueAndAvailability(False, False)
        self.property["Smudge Mode"].setValueAndAvailability(False, False)
         
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

        if prop == "Smudge Mode" :
            if not self.property["Smudge Length"].value : return False

        if(cur_state == True):
            new_value = str(self.translatePropertyState(prop, False))
            self.property[prop].value = False
        else:
            new_value = str(self.translatePropertyState(prop, True))
            self.property[prop].value = True
           
        self.setPropertyValue( prop , new_value ) 
        self.toggleIcon(prop)

        if prop == "Smudge Length":
            if not self.property[prop].value :   
                self.BrushProperty["Smudge Mode"].setStyleSheet(self.theme_color[self.theme]["disabled"])
                self.BrushProperty["Smudge Mode"].setEnabled(False)
            else:
                self.toggleIcon("Smudge Mode")
                self.BrushProperty["Smudge Mode"].setEnabled(True) 
      

    def translatePropertyState(self, prop, state):
        if prop in ["MergedPaint", "HairyInk/soak", "PaintOpAction"]:
            return 2 if state else 1  
        elif prop in [ "Smudge Mode" ]:
            return 0 if state else 1   #1 Dulling #0 Smearing
        else:
            return "true" if state else "false"
           
  
    def toggleIcon(self, prop): 
        state = self.property[prop].value  

        def_color  = self.theme_color[self.theme]["off"] if not state  else self.theme_color[self.theme]["on"]
        def_color  = def_color if self.property[prop].is_available else self.theme_color[self.theme]["disabled"]

        icon = self.property[prop].icon_off if not state else self.property[prop].icon_on
        
        self.BrushProperty[prop].setIcon(self.cbt_icons.icon(icon)) 
        self.BrushProperty[prop].setStyleSheet(def_color)

  
    #----------------------------------------------------#
    # Load the current state of brush property toggles   #
    #                                                    #
    #----------------------------------------------------#
 
    def loadState(self): 
        view = Krita.instance().activeWindow().activeView() 
        preset = Preset(view.currentBrushPreset())

        presetXMLString = preset.toXML()
        presetTree = ET.fromstring(presetXMLString)
         
        for param in presetTree.findall('param'): 
            name = param.get('name')
             
            if name in self.property_list :   
                self.property[self.property_list[name]].is_available = True 
                if name in ["MergedPaint", "HairyInk/soak", "PaintOpAction"]: 
                    self.property[self.property_list[name]].value = True if param.text == 2 else False 
                if name in ["SmudgeRateMode"]: 
                    self.property[self.property_list[name]].value = True if param.text == 1 else False 
                else:
                    self.property[self.property_list[name]].value = True if param.text == "true" else False
                
            elif name == "brush_definition":
                brushdef = ET.fromstring( param.text) 
                if(brushdef.get("type") != "auto_brush"): continue 
                brushopt = brushdef.find('MaskGenerator')
                self.brush_definition["Fade"].value = float(brushopt.get('hfade'))
                self.brush_definition["Fade"].is_available = True
            else:
                pass
                
        self.isPropertyExist()


    def isPropertyExist(self): 
        if self.brush_definition["Fade"].is_available :  
            self.BrushFadeSlider.setValue( int( self.brush_definition["Fade"].value * 100 ) )  
            self.BrushFade.setValue( self.brush_definition["Fade"].value )
            self.BrushFadeSlider.setEnabled(True)
            self.BrushFade.setEnabled(True) 
        else: 
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
    # Set the Toggle Value of The Corresponding Property # 
    #----------------------------------------------------#  
    def setPropertyValue(self, prop, new_value): 
        view = Krita.instance().activeWindow().activeView() 
        preset = Preset(view.currentBrushPreset())

        presetXMLString = preset.toXML()
        presetTree = ET.fromstring(presetXMLString)
        
        brush_property = self.property[prop] 
  
        for param in presetTree.findall('param'):   
            if param.get('name') == brush_property.name : 
                param.text = new_value 

                if brush_property.sub_name == "": continue
                 
                for sub_param in presetTree.findall('param'): 
                    if sub_param.get('name') ==  brush_property.sub_name:
                        sub_param.text = new_value
            
        
        presetXMLString = ET.tostring(presetTree, encoding="unicode")
        preset.fromXML(presetXMLString)


    #----------------------------------------------------#
    # Set the Value of Brush HFade in the Brush          #
    # Property Editor                                    #
    #----------------------------------------------------#
    def setBrushFadeValue(self):  
        view = Krita.instance().activeWindow().activeView() 
        preset = Preset(view.currentBrushPreset())

        presetXMLString = preset.toXML()
        presetTree = ET.fromstring(presetXMLString)
           
        for param in presetTree.findall('param'):   
            if param.get('name') == "brush_definition" : 
                brushdef = ET.fromstring( param.text)  
                if(brushdef.get("type") != "auto_brush"): continue
                
                brushopt = brushdef.find('MaskGenerator')
                brushopt.set('hfade', str(self.BrushFade.value()) ) 
                brushopt.set('vfade', str(self.BrushFade.value()) ) 

                xmlbrushdef = ET.tostring(brushdef, encoding="unicode")
                param.text = xmlbrushdef

        presetXMLString = ET.tostring(presetTree, encoding="unicode")
        preset.fromXML(presetXMLString)
 
    #-----------------------#
    # Classes               #
    #-----------------------#
    class BrushSetting(): 
        def __init__(self, name, value, is_available, sub_name = ""):
            self.name = name
            self.sub_name = sub_name
            self.value = value
            self.is_available = is_available
            self.icon_on = ""
            self.icon_off = ""

        def setIcons(self, on, off):
            self.icon_on = on
            self.icon_off = off

        def setValueAndAvailability(self, value, is_available):
            self.value = value
            self.is_available = is_available
 
        def toString(self):
            return self.name + " : " + str(self.value) + " - " + str(self.is_available)
   
        