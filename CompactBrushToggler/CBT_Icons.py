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

import os

from PyQt5.QtCore import (
    QSize
)
from PyQt5.QtGui import (
    QIcon 
) 

class CBT_Icons():
    icon_names = [
        "pressure_off",
        "pressure_size",
        "pressure_size_off",
        "pressure_opacity",
        "pressure_opacity_off",
        "pressure_flow",
        "pressure_softness",
        "pressure_softness_off",
        "pressure_rotation",
        "pressure_rotation_off",
        "pressure_scatter",
        "pressure_scatter_off",
        "pressure_smudlen",
        "pressure_smudlen_off",
        "smudge_dulling",
        "smudge_smearing",
        "pressure_colrate",
        "pressure_colrate_off",
        "paint_buildup",
        "paint_wash",
        "overlay_off",
        "overlay_on",
        "soak_ink_off",
        "soak_ink", 
    ]
    icon_list = {
        "light" : {},
        "dark"  : {}
    }

    def __init__(self, parent, size = 22, theme = "light"):
        self.icon_theme = theme
        self.parent = parent
        self.size  = QSize(size, size) 
        for name in self.icon_names:
            self.addIconFromFile("light",name)
            self.addIconFromFile("dark",name)
        
        
    def setTheme(self, theme):
        self.icon_theme = theme

    def icon(self, icon_name):
        if icon_name in self.icon_list[self.icon_theme]:
            return self.icon_list[self.icon_theme][icon_name] 
        else:
            return self.icon_list[self.icon_theme]["pressure_off"]  
        
    def addIconFromFile(self, theme, icon_name):
        icon_file =  os.path.dirname(os.path.realpath(__file__)) + '/pics/' + theme + "_" + icon_name + '.svg'
        
        isExist = os.path.exists(icon_file)
        if isExist :  
            self.icon_list[theme][icon_name] = QIcon()
            self.icon_list[theme][icon_name].addFile(icon_file,self.size)
        else: 
            return False 