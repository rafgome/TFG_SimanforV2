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

# TODO: cambiar el encabezado de los scripts y revisar las librerías que no se usan - silenciar
from abc import ABCMeta
from abc import abstractmethod
from data import Tree
from data import Plot
from data.general import Area, Model, Warnings
from util import Tools
from scipy import integrate
from models.trees.equations_tree_models import TreeEquations
from data.general import Area
from data.variables import TREE_VARS

import logging
import math
import numpy as np


class MixedEquations(metaclass=ABCMeta):

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

 ######################################################################################################################
######################################################################################################################

    def print_run_info(plot):
        """
        Function to print helpful information to check which model and plot is actually running.
        Args.:
            - plot: plot information
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print(' Running: Spanish mixed models for species ', int(plot.id_sp1), ' and ', int(plot.id_sp2), '. Plot: ', plot.plot_id, sep = '')
        print('#--------------------------------------------------------------------------------------------------#')


    def get_bal_per_sp(list_of_trees, plot):
        """
        Calculates bal competition index per hectare in m2/ha, also separating by tree species.
        It includes/rewrite the result on the corresponding tree variable.
        Args.:
            - list_of_trees: is the list of trees from each plot that must be ordered following a basal area criteria before
            - plot: plot data needed to check the species codes
        """

        bal = bal_sp1 = bal_sp2 = bal_sp3 = 0  # bigger tree in the plot

        for tree in list_of_trees: # for each tree...

            if int(tree.specie) == int(plot.id_sp1):  # species 1 condition
                # TODO: preguntar a Felipe si debo meter especies externas en interspecifico o no
                tree.add_value('bal', bal)  # bal value without consider species (m2/ha)
                tree.add_value('bal_intrasp', bal_sp1)  # bal value for species 1 (m2/ha)
                tree.add_value('bal_intersp', bal_sp2 + bal_sp3)  # bal value for other species (m2/ha)

                bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                bal_sp1 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variables


            elif int(tree.specie) == int(plot.id_sp2):  # species 2 condition

                tree.add_value('bal', bal)  # bal value without consider species (m2/ha)
                tree.add_value('bal_intrasp', bal_sp2)  # bal value for species 1 (m2/ha)
                tree.add_value('bal_intersp', bal_sp1 + bal_sp3)  # bal value for other species (m2/ha)

                bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                bal_sp2 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variables

            else:

                tree.add_value('bal', bal)  # bal value without consider species (m2/ha)
                tree.add_value('bal_intrasp', bal_sp3)  # bal value for species 1 (m2/ha)
                tree.add_value('bal_intersp', bal_sp1 + bal_sp2)  # bal value for other species (m2/ha)

                bal += tree.basal_area*tree.expan/10000  # that value is accumulated
                bal_sp3 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variables


    def get_stand_by_sp(list_of_trees, plot, M):
        """
        Calculates stand variables by tree species.
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - list_of_trees: is the list of trees from each plot that must be ordered following a basal area criteria before
            - plot: plot data needed to check the species codes
            - M: is the Martonne Index value previously selected on other function. If it is not available, variables that
                needs it will be not calculated
        """

        # create variables needed as accumulators
        total_trees = other_trees = 0
        g_sp1 = g_sp2 = g_sp3 = N_sp1 = N_sp2 = N_sp3 = dg_sp1 = dg_sp2 = dg_sp3 = 0
        dbh_sp1 = max_dbh_sp1 = max_h_sp1 = max_ba_sp1 = h_sp1 = dbh_sp2 = max_dbh_sp2 = max_h_sp2 = max_ba_sp2 = \
            h_sp2 = dbh_sp3 = max_dbh_sp3 = max_h_sp3 = max_ba_sp3 = h_sp3 = 0
        min_dbh_sp1 = min_ba_sp1 = min_h_sp1 = min_dbh_sp2 = min_ba_sp2 = min_h_sp2 = min_dbh_sp3 = min_ba_sp3 = min_h_sp3 = 9999

        # on that for loop, accumulators are created to later use them on the correct variables
        for tree in list_of_trees:  # for each tree...

            total_trees += 1  # count the total of trees

            if int(tree.specie) == int(plot.id_sp1):  # species 1 condition

                N_sp1 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                dg_sp1 += math.pow(tree.dbh, 2) * tree.expan  # accumulator to calculate dg per specie
                g_sp1 += tree.basal_area * tree.expan / 10000  # accumulator to calculate that plot variable (m2/ha)
                dbh_sp1 += tree.dbh * tree.expan  # accumulator to calculate mean dbh per specie
                h_sp1 += tree.height * tree.expan  # accumulator to calculate mean height per specie

                max_dbh_sp1 = tree.dbh if tree.dbh > max_dbh_sp1 else max_dbh_sp1
                min_dbh_sp1 = tree.dbh if tree.dbh < min_dbh_sp1 else min_dbh_sp1

                max_h_sp1 = tree.height if tree.height > max_h_sp1 else max_h_sp1
                min_h_sp1 = tree.height if tree.height < min_h_sp1 else min_h_sp1

                max_ba_sp1 = tree.basal_area if tree.basal_area > max_ba_sp1 else max_ba_sp1
                min_ba_sp1 = tree.basal_area if tree.basal_area < min_ba_sp1 else min_ba_sp1

            elif int(tree.specie) == int(plot.id_sp2):  # species 2 condition

                N_sp2 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                dg_sp2 += math.pow(tree.dbh, 2) * tree.expan  # accumulator to calculate dg per specie
                g_sp2 += tree.basal_area * tree.expan / 10000  # accumulator to calculate that plot variable (m2/ha)
                dbh_sp2 += tree.dbh * tree.expan  # accumulator to calculate mean dbh per specie
                h_sp2 += tree.height * tree.expan  # accumulator to calculate mean height per specie

                max_dbh_sp2 = tree.dbh if tree.dbh > max_dbh_sp2 else max_dbh_sp2
                min_dbh_sp2 = tree.dbh if tree.dbh < min_dbh_sp2 else min_dbh_sp2

                max_h_sp2 = tree.height if tree.height > max_h_sp2 else max_h_sp2
                min_h_sp2 = tree.height if tree.height < min_h_sp2 else min_h_sp2

                max_ba_sp2 = tree.basal_area if tree.basal_area > max_ba_sp2 else max_ba_sp2
                min_ba_sp2 = tree.basal_area if tree.basal_area < min_ba_sp2 else min_ba_sp2

            else:  # other species

                other_trees += 1  # count trees from other species

                N_sp3 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                dg_sp3 += math.pow(tree.dbh, 2) * tree.expan  # accumulator to calculate dg per specie
                g_sp3 += tree.basal_area * tree.expan / 10000  # accumulator to calculate that plot variable (m2/ha)
                dbh_sp3 += tree.dbh * tree.expan  # accumulator to calculate mean dbh per specie
                h_sp3 += tree.height * tree.expan  # accumulator to calculate mean height per specie

                max_dbh_sp3 = tree.dbh if tree.dbh > max_dbh_sp3 else max_dbh_sp3
                min_dbh_sp3 = tree.dbh if tree.dbh < min_dbh_sp3 else min_dbh_sp3

                max_h_sp3 = tree.height if tree.height > max_h_sp3 else max_h_sp3
                min_h_sp3 = tree.height if tree.height < min_h_sp3 else min_h_sp3

                max_ba_sp3 = tree.basal_area if tree.basal_area > max_ba_sp3 else max_ba_sp3
                min_ba_sp3 = tree.basal_area if tree.basal_area < min_ba_sp3 else min_ba_sp3

        if other_trees != 0:  # show number of trees from species not included in the model

            print(' ')
            print(other_trees, 'of the total', total_trees,
                  'trees are not of the main species of the model')
            print('That trees will be shown underlined at the output, and they will be maintained at simulations, '
                  'not applying model species specific equations over them.')
            print(' ')

            if other_trees == total_trees:
                Warnings.specie_error_trees = 1  # activate a warning message on the output

        # create needed variables
        selection_trees_sp1 = selection_trees_sp2 = selection_trees_sp3 = list()
        tree_expansion_sp1 = tree_expansion_sp2 = tree_expansion_sp3 = 0

        # on that for loop, accumulators previously calculated are assigned to the correct variables (basal areas)
        for tree in list_of_trees:  # for each tree...

            if int(tree.specie) == int(plot.id_sp1):  # species 1 condition

                # add both basal area intra- and interspecific (m2/ha)
                tree.add_value('basal_area_intrasp', g_sp1)
                tree.add_value('basal_area_intersp', g_sp2 + g_sp3)

                if tree_expansion_sp1 < 100:  # select trees list, by species, to calculate Ho and Do of each group

                    tree_expansion_sp1 += tree.expan
                    selection_trees_sp1.append(tree)

            elif int(tree.specie) == int(plot.id_sp2):  # species 2 condition

                # add both basal area intra- and interspecific (m2/ha)
                tree.add_value('basal_area_intrasp', g_sp2)
                tree.add_value('basal_area_intersp', g_sp1 + g_sp3)

                if tree_expansion_sp2 < 100:  # select trees list, by species, to calculate Ho and Do of each group

                    tree_expansion_sp2 += tree.expan
                    selection_trees_sp2.append(tree)

            else:  # other species condition

                # add both basal area intra- and interspecific (m2/ha)
                tree.add_value('basal_area_intrasp', g_sp3)
                tree.add_value('basal_area_intersp', g_sp1 + g_sp2)

                if tree_expansion_sp3 < 100:  # select trees list, by species, to calculate Ho and Do of each group

                    tree_expansion_sp3 += tree.expan
                    selection_trees_sp3.append(tree)

        # here, trees selected following their sizes are used to calculate Ho, Do and So by species
        plot.add_value('DOMINANT_H_SP1', Plot.get_dominant_height(plot, selection_trees_sp1))
        plot.add_value('DOMINANT_DBH_SP1', Plot.get_dominant_diameter(plot, selection_trees_sp1))
        plot.add_value('DOMINANT_SECTION_SP1', Plot.get_dominant_section(plot, selection_trees_sp1))
        plot.add_value('DOMINANT_H_SP2', Plot.get_dominant_height(plot, selection_trees_sp2))
        plot.add_value('DOMINANT_DBH_SP2', Plot.get_dominant_diameter(plot, selection_trees_sp2))
        plot.add_value('DOMINANT_SECTION_SP2', Plot.get_dominant_section(plot, selection_trees_sp2))
        plot.add_value('DOMINANT_H_SP3', Plot.get_dominant_height(plot, selection_trees_sp3))
        plot.add_value('DOMINANT_DBH_SP3', Plot.get_dominant_diameter(plot, selection_trees_sp3))
        plot.add_value('DOMINANT_SECTION_SP3', Plot.get_dominant_section(plot, selection_trees_sp3))

        # here variables for each species sizes are assigned
        if N_sp1 != 0:  # if there are trees from that species, data is calculated; else, values will be empty (instead of 0)
            plot.add_value('BA_MAX_SP1', max_ba_sp1)
            plot.add_value('DBH_MAX_SP1', max_dbh_sp1)
            plot.add_value('H_MAX_SP1', max_h_sp1)
            plot.add_value('BA_MIN_SP1', min_ba_sp1)
            plot.add_value('DBH_MIN_SP1', min_dbh_sp1)
            plot.add_value('H_MIN_SP1', min_h_sp1)
            plot.add_value('MEAN_BA_SP1', g_sp1 * 10000 / N_sp1)
            plot.add_value('MEAN_DBH_SP1', dbh_sp1 / N_sp1)
            plot.add_value('MEAN_H_SP1', h_sp1 / N_sp1)

        if N_sp2 != 0:  # if there are trees from that species, data is calculated; else, values will be empty (instead of 0)
            plot.add_value('BA_MAX_SP2', max_ba_sp2)
            plot.add_value('DBH_MAX_SP2', max_dbh_sp2)
            plot.add_value('H_MAX_SP2', max_h_sp2)
            plot.add_value('BA_MIN_SP2', min_ba_sp2)
            plot.add_value('DBH_MIN_SP2', min_dbh_sp2)
            plot.add_value('H_MIN_SP2', min_h_sp2)
            plot.add_value('MEAN_BA_SP2', g_sp2 * 10000 / N_sp2)
            plot.add_value('MEAN_DBH_SP2', dbh_sp2 / N_sp2)
            plot.add_value('MEAN_H_SP2', h_sp2 / N_sp2)

        if N_sp3 != 0:  # if there are trees from that species, data is calculated; else, values will be empty (instead of 0)
            plot.add_value('BA_MAX_SP3', max_ba_sp3)
            plot.add_value('DBH_MAX_SP3', max_dbh_sp3)
            plot.add_value('H_MAX_SP3', max_h_sp3)
            plot.add_value('BA_MIN_SP3', min_ba_sp3)
            plot.add_value('DBH_MIN_SP3', min_dbh_sp3)
            plot.add_value('H_MIN_SP3', min_h_sp3)
            plot.add_value('MEAN_BA_SP3', g_sp3 * 10000 / N_sp3)
            plot.add_value('MEAN_DBH_SP3', dbh_sp3 / N_sp3)
            plot.add_value('MEAN_H_SP3', h_sp3 / N_sp3)

        # here, stand variables by species are assignated: N, N proportion, DG and G
        plot.add_value('DENSITY_SP1', N_sp1)
        plot.add_value('DENSITY_SP2', N_sp2)
        plot.add_value('DENSITY_SP3', N_sp3)

        # density proportions
        plot.add_value('SP1_N_PROPORTION', N_sp1 / (N_sp1 + N_sp2 + N_sp3))
        plot.add_value('SP2_N_PROPORTION', N_sp2 / (N_sp1 + N_sp2 + N_sp3))
        plot.add_value('SP3_N_PROPORTION', N_sp3 / (N_sp1 + N_sp2 + N_sp3))

        # DG
        if N_sp1 != 0:
            qm_dbh_sp1 = math.sqrt(dg_sp1 / N_sp1)
        else:
            qm_dbh_sp1 = 0
        plot.add_value('QM_DBH_SP1', qm_dbh_sp1)

        if N_sp2 != 0:
            qm_dbh_sp2 = math.sqrt(dg_sp2 / N_sp2)
        else:
            qm_dbh_sp2 = 0
        plot.add_value('QM_DBH_SP2', qm_dbh_sp2)

        if N_sp3 != 0:
            qm_dbh_sp3 = math.sqrt(dg_sp3 / N_sp3)
        else:
            qm_dbh_sp3 = 0
        plot.add_value('QM_DBH_SP3', qm_dbh_sp3)

        # basal area
        plot.add_value('BASAL_AREA_SP1', g_sp1)
        plot.add_value('BASAL_AREA_SP2', g_sp2)
        plot.add_value('BASAL_AREA_SP3', g_sp3)

        # the following variables could be not needed, just for the species combinations of Rodríguez de Prado (2022)
        # get SDI, SDImax and species proportions by area
        MixedEquations.choose_SDI_function(plot)


    def get_RPrado_2022_combis(combi):
        """
        Function that returns a list of species mixtures corresponding to the model structure of Rodríguez de Prado (2022).
        That lists are the species combination that follows the approach proposed on Rodríguez de Prado (2022).
        In them, species are included in the original order (mix_species_combis) and both orders (mix_species_combis_both_directions)
        Args.:
            - combi: the type of list must be specified by 'simple' or 'all', referring to each type of list
        Refs.:
            - Rodríguez de Prado, D. (2022). New insights in the modeling and simulation of tree and stand level
            variables in Mediterranean mixed forests in the present context of climate change. Doctoral dissertation.
        """

        if combi == 'simple':

            # mix_species_combis on the original order
            mix_species_combis = ['24_25', '24_26', '24_23', '25_26', '25_21', '26_21', '23_26', '21_22', '71_42',
            '71_43', '71_41', '44_45', '45_43', '45_46', '43_41', '24_44', '24_45', '25_44', '25_45', '26_45',
            '26_43','26_46', '23_45', '23_46', '21_71', '21_44', '21_45', '21_42', '21_43']

        elif combi == 'all':

            # mix_species_combis in both directions (sp1 and sp2)
            mix_species_combis = ['24_25', '25_24', '24_26', '26_24', '24_23', '23_24', '26_25', '25_26',
            '21_25', '25_21', '21_26', '26_21', '23_26', '26_23', '21_22', '22_21', '42_71', '71_42', '43_71', '71_43',
            '41_71', '71_41', '44_45', '45_44', '43_45', '45_43', '46_45', '45_46', '41_43', '43_41', '44_24', '24_44',
            '45_24', '24_45', '44_25', '25_44', '45_25', '25_45', '45_26', '26_45', '43_26', '26_43', '46_26', '26_46',
            '45_23', '23_45', '46_23', '23_46', '71_21', '21_71', '44_21', '21_44', '45_21', '21_45', '42_21', '21_42',
            '43_21', '21_43']

        else:

            # empty list is the request is not correct
            mix_species_combis = []

        return mix_species_combis


    def get_plot_combis(id_sp1, id_sp2):
        """
        Function that returns a string with the combination of species used on the plot.
        Args.:
            - id_sp1: SFNI/IFN code of plot species 1
            - id_sp2: SFNI/IFN code of plot species 2
        """

        # get the combination of species of each plot: original and reverse
        plot_combi = '_'.join((str(int(id_sp1)), str(int(id_sp2))))
        plot_combi_reverse = '_'.join((str(int(id_sp2)), str(int(id_sp1))))

        return plot_combi, plot_combi_reverse


    def apply_survival_model(tree, plot):
        """
        Check the species combination of the plot and applies the correct survival model.
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - tree: is the information of the tree over the one we want to apply the survival model
            - plot: plot data needed to check the species codes
        """

        # get species combis for mixed models
        mix_species_combis = MixedEquations.get_RPrado_2022_combis('simple')

        # get species combi of the plot
        plot_combi, plot_combi_reverse = MixedEquations.get_plot_combis(plot.id_sp1, plot.id_sp2)

        # if the combination is in Rodríguez de Prado (2022)
        if plot_combi in mix_species_combis or plot_combi_reverse in mix_species_combis:

            if int(tree.specie) == int(plot.id_sp1):  # species 1 condition
                if plot.reineke_sp1 > plot.reineke_max_sp1:  # SDI condition
                    return 0.98  # reduce a 2% of the tree expan (2% of the total plot density)
                else:
                    return 1  # the tree survives

            elif int(tree.specie) == int(plot.id_sp2):  # species 2 condition
                if plot.reineke_sp2 > plot.reineke_max_sp2:  # SDI condition
                    return 0.98  # reduce a 2% of the tree expan
                else:
                    return 1  # the tree survives

        elif plot_combi == '41_72' or plot_combi_reverse == '41_72':  # Qrobur x Csativa
            # TODO: *irene* mete aquí tus ecuaaciones de supervivencia silenciadas y ya vemos como montarlas
            # if int(old_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
            #   sup = {'int':5.5768506,'N':0.0003787,'porcentageN':-1.4679638,
            #          'Dg':-0.0551673,'SDI':0.0019533,'Ho':-0.0553423,
            #          'HartB41':0.0017837}
            # elif int(old_tree.specie) == TreeEquations.get_ifn_id('Csativa'):
            #   sup = {'int':5.6830108,'G':0.0305657,'N':0.0003909,
            #           'porcentageG':0.8007021,'porcentageN':1.3059975,
            #           'Dg':-0.0551673,'Ho':-0.0643203,'Ho72':-0.0987610,
            #           'HartB72':-0.0202069}
            return 1

        # if the combination is different...
        else:
            return 1  # not mortality equation available


    def apply_growth_model(time, plot, old_tree, new_tree):
        """
        Check the species combination of the plot and applies the correct growth model.
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - time: projection time. It must be the time needed for the projection
            - plot: plot data needed to check the species codes
            - old_tree: is the information of the tree over the one we want to apply the growth model; data before projection
            - new_tree: is the information of the tree over the one we want to apply the growth model; data after projection
        """

        # update tree age; if tree_age is empty, the value will remain empty
        new_tree.sum_value('tree_age', time)

        # time is automatically updated after the execution process, but new_year will be used if needed
        new_year = plot.year + time

        # get Martonne index to the corresponding year (period between before and after the projection)
        M = TreeEquations.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))  # TODO: list of years temporal

        # get species combis for mixed models
        mix_species_combis = MixedEquations.get_RPrado_2022_combis('simple')

        # get species combi of the plot
        plot_combi, plot_combi_reverse = MixedEquations.get_plot_combis(plot.id_sp1, plot.id_sp2)

        p_bai = {}  # create an empty dictionary to store the parameters of the model

        # if the combination is in Rodríguez de Prado (2022)
        if plot_combi in mix_species_combis or plot_combi_reverse in mix_species_combis:

        # TODO: tener cuidado, si hacen falta datos de old_tree entonces hay que buscar la manera de copiarlos antes, se sobreescriben

            # check species combination
            if plot_combi == '21_25' or plot_combi_reverse == '21_25':  # Psylvestris x Pnigra

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -1.3287, 'd': -0.044, 'logd': 2.2713, 'h': 0, 'dg': -0.0382, 'ba': 0,
                             'baintra': -0.0181, 'bainter': -0.0218, 'bal': 0,
                             'balintra': -0.0018, 'balinter': -0.008, 'm': 0.0081}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                    p_bai = {'int': -1.7176, 'd': -0.0495, 'logd': 2.3873, 'h': 0.0187, 'dg': -0.0464, 'ba': 0,
                             'baintra': -0.0255, 'bainter': -0.0095, 'bal': 0,
                             'balintra': 0, 'balinter': -0.0087, 'm': 0.0158}

            # check species combination
            elif plot_combi == '21_26' or plot_combi_reverse == '21_26':  # Psylvestris x Ppinaster

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -1.4576, 'd': -0.0393, 'logd': 2.3275, 'h': 0.0225, 'dg': -0.0441, 'ba': 0,
                             'baintra': -0.0205, 'bainter': -0.013, 'bal': 0,
                             'balintra': -0.0016, 'balinter': 0, 'm': 0.01}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                     p_bai = {'int': -0.6012, 'd': -0.0249, 'logd': 2.1674, 'h': 0, 'dg': -0.0419, 'ba': -0.0149,
                         'baintra': 0, 'bainter': 0, 'bal': 0, 'balintra': -0.0033, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '21_71' or plot_combi_reverse == '21_71':  # Psylvestris x Fsylvatica

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -1.9057, 'd': -0.0366, 'logd': 2.2551, 'h': 0.0173, 'dg': -0.0224, 'ba': 0,
                         'baintra': -0.0162, 'bainter': -0.0305, 'bal': 0, 'balintra': 0, 'balinter': 0, 'm': 0.0083}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                     p_bai = {'int': -3.0448, 'd': -0.0378, 'logd': 2.3552, 'h': 0.0421, 'dg': -0.0159, 'ba': 0,
                         'baintra': -0.0361, 'bainter': -0.0214, 'bal': 0, 'balintra': 0, 'balinter': 0, 'm': 0.0178}

            # check species combination
            elif plot_combi == '24_25' or plot_combi_reverse == '24_25':  # Phalepensis x Pnigra

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                    p_bai = {'int': -2.1909, 'd': -0.0399, 'logd': 2.0757, 'h': 0.0334, 'dg': -0.0291, 'ba': 0,
                              'baintra': -0.0208, 'bainter': -0.0325, 'bal': 0,
                              'balintra': 0, 'balinter': 0, 'm': 0.0347}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                    p_bai = {'int': 2.7944, 'd': 0.0522, 'logd': 0, 'h': 0.0725, 'dg': -0.029, 'ba': 0,
                                  'baintra': -0.0344, 'bainter': 0, 'bal': 0, 'balintra': 0, 'balinter': 0, 'm': 0.0131}

            # check species combination
            elif plot_combi == '24_26' or plot_combi_reverse == '24_26':  # Phalepensis x Ppinaster

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                    p_bai = {'int': -1.6673, 'd': -0.0363, 'logd': 1.9709, 'h': 0, 'dg': -0.0252, 'ba': 0,
                            'baintra': -0.0181, 'bainter': -0.0283, 'bal': -0.0063,
                            'balintra': 0, 'balinter': 0, 'm': 0.0581}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                    p_bai = {'int': -1.0381, 'd': -0.0373, 'logd': 1.9721, 'h': 0.0262, 'dg': -0.0205, 'ba': 0,
                            'baintra': -0.0343, 'bainter': 0, 'bal': 0, 'balintra': 0, 'balinter': 0,
                            'm': 0.0238}

            # check species combination
            elif plot_combi == '23_24' or plot_combi_reverse == '23_24':  # Phalepensis x Ppinea
                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                    p_bai = {'int': 0.8052, 'd': 0, 'logd': 1.2766, 'h': 0, 'dg': -0.0335, 'ba': 0,
                            'baintra': -0.0154, 'bainter': 0, 'bal': 0,
                            'balintra': 0, 'balinter': -0.0266, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                    p_bai = {'int': -1.4508, 'd': -0.047, 'logd': 2.4045, 'h': 0.0573, 'dg': -0.0449, 'ba': 0,
                            'baintra': -0.0348, 'bainter': 0, 'bal': 0, 'balintra': 0, 'balinter': 0,
                            'm': 0}

            # check species combination
            elif plot_combi == '25_26' or plot_combi_reverse == '25_26':  # Pnigra x Ppinaster
                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                    p_bai = {'int': -1.1313, 'd': -0.0323, 'logd': 2.0101, 'h': 0, 'dg': -0.0308, 'ba': 0,
                            'baintra': -0.016, 'bainter': -0.0257, 'bal': 0,
                            'balintra': -0.0051, 'balinter': 0, 'm': 0.0314}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                    p_bai = {'int': -2.3026, 'd': -0.0365, 'logd': 2.3215, 'h': 0, 'dg': -0.0466, 'ba': 0,
                            'baintra': -0.0234, 'bainter': -0.0127, 'bal': 0, 'balintra': 0, 'balinter': 0,
                            'm': 0.0448}

            # check species combination
            elif plot_combi == '23_26' or plot_combi_reverse == '23_26':  # Ppinea x Ppinaster
                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                    p_bai = {'int': -1.2902, 'd': -0.044, 'logd': 2.3163, 'h': 0, 'dg': -0.0148, 'ba': -0.0154,
                            'baintra': 0, 'bainter': 0, 'bal': 0,
                            'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                    p_bai = {'int': 1.8982, 'd': 0, 'logd': 1.1735, 'h': 0, 'dg': -0.0185, 'ba': 0,
                            'baintra': -0.0329, 'bainter': 0, 'bal': 0, 'balintra': 0, 'balinter': 0,
                            'm': -0.0261}

            # check species combination
            elif plot_combi == '21_22' or plot_combi_reverse == '21_22':  # Psylvestris x Puncinata
                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Puncinata'):
                    p_bai = {'int': -0.7357, 'd': -0.0236, 'logd': 1.627, 'h': 0, 'dg': -0.0178, 'ba': 0,
                            'baintra': -0.0183, 'bainter': -0.023, 'bal': 0,
                            'balintra': 0, 'balinter': 0, 'm': 0.0088}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -0.4978, 'd': -0.0257, 'logd': 1.6305, 'h': 0.0151, 'dg': -0.019, 'ba': 0,
                            'baintra': -0.0175, 'bainter': -0.0134, 'bal': 0, 'balintra': 0, 'balinter': 0,
                            'm': 0.0106}

            # check species combination
            elif plot_combi == '71_42' or plot_combi_reverse == '71_42':  # Fsylvatica x Qpetraea

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qpetraea'):
                    p_bai = {'int': -1.439, 'd': -0.0205, 'logd': 1.7953, 'h': 0.0428, 'dg': 0, 'ba': -0.0191,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                    p_bai = {'int': -2.2101, 'd': -0.0266, 'logd': 2.0872, 'h': 0.0434, 'dg': 0, 'ba': 0,
                             'baintra': -0.0339, 'bainter': -0.0117, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '71_43' or plot_combi_reverse == '71_43':  # Fsylvatica x Qpyrenaica

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                    p_bai = {'int': -2.8565, 'd': -0.0519, 'logd': 2.3692, 'h': 0.06, 'dg': -0.0218, 'ba': 0,
                             'baintra': -0.0243, 'bainter': -0.0404, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0158}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                    p_bai = {'int': -1.3884, 'd': -0.0199, 'logd': 1.9848, 'h': 0.0309, 'dg': -0.0194, 'ba': 0,
                             'baintra': -0.0282, 'bainter': 0, 'bal': 0,
                             'balintra': -0.0045, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '71_41' or plot_combi_reverse == '71_41':  # Fsylvatica x Qrobur

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
                    p_bai = {'int': -3.0948, 'd': -0.0385, 'logd': 2.8737, 'h': 0, 'dg': 0, 'ba': -0.0482,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                    p_bai = {'int': -3.3249, 'd': -0.0386, 'logd': 2.8025, 'h': 0.0148, 'dg': 0, 'ba': 0,
                             'baintra': -0.0423, 'bainter': 0, 'bal': -0.0057,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi =='44_45' or plot_combi_reverse == '44_45':  # Qfaginea x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -1.8672, 'd': -0.0319, 'logd': 1.7637, 'h': 0.0652, 'dg': 0, 'ba': -0.0161,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0114}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                    p_bai = {'int': -2.2426, 'd': -0.0361, 'logd': 1.8621, 'h': 0.0827, 'dg': 0, 'ba': 0,
                             'baintra': -0.0292, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0129}

            # check species combination
            elif plot_combi == '43_45' or plot_combi_reverse == '43_45':  # Qpyrenaica x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                    p_bai = {'int': -1.3431, 'd': -0.0425, 'logd': 1.7239, 'h': 0.1162, 'dg': 0, 'ba': 0,
                             'baintra': -0.0433, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': -0.0414, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -0.2648, 'd': 0, 'logd': 1.3493, 'h': 0, 'dg': 0, 'ba': -0.0275,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '46_45' or plot_combi_reverse == '46_45':  # Qsuber x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qsuber'):
                    p_bai = {'int': 0.1117, 'd': -0.0093, 'logd': 0.9492, 'h': 0.0924, 'dg': 0.0185, 'ba': 0,
                             'baintra': -0.0296, 'bainter': -0.0141, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -0.8205, 'd': -0.0294, 'logd': 1.3885, 'h': 0.1355, 'dg': 0, 'ba': 0,
                             'baintra': -0.0364, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '41_43' or plot_combi_reverse == '41_43':  # Qpyrenaica x Qrobur

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
                    p_bai = {'int': -1.3817, 'd': -0.0311, 'logd': 2.1817, 'h': 0, 'dg': 0, 'ba': 0,
                             'baintra': -0.0433, 'bainter': -0.0319, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                    p_bai = {'int': 0.1827, 'd': -0.0209, 'logd': 1.4183, 'h': 0, 'dg': 0, 'ba': -0.0284,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '24_44' or plot_combi_reverse == '24_44':  # Phalepensis x Qfaginea

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                    p_bai = {'int': -3.3523, 'd': -0.0824, 'logd': 2.9723, 'h': 0, 'dg': 0, 'ba': 0,
                             'baintra': -0.0523, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': -0.043, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                    p_bai = {'int': -1.91, 'd': -0.0545, 'logd': 2.2627, 'h': 0.0505, 'dg': -0.036, 'ba': 0,
                             'baintra': -0.0232, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0296}

            # check species combination
            elif plot_combi == '24_45' or plot_combi_reverse == '24_45':  # Phalepensis x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -1.1688, 'd': 0, 'logd': 1.0882, 'h': 0.1416, 'dg': -0.0232, 'ba': 0,
                             'baintra': -0.0405, 'bainter': -0.0133, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0289}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                    p_bai = {'int': -1.7286, 'd': -0.0513, 'logd': 2.3588, 'h': 0.0469, 'dg': -0.0382, 'ba': 0,
                             'baintra': -0.0284, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0114}

            # check species combination
            elif plot_combi == '25_44' or plot_combi_reverse == '25_44':  # Pnigra x Qfaginea

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                    p_bai = {'int': -1.7441, 'd': -0.0312, 'logd': 1.7971, 'h': 0.098, 'dg': 0, 'ba': -0.0269,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                    p_bai = {'int': -2.5009, 'd': -0.0607, 'logd': 2.4259, 'h': 0.0389, 'dg': -0.0421, 'ba': 0,
                             'baintra': -0.0305, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0325}

            # check species combination
            elif plot_combi == '25_45' or plot_combi_reverse == '25_45':  # Pnigra x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -1.2536, 'd': -0.0288, 'logd': 1.5467, 'h': 0.0988, 'dg': 0, 'ba': 0,
                             'baintra': -0.0411, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                    p_bai = {'int': -2.1206, 'd': -0.0559, 'logd': 2.518, 'h': 0.0217, 'dg': -0.0268, 'ba': -0.022,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': -0.0052, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '26_45' or plot_combi_reverse == '26_45':  # Ppinaster x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -1.6101, 'd': -0.0381, 'logd': 1.5558, 'h': 0.1836, 'dg': 0, 'ba': 0,
                             'baintra': -0.0227, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                    p_bai = {'int': -0.7777, 'd': -0.0245, 'logd': 1.7932, 'h': 0, 'dg': 0, 'ba': 0,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': -0.0055, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '26_43' or plot_combi_reverse == '26_43':  # Ppinaster x Qpyrenaica

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                    p_bai = {'int': -2.7258, 'd': -0.0527, 'logd': 2.7721, 'h': 0, 'dg': -0.0139, 'ba': 0,
                             'baintra': -0.035, 'bainter': -0.0204, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': -0.0059}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                    p_bai = {'int': -0.597, 'd': -0.0404, 'logd': 2.1635, 'h': 0, 'dg': 0, 'ba': 0,
                             'baintra': -0.0255, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '26_46' or plot_combi_reverse == '26_46':  # Ppinaster x Qsuber

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qsuber'):
                    p_bai = {'int': 0.2845, 'd': 0, 'logd': 0.9688, 'h': 0.0612, 'dg': 0, 'ba': 0,
                             'baintra': -0.0234, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': -0.026, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                    p_bai = {'int': -0.9839, 'd': -0.0287, 'logd': 2.1165, 'h': 0, 'dg': -0.0184, 'ba': 0,
                             'baintra': -0.0285, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0136}

            # check species combination
            elif plot_combi == '23_45' or plot_combi_reverse == '23_45':  # Ppinea x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -1.053, 'd': -0.0315, 'logd': 1.4928, 'h': 0.1113, 'dg': 0, 'ba': -0.023,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                    p_bai = {'int': 0.4764, 'd': 0, 'logd': 1.5955, 'h': -0.0449, 'dg': -0.0236, 'ba': -0.032,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '23_46' or plot_combi_reverse == '23_46':  # Ppinea x Qsuber

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qsuber'):
                    p_bai = {'int': 0.9728, 'd': 0, 'logd': 0.811, 'h': 0.1237, 'dg': 0, 'ba': -0.0282,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': -0.0244}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                    p_bai = {'int': 0.6606, 'd': 0, 'logd': 1.3249, 'h': 0, 'dg': 0, 'ba': 0,
                             'baintra': -0.0427, 'bainter': -0.0187, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '21_44' or plot_combi_reverse == '21_44':  # Psylvestris x Qfaginea

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                    p_bai = {'int': -2.2906, 'd': -0.045, 'logd': 1.9224, 'h': 0.078, 'dg': 0, 'ba': -0.0232,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.0149}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -1.4388, 'd': -0.0384, 'logd': 1.9542, 'h': 0.015, 'dg': -0.0237, 'ba': 0,
                             'baintra': -0.0207, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0.019}


            # check species combination
            elif plot_combi == '21_45' or plot_combi_reverse == '21_45':  # Psylvestris x Qilex

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                    p_bai = {'int': -0.8542, 'd': -0.0239, 'logd': 1.3615, 'h': 0.1229, 'dg': 0, 'ba': 0,
                             'baintra': -0.0315, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': -0.0206, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -0.7816, 'd': -0.0299, 'logd': 1.7776, 'h': 0.0202, 'dg': 0, 'ba': -0.0199,
                             'baintra': 0, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '21_42' or plot_combi_reverse == '21_42':  # Psylvestris x Qpetraea

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qpetraea'):
                    p_bai = {'int': -1.5479, 'd': -0.0401, 'logd': 1.8118, 'h': 0.0827, 'dg': 0, 'ba': 0,
                             'baintra': -0.0522, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -0.0273, 'd': 0, 'logd': 1.2849, 'h': 0.0264, 'dg': 0, 'ba': 0,
                             'baintra': -0.0158, 'bainter': 0, 'bal': 0,
                             'balintra': 0, 'balinter': 0, 'm': 0}

            # check species combination
            elif plot_combi == '21_43' or plot_combi_reverse == '21_43':  # Psylvestris x Qpyrenaica

                # check tree species
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):

                    p_bai = {'int': -2.2915, 'd': -0.0568, 'logd': 2.3202, 'h': 0.0671, 'dg': 0, 'ba': 0,
                             'baintra': -0.0258, 'bainter': -0.0174, 'bal': 0,
                             'balintra': 0, 'balinter': -0.0132, 'm': 0}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_bai = {'int': -1.1121, 'd': -0.0374, 'logd': 2.2161, 'h': 0.0191, 'dg': -0.0447, 'ba': 0,
                             'baintra': -0.0206, 'bainter': 0, 'bal': 0,
                             'balintra': -0.0024, 'balinter': 0, 'm': 0.0133}

            else:  # other mixtures
                p_bai = {}

            # if species is in Rodríguez de Prado (2022)
            if len(p_bai) != 0:

                # calculate bai growth
                bai5 = math.exp(p_bai['int'] + p_bai['d'] * old_tree.dbh + p_bai['logd'] *
                    math.log(old_tree.dbh) + p_bai['h'] * old_tree.height + p_bai['dg'] * plot.qm_dbh +
                    p_bai['ba'] * plot.basal_area + p_bai['baintra'] * old_tree.basal_area_intrasp + p_bai['bainter'] *
                    old_tree.basal_area_intersp + p_bai['balintra'] * old_tree.bal_intrasp + p_bai['balinter'] *
                    old_tree.bal_intersp + p_bai['m'] * M)

                # add bai growth (cm2)
                new_tree.sum_value("basal_area", bai5)
                new_tree.add_value("basal_area_i", bai5)

                # update dbh (cm)
                old_dbh = old_tree.dbh
                new_tree.add_value('dbh', 2 * math.sqrt(new_tree.basal_area / math.pi))
                new_tree.add_value('dbh_i', new_tree.dbh - old_dbh)

                # upload height (m)
                old_height = old_tree.height
                new_height = MixedEquations.apply_hd_model(plot, new_tree)
                new_tree.add_value("height", new_height)
                new_tree.add_value("height_i", new_height - old_height)

        else:

            if plot_combi == '41_72' or plot_combi_reverse == '41_72':  # Qrobur x Csativa
                # TODO: *irene* mete aquí tus ecuaciones de crecimiento silenciadas y ya vemos como montarlas
                if int(old_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
                    p_bai = {'int': -1801.601, 'dbh':7.933, 'slenderness':13.574, 'dg': 5.043, 'G': -3.374,
                             'porcentajeG': -397.132, 'dummyF': -141.588}

                elif int(old_tree.specie) == TreeEquations.get_ifn_id('Csativa'):
                    p_bai = {'int': -2184.86, 'dbh':14.39,'slenderness': 31.36, 'hartB': -13.1, 'G': -20.32,
                             'BAL':-15.68, 'BALTotal': 22.04, 'height':-145.5, 'dummyF':257.74}



    def apply_hd_model(plot, new_tree):
        """
        Check the species combination of the plot and applies the correct height-diameter model.
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - plot: plot data needed to check the species codes
            - new_tree: is the information of the tree over the one we want to apply the growth model; data after projection
        """

        # get Martonne index to the corresponding year (period between before and after the projection)
        M = TreeEquations.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))  # TODO: list of years temporal

        # get species combis for mixed models
        mix_species_combis = MixedEquations.get_RPrado_2022_combis('simple')

        # get species combi of the plot
        plot_combi, plot_combi_reverse = MixedEquations.get_plot_combis(plot.id_sp1, plot.id_sp2)

        p_h = {}  # create an empty dictionary to store the parameters of the model

        # if the combination is in Rodríguez de Prado (2022)
        if plot_combi in mix_species_combis or plot_combi_reverse in mix_species_combis:

            # check species combination
            if plot_combi == '21_25' or plot_combi_reverse == '21_25':  # Psylvestris x Pnigra

                # check tree species
                if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                    p_h = {'model': 'M5', 'form': 'A', 'int': 0.8792, 'bal': -0.0068, 'dg': 0.0465,
                           'dgi': 0, 'mi': 0, 'm': 0, 'ho': 0,
                           'hoi': 0, 'beta0': 0, 'beta1': 0}

                elif int(new_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                    p_h = {'model': 'M1', 'form': 'A', 'int': 1.4454, 'bal': -0.0137, 'dg': 0.0474,
                           'dgi': 0, 'mi': 0, 'm': 0, 'ho': 0,
                           'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '24_25' or plot_combi_reverse == '24_25':  # Phalepensis x Pnigra

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                   p_h = {'model': 'M3', 'form': 'A', 'int': 0.8740, 'bal': -0.0097, 'dg': 0,
                          'dgi': -0.0092, 'mi': 0.1385, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': -5.6254}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0.9181, 'bal': -0.0168, 'dg': 0.0797,
                          'dgi': 0, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '24_26' or plot_combi_reverse == '24_26':  # Phalepensis x Ppinaster

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 1.213, 'bal': -0.0402, 'dg': 0,
                          'dgi': 0.0431, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': -0.0173, 'dg': 0.0734,
                          'dgi': 0, 'mi': 1.5235, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '23_24' or plot_combi_reverse == '23_24':  # Phalepensis x Ppinea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': -0.0125, 'dg': 0,
                          'dgi': 0.0390, 'mi': 1.2598, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                   p_h = {'model': 'M5', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0.0997, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '24_44' or plot_combi_reverse == '24_44':  # Phalepensis x Qfaginea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0.0294, 'mi': 1.0935, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2481, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 1.3855, 'beta0': 0, 'beta1': -4.2707}

            # check species combination
            elif plot_combi == '24_45' or plot_combi_reverse == '24_45':  # Phalepensis x Qilex

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 1.3583, 'bal': -0.0151, 'dg': 0,
                          'dgi': -0.02, 'mi': 1.4876, 'm': -0.0307, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2772, 'mi': -0.0425, 'm': 0.1651, 'ho': 0,
                          'hoi': 1.1925, 'beta0': 0, 'beta1': -6.0763}

            # check species combination
            elif plot_combi == '25_26' or plot_combi_reverse == '25_26':  # Pnigra x Ppinaster

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 1.0318, 'bal': -0.0112, 'dg': 0.0440,
                          'dgi': 0, 'mi': 0.6216, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 1.88, 'bal': -0.0183, 'dg': 0.0499,
                          'dgi': 0, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '25_44' or plot_combi_reverse == '25_44':  # Pnigra x Qfaginea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0.7447, 'bal': 0, 'dg': 0,
                          'dgi': -0.0319, 'mi': 2.1911, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.3677, 'mi': 0, 'm': 0.2853, 'ho': 0,
                          'hoi': 1.1564, 'beta0': 0, 'beta1': -7.0128}

            # check species combination
            elif plot_combi == '25_45' or plot_combi_reverse == '25_45':  # Pnigra x Qilex

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Pnigra'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': -0.0068, 'dg': 0,
                          'dgi': -0.0209, 'mi': 2.8952, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.3333, 'mi': 0, 'm': 0.1989, 'ho': 0,
                          'hoi': 1.2466, 'beta0': 0, 'beta1': -6.5164}

            # check species combination
            elif plot_combi == '26_23' or plot_combi_reverse == '26_23':  # Ppinaster x Ppinea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M1', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0.2314 ,'mi': 0.3722 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 4.0383 , 'bal': -0.0221, 'dg': 0,
                          'dgi': 0, 'mi': 1.5266, 'm': -0.1198, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '26_21' or plot_combi_reverse == '26_21':  # Ppinaster x Psylvestris

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 2.7801, 'bal': -0.0132, 'dg': -0.0203,
                          'dgi': 0 ,'mi': 0 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M3', 'form': 'A', 'int': 0.1674 , 'bal': 0, 'dg': 0,
                          'dgi': 0, 'mi': -0.0846, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 5.7848}

            # check species combination
            elif plot_combi == '26_45' or plot_combi_reverse == '26_45':  # Ppinaster x Qilex

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M1', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 2.8266 , 'm': 0.3382, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0 , 'bal': 0, 'dg': 0,
                          'dgi': -0.1802, 'mi': 0, 'm': 0.1547, 'ho': 0,
                          'hoi': 1.0835, 'beta0': 0, 'beta1': -5.9781}

            # check species combination
            elif plot_combi == '26_43' or plot_combi_reverse == '26_43':  # Ppinaster x Qpyrenaica

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': -0.0104, 'dg': 0,
                          'dgi': 0.0319 ,'mi': 1.6618 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0 , 'bal': -0.0368, 'dg': 0.1155,
                          'dgi': 0, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '26_46' or plot_combi_reverse == '26_46':  # Ppinaster x Qsuber

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):
                   p_h = {'model': 'M3', 'form': 'A', 'int': -0.6969, 'bal': 0, 'dg': 0,
                          'dgi': 0.0137 ,'mi': 0.1964 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 13.9493}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qsuber'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0 , 'bal': -0.0332, 'dg': 0,
                          'dgi': 0, 'mi': 2.6535, 'm': 0.0252, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '23_45' or plot_combi_reverse == '23_45':  # Ppinea x Qilex

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                   p_h = {'model': 'M3', 'form': 'A', 'int': 1.3421, 'bal': 0, 'dg': 0,
                          'dgi': -0.0162 ,'mi': 0 , 'm': -0.0079, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': -8.4247}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0 , 'bal': 0, 'dg': 0,
                          'dgi': -0.1910, 'mi': 0, 'm': 0.1413, 'ho': 0,
                          'hoi': 1.1488, 'beta0': 0, 'beta1': -6.6968}

            # check species combination
            elif plot_combi == '23_46' or plot_combi_reverse == '23_46':  # Ppinea x Qsuber

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Ppinea'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 2.1130, 'bal': -0.0258, 'dg': 0,
                          'dgi': -0.0460 ,'mi': 1.2023 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qsuber'):
                   p_h = {'model': 'M1', 'form': 'M', 'int': 0 , 'bal': 0, 'dg': 0,
                          'dgi': 0.3620, 'mi': 0.8264, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '21_71' or plot_combi_reverse == '21_71':  # Psylvestris x Fsylvatica

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M3', 'form': 'A', 'int': -0.1063, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 0 , 'm': 0.0037, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 7.1987}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0 , 'bal': -0.0049, 'dg': 0,
                          'dgi': 0.0243, 'mi': 0.6819, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '21_22' or plot_combi_reverse == '21_22':  # Psylvestris x Puncinata

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 0 , 'm': 0.0271, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Puncinata'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 0 , 'm': 0.0244, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '21_44' or plot_combi_reverse == '21_44':  # Psylvestris x Qfaginea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M5', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0.1286,'mi': 0.6005, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.3601, 'mi': 0, 'm': 0.3284, 'ho': 0,
                          'hoi': 1.0817, 'beta0': 0, 'beta1': -8.4275}

            # check species combination
            elif plot_combi == '21_45' or plot_combi_reverse == '21_45':  # Psylvestris x Qilex

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': -1.1988, 'bal': -0.0104, 'dg': 0,
                          'dgi': 0.0241 ,'mi': 1.6356 , 'm': 0.0178, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.3877 ,'mi': -0.0143 , 'm': 0.2363, 'ho': 0,
                          'hoi': 1.2026, 'beta0': 0, 'beta1': -6.3941}

            # check species combination
            elif plot_combi == '21_42' or plot_combi_reverse == '21_42':  # Psylvestris x Qpetraea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0, 'mi': 0, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 1.3877, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qpetraea'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.3962, 'mi': 0, 'm': 0.3045, 'ho': 0,
                          'hoi': 1.1671, 'beta0': 0, 'beta1': -9.1325}

            # check species combination
            elif plot_combi == '21_43' or plot_combi_reverse == '21_43':  # Psylvestris x Qpyrenaica

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):
                   p_h = {'model': 'M3', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 0 , 'm': 0.0038, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 4.3652}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': -0.0091, 'dg': 0,
                          'dgi': 0.0163 ,'mi': 1.2693 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '71_42' or plot_combi_reverse == '71_42':  # Fsylvatica x Qpetraea

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0.9408, 'bal': -0.0066, 'dg': 0.0184,
                          'dgi': 0 ,'mi': 0 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qpetraea'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2111 ,'mi': -0.0364 , 'm': 0.1916, 'ho': 0,
                          'hoi': 1.0490, 'beta0': 0, 'beta1': -7.3359}

            # check species combination
            elif plot_combi == '71_43' or plot_combi_reverse == '71_43':  # Fsylvatica x Qpyrenaica

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                   p_h = {'model': 'M1', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0.3293 ,'mi': 0.5965 , 'm': -0.2352, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                   p_h = {'model': 'M1', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0.1170,
                          'dgi': 0 ,'mi': 0 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '71_41' or plot_combi_reverse == '71_41':  # Fsylvatica x Qrobur

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': -0.1038,
                          'dgi': 0 ,'mi': -0.0509 , 'm': 0.1244, 'ho': 1.0300,
                          'hoi': 0, 'beta0': 0, 'beta1': -9.4827}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2329,'mi': 0 , 'm': 0.3245, 'ho': 0,
                          'hoi': 0.9650, 'beta0': 0, 'beta1': -11.7381}

            # check species combination
            elif plot_combi == '44_45' or plot_combi_reverse == '44_45':  # Qfaginea  x Qilex

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0.7578, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 0.8303 , 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 0, 'bal': -0.0282, 'dg': 0,
                          'dgi': 0 ,'mi': 1.1636 , 'm': 0.0407, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '45_43' or plot_combi_reverse == '45_43':  # Qilex x Qpyrenaica

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2510 ,'mi': 0 , 'm': 0, 'ho': 0,
                          'hoi': 1.4862, 'beta0': 0, 'beta1': -6.8655}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                   p_h = {'model': 'M5', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': 0 ,'mi': 1.4330, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '45_46' or plot_combi_reverse == '45_46':  # Qilex x Qsuber

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Qilex'):
                   p_h = {'model': 'M12', 'form': 'A', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2571 ,'mi': -0.0324 , 'm': 0.2214, 'ho': 0,
                          'hoi': 1.0963, 'beta0': 0, 'beta1': -7.2568}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qsuber'):
                   p_h = {'model': 'M1', 'form': 'A', 'int': 1.4835, 'bal': -0.0386, 'dg': 0.0578,
                          'dgi': 0 ,'mi': 0.8232, 'm': 0, 'ho': 0,
                          'hoi': 0, 'beta0': 0, 'beta1': 0}

            # check species combination
            elif plot_combi == '43_41' or plot_combi_reverse == '43_41':  # Qpyrenaica x Qrobur

               # check tree species
               if int(new_tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2799 ,'mi': 0 , 'm': 0.2404, 'ho': 0,
                          'hoi': 1.0418, 'beta0': 0, 'beta1': -7.7023}

               elif int(new_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
                   p_h = {'model': 'M12', 'form': 'M', 'int': 0, 'bal': 0, 'dg': 0,
                          'dgi': -0.2167,'mi': 0 , 'm': 0.1838, 'ho': 0,
                          'hoi': 1.0630, 'beta0': 0, 'beta1': -8.1876}

            else:  # other mixtures

                p_h = {}

        else: # if species are not in Rodríguez de Prado (2022)

            # TODO: desviar el cálculo de la altura a función aparte para cada especie y comprobar que funciona
            p_h = {}


        # initialize height
        height = 0

        # if species is in Rodríguez de Prado (2022)
        if len(p_h) != 0:

            # get beta0 value
            beta0 = MixedEquations.hd_model_form(p_h, plot, new_tree, M)

            # TODO: comprobar esto
            # for one species beta0 value is provided
            if (plot_combi == "21_42" or plot_combi_reverse == "21_42") and new_tree.specie == TreeEquations.get_ifn_id('Psylvestris'):

                beta0 = p_h['beta0']

            # equation selection for each species and species combination
            # Note: models not used were not programmed
            if p_h['model'] == 'M1':

                # h-d equation M1: Cañadas et al. (1999) in Rodríguez de Prado (2022)
                if beta0 == '':
                    height = new_tree.height
                else:
                    height = 1.3 + (beta0 * (1 / new_tree.dbh - 1 / plot.dominant_dbh) + ((1 / (plot.dominant_h - 1.3))
                         ** 0.5)) ** (-2)

            elif p_h['model'] == 'M3':

                # h-d equation M3: Gaffrey (1988) modified by Diéguez et al. (2005) in Rodríguez de Prado (2022)
                if beta0 == '':
                    height = new_tree.height
                else:
                    height = 1.3 + (plot.dominant_h - 1.3) * math.exp(beta0 * (1 - plot.dominant_dbh / new_tree.dbh) +
                             p_h['beta1'] * (1 / plot.dominant_dbh - 1 / new_tree.dbh))

            elif p_h['model'] == 'M5':

                # h-d equation M5: Monnes (1982) in Rodríguez de Prado (2022)
                if beta0 == '':
                    height = new_tree.height
                else:
                    height = 1.3 + (beta0 * (1 / new_tree.dbh - 1 / plot.dominant_dbh) + ((1 / (plot.dominant_h - 1.3)) **
                         (1 / 3))) ** (-3)

            elif p_h['model'] == 'M12':

                # h-d equation M12: Schumacher (1939) in Rodríguez de Prado (2022)
                if beta0 == '':
                    height = new_tree.height
                else:
                    height = 1.3 + beta0 * math.exp(p_h['beta1'] / new_tree.dbh)

        return height


    def hd_model_form(p_h, plot, new_tree, M):
        """
        Support function to the applu_hd_model function. It returns the beta0 value for the h-d equation.
        :param plot: plot information
        :param new_tree: tree information
        :param M: Martonne Aridity Index
        :return: beta0 value used on the h-d equation
        """

        # beta0 for equation with form A
        if p_h['form'] == 'A':

            # species condition needed to assign the correct species proportion by area
            if int(new_tree.specie) == int(plot.id_sp1):
                beta0 = p_h['int'] + p_h['bal'] * new_tree.bal + p_h['dg'] * plot.qm_dbh + p_h['mi'] * \
                        plot.sp1_proportion + p_h['m'] * M + p_h['ho'] * plot.dominant_h

            elif int(new_tree.specie) == int(plot.id_sp2):
                beta0 = p_h['int'] + p_h['bal'] * new_tree.bal + p_h['dg'] * plot.qm_dbh + p_h['mi'] * \
                        plot.sp2_proportion + p_h['m'] * M + p_h['ho'] * plot.dominant_h

            else:
                beta0 = ''

        # beta0 for equation with form M
        elif p_h['form'] == 'M':

            # species condition needed to assign the correct species proportion by area
            if int(new_tree.specie) == int(plot.id_sp1):

                # avoid mistakes when multiplying
                if p_h['int'] == 0:
                    p_h['int'] = 1

                beta0 = p_h['int'] * (new_tree.bal ** p_h['bal']) * (plot.qm_dbh ** p_h['dg']) * \
                        (plot.sp1_proportion ** p_h['mi']) * (M ** p_h['m']) * (plot.dominant_h ** p_h['ho'])

            elif int(new_tree.specie) == int(plot.id_sp2):

                # avoid mistakes when multiplying
                if p_h['int'] == 0:
                    p_h['int'] = 1

                beta0 = p_h['int'] * (new_tree.bal ** p_h['bal']) * (plot.qm_dbh ** p_h['dg']) * \
                        (plot.sp2_proportion ** p_h['mi']) * (M ** p_h['m']) * (plot.dominant_h ** p_h['ho'])

            else:
                beta0 = ''

        # other situations
        else:
            beta0 = ''

        return beta0


    def apply_ingrowth_model(time, plot):
        """
        Check the species combination of the plot and applies the correct ingrowth model.
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - time: projection time. It must be the time needed for the projection
            - plot: plot data needed to check the species codes
        """

        # TODO: *irene* escribe aquí tus ecuaciones con filtro de especie y la repartición de clase diamétrica, déjalo silenciado
        # TODO: hacer para la combinación de Irene, el resto 0

        # elif plot_combi == '41_72' or plot_combi_reverse == '41_72':  # Qrobur x Csativa
            # if int(old_tree.specie) == TreeEquations.get_ifn_id('Qrobur'):
            #   sup = {'int':6.4658594,'G':-0.0085081,'N':0.0001891,
            #          'porcentageG':0.363919,'porcentageN':-0.3712658,
            #          'Dg':-0.0334438,'Ho':-0.0205513,'Ho41':0.0532834,
            #          'HartB41':-0.0027}
            # elif int(old_tree.specie) == TreeEquations.get_ifn_id('Csativa'):
            #   sup = {'int':9.913005,'G':-0.026818,'porcentageG':-0.237277,
            #          'porcentageN':-0.160921,'Dg':-0.0551673,'Ho':-0.069319,
            #          'HartB':-0.006262,'Ho72':-0.068032,'HartB72':-0.014343}


        return 0


    def apply_ingrowth_distribution(time, plot, area):
        """
        Check the species combination of the plot and applies the correct ingrowth model.
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - time: projection time. It must be the time needed for the projection
            - plot: plot data needed to check the species
            - area: ingrowth previously calculated in terms of stand basal area (m2/ha)
        """

        # TODO: hacer para la combinación de Irene, el resto []

        if area > 0:

            distribution = []

        else:

            distribution = None

        return distribution


    def choose_SDI_function(plot):
        """
        Function that returns the Stand Density Index (normal and maximum based on climate conditions) for species
        mixtures corresponding to the plot.
        Depending on data available, it uses the 'basic' function (without climate data) or the 'climatic' function.
        Args.:
            - plot: plot data needed to check the species, get data and update it
        Refs.:
            - Rodríguez de Prado, D. (2022). New insights in the modeling and simulation of tree and stand level
            variables in Mediterranean mixed forests in the present context of climate change. Doctoral dissertation.
        """

        # it uses basic functions by default, but if in any moment the climatic functions are implemented, then that

        # get SDI, SDImax and species proportions by area
        MixedEquations.set_SDIs_mixed_plots_basic(plot)

        # best model programmed but climatic variables not included
        # MixedEquations.set_SDIs_mixed_plots_climatic(plot)


    def set_SDIs_mixed_plots_basic(plot):
        """
        Function that returns the Stand Density Index (normal and maximum based on climate conditions) for species
        mixtures corresponding to the plot. In addition, the proportion of both species based on area is calculated,
        according Rodríguez de Prado (2022).
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - plot: plot data needed to check the species, get data and update it
        Refs.:
            - Rodríguez de Prado, D. (2022). New insights in the modeling and simulation of tree and stand level
            variables in Mediterranean mixed forests in the present context of climate change. Doctoral dissertation.
        """

        # get parameters for each species
        params1 = MixedEquations.SDI_params_basic(plot.id_sp1)
        params2 = MixedEquations.SDI_params_basic(plot.id_sp2)

        # using the previous parameters for each species, SDImax is calculated
        if len(params1) != 0:

            plot.add_value('REINEKE_MAX_SP1', math.exp(params1['alpha0'] + params1['beta0'] * math.log(25)))

            if plot.qm_dbh_sp1 != 0:  # skip ZeroDivision Error
                plot.add_value('REINEKE_SP1', math.exp(params1['alpha0'] + params1['beta0'] * math.log(plot.qm_dbh_sp1)))

        if len(params2) != 0:

            plot.add_value('REINEKE_MAX_SP2', math.exp(params2['alpha0'] + params2['beta0'] * math.log(25)))

            if plot.qm_dbh_sp2 != 0:  # skip ZeroDivision Error
                plot.add_value('REINEKE_SP2',
                               math.exp(params2['alpha0'] + params2['beta0'] * math.log(plot.qm_dbh_sp2)))

        # get species proportion based on area (Rodriguez de Prado, 2022)
        if len(params1) != 0 and len(params2) != 0:

            if plot.qm_dbh_sp1 != 0 and plot.qm_dbh_sp2 != 0:

                plot.add_value('SP1_PROPORTION', plot.reineke_sp1 / (plot.reineke_sp1 + plot.reineke_sp2))
                plot.add_value('SP2_PROPORTION', plot.reineke_sp2 / (plot.reineke_sp1 + plot.reineke_sp2))


    def SDI_params_basic(species):
        """
        Function that returns the parameters for the Stand Density Index using the basic model (without climate data).
        Parameters are selected by species.
        Args.:
            - species: species code to request parameters
        """

        # get parameters for each species
        if species == TreeEquations.get_ifn_id('Psylvestris'):
            params = {'alpha0': 12.685, 'alpha1': 0, 'beta0': -1.7524, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Puncinata'):
            params = {'alpha0': 12.519, 'alpha1': 0, 'beta0': -1.7336, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Pnigra'):
            params = {'alpha0': 12.756, 'alpha1': 0, 'beta0': -1.8346, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Pcanariensis'):
            params = {'alpha0': 12.672, 'alpha1': 0, 'beta0': -1.8226, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Phalepensis'):
            params = {'alpha0': 11.982, 'alpha1': 0, 'beta0': -1.7760, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Ppinaster'):
            params = {'alpha0': 13.096, 'alpha1': 0, 'beta0': -1.9063, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Ppinea'):
            params = {'alpha0': 13.562, 'alpha1': 0, 'beta0': -2.1855, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Pradiata'):
            params = {'alpha0': 12.947, 'alpha1': 0, 'beta0': -1.8254, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Fsylvatica'):
            params = {'alpha0': 13.170, 'alpha1': 0, 'beta0': -1.9471, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Qfaginea'):
            params = {'alpha0': 12.097, 'alpha1': 0, 'beta0': -1.7055, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Qilex'):
            params = {'alpha0': 12.508, 'alpha1': 0, 'beta0': -2.0951, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Qpetraea'):
            params = {'alpha0': 12.277, 'alpha1': 0, 'beta0': -1.6777, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Qpyrenaica'):
            params = {'alpha0': 12.271, 'alpha1': 0, 'beta0': -1.7203, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Qrobur'):
            params = {'alpha0': 12.043, 'alpha1': 0, 'beta0': -1.6698, 'beta1': 0}
        elif species == TreeEquations.get_ifn_id('Qsuber'):
            params = {'alpha0': 12.704, 'alpha1': 0, 'beta0': -1.9674, 'beta1': 0}
        else:  # if no parameters available for the species
            params = {}

        return params


    def set_SDIs_mixed_plots_clim(plot, M):
        """
        Function that returns the Stand Density Index (normal and maximum based on climate conditions) for species
        mixtures corresponding to the plot. In addition, the proportion of both species based on area is calculated,
        according Rodríguez de Prado (2022).
        It includes/rewrite the result on the corresponding tree or stand variable.
        Args.:
            - plot: plot data needed to check the species, get data and update it
            - M: Martonne aridity index previously selected by other function. Must be available at the inventory
        Refs.:
            - Rodríguez de Prado, D. (2022). New insights in the modeling and simulation of tree and stand level
            variables in Mediterranean mixed forests in the present context of climate change. Doctoral dissertation.
        """

        # get parameters for each species
        params1, var = MixedEquations.SDI_params_clim(plot.id_sp1)
        params2, var = MixedEquations.SDI_params_clim(plot.id_sp2)

        # get Clim value according to the var obtained in the previous function
        # Clim = var

        # using the previous parameters for each species, SDImax is calculated
        if len(params1) != 0:

            plot.add_value('REINEKE_MAX_SP1', math.exp((params1['alpha0'] + params1['alpha1'] * math.log(Clim)) +
                                                   ((params1['beta0'] - params1['beta1'] * Clim) * math.log(25))))

            if plot.qm_dbh_sp1 != 0:  # skip ZeroDivision Error
                plot.add_value('REINEKE_SP1', plot.density_sp1 * ((25 / plot.qm_dbh_sp1) **
                                                                  (params1['beta0'] - params1['beta1'] * Clim)))

            if len(params2) != 0:

                plot.add_value('REINEKE_MAX_SP2', math.exp((params2['alpha0'] + params2['alpha1'] * math.log(Clim)) +
                                                   ((params2['beta0'] - params2['beta1'] * Clim) * math.log(25))))

            if plot.qm_dbh_sp2 != 0:  # skip ZeroDivision Error
                plot.add_value('REINEKE_SP2', plot.density_sp2 * ((25 / plot.qm_dbh_sp2) **
                                                                  (params2['beta0'] - params2['beta1'] * Clim)))

        # get species proportion based on area (Rodriguez de Prado, 2022)
        if len(params1) != 0 or len(params2) != 0:

            if plot.qm_dbh_sp1 != 0 and plot.qm_dbh_sp2 != 0:

                plot.add_value('SP1_PROPORTION', plot.reineke_sp1 / (plot.reineke_sp1 + plot.reineke_sp2))
                plot.add_value('SP2_PROPORTION', plot.reineke_sp2 / (plot.reineke_sp1 + plot.reineke_sp2))


    def SDI_params_clim(species):
        """
        Function that returns the parameters for the Stand Density Index using the climatic model.
        Parameters are selected by species.
        Args.:
            - species: species code to request parameters
        """

        # get parameters for each species
        if species == TreeEquations.get_ifn_id('Psylvestris'):
            params = {'alpha0': 66.470, 'alpha1': -9.442, 'beta0': -1.7478, 'beta1': 0}
            var = 'TAR'
        elif species == TreeEquations.get_ifn_id('Puncinata'):
            params = {'alpha0': 12.918, 'alpha1': 0, 'beta0': -1.6378, 'beta1': -0.0031}
            var = 'PET3'
        elif species == TreeEquations.get_ifn_id('Pnigra'):
            params = {'alpha0': 140.953, 'alpha1': -22.536, 'beta0': -1.9324, 'beta1': 0}
            var = 'MXT3'
        elif species == TreeEquations.get_ifn_id('Pcanariensis'):
            params = {'alpha0': 3.639, 'alpha1': 2.448, 'beta0': -2.0891, 'beta1': 0}
            var = 'P1'
        elif species == TreeEquations.get_ifn_id('Phalepensis'):
            params = {'alpha0': 9.241, 'alpha1': 0.886, 'beta0': -1.5559, 'beta1': -0.0095}
            var = 'M'
        elif species == TreeEquations.get_ifn_id('Ppinaster'):
            params = {'alpha0': 13.446, 'alpha1': 0, 'beta0': 4.1770, 'beta1': -0.0213}
            var = 'MXT'
        elif species == TreeEquations.get_ifn_id('Ppinea'):
            params = {'alpha0': 15.072, 'alpha1': -0.460, 'beta0': -2.4379, 'beta1': 0.0093}
            var = 'P4'
        elif species == TreeEquations.get_ifn_id('Pradiata'):
            params = {'alpha0': 110.968, 'alpha1': -21.507, 'beta0': -8.0490, 'beta1': 0.0652}
            var = 'PET3'
        elif species == TreeEquations.get_ifn_id('Fsylvatica'):
            params = {'alpha0': 12.870, 'alpha1': 0, 'beta0': 2.0880, 'beta1': -0.0137}
            var = 'MXT3'
        elif species == TreeEquations.get_ifn_id('Qfaginea'):
            params = {'alpha0': 247.037, 'alpha1': -41.233, 'beta0': -1.7874, 'beta1': 0}
            var = 'MXTWM'
        elif species == TreeEquations.get_ifn_id('Qilex'):
            params = {'alpha0': 11.777, 'alpha1': 0, 'beta0': -1.3094, 'beta1': -0.0044}
            var = 'PET3'
        elif species == TreeEquations.get_ifn_id('Qpetraea'):
            params = {'alpha0': -489.861, 'alpha1': 88.759, 'beta0': 36.5003, 'beta1': -0.1334}
            var = 'MXT'
        elif species == TreeEquations.get_ifn_id('Qpyrenaica'):
            params = {'alpha0': -187.581, 'alpha1': 35.255, 'beta0': 17.946, 'beta1': -0.0679}
            var = 'T4'
        elif species == TreeEquations.get_ifn_id('Qrobur'):
            params = {'alpha0': -795.789, 'alpha1': 143.317, 'beta0': 49.1578, 'beta1': -0.1812}
            var = 'MNT3'
        elif species == TreeEquations.get_ifn_id('Qsuber'):
            params = {'alpha0': 11.948, 'alpha1': 0, 'beta0': -1.2349, 'beta1': -0.0043}
            var = 'PET3'
        else:  # if no parameters available for the species
            params = {}

        return params, var