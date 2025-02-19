# This file is part of SSW-2D.
# SSW-2D is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# SSW-2D is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Foobar. If not, see
# <https://www.gnu.org/licenses/>.

##
# @package read_config
# @author Remi Douvenot
# @date 19/07/2021
# @brief Fill the config class with the input from input file
##

# where config class is defined
from src.classes_and_files.classes import *
import csv
import numpy as np


def read_config(file_configuration, file_source_config):
    # ----------------------------- #
    # --- Reading configuration --- #
    # ----------------------------- #
    f_config = open(file_configuration, newline='')
    file_tmp = csv.reader(f_config)
    for row in file_tmp:
        if row[0] == 'method':
            Config.method = row[1]
        elif row[0] == 'N_z':
            Config.N_z = np.int(row[1])
        elif row[0] == 'N_x':
            Config.N_x = np.int(row[1])
        elif row[0] == 'x_step':
            Config.x_step = np.float(row[1])
        elif row[0] == 'z_step':
            Config.z_step = np.float(row[1])
        elif row[0] == 'frequency':
            Config.freq = np.float(row[1]) * 1e6  # freq in MHz
        elif row[0] == 'polarisation':
            Config.polar = row[1]  # 'TE' or 'TM'
        elif row[0] == 'Max compression error':
            Config.max_compression_err = np.float(row[1])  # Max compression error
        elif row[0] == 'wavelet level':
            Config.wv_L = np.int(row[1])  # Max compression error
        elif row[0] == 'wavelet family':
            Config.wv_family = row[1]  # Max compression error
        elif row[0] == 'apodisation window':
            Config.apo_window = row[1]  # Type of the apodisation window
        elif row[0] == 'apodisation size':
            Config.apo_z = np.float(row[1])  # apodisation size along z
        elif row[0] == 'image size':
            Config.image_layer = np.float(row[1])  # image layer size (in ground) along z
        elif row[0] == 'ground':
            Config.ground = row[1]  # ground type
        elif row[0] == 'epsr':
            Config.epsr = np.float(row[1])  # ground relative permittivity
        elif row[0] == 'sigma':
            Config.sigma = np.float(row[1])  # ground conductivity
        elif row[0] == 'atmosphere':
            Config.atmosphere = row[1]  # atmospheric profile type
        elif row[0] == 'c0':
            Config.c0 = np.float(row[1])  # standard atm gradient
        elif row[0] == 'delta':
            Config.delta = np.float(row[1])  # evaporation duct height
        elif row[0] == 'zb':
            Config.zb = np.float(row[1])  # base height of a trilinear duct
        elif row[0] == 'c2':
            Config.c2 = np.float(row[1])  # gradient in a trilinear duct
        elif row[0] == 'zt':
            Config.zt = np.float(row[1])  # thickness of a trilinear duct
        elif row[0] == 'atm filename':
            Config.atm_filename = row[1]  # file for a hand-generated atmospheric profile
        elif row[0] == 'turbulence':
            Config.turbulence = row[1]
        elif row[0] == 'Cn2':
            Config.Cn2 = np.float(row[1])
        elif row[0] == 'L0':
            Config.L0 = np.float(row[1])
        elif row[0] == 'Property':
            pass  # first line
        elif row[0] == 'dynamic':  # only used for HMI plots
            pass  # first line
        elif row[0] == 'py_or_cy':  # only used for field calculation. Does not change the result
            pass  # first line
        else:
            raise ValueError(['Input file of the configuration is not valid. Input "' + row[0] + '" not valid'])
    # check for some values
    if Config.apo_z < 0 or Config.image_layer < 0 or Config.apo_z > 0.5 or Config.image_layer > 0.5:
        raise ValueError(['Apodisation and image layer must be in [0,0.5] (percentage of the total field size'])

    if (Config.ground != 'None') & (Config.ground != 'PEC') & (Config.ground != 'Dielectric'):
        raise ValueError(['Ground must be chosen among: None, PEC, or Dielectric'])
    # ------------ END ------------ #
    # --- Reading configuration --- #
    # ----------------------------- #

    # check apodisation window
    if Config.apo_window == 'Hanning':
        print('Hanning apodisation window')
    else:
        raise (ValueError([Config.apo_window, 'is not a valid apodisation type']))

    # --- Check the size of the vectors, multiple of 2^n --- #
    n_scaling_fct = 2 ** Config.wv_L
    modulo_nz = Config.N_z % n_scaling_fct
    if modulo_nz != 0:
        raise (ValueError(['N_z must be multiple of', n_scaling_fct, ' = 2^L']))

    # --- Configuration first --- #
    f_source_config = open(file_source_config, newline='')
    file_tmp = csv.reader(f_source_config)
    for row in file_tmp:
        # geometry must match with the source generation
        if row[0] == 'x_s':
            Config.x_s = np.float(row[1])  # distance in m
            if Config.x_s >= 0:
                raise ValueError(['Source position along x must be <0'])

        # --- The electric field itself --- #

    return Config


def read_source(config, file_source_config, file_e_init):
    # ------------------------------ #
    # --- Reading source E-field --- #
    # ------------------------------ #

    # --- Configuration first --- #
    f_source_config = open(file_source_config, newline='')
    file_tmp = csv.reader(f_source_config)
    for row in file_tmp:
        # geometry must match with the source generation
        if row[0] == 'N_z':
            n_z = np.int(row[1])
            if n_z != config.N_z:
                raise ValueError(['n_z value does not match with source generation'])
        elif row[0] == 'z_step':
            z_step = np.float(row[1])
            if z_step != config.z_step:
                raise ValueError(['z_step value does not match with source generation'])
        # geometry must match with the source generation
        elif row[0] == 'frequency':
            freq = np.float(row[1]) * 1e6  # freq in MHz
            if freq != config.freq:
                raise ValueError(['frequency ', freq, ' MHz value does not match with source generation',
                                  config.freq, ' MHz'])
        # x_s is the source position in the x direction (must be <0)
        elif row[0] == 'x_s':
            config.x_s = np.float(row[1])  # distance in m
            if config.x_s >= 0:
                raise ValueError(['Source position along x must be <0'])
        elif row[0] == 'Property':
            pass  # first line
        else:
            raise ValueError(['Output file of the source generation is not valid. Input "' + row[0] + '" not valid'])

    # --- The electric field itself --- #
    e_field = np.loadtxt(file_e_init, delimiter=',', dtype="complex")
    n_z = e_field.size
    # size of the electric field must match the geometry parameters
    if n_z != config.N_z:
        raise ValueError(['N_z value does not match with saved initial field'])

    # ------------- END ------------ #
    # --- Reading source E-field --- #
    # ------------------------------ #

    return e_field


def read_relief(config, file_relief_config, file_relief):

    # ---------------------- #
    # --- Reading relief --- #
    # ---------------------- #

    # --- Configuration first --- #
    f_source_config = open(file_relief_config, newline='')
    file_tmp = csv.reader(f_source_config)
    for row in file_tmp:
        # geometry must match with the relief generation
        if row[0] == 'N_x':
            n_x = np.int(row[1])
            if n_x != config.N_x:
                raise ValueError(['n_x value does not match with relief'])
        # geometry must match with the source generation
        elif row[0] == 'x_step':
            x_step = np.float(row[1])  # horizontal step in m
        elif row[0] == 'z_max_relief':
            z_max_relief = np.float(row[1])  # max relief in m
            if z_max_relief > config.z_step*config.N_z:
                raise ValueError(['Relief is higher than the computation domain!'])
        # x_s is the source position in the x direction (must be <0)
        elif row[0] == 'type':
            config.type = row[1]  #
        elif row[0] == 'iterations':
            config.iterations = int(row[1])  #
        elif row[0] == 'center':
            config.center = np.float(row[1])  #
        elif row[0] == 'width':
            config.width = np.float(row[1])  #
        elif row[0] == 'Property':
            pass  # first line
        else:
            raise ValueError(['Output file of the relief generation is not valid. Input "' + row[0] + '" not valid'])

    # --- The relief itself --- #
    z_relief = np.loadtxt(file_relief, delimiter=',', dtype="float")
    # size of the electric field must match the geometry parameters
    z_relief = config.z_step*np.round(z_relief/config.z_step)

    return z_relief

# read_Config_plot

##
# @package read_config_plot
# @author Remi Douvenot
# @date 16/06/2022
# @brief Fill the Config_plot class with the input from input file
##


def read_config_plot(file_config_plot):

    # --------------------------- #
    # --- Reading plot config --- #
    # --------------------------- #

    # --- Configuration first --- #
    f_plot_config = open(file_config_plot, newline='')
    file_tmp = csv.reader(f_plot_config)
    for row in file_tmp:
        # data type to plot. E, F, or S (field, propag factor or Poynting vector)
        if row[0] == 'Data type':
            Config_plot.output_type = row[1]
        # plot the final field?
        elif row[0] == 'Final field':
            Config_plot.final_flag = row[1]  # Y or N
        # plot the total field?
        elif row[0] == 'Total field':
            Config_plot.total_flag = row[1]  # Y or N
        # dynamic (difference between min and max plotted)
        elif row[0] == 'Dynamic':
            Config_plot.dynamic = np.float(row[1])  #
        # plot a wavelet representation (Y or N)
        elif row[0] == 'Wavelet decomposition':
            Config_plot.wavelets = row[1]  #
        # Distance of the vertical cut (wavelet representation)
        elif row[0] == 'Cut':
            Config_plot.cut = np.float(row[1])  #
        # Plot the dictionary of wavelet propagators?
        elif row[0] == 'Dictionary':
            Config_plot.library = row[1]  #
        elif row[0] == 'Property':
            pass  # first line
        else:
            raise ValueError(['Output file of the relief generation is not valid. Input "' + row[0] + '" not valid'])
    return Config_plot
