# Compact Brush Toggler

A plugin for [Krita](https://krita.org).


## What is Compact Brush Toggler? 

*Compact Brush Toggler* is a Python plugin made for [Krita](https://krita.org) (free professional and open-source painting program). 

This plugin allows one access to "Use Pressure Curve" checkboxes, that toggles pressure on/off specific brush property and "Horizontal Brush Fade" Slider , that controls the horizontal fade/blur of the brush, from a smaller docker without opening the Brush Editor. 

---

## ScreenShots 

*Interface* 
Interface Adjust Depending on the ratio of height and width of the button

| Icon Only | 3 Letter Abbr | Full Length Word |
| --------- | ------------- | ----------- |
![Interface](./screenshots/ui3.jpeg) |  ![Interface](./screenshots/ui.jpeg) | ![Interface](./screenshots/ui2.jpeg) |

 
| Icon On | Icon Off | Abbreviation | Description | 
| ------- | -------- | ------------ | ----------- |
|         |          | Fade         | Brush Fade Slider |
| ![Interface](./screenshots/icons/ico-size-on.png)    | ![Interface](./screenshots/icons/ico-size-off.png)  | Sze       | Size Pen Pressure Toggle |
| ![Interface](./screenshots/icons/ico-opc-on.png)     | ![Interface](./screenshots/icons/ico-opc-off.png)  | Opc       | Opacity Pen Pressure Toggle |
| ![Interface](./screenshots/icons/ico-flw-on.png)     | ![Interface](./screenshots/icons/ico-flw-off.png)  | Flw       | Flow Pen Pressure Toggle |
| ![Interface](./screenshots/icons/ico-sft-on.png)     | ![Interface](./screenshots/icons/ico-sft-off.png)  | Sft       | Softness Pen Pressure Toggle |
| ![Interface](./screenshots/icons/ico-rot-on.png)     | ![Interface](./screenshots/icons/ico-rot-off.png)  | Rot       | Rotation Pen Pressure Toggle|
| ![Interface](./screenshots/icons/ico-sct-on.png)     | ![Interface](./screenshots/icons/ico-sct-off.png)  | Sca       | Scatter Pen Pressure Toggle |
| ![Interface](./screenshots/icons/ico-smdl-on.png)     | ![Interface](./screenshots/icons/ico-smdl-off.png)  | Rot       | Smudge Length Pressure Toggle - Smudge Brush |
| ![Interface](./screenshots/icons/ico-smdm-on.png)    | ![Interface](./screenshots/icons/ico-smdm-off.png) | Sca       | Smudge Moed Toggle - Smudge Brush : On -> Smearing , Off -> Dulling  |
| ![Interface](./screenshots/icons/ico-col-on.png)     | ![Interface](./screenshots/icons/ico-col-off.png)   | SmdLn       | Color Rate Pressure Toggle |
| ![Interface](./screenshots/icons/ico-ovl-on.png)     | ![Interface](./screenshots/icons/ico-ovl-off.png)  | SmdMd       | Overlay Mode - Smudge Brush|
| ![Interface](./screenshots/icons/ico-sok-on.png)     | ![Interface](./screenshots/icons/ico-sok-off.png)  | Sok       | Soak Ink - Bristle Brush|
| ![Interface](./screenshots/icons/ico-ptm-wash.png)   | ![Interface](./screenshots/icons/ico-ptm-bld.png)  | PtM       | Painting Mode : On -> Wash , Off -> Build |
 
The plugin loads the state of the pressure settings once a brush is selected; 
-- if its highlighted blue then the pressure setting is active
-- if its not highlighted the pressure setting is inactive. 

*Control Toggles + Painting Mode*
![Use Pressure Curve Toggles](./screenshots/ui-brushtoggler1.jpeg)
 
*Smudge Brush Toggles*
![Smudge Brush Toggles](./screenshots/ui-brushtoggler3.jpeg)

*Soak Ink for Bristle Brush*
![Bristle Brush](./screenshots/ui-brushtoggler2.jpeg)

*Brush Fade Slider* 
![Brush Fade Slider](./screenshots/ui-brushfade.jpeg)


### Shortcuts
Assigning Shortcut are now available; 
There are no default shortcut.
![Shortcut](./screenshots/ui-brushtoggler4.jpeg)





### Functionalities

This plugin main function  are;

1. Toggle Pen Pressure setting of a particular brush property
> For now the pressure toggle are limited to 8 property namely,
- Size
- Opacity
- Flow
- Softness
- Rotation
- Scatter
- Smudge Length
- Color Rate
2. Adjust the Horizontal Brush Fade setting of brushes with horizontal brush fade. 
> This would allow adjustment to both fade property if the ratio link is connected. 
3. 4 option Toggle that are not Pen Pressure  
- Overlay
- Soak Ink
- Painting Mode
- Smudge Mode

If the global pressure setting is off, then this plugin pressure setting will also be off. 

[Video Compact Brush Toggler in Action](https://drive.google.com/file/d/1pQa8cNno-4sxo2xajcnBNjxIr7wJ17fM/view?usp=sharing)

### Notes

This plugin as of 5.2 uses Krita Preset class to set brush properties.
Prior to 5.2 it traverses the ui to find the properties to set. 


### Plans --
 
- Add / remove property to toggle
- A way to change to a skinnier interface or maybe vertical stack layout. 
  

### Bugs and Known Issues

1. Currently the pressure setting initial states loads only upon selection of a brush. 
If the pressure setting is editted by the Brush Editor this current state wont reflect on the docker. 
You would need to switch to a different brush and back for it to properly reflect. 

## Downloads - Install - Execute 

### Download
- **[ZIP](https://github.com/kaichi1342/CompactBrushToggler/archive/refs/heads/v.1.0.0.zip)**
- **[Source](https://github.com/kaichi1342/CompactBrushToggler)**

### Install

1. Open [Krita](https://krita.org)
2. Got to Tools -> Scripts -> **Import Python Plugins** and select 
**CompactBrushToggler.zip** archive. 
3. Restart [Krita](https://krita.org)
4. Make sure Compact Brush Toggler is enabled in Plugin Manager. 
if not enable it by going to Settings -> Configure Krita -> **Python Plugin Manager** and click to check **Compact Brush Toggler**.
5. Restart Krita.
6. View **Compact Brush Toggler** to your screen by going to Settings -> Dockers -> **Compact Brush Toggler**


### Tested Platforms
V. 1.0.0
- Krita 5.2 

V. 0.0.1 to V. 1.0.4 
- Krita 5.1
- Krita 5.1.0 Pre-alpha
- Krita 5 beta 5

### Release Log

2024-02-28 : Version 0.1.6   
- Added new icons 
- Added shortcuts

2024-02-10 : Version 1.0.0
- Rewritte to use Preset Class
- Added Smudge Length and Mode
- Added new icons 
- Added shortcuts

2024-01-13 : Version 0.1.5
- Fix Enabling/Disabling Bug
- Added Support for French, Spanish, Korean Languages
- Added French, Spanish, Korean Translation  

2023-01-05 : Version 0.1.4
- Added Icons and Icon Only Mode
- Remove Fade Label on Fade Slider
- Can now be used for Krita 5.2 and 5.1 

2022-01-04 : Version 0.1.3a
- Re added Color Rate
- Added Soak Ink and Painting Mode

2022-03-11  : Version 0.1.2
- Fix Opacity / Flow Load Status
- Added Overlay Mode for Smudge Brush
- Added disabling of none existing properties
- Re-organize UI 

2021-12-22  : Version 0.1.1b
- First Released Version 
- Added ability to toggle listview checkbox of the brush property
- Added rotation and scatter toggles
- Added a slider control for brush fade
- Re-organized UI 
- Removed brush name label

2021-12-16  : Version 0.1.0 
- First Implemented Version

### Thanks to:
This docker has been possible with the help of AkiR , Grum999, KnowZero 
who provided much of the base code that have helped me develop this.   
Also to Blender Layer for providing source on how to connect actions to a docker.        

## License

### *Compact Brush Toggler* is released under the GNU General Public License (version 3 or any later version).

*Compact Brush Toggler* is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.                               
    
*Compact Brush Toggler* is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/                                   



                            
 
