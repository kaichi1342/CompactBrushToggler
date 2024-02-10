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

 

from PyQt5.QtCore import (  QLocale )


class CBT_Translation():
    translation = {
         "Size"          : { "en" : "Size",          "tr" : "",  "abr"  : ""},
         "Opacity"       : { "en" : "Opacity",       "tr" : "",  "abr"  : "" },
         "Flow"          : { "en" : "Flow",          "tr" : "",  "abr"  : "" },
         "Softness"      : { "en" : "Softness",      "tr" : "",  "abr"  : "" },
         "Rotation"      : { "en" : "Rotation",      "tr" : "",  "abr"  : "" },
         "Scatter"       : { "en" : "Scatter",       "tr" : "",  "abr"  : "" },
         "Color Rate"    : { "en" : "Color Rate",    "tr" : "",  "abr"  : "" },
         "Overlay Mode"  : { "en" : "Overlay Mode",  "tr" : "",  "abr"  : "" },
         "Ink depletion" : { "en" : "Soak Ink",      "tr" : "",  "abr"  : "" },
         "Painting Mode" : { "en" : "Painting Mode", "tr" : "",  "abr"  : "" },
         "Brush Tip"     : { "en" : "Brush Tip",     "tr" : "",  "abr"  : "" },
         "Smudge Length" : { "en" : "Smudge Length", "tr" : "",  "abr"  : "" },
         "Smudge Mode"   : { "en" : "Smudge Mode",   "tr" : "",  "abr"  : "" },
         "Dulling"       : { "en" : "Painting Mode", "tr" : "",  "abr"  : "" },
         "Smearing"      : { "en" : "Brush Tip",     "tr" : "",  "abr"  : "" },
 
    }
 
    def __init__(self, parent): 
        self.parent = parent 
        self.setLanguage()

    def getLanguage(self):
        lang    = QLocale().languageToString(QLocale().language())
        country = QLocale().countryToString(QLocale().country())
        return lang + " " + country

    def setLanguage(self):
        lang    = QLocale().languageToString(QLocale().language())
        country = QLocale().countryToString(QLocale().country())
       
        if lang == "French" and country == "France": 
            self.setFR_fr()
        elif lang == "Spanish"  and country == "Mexico": 
            self.setSP_sp()
        elif lang == "Spanish"  and country == "Spain": 
            self.setSP_sp()
        elif lang == "Korean"   and country == "South Korea": 
            self.setKr_sk()
        else:
            self.setEN_us()

    def getTranslationTable(self):
        return self.translation

    def setEN_us(self):
        self.translation["Size"]["tr"]          = "Size"
        self.translation["Opacity"]["tr"]       = "Opacity"
        self.translation["Flow"]["tr"]          = "Flow"
        self.translation["Softness"]["tr"]      = "Softness"
        self.translation["Rotation"]["tr"]      = "Rotation"
        self.translation["Scatter"]["tr"]       = "Scatter"
        self.translation["Color Rate"]["tr"]    = "Color Rate"
        self.translation["Overlay Mode"]["tr"]  = "Overlay Mode"
        self.translation["Ink depletion"]["tr"] = "Soak Ink"
        self.translation["Painting Mode"]["tr"] = "Painting Mode"
        self.translation["Brush Tip"]["tr"]     = "Brush Tip"
        self.translation["Dulling"]["tr"]       = "Dulling"
        self.translation["Smearing"]["tr"]      = "Smearing"
        self.translation["Smudge Length"]["tr"] = "Smudge Length"
        self.translation["Smudge Mode"]["tr"]   = "Smudge Mode"
        
        self.translation["Size"]["abr"]          = "Sze"
        self.translation["Opacity"]["abr"]       = "Opc"
        self.translation["Flow"]["abr"]          = "Flw"
        self.translation["Softness"]["abr"]      = "Sft"
        self.translation["Rotation"]["abr"]      = "Rot"
        self.translation["Scatter"]["abr"]       = "Sct"
        self.translation["Color Rate"]["abr"]    = "Col"
        self.translation["Overlay Mode"]["abr"]  = "Ovl"
        self.translation["Ink depletion"]["abr"] = "Sok"
        self.translation["Painting Mode"]["abr"] = "Ptm" 
        self.translation["Smudge Length"]["abr"] = "SmL"
        self.translation["Smudge Mode"]["abr"]   = "SmM" 

    def setFR_fr(self):
        self.translation["Size"]["tr"]          = "Taille"
        self.translation["Opacity"]["tr"]       = "Opacité"
        self.translation["Flow"]["tr"]          = "Débit"
        self.translation["Softness"]["tr"]      = "Douceur"
        self.translation["Rotation"]["tr"]      = "Rotation"
        self.translation["Scatter"]["tr"]       = "Dispersion"
        self.translation["Color Rate"]["tr"]    = "Taux de couleur"
        self.translation["Overlay Mode"]["tr"]  = "Mode Incrustation"
        self.translation["Ink depletion"]["tr"] = "Épuisement de l'encre"
        self.translation["Painting Mode"]["tr"] = "Mode de dessin"
        self.translation["Brush Tip"]["tr"]     = "Pointe de brosse"
        self.translation["Smudge Length"]["tr"] = "Longueur d'étalement"
        self.translation["Smudge Mode"]["tr"]   = "Mode d'étalement"
        
        self.translation["Size"]["abr"]          = "Tle"
        self.translation["Opacity"]["abr"]       = "Opc"
        self.translation["Flow"]["abr"]          = "Dbt"
        self.translation["Softness"]["abr"]      = "Dcr"
        self.translation["Rotation"]["abr"]      = "Rot"
        self.translation["Scatter"]["abr"]       = "Dis"
        self.translation["Color Rate"]["abr"]    = "Col"
        self.translation["Overlay Mode"]["abr"]  = "Inc"
        self.translation["Ink depletion"]["abr"] = "Épu"
        self.translation["Painting Mode"]["abr"] = "Des" 
        self.translation["Smudge Length"]["abr"] = "Ldé"
        self.translation["Smudge Mode"]["abr"]   = "Mdé" 

    def setSP_sp(self):
        self.translation["Size"]["tr"]          = "Tamaño"
        self.translation["Opacity"]["tr"]       = "Opacidad"
        self.translation["Flow"]["tr"]          = "Flujo"
        self.translation["Softness"]["tr"]      = "Suavidad"
        self.translation["Rotation"]["tr"]      = "Rotación"
        self.translation["Scatter"]["tr"]       = "Dispersar"
        self.translation["Color Rate"]["tr"]    = "Proporción de color"
        self.translation["Overlay Mode"]["tr"]  = "Modo de superposición"
        self.translation["Ink depletion"]["tr"] = "Agotamiento de la tinta"
        self.translation["Painting Mode"]["tr"] = "Modo de pintura"
        self.translation["Brush Tip"]["tr"]     = "Punta del pincel"
        self.translation["Smudge Length"]["tr"] = "Longitud de la mancha"
        self.translation["Smudge Mode"]["tr"]   = "Modo de manchado"

        self.translation["Size"]["abr"]          = "Tmñ"
        self.translation["Opacity"]["abr"]       = "Opc"
        self.translation["Flow"]["abr"]          = "Flj"
        self.translation["Softness"]["abr"]      = "Svd"
        self.translation["Rotation"]["abr"]      = "Rot"
        self.translation["Scatter"]["abr"]       = "Dis"
        self.translation["Color Rate"]["abr"]    = "Col"
        self.translation["Overlay Mode"]["abr"]  = "Sup"
        self.translation["Ink depletion"]["abr"] = "Ago"
        self.translation["Painting Mode"]["abr"] = "Pin" 
        self.translation["Smudge Length"]["abr"] = "Ldé"
        self.translation["Smudge Mode"]["abr"]   = "Mdm" 

    def setKr_sk(self):
        self.translation["Size"]["tr"]          = "크기"
        self.translation["Opacity"]["tr"]       = "불투명도"
        self.translation["Flow"]["tr"]          = "흐름"
        self.translation["Softness"]["tr"]      = "부드러움"
        self.translation["Rotation"]["tr"]      = "회전"
        self.translation["Scatter"]["tr"]       = "분산"
        self.translation["Color Rate"]["tr"]    = "색상 비율"
        self.translation["Overlay Mode"]["tr"]  = "오버레이 모드"
        self.translation["Ink depletion"]["tr"] = "잉크 소모"
        self.translation["Painting Mode"]["tr"] = "그리기 모드"
        self.translation["Brush Tip"]["tr"]     = "브고시 끌"
        self.translation["Smudge Length"]["tr"] = "번짐 길이"
        self.translation["Smudge Mode"]["tr"]   = "색상 번짐 모드"

        self.translation["Size"]["abr"]          = "크기"
        self.translation["Opacity"]["abr"]       = "불투명"
        self.translation["Flow"]["abr"]          = "흐름"
        self.translation["Softness"]["abr"]      = "부드러"
        self.translation["Rotation"]["abr"]      = "회전"
        self.translation["Scatter"]["abr"]       = "분산"
        self.translation["Color Rate"]["abr"]    = "색상"
        self.translation["Overlay Mode"]["abr"]  = "오버레"
        self.translation["Ink depletion"]["abr"] = "잉크"
        self.translation["Painting Mode"]["abr"] = "그리기" 
        self.translation["Smudge Length"]["tr"]  = "번짐길"
        self.translation["Smudge Mode"]["tr"]    = "번짐모" 