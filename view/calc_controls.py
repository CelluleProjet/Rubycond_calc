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


import numpy as np
import sys 

from lmfit import Parameters, minimize

from PyQt5 import QtWidgets, QtCore
try:
    import Equations_RubySam_Scale as RS
except:
    from . import Equations_RubySam_Scale as RS


class controls(QtWidgets.QScrollArea):
    
    signal_plot_data = QtCore.pyqtSignal(np.ndarray)
    signal_quit = QtCore.pyqtSignal()
    
    def __init__(self, model = None, debug = False):
        super().__init__()
        self.model = model
        self.debug = debug
        self.ruby_pressure_gauge = ['Shen 2020', 'Mao hydro 1986', 'Mao non hydro 1986', 'Dewaele 2008', 'Dorogokupets and Oganov 2007']
        self.temperature_gauge = ['Not Used', 'Datchi 2004']
        self.sam_pressure_gauge = ['Rashchenko 2015', 'Datchi 1997']
        
        self.last_ruby_selected = 'Ruby L selected'
        self.last_sam_selected = 'Samarium L selected'
        
        self.Ruby_calc_all_P_gauges = (RS.Ruby_Shen, RS.Ruby_hydro, RS.Ruby_non_hydro, RS.Ruby_Dewaele, RS.Ruby_Dorogokupets_forDatchiT)
        self.Sam_calc_all_P_gauges = (RS.Sam_Rashchenko, RS.Sam_Datchi)
        
        if self.debug : print('\nopen_file_commands\n')
        
        self.max_width = 400
        
        self.ruby_lambda = None
        self.ruby_lambda_zero = None
        self.ruby_T_lambda_zero = None
        self.ruby_T_lambda = None
        
        
        
        self.sam_lambda_zero = None
        
        ### Tab Ruby
        
        #Group Initial Parameters: ruby_init_pars_
        
        self.ruby_init_pars_button_lambda_zero = QtWidgets.QPushButton()
        self.ruby_init_pars_button_T_lambda_zero = QtWidgets.QPushButton()
        
        self.group_ruby_init_pars_layout = QtWidgets.QGridLayout()
        
        self.group_ruby_init_pars_layout.addWidget(self.ruby_init_pars_button_lambda_zero, 0, 0)
        self.group_ruby_init_pars_layout.addWidget(self.ruby_init_pars_button_T_lambda_zero, 0, 1)
        
        self.group_ruby_init_pars = QtWidgets.QGroupBox("Initial Parameters")
        self.group_ruby_init_pars.setLayout(self.group_ruby_init_pars_layout)
        
        #Group Parameters: ruby_pars_
        
        
        self.ruby_pars_button_lambda = QtWidgets.QPushButton()
        self.ruby_pars_button_pressure = QtWidgets.QPushButton("P = 0 GPa")
        self.ruby_pars_button_temperature = QtWidgets.QPushButton()
        
        self.ruby_pars_combobox_pressure_gauge = QtWidgets.QComboBox()
        self.ruby_pars_combobox_pressure_gauge.addItems(self.ruby_pressure_gauge)
        
        self.ruby_pars_combobox_temperature_gauge = QtWidgets.QComboBox()
        self.ruby_pars_combobox_temperature_gauge.addItems(self.temperature_gauge)
        
        self.group_ruby_pars_layout = QtWidgets.QGridLayout()
        

        self.group_ruby_pars_layout.addWidget(self.ruby_pars_button_lambda, 1, 0)
        self.group_ruby_pars_layout.addWidget(self.ruby_pars_button_pressure, 2, 0)
        self.group_ruby_pars_layout.addWidget(self.ruby_pars_combobox_pressure_gauge, 2, 1)
        self.group_ruby_pars_layout.addWidget(self.ruby_pars_button_temperature, 3, 0)
        self.group_ruby_pars_layout.addWidget(self.ruby_pars_combobox_temperature_gauge, 3, 1)
        
        
        
        self.group_ruby_pars = QtWidgets.QGroupBox("Parameters")
        self.group_ruby_pars.setLayout(self.group_ruby_pars_layout)
        
        #Group File: r_out_
        
        #Opzione griglia
        
        # self.r_out_0 = QtWidgets.QLabel(self.ruby_pressure_gauge[0])
        # self.r_out_1 = QtWidgets.QLabel(self.ruby_pressure_gauge[1])
        # self.r_out_2 = QtWidgets.QLabel(self.ruby_pressure_gauge[2])
        # self.r_out_3 = QtWidgets.QLabel(self.ruby_pressure_gauge[3])
        # self.r_out_4 = QtWidgets.QLabel(self.ruby_pressure_gauge[4])
        
        # self.r_out_0_val = QtWidgets.QLabel("--- GPa")
        # self.r_out_1_val = QtWidgets.QLabel("--- GPa")
        # self.r_out_2_val = QtWidgets.QLabel("--- GPa")
        # self.r_out_3_val = QtWidgets.QLabel("--- GPa")
        # self.r_out_4_val = QtWidgets.QLabel("--- GPa")
        
        # self.group_r_out_layout = QtWidgets.QGridLayout()
        
        # self.group_r_out_layout.addWidget(self.r_out_0, 0, 0)
        # self.group_r_out_layout.addWidget(self.r_out_1, 1, 0)
        # self.group_r_out_layout.addWidget(self.r_out_2, 2, 0)
        # self.group_r_out_layout.addWidget(self.r_out_3, 3, 0)
        # self.group_r_out_layout.addWidget(self.r_out_4, 4, 0)
        
        # self.group_r_out_layout.addWidget(self.r_out_0_val, 0, 1)
        # self.group_r_out_layout.addWidget(self.r_out_1_val, 1, 1)
        # self.group_r_out_layout.addWidget(self.r_out_2_val, 2, 1)
        # self.group_r_out_layout.addWidget(self.r_out_3_val, 3, 1)
        # self.group_r_out_layout.addWidget(self.r_out_4_val, 4, 1)
        
        #Opzione Ruby singola cella
        self.ruby_output = QtWidgets.QLabel()
        self.ruby_output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
    
        
        self.group_r_out_layout = QtWidgets.QGridLayout()
        self.group_r_out_layout.addWidget(self.ruby_output)
        
        
        #Fine opzione
        
        self.group_r_out = QtWidgets.QGroupBox("Gauges")
        self.group_r_out.setLayout(self.group_r_out_layout)
        
        
        
        #Final ruby layout
        
    
        layout_controlsH = QtWidgets.QHBoxLayout()
        layout_controlsV = QtWidgets.QVBoxLayout()

        layout_controlsV.addWidget(self.group_ruby_init_pars)
        layout_controlsV.addWidget(self.group_ruby_pars)
        layout_controlsV.addWidget(self.group_r_out)

        
        layout_controlsV.addStretch(1) #No vertical Stretch
        layout_controlsV.setAlignment(QtCore.Qt.AlignTop)

        # layout_controls.setAlignment(QtCore.Qt.AlignTop)
        layout_controlsH.addLayout(layout_controlsV)
        layout_controlsH.addStretch(1) #No horizontal Stretch
        
        self.frame_ruby = QtWidgets.QFrame()
        self.frame_ruby.setLayout(layout_controlsH)
        
        self.frame_sam = QtWidgets.QFrame()
        
        ### Tab Samarium
        
        #Group Initial Parameters: sam_init_pars_
        
        self.sam_init_pars_button_lambda_zero = QtWidgets.QPushButton()
        
        
        self.group_sam_init_pars_layout = QtWidgets.QGridLayout()
        
        self.group_sam_init_pars_layout.addWidget(self.sam_init_pars_button_lambda_zero, 0, 0)

        
        self.group_sam_init_pars = QtWidgets.QGroupBox("Initial Parameters")
        self.group_sam_init_pars.setLayout(self.group_sam_init_pars_layout)
        
        #Group Parameters: sam_pars_
        
        
        self.sam_pars_button_lambda = QtWidgets.QPushButton()
        self.sam_pars_button_pressure = QtWidgets.QPushButton()

        
        self.sam_pars_combobox_pressure_gauge = QtWidgets.QComboBox()
        self.sam_pars_combobox_pressure_gauge.addItems(self.sam_pressure_gauge)
        

        
        self.group_sam_pars_layout = QtWidgets.QGridLayout()
        

        self.group_sam_pars_layout.addWidget(self.sam_pars_button_lambda, 1, 0)
        self.group_sam_pars_layout.addWidget(self.sam_pars_button_pressure, 2, 0)
        self.group_sam_pars_layout.addWidget(self.sam_pars_combobox_pressure_gauge, 2, 1)

        
        
        
        self.group_sam_pars = QtWidgets.QGroupBox("Parameters")
        self.group_sam_pars.setLayout(self.group_sam_pars_layout)
        
        #Opzione Sam singola cella
        self.sam_output = QtWidgets.QLabel()
        self.sam_output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
    
        
        self.group_s_out_layout = QtWidgets.QGridLayout()
        self.group_s_out_layout.addWidget(self.sam_output)
        
        
        #Fine opzione
        
        self.group_s_out = QtWidgets.QGroupBox("Gauges")
        self.group_s_out.setLayout(self.group_s_out_layout)
        
        #Final sam layout
        
    
        layout_controlsH = QtWidgets.QHBoxLayout()
        layout_controlsV = QtWidgets.QVBoxLayout()

        layout_controlsV.addWidget(self.group_sam_init_pars)
        layout_controlsV.addWidget(self.group_sam_pars)
        layout_controlsV.addWidget(self.group_s_out)

        
        layout_controlsV.addStretch(1) #No vertical Stretch
        layout_controlsV.setAlignment(QtCore.Qt.AlignTop)

        # layout_controls.setAlignment(QtCore.Qt.AlignTop)
        layout_controlsH.addLayout(layout_controlsV)
        layout_controlsH.addStretch(1) #No horizontal Stretch
        
        self.frame_sam = QtWidgets.QFrame()
        self.frame_sam.setLayout(layout_controlsH)
        
        #Fial Tab
        
        tabs = QtWidgets.QTabWidget()
        
        self.tab_1 = tabs.addTab(self.frame_ruby, "Ruby Cr³⁺:Al₂O₃")
        self.tab_2 = tabs.addTab(self.frame_sam, "Samarium Sm²⁺:SrB₄O₇")

        self.setWidgetResizable(True)
        self.setWidget(tabs)
        
        self.update_ruby_lambda(694.25)
        self.update_ruby_lambda_zero(694.25)
        self.update_ruby_T_lambda(273.15+20)
        self.update_ruby_T_lambda_zero(273.15+20)
        self.update_ruby_pressure(0)
        self.update_sam_lambda_zero(685.51)
        self.update_sam_lambda(685.51)
        self.update_sam_pressure(0)
        
        self.calc_ruby_pressures()
        self.calc_sam_pressures()
        
        #actions
        self.sam_init_pars_button_lambda_zero.clicked.connect(self.change_sam_lambda_zero)
        self.sam_pars_button_lambda.clicked.connect(self.change_sam_lambda)
        self.sam_pars_button_pressure.clicked.connect(self.change_sam_pressure)
        
        self.ruby_init_pars_button_T_lambda_zero.clicked.connect(self.change_ruby_T_lambda_zero)
        self.ruby_init_pars_button_lambda_zero.clicked.connect(self.change_ruby_lambda_zero)
        
        self.ruby_pars_button_lambda.clicked.connect(self.change_ruby_lambda)
        self.ruby_pars_button_pressure.clicked.connect(self.change_ruby_pressure)
        self.ruby_pars_button_temperature.clicked.connect(self.change_ruby_T_lambda)
        
        self.ruby_pars_combobox_pressure_gauge.activated.connect(self.calc_ruby_lambda)
        self.ruby_pars_combobox_temperature_gauge.activated.connect(self.calc_ruby_pressures)
        
        self.sam_pars_combobox_pressure_gauge.activated.connect(self.calc_sam_lambda)
        
        
    def update_sam_lambda(self, value):
        self.sam_lambda = value
        self.sam_pars_button_lambda.setText(f"λ = {self.sam_lambda:.2f} nm")
    
    def change_sam_lambda(self):
        title = 'Change Value'
        label = 'Enter new λ value in nm'
        value = self.sam_lambda
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            self.update_sam_lambda(new_value)
            self.calc_sam_pressures()
            
    def update_sam_pressure(self, value):
        self.sam_pressure = value
        self.sam_pars_button_pressure.setText(f"P = {value:.2f} GPa")
    
    def change_sam_pressure(self):
        title = 'Change Value'
        label = 'Enter new pressure value in GPa'
        value = self.sam_pressure
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            self.update_sam_pressure(new_value)
            self.calc_sam_lambda()
        
    def update_sam_lambda_zero(self, value) :
        self.sam_lambda_zero = value
        self.sam_init_pars_button_lambda_zero.setText(f"λ₀ = {self.sam_lambda_zero:.2f} nm")
    
    def change_sam_lambda_zero(self):
        title = 'Change Value'
        label = 'Enter new λ₀ value in nm'
        value = self.sam_lambda_zero
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            self.update_sam_lambda_zero(new_value)
            self.calc_sam_last_selected()
    
    def update_ruby_lambda(self, value):
        self.ruby_lambda = value
        self.ruby_pars_button_lambda.setText(f"λ = {self.ruby_lambda:.2f} nm")
    
    def change_ruby_lambda(self):
        title = 'Change Value'
        label = 'Enter new λ value in nm'
        value = self.ruby_lambda
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            self.update_ruby_lambda(new_value)
            self.calc_ruby_pressures()
        
    def update_ruby_lambda_zero(self, value):
        self.ruby_lambda_zero = value
        self.ruby_init_pars_button_lambda_zero.setText(f"λ₀ = {self.ruby_lambda_zero:.2f} nm") 
    
    def change_ruby_lambda_zero(self):
        title = 'Change Value'
        label = 'Enter new λ₀ value in nm'
        value = self.ruby_lambda_zero
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            self.update_ruby_lambda_zero(new_value)
            self.calc_ruby_last_selected()
    
    def update_ruby_T_lambda(self, value):
        self.ruby_T_lambda = value
        self.ruby_pars_button_temperature.setText(f"T(λ) = {self.ruby_T_lambda:.2f} K / {self.ruby_T_lambda - 273.15:.2f} °C ")
    
    def change_ruby_T_lambda(self):
        title = 'Change Value'
        label = 'Enter new T(λ) value in K'
        value = self.ruby_T_lambda
        minvalue = -1
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            if new_value <=0:
                self.update_ruby_T_lambda(273.15+20)
            else:
                self.update_ruby_T_lambda(new_value)
            self.calc_ruby_last_selected()
        
    def update_ruby_T_lambda_zero(self, value):
        self.ruby_T_lambda_zero = value
        self.ruby_init_pars_button_T_lambda_zero.setText(f"T(λ₀) = {self.ruby_T_lambda_zero:.2f} K / {self.ruby_T_lambda_zero - 273.15:.2f} °C ")
        
    def change_ruby_T_lambda_zero(self):
        title = 'Change Value'
        label = 'Enter new T(λ₀) value in K'
        value = self.ruby_T_lambda_zero
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            if new_value <=0:
                self.update_ruby_T_lambda_zero(273.15+20)
            else:
                self.update_ruby_T_lambda_zero(new_value)
            self.calc_ruby_last_selected()
    
    def update_ruby_pressure(self, value):
        self.ruby_pressure = value
        self.ruby_pars_button_pressure.setText(f"P = {value:.2f} GPa")
    
    def change_ruby_pressure(self):
        title = 'Change Value'
        label = 'Enter new pressure value in GPa'
        value = self.ruby_pressure
        minvalue = 0
        maxvalue = 10000
        new_value, ok = QtWidgets.QInputDialog.getDouble(self, title, label , value, minvalue, maxvalue, decimals=2)
        if ok:
            self.update_ruby_pressure(new_value)
            self.calc_ruby_lambda()
            
    def ruby_format_output(self):
        ruby_output = ''
        test = [11.12, 13.34, 15.56, 17.78, 19.90]
        for val, i in enumerate(self.ruby_pressure_gauge):
            #ruby_output+= f'{val:.2f} Gpa {i:<30} \n'
            ruby_output+= f'{test[val]:.2f} GPa {i} \n'
        return ruby_output
    
    def ruby_format_output_str(self, pres):
        ruby_output = ''
        
        for val, i in enumerate(self.ruby_pressure_gauge):
            #ruby_output+= f'{val:.2f} Gpa {i:<30} \n'
            ruby_output+= f'{pres[val]:.2f} GPa {i} \n'
        return ruby_output
    
    def calc_ruby_pressures(self):
        # See Gauge_eq_Ruby
        # print('Ruby L selected')
        self.last_ruby_selected = 'Ruby L selected'
        L0 = self.ruby_lambda_zero
        T0 = self.ruby_T_lambda_zero

        lambda_value = self.ruby_lambda 
        
        T_value = self.ruby_T_lambda 

            #self.Ruby_calc_T_value.set('298')
            #T_value = 298

        temperature_gauge = str(self.ruby_pars_combobox_temperature_gauge.currentText())
        
        header = 'Ruby λ selected\n'
        header+= f'λ = {lambda_value} nm, '
        
        if temperature_gauge == "Datchi 2004":
            f = RS.Ruby_Datchi_T
            P = [g(f(T_value,lambda_value),f(T0,L0)) for g in self.Ruby_calc_all_P_gauges]
            header+= f'T(λ) = {T_value}, Datchi 2004 \n'
            header+= f'λ₀ = {L0} nm, T(λ₀) = {T0} \n\n'
        else:
            P = [g(lambda_value,L0) for g in self.Ruby_calc_all_P_gauges]
            header+= 'T(λ) Not Used \n'
            header+= f'λ₀ = {L0} nm, T(λ₀) Not Used \n\n'
        nice_output = self.ruby_format_output_str(P)
        self.ruby_output.setText(header + nice_output)
        P= [lambda_value, L0, T_value, T_value - 273.15] + P

        #print(P)
    
    def calc_ruby_lambda(self):
        #print('Ruby P selected')
        self.last_ruby_selected = 'Ruby P selected'
        L0 = self.ruby_lambda_zero
        P_value = self.ruby_pressure 
        
        pressure_gauge = str(self.ruby_pars_combobox_pressure_gauge.currentText())
        #print(pressure_gauge)
        if pressure_gauge == "Shen 2020":
            g = RS.Ruby_Shen
        elif pressure_gauge == "Mao hydro 1986":
            g = RS.Ruby_hydro
        elif pressure_gauge == "Mao non hydro 1986":
            g = RS.Ruby_non_hydro
        elif pressure_gauge == "Dewaele 2008":
            g = RS.Ruby_Dewaele
        elif pressure_gauge == "Dorogokupets and Oganov 2007":
            g = RS.Ruby_Dorogokupets_forDatchiT
        
        def residual(p):
            v = p.valuesdict()
            return abs(g(v['L'], v['L0']) - v['P'])


        params = Parameters()
        params.add('L', value = L0+10, min = L0)
        params.add('L0', value = L0, vary = False)
        params.add('P', value = P_value, vary = False)

        mi = minimize(residual, params, method='nelder', nan_policy='omit')

        # print()
        # print(mi.params.pretty_print())
        # print()

        res_L = mi.params['L'].value
        P = [g(res_L,L0) for g in self.Ruby_calc_all_P_gauges]
        header = 'Ruby P selected\n'
        header+= pressure_gauge + '\n'
        header+= f'P = {P_value} GPa, λ(P) = {res_L:.3f} nm\n'
        header+= f'λ₀ = {L0} nm, T Not Implemented \n\n'
        nice_output = self.ruby_format_output_str(P)
        self.ruby_output.setText(header + nice_output)
        #print(P)
    
    def calc_ruby_last_selected(self):
        if self.last_ruby_selected == 'Ruby L selected':
            self.calc_ruby_pressures()
        else:
            self.calc_ruby_lambda()
    
    def calc_sam_last_selected(self):
        if self.last_sam_selected == 'Samarium L selected':
            self.calc_sam_pressures()
        else:
            self.calc_sam_lambda()
    
    def calc_sam_lambda(self):
        #print('Samarium P selected')
        self.last_sam_selected = 'Samarium P selected'
        P_value = self.sam_pressure

        pressure_gauge = str(self.sam_pars_combobox_pressure_gauge.currentText())
        L0 = self.sam_lambda_zero
            
        if pressure_gauge == 'Rashchenko 2015':
            g = RS.Sam_Rashchenko
        elif pressure_gauge == 'Datchi 1997':
            g = RS.Sam_Datchi
        
        def residual(p):
            v = p.valuesdict()
            return abs(g(v['L'], v['L0']) - v['P'])


        params = Parameters()
        params.add('L', value = L0+10, min = L0)
        params.add('L0', value = L0, vary = False)
        params.add('P', value = P_value, vary = False)

        mi = minimize(residual, params, method='nelder', nan_policy='omit')

        # print()
        # print(mi.params.pretty_print())
        # print()

        res_L = mi.params['L'].value
        P = [g(res_L,L0) for g in self.Sam_calc_all_P_gauges]
        #P= [lambda_value, 1e7/lambda_value, L0, 1e7/L0, T_value, T_value - 273.15] + P
        header = 'Samarium P selected\n'
        header+= pressure_gauge + '\n'
        header+= f'P = {P_value} GPa, λ(P) = {res_L:.3f} nm\n'
        header+= f'λ₀ = {L0} nm\n\n'
        nice_output = self.sam_format_output_str(P)
        self.sam_output.setText(header + nice_output)
        #print(P)
 
    
    def calc_sam_pressures(self):
        #print('Samarium L selected')
        self.last_sam_selected = 'Samarium L selected'
        L_value = self.sam_lambda
        L0 = self.sam_lambda_zero
        P = [g(L_value,L0) for g in self.Sam_calc_all_P_gauges]
        
        header = 'Samarium λ selected\n'
        header+= f'λ = {L_value} nm, '
        header+= f'λ₀ = {L0} nm\n\n'
        
        nice_output = self.sam_format_output_str(P)
        self.sam_output.setText(header + nice_output)
        
        P= [L_value, L0] + P
        #print(P)
    
    def sam_format_output_str(self, pres):
        sam_output = ''
        
        for val, i in enumerate(self.sam_pressure_gauge):
            #ruby_output+= f'{val:.2f} Gpa {i:<30} \n'
            sam_output+= f'{pres[val]:.2f} GPa {i} \n'
        return sam_output
                    
    #change_ruby_lambda => call calc_ruby_pressures
    #change_ruby_pressure => call calc_ruby_lambdas
    
if __name__ == "__main__":
    
    #https://www.w3schools.com/cssref/css_colors.php
    
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 20px;
                    }
QGroupBox { font-weight: bold;  color : blueviolet; } 
QPushButton { text-align:left;}
""")

    window = controls()

    window.show()
    sys.exit(app.exec())