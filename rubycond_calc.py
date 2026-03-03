# -*- coding: utf-8 -*-
"""

Title: Rubycond_calc: Ruby and Samarium fluorescence pressure / wavelength calculators for Rubycond

Rubycond: Python software to determine pressure in diamond anvil cell experiments by Ruby and Samarium luminescence.

Version 0.2.0
Release 260301

Author:

Yiuri Garino:

Copyright (c) 2023-2026 Yiuri Garino

Download: 
    https://github.com/CelluleProjet/Rubycond_calc

Contacts:

Yiuri Garino
    yiuri.garino@cnrs.fr

Silvia Boccato
    silvia.boccato@cnrs.fr

License: GPLv3

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

def reset():
    import sys
    
    if hasattr(sys, 'ps1'):
        
        #clean Console and Memory
        from IPython import get_ipython
        get_ipython().run_line_magic('clear','/')
        get_ipython().run_line_magic('reset','-sf')
        print("Running interactively")
        print()
    else:
        print("Running in terminal")
        print()


if __name__ == '__main__':
    reset()


import os, sys
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

debug = True

if debug:
    script = os.path.abspath(__file__)
    script_dir = os.path.dirname(script)
    script_name = os.path.basename(script)
    now = datetime.now()
    date = now.isoformat(sep = ' ', timespec = 'seconds') #example = '2024-03-27 18:04:46'
    date_short = date[2:].replace('-','').replace(' ','_').replace(':','') #example = '240327_180446'
    print("File folder = " + script_dir)
    print("File name = " + script_name)
    print("Current working directory (AKA Called from ...) = " + os.getcwd())
    print("Python version = " + sys.version)
    print("Python folder = " + sys.executable)
    print()
    print("Started @ " + date +' AKA ' + date_short) #example = 'Started @ 2024-03-27 18:04:46 AKA 240327_180446'
    print()
    print('_/‾\\'*20)
    print()

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
import os, sys, platform
script = os.path.abspath(__file__)
script_dir = os.path.dirname(script)
sys.path.append(script_dir)

from view.calc_controls import controls
from view.calc_about import about

class pop_up_simple(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        layout.addWidget(self.label)
        self.setLayout(layout)

class rubycond_calc(QtWidgets.QMainWindow):
    
    my_Serial_Thread_Open_start = QtCore.pyqtSignal()
    my_Serial_Thread_Read_start = QtCore.pyqtSignal()
    my_Serial_Thread_Reset_start = QtCore.pyqtSignal()
    
    def __init__(self, debug = False):
        super().__init__()
        self.controls = controls()
        
        self.__name__ = 'Rubycond Pressure Calculator'
        self.__version__ = '0.2.0' 
        self.__release__ = '260301'

        self.about = about(self.__name__, self.__version__, self.__release__)
        self.setWindowTitle(self.__name__ + ' Version = ' + self.__version__ + ' Release = ' + self.__release__)
        
        tabs = QtWidgets.QTabWidget()
        #tabs.setTabPosition(QtWidgets.QTabWidget.West) ToDo Orientation
        
        self.tab_1 = tabs.addTab(self.controls, "Calculator")
        self.tab_2 = tabs.addTab(self.about, "About Calculator")
        
        #self.setCentralWidget(self.controls)
        self.setCentralWidget(tabs)

        self.pop_up_info = pop_up_simple()
        
        #Shortcuts
        
        shortcut = QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        shortcut = QtWidgets.QShortcut(shortcut, self)
        shortcut.activated.connect(self.script_info) 

    
    def script_info(self):
        script = os.path.abspath(__file__)
        script_dir = os.path.dirname(script)
        script_name = os.path.basename(script)
        now = datetime.now()
        date = now.isoformat(sep = ' ', timespec = 'seconds') #example = '2024-03-27 18:04:46'
        
        print()
        print('_/‾\\'*20)
        print()
        print(date)
        print()
        print("File folder = " + script_dir)
        print("File name = " + script_name)
        print("Current working directory (AKA Called from ...) = " + os.getcwd())
        print("Python version = " + sys.version)
        print("Python folder = " + sys.executable)
        print()
        print('_/‾\\'*20)
        print()
        
        time = datetime.now().strftime("%d %B %Y %H:%M:%S")
        message = '\n'
        message+= f'Program name = {self.__name__}\n'
        message+= f'Version {self.__version__} | Release {self.__release__}\n'
        message+= '\n'
        message+= "Sys Info:\n"
        message+= '\n'
        message+= f"OS: {platform.system()} {platform.release()}\n"
        message+= f"Architecture: {platform.machine()}\n"
        message+= '\n'
        message+= 'Script Info:\n'
        message+= '\n'
        message+= f"File folder = {script_dir}\n"
        message+= f"File name = {script_name}\n"
        message+= f"Current working directory = {os.getcwd()}\n"
        message+= f"Python version = {sys.version}\n"
        message+= f"Python folder = {sys.executable}\n"
        message+= '\n'
        self.pop_up_info.setWindowTitle('Info ' + time)
        self.pop_up_info.label.setText(message)
        self.pop_up_info.show()
    
        
    def closeEvent(self, event):
        choice = QtWidgets.QMessageBox.question(self, "Quit", f"Do you want to Quit {self.about.name} ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        QtWidgets.QMessageBox()
        if choice == QtWidgets.QMessageBox.Yes:            
            self.about.close()
            #self.main_thread.quit() #Thread_7) Close Main Thread at the end
            event.accept()
        else:
            event.ignore()
            
   
def main():
    #Entry point in poetry pyproject.toml
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 20px;
                    }
QGroupBox { font-weight: bold;  color : blueviolet; } 
QPushButton { text-align:left;}
""")
    window = rubycond_calc() 
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()











if debug:
    now_end = datetime.now()
    date_end = now_end.isoformat(sep = ' ', timespec = 'seconds') #example = '2024-03-27 18:04:46'
    date_short_end = date_end[2:].replace('-','').replace(' ','_').replace(':','') #example = '240327_180446'
    timedelta = (datetime.now() - now)
    print()
    print('_/‾\\'*20)
    print()
    print()
    print("Done @ " + date_end +' AKA ' + date_short_end) #example = 'Started @ 2024-03-27 18:04:46 AKA 240327_180446'
    print()
    print(f"Elapsed time {timedelta} ({timedelta.seconds + round(timedelta.microseconds/1000)/1000})" )