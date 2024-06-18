#!/usr/bin/env python
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License", Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing", software
# distributed under the License is distributed on an "AS IS" BASIS",
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND", either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


from abc import ABCMeta
from abc import abstractmethod
from data import Tree
from data import Plot
from data.general import Area, Model, Warnings
from util import Tools
from scipy import integrate
from models.trees import *
from data.general import Area
from data.variables import AREA_VARS, PLOT_VARS

import logging
import math
import numpy as np
import pandas as pd
import collections
import itertools


class TreeEquations(metaclass=ABCMeta):

    def __init__(self, name: str, version: int):
        self.__tree = None
        self.__name = name
        self.__version = version

        Tools.print_log_line("Loading model " + str(self.name) + "(" + str(self.version) + ")", logging.INFO)

    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def tree(self):
        return self.__tree

    def set_tree(self, tree: Tree):
        Tools.print_log_line("Loading tree (" + tree.id + ") into model" + self.tree + "(" + self.version + ")", logging.INFO)
        self.__tree = tree


    def get_ifn_id(species):
        """
        Function that returns the Spanish Forest National Inventory (SFNI, IFN) code of each species.
        Args.:
            - species: species genus first letter in uppercase and species full word in lowercase (see examples)
        """

        if species == 'Falnus':
            id = 3
        elif species == 'Mcommunis':
            id = 6
        elif species == 'Acacia':
            id = 7
        elif species == 'Aaltissima':
            id = 11
        elif species == 'Msylvestris':
            id = 12
        elif species == 'Caustralis':
            id = 13
        elif species == 'Tbaccata':
            id = 14
        elif species == 'Crataegus':
            id = 15
        elif species == 'Pyrus':
            id = 16
        elif species == 'Catlantica':
            id = 17
        elif species == 'Clawsoniana':
            id = 18
        elif species == 'Psylvestris':
            id = 21
        elif species == 'Puncinata':
            id = 22
        elif species == 'Ppinea':
            id = 23
        elif species == 'Phalepensis':
            id = 24
        elif species == 'Pnigra':
            id = 25
        elif species == 'Ppinaster':
            id = 26
        elif species == 'Pcanariensis':
            id = 27
        elif species == 'Pradiata':
            id = 28
        elif species == 'Potros':
            id = 29
        elif species == 'MixConiferas':
            id = 30
        elif species == 'Aalba':
            id = 31
        elif species == 'Apinsapo':
            id = 32
        elif species == 'Pabies':
            id = 33
        elif species == 'Pmenziesii':
            id = 34
        elif species == 'Larix':
            id = 35
        elif species == 'Csempervirens':
            id = 36
        elif species == 'Jcommunis':
            id = 37
        elif species == 'Jthurifera':
            id = 38
        elif species == 'Jphoenicea':
            id = 39
        elif species == 'Quercus':
            id = 40
        elif species == 'Qrobur':
            id = 41
        elif species == 'Qpetraea':
            id = 42
        elif species == 'Qpyrenaica':
            id = 43
        elif species == 'Qfaginea':
            id = 44
        elif species == 'Qilex':
            id = 45
        elif species == 'Qsuber':
            id = 46
        elif species == 'Qcanariensis':
            id = 47
        elif species == 'Qrubra':
            id = 48
        elif species == 'Qotros':
            id = 49
        elif species == 'MixRibera':
            id = 50
        elif species == 'Palba':
            id = 51
        elif species == 'Ptremula':
            id = 52
        elif species == 'Tamarix':
            id = 53
        elif species == 'Aglutinosa':
            id = 54
        elif species == 'Fangustifolia':
            id = 55
        elif species == 'Uminor':
            id = 56
        elif species == 'Salix':
            id = 57
        elif species == 'Pnigra':
            id = 58
        elif species == 'MixEucaliptos':
            id = 60
        elif species == 'Eglobulus':
            id = 61
        elif species == 'Ecamaldulensis':
            id = 62
        elif species == 'Eotros':
            id = 63
        elif species == 'Enitens':
            id = 64
        elif species == 'Iaquifolium':
            id = 65
        elif species == 'Oeuropaea':
            id = 66
        elif species == 'Csiliqua':
            id = 67
        elif species == 'Aunedo':
            id = 68
        elif species == 'Phoenix':
            id = 69
        elif species == 'MixFrondosasGrandes':
            id = 70
        elif species == 'Fsylvatica':
            id = 71
        elif species == 'Csativa':
            id = 72
        elif species == 'Betula':
            id = 73
        elif species == 'Cavellana':
            id = 74
        elif species == 'Jregia':
            id = 75
        elif species == 'Acampestre':
            id = 76
        elif species == 'Tilia':
            id = 77
        elif species == 'Sorbus':
            id = 78
        elif species == 'Plhispanica':
            id = 79
        elif species == 'Laurisilva':
            id = 80
        elif species == 'Mfaya':
            id = 81
        elif species == 'Icanariensis':
            id = 82
        elif species == 'Earborea':
            id = 83
        elif species == 'Pindica':
            id = 84
        elif species == 'Smarmulano':
            id = 85
        elif species == 'Pexcelsa':
            id = 86
        elif species == 'Ophoetens':
            id = 87
        elif species == 'Abarbujana':
            id = 88
        elif species == 'MixLaurisilvas':
            id = 89
        elif species == 'MixFrondosasPequeñas':
            id = 90
        elif species == 'Bsempervirens':
            id = 91
        elif species == 'Rpseudacacia':
            id = 92
        elif species == 'Pterebinthus':
            id = 93
        elif species == 'Lnobilis':
            id = 94
        elif species == 'Prunus':
            id = 95
        elif species == 'Rcoriaria':
            id = 96
        elif species == 'Snigra':
            id = 97
        elif species == 'Cbetulus':
            id = 98
        elif species == 'Mixfrondosas':
            id = 99
        elif species == 'Amelanoxylon':
            id = 207
        elif species == 'Cmonogyna':
            id = 215
        elif species == 'Cdeodara':
            id = 217
        elif species == 'Carizonica':
            id = 236
        elif species == 'Joxycedrus':
            id = 237
        elif species == 'Jturbinata':
            id = 238
        elif species == 'Jsabina':
            id = 239
        elif species == 'Qpubescens' or species == 'Qhumilis':
            id = 243
        elif species == 'Qlusitanica':
            id = 244
        elif species == 'Tcanariensis':
            id = 253
        elif species == 'Fexcelsior':
            id = 255
        elif species == 'Uglabra':
            id = 256
        elif species == 'Salba':
            id = 257
        elif species == 'Pxcanadensis' or species == 'Pxeuroamericana':
            id = 258
        elif species == 'Balba':
            id = 273
        elif species == 'Amonspessulanum':
            id = 276            
        elif species == 'Saria':
            id = 278
        elif species == 'Pspinosa':
            id = 295
        elif species == 'Clibani':
            id = 317
        elif species == 'Clusinatica':
            id = 336
        elif species == 'Fornus':
            id = 355
        elif species == 'Upumila':
            id = 356
        elif species == 'Satrocinerea':
            id = 357            
        elif species == 'Bpendula':
            id = 373
        elif species == 'Anegundo':
            id = 376
        elif species == 'Saucuparia':
            id = 378            
        elif species == 'Pavium':
            id = 395
        elif species == 'Cmacrocarpa':
            id = 436
        elif species == 'Sbabylonica':
            id = 457
        elif species == 'Aopalus':
            id = 476            
        elif species == 'Sdomestica':
            id = 478            
        elif species == 'Plusitanica':
            id = 495
        elif species == 'Scantabrica':
            id = 557
        elif species == 'Apseudoplatanus':
            id = 576
        elif species == 'Storminalis':
            id = 578            
        elif species == 'Ppadus':
            id = 595
        elif species == 'Scaprea':
            id = 657
        elif species == 'Aplatanoides':
            id = 676            
        elif species == 'Slatifolia':
            id = 678            
        elif species == 'Selaeagnos':
            id = 757     
        elif species == 'Schamaemespilus':
            id = 778            
        elif species == 'Sfragilis':
            id = 857
        elif species == 'Scanariensis':
            id = 858                               
        elif species == 'Cedrus':
            id = 917
        elif species == 'Cupressus':
            id = 936
        elif species == 'Juniperus':
            id = 937
        elif species == 'Fraxinus':
            id = 955
        elif species == 'Ulmus':
            id = 956
        elif species == 'Spurpurea':
            id = 957	    
        elif species == 'Juglans':
            id = 975
        elif species == 'Acer':
            id = 976	    
        else:
            id = ''

        return id


    def set_null_growth(list_of_trees):
        """
        Function that assing null growth to the tree growth variables.
        Args.:
            - list_of_trees: is the list of trees from each plot that must be ordered following a basal area criteria before
        """

        for tree in list_of_trees:
            tree.add_value('dbh_i', 0)
            tree.add_value('height_i', 0)
            tree.add_value('basal_area_i', 0)


    def get_reineke_value(species):
        """
        Get specific species value to calculate SDI index.
        Args.:
            - species: tree species code following the classification of the SFNI 
        """


        # TODO: check bibliography and write for each species
        if species == species:

            r_value = -1.605 # default

        return r_value


    def set_reineke_value(species):
        """
        Set specific species value to calculate SDI index.
        Args.:
            - species: tree species code following the classification of the SFNI
        """


        # TODO: check bibliography and write for each species
        if species == species:

            r_value = -1.605 # default

        return r_value


    def choose_martonne(plot_id, year, list_years):
        """
        Function created to select the Martonne Index corresponding to the year of the plot.
        Initially, it was created to be applied at mixed tree models.
        Args.:
            - plot_id: plot unique identification code
            - year: actual real year on the simulation
            - list_years: list of years when the user want to update the Martonne Index
        """

        # if the inventory has this variable...
        if 'MARTONNE' in AREA_VARS and Area.martonne != '':

            if year <= list_years[0]: # under 2020 (default)
                M = Area.martonne[plot_id]

            else:

                # if the inventory has this variable we consider that the others are also available...
                if 'MARTONNE_2080' in AREA_VARS and Area.martonne_2080 != '':

                    if year <= list_years[1]: # 2021-2040
                        M = Area.martonne_2020[plot_id]
                    elif year <= list_years[2]: # 2041-2060
                        M = Area.martonne_2040[plot_id]
                    elif year <= list_years[3]: # 2061-2080
                        M = Area.martonne_2060[plot_id]
                    elif year <= list_years[4]: # 2081-2100
                        M = Area.martonne_2080[plot_id]
                    else:  # > 2100
                        M = Area.martonne_2080[plot_id]  # the most extreme one

                else:
                    M = Area.martonne[plot_id]  # value by default

        else:

            M = '' # no value

        return M


    def get_g(tree):
        """
        Calculates tree basal area in cm2.
        It returns the result on the corresponding tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm
        """

        g = math.pi*(tree.dbh/2)**2  # tree basal area (cm2)
        return g

    def set_g(tree):
        """
        Calculates tree basal area in cm2.
        It includes/rewrite the result on the corresponding tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm
        """

        g = math.pi * (tree.dbh / 2) ** 2  # tree basal area (cm2)
        tree.add_value('basal_area', g)  # add value to each tree


    def get_g_ha(tree):
        """
        Calculates tree basal area per hectare in m2/ha.
        It returns the result on the corresponding tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm and tree expan
        """

        g_ha = (math.pi*(tree.dbh/2)**2)*tree.expan / 10000  # tree basal area per hectare (m2/ha)
        return g_ha


    def set_g_ha(tree):
        """
        Calculates tree basal area per hectare in m2/ha.
        It includes/rewrite the result on the corresponding tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm and tree expan
        """

        g_ha = (math.pi*(tree.dbh/2)**2)*tree.expan / 10000  # tree basal area per hectare (m2/ha)
        tree.add_value('ba_ha', g_ha)  # add value to each tree


    def get_bal(list_of_trees):
        """
        Calculates bal competition index per hectare in m2/ha.
        It includes/rewrite the result on the correspong tree variable.
        Args.:
            - list_of_trees: is the list of trees from each plot that must be ordered following a basal area criteria before
        """

        bal = 0  # bigger tree in the plot

        for tree in list_of_trees:

            tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
            bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated


    def get_slenderness(tree):
        """
        Calculates tree slenderness.
        It returns the result on the corresponding tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm and tree height in m
        """

        slenderness = tree.height*100/tree.dbh  # height/diameter ratio (%)
        return slenderness


    def set_slenderness(tree):
        """
        Calculates tree slenderness.
        It includes/rewrite the result on the correspong tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm and tree height in m
        """

        slenderness = tree.height * 100 / tree.dbh  # height/diameter ratio (%)
        tree.add_value('slenderness', slenderness)  # add value to each tree


    def get_circumference(tree):
        """
        Calculates tree normal circumference in cm.
        It returns the result on the corresponding tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm 
        """

        circ = math.pi*tree.dbh  # normal circumference (cm)
        return circ


    def set_circumference(tree):
        """
        Calculates tree normal circumference in cm.
        It includes/rewrite the result on the correspong tree variable.
        Args.:
            - tree: tree information that includes tree dbh in cm
        """

        circ = math.pi*tree.dbh  # normal circumference (cm)
        tree.add_value('normal_circumference', circ)  # add value to each tree


    def get_height(tree, plot):
        """

        :param plot:
        :return:
        """

        # TODO: include all the species we have in here / set_height function
        # TODO: explain that function and create calc_height function

        if int(tree.specie) == 0:
            beta0 = 2.7801 - 0.0132 * tree.bal - 0.0203 * plot.qm_dbh
            h = 1.3 + (beta0 * (1 / tree.dbh - 1 / plot.dominant_dbh) +
                           (1 / (plot.dominant_h - 1.3)) ** 0.5) ** (-2)

        tree.add_value('height', h)


    def check_projection_time(time):
        """
        Function to print helpful information to check is the projection time is the correct on the model that is being
        using. It also returns a message on the output if the time provided by the user is not correct.
        Args.:
            - time: time projection provided by the user (years)
        """
        # TODO: rename exec_time as projection_time
        # if the user time is not the same as the execution model time, a warning message will be notified
        if time != Model.exec_time:
            print('BE CAREFUL! That model was developed to ', Model.exec_time,' years projection, and you are trying to '
                  'make a ', time, ' years projection!', sep = '')
            print('Please, change your projection time to the recommended (', Model.exec_time, ' years projection).'
                  ' If not, the output values will be not correct.', sep = '')

            # that variable must be activated when the execution time of the user is not the same as the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output


    def update_year_and_age(plot, time):
        """
        Function that update year and age stand values to have them temporally available.
        It doesn't overwrite the plot values, as they will be automatically updated by SIMANFOR.
        Args.:
            - plot: plot data needed to check the previous year and age values
            - time: projection time provided by the user (years)
        """

        # by default values (if variables needed are not available)
        new_plot_year = new_plot_age = ''

        if 'YEAR' in PLOT_VARS:
            new_plot_year = plot.year + time  # YEAR is automatically updated after the execution process
        if 'AGE' in PLOT_VARS:
            new_plot_age = plot.age + time  # AGE is automatically updated after the execution process

        return new_plot_year, new_plot_age


    def set_diversity_indexes(plot, list_of_trees):
        """
        Function that calculates the different diversity indexes for each plot.
        Args.:
            - plot: plot data needed to check the previous year and age values
            - list_of_trees: list of the trees in the plot to obtain species and expan values
        """

        if 'SHANNON' in PLOT_VARS:
            plot.add_value('shannon', TreeEquations.get_shannon_index(plot, list_of_trees))
        if 'SIMPSON' in PLOT_VARS:
            plot.add_value('simpson', TreeEquations.get_simpson_index(plot, list_of_trees))
        if 'MARGALEF' in PLOT_VARS:
            plot.add_value('margalef', TreeEquations.get_margalef_index(plot, list_of_trees))
        if 'PIELOU' in PLOT_VARS:
            plot.add_value('pielou', TreeEquations.get_pielou_index(plot, list_of_trees))


    def get_shannon_index(plot, list_of_trees):
        """
        Function that calculates Shannon-Weaver Diversity Index.
        Ref.: Omoro L.M., Pellikka P.K., & Rogers P.C. (2010). Tree species diversity, richness, and similarity between
        exotic and indigenous forests in the cloud forests of Eastern Arc Mountains, Taita Hills, Kenya. Journal of
        Forestry Research, 21(3), 255–264.

        Args.:
            - plot: plot data needed to check the previous year and age values
            - list_of_trees: list of the trees in the plot to obtain species and expan values
        """

        # get species and expan or the plot
        species_list = []
        expan_list = []

        for tree in list_of_trees:

            species_list.append(int(tree.specie))
            expan_list.append(tree.expan)

        # create a df with species and expan data
        df = pd.DataFrame({'species': species_list, 'expan': expan_list})

        # group by species
        df_grouped = df.groupby('species')['expan'].sum()

        # calculate total expan
        total_expan = df_grouped.sum()

        # calculate species proportion
        sp_prop = df_grouped.values/total_expan

        # for each species, calculate the corresponding shannon value
        for row in sp_prop:

            shannon_row = - row * math.log(row)

        # calculate shannon index for the plot
        shannon = shannon_row.sum()

        return shannon


    def get_simpson_index(plot, list_of_trees):
        """
        Function that calculates Simpson Diversity Index.
        Ref.: Edward H. Simpson (1949) Measurement of diversity. Nature 163:688

        Args.:
            - plot: plot data needed to check the previous year and age values
            - list_of_trees: list of the trees in the plot to obtain species and expan values
        """

        # get species and expan or the plot
        species_list = []
        expan_list = []

        for tree in list_of_trees:

            species_list.append(int(tree.specie))
            expan_list.append(tree.expan)

        # create a df with species and expan data
        df = pd.DataFrame({'species': species_list, 'expan': expan_list})

        # group by species
        df_grouped = df.groupby('species')['expan'].sum()

        # calculate total expan
        total_expan = df_grouped.sum()

        # calculate species abundance
        sp_abundance = df_grouped.values

        # for each species, calculate the corresponding simpson value
        for row in sp_abundance:

            simpson_row = row * (row - 1)

        # calculate simpson index for the plot: values = 0 means no diversity, and 1 very diverse
        simpson = 1 - simpson_row.sum() / (total_expan * (total_expan - 1))

        return simpson


    def get_margalef_index(plot, list_of_trees):
        """
        Function that calculates Margalef Specific Diversity Index.
        Ref.: Ulanowicz R.E. (2001). Information theory in ecology. Computers & chemistry, 25(4), 393–399.
        doi: 10.1016/s0097-8485(01)00073-0

        Args.:
            - plot: plot data needed to check the previous year and age values
            - list_of_trees: list of the trees in the plot to obtain species and expan values
        """

        # get species and expan or the plot
        species_list = []
        expan_list = []

        for tree in list_of_trees:

            species_list.append(int(tree.specie))
            expan_list.append(tree.expan)

        # create a df with species and expan data
        df = pd.DataFrame({'species': species_list, 'expan': expan_list})

        # group by species
        df_grouped = df.groupby('species')['expan'].sum()

        # calculate total expan
        total_expan = df_grouped.sum()

        # calculate number of different species
        n_sp = df_grouped.nunique()

        # calculate margalef specific diversity index for the plot: under 2 means low diversity, upper 5 high diversity
        margalef = (n_sp - 1) / math.log(total_expan)

        return margalef


    def get_pielou_index(plot, list_of_trees):
        """
        Function that calculates Pielou Diversity Index.
        Ref.: Bray J.R., & Curtis J.T. (1957). An ordination of the upland forest communities of southern Wisconsin.
        Ecological monographs, 27(4), 325–349.

        Args.:
            - plot: plot data needed to check the previous year and age values
            - list_of_trees: list of the trees in the plot to obtain species and expan values
        """

        # get species and expan or the plot
        species_list = []
        expan_list = []

        for tree in list_of_trees:
            species_list.append(int(tree.specie))
            expan_list.append(tree.expan)

        # create a df with species and expan data
        df = pd.DataFrame({'species': species_list, 'expan': expan_list})

        # group by species
        df_grouped = df.groupby('species')['expan'].sum()

        # calculate total expan
        total_expan = df_grouped.sum()

        # calculate species proportion and species number
        sp_prop = df_grouped.values / total_expan
        n_sp = df_grouped.nunique()

        # for each species, calculate the corresponding shannon value
        for row in sp_prop:
            shannon_row = - row * math.log(row)

        # calculate shannon index for the plot
        shannon = shannon_row.sum()

        # calculate pielou index using shannon, just if species number is > 1
        if n_sp != 1:
            pielou = shannon / math.log(n_sp)
        else:
            pielou = ''

        return pielou


    def get_shannon_and_pielou_index(plot, list_of_trees):
        """
        Function that calculates both Shannon-Weaver Diversity Index and Pielou Diversity Index.
        That function was created as Pielou needs Shannon index to run.
        Ref.: Omoro L.M., Pellikka P.K., & Rogers P.C. (2010). Tree species diversity, richness, and similarity between
        exotic and indigenous forests in the cloud forests of Eastern Arc Mountains, Taita Hills, Kenya. Journal of
        Forestry Research, 21(3), 255–264.
        Ref.: Bray J.R., & Curtis J.T. (1957). An ordination of the upland forest communities of southern Wisconsin.
        Ecological monographs, 27(4), 325–349.

        Args.:
            - plot: plot data needed to check the previous year and age values
            - list_of_trees: list of the trees in the plot to obtain species and expan values
        """

        # get species and expan or the plot
        species_list = []
        expan_list = []

        for tree in list_of_trees:
            species_list.append(int(tree.specie))
            expan_list.append(tree.expan)

        # create a df with species and expan data
        df = pd.DataFrame({'species': species_list, 'expan': expan_list})

        # group by species
        df_grouped = df.groupby('species')['expan'].sum()

        # calculate total expan
        total_expan = df_grouped.sum()

        # calculate species proportion and species number
        sp_prop = df_grouped.values / total_expan
        n_sp = df_grouped.nunique()

        # for each species, calculate the corresponding shannon value
        for row in sp_prop:
            shannon_row = - row * math.log(row)

        # calculate shannon index for the plot
        shannon = shannon_row.sum()

        # calculate pielou index using shannon, just if species number is > 1
        if n_sp != 1:
            pielou = shannon / math.log(n_sp)
        else:
            pielou = ''

        return shannon, pielou


    def get_deadwood_index_cesefor_g(plot, dead_trees_list):
        """
        Function that calculates a Deadwood Biodiversity Index developed by CESEFOR.
        It considers the quantity of deadwood in stands with a quadratic mean diameter (dg) of greater than or equal
        to 17.5 cm. If the stand basal area of deadwood exceeds 6% of the trees with a dbh of 17.5 cm or larger, the stand's
         deadwood status is classified as positive (1). If the percentage is lower, the status is deemed insufficient
         (0). This index is not applied to stands with a dg of less than 17.5 cm (-).
         This index was developed to be included on Life Rebollo project simulations.

        Args.:
            - plot: plot data needed to check the previous year and age values
            - dead_trees_list: list of the dead trees in the plot. Contains:
                [tree.tree_id, tree.dbh, tree.expan, tree.basal_area, tree.vol, dead_expan]
        """

        # variable to accumulate g of dead trees
        g_dead = 0

        # calculate the amount of deadwood that overpass the criteria
        for tree in dead_trees_list:

            if tree[1] >= 17.5:  # dbh >= 17.5

                g_dead += tree[2] * tree[3] * tree[5]  # expan * g * dead_expan

        # change the amount of deadwood to %
        g_dead = ((g_dead/10000)/plot.basal_area)*100

        # assing index value
        if plot.qm_dbh < 17.5:

            index = '-'

        elif plot.qm_dbh >= 17.5 and g_dead >= 6:

            index = '1'

        else:

            index = '0'

        return index


    def get_deadwood_index_cesefor_v(plot, dead_trees_list):
        """
        Function that calculates a Deadwood Biodiversity Index developed by CESEFOR.
        It considers the quantity of deadwood in stands with a quadratic mean diameter (dg) of greater than or equal
        to 17.5 cm. If the stand volume of deadwood exceeds 6% of the trees with a dbh of 17.5 cm or larger, the stand's
         deadwood status is classified as positive (1). If the percentage is lower, the status is deemed insufficient
         (0). This index is not applied to stands with a dg of less than 17.5 cm (-).
         This index was developed to be included on Life Rebollo project simulations.

        Args.:
            - plot: plot data needed to check the previous year and age values
            - dead_trees_list: list of the dead trees in the plot. Contains:
                [tree.tree_id, tree.dbh, tree.expan, tree.basal_area, tree.vol, dead_expan]
        """

        # variable to accumulate v of dead trees
        v_dead = 0

        # calculate the amount of deadwood that overpass the criteria
        for tree in dead_trees_list:

            if tree[1] >= 17.5:  # dbh >= 17.5

                v_dead += tree[2] * tree[4] * tree[5]  # expan * g * dead_expan

        # change the amount of deadwood to %
        v_dead = ((v_dead/10000)/plot.vol)*100

        # assign index value
        if plot.qm_dbh < 17.5:

            index = '-'

        elif plot.qm_dbh >= 17.5 and v_dead >= 6:

            index = '1'

        else:

            index = '0'

        return index
