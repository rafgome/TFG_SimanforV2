#!/usr/bin/env python3
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

from models import TreeModel
from data import Distribution
from data import DESC
from data import Plot
from data import Tree
from data.general import Area, Model, Warnings
from scipy import integrate
from util import Tools
from data.variables import TREE_VARS, PLOT_VARS, AREA_VARS, MODEL_VARS, WARNING_VARS
from data.variables import Variables

import math
import sys
import logging
import numpy as np
import os

# Basic Tree Model model (Spain), version 01
# Written by iuFOR
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (dbhiversity of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, dbhiversity of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/


class BasicTreeModel(TreeModel):

    def __init__(self, configuration=None):
        super().__init__(name="BasicTreeModel", version=1)


    def catch_model_exception(self):  # that Function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def model_info(self):
        """
        Function to set the model information at the at the output.
        It will be runned by initialize function once.
        """

        try:  # errors inside that construction will be annodbhced
        
            Model.model_name = 'tree_template'  # set the model name to show it at the output
            Model.specie_ifn_id = 999  # Set the model specie ID to mark the trees of different species         
            Model.exec_time = 5  # recommended executions time to use that model
            Model.aplication_area = 'none'  # area reccomended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = 'example'  # provenance regions reccomended to use the model
            Model.model_type = 'under_development'  # SIMANFOR model type. It can be: '' are neccesary
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'link'  # link to model card in english
            Model.model_card_es = 'link'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def initialize(self, plot: Plot):
        """
        Function that update the gaps of information at the initial inventory
        Source:
            Doc.:
            Ref.:
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                        Running: BasicTreeModel model (xx). Plot:', plot.plot_id                     )
        print('#--------------------------------------------------------------------------------------------------#')

        try:  # errors inside that construction will be annodbhced

            self.model_info()
            plot.add_value('REINEKE_VALUE', -1.605)  # r contstant value of SDI  to the specie of the model (-1.605 as default)
            other_trees = total_trees = 0  # variables to count the number of trees from a different specie that the principal one and the total of trees

            #-----------------------------------SI-----------------------------------------#

            if plot.si == 0 or plot.si == '':
                t2 =   # age to estimate the SI and Dominant_diamter (years)
                plot.add_value('REF_SI_AGE', t2)  
                SI = 
                plot.add_value('SI', SI)  # Site Index (m) calculation

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables
            bal: float = 0

            for tree in plot_trees:  # for each tree...

                total_trees += 1

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    #-----------------------------------BASAL AREA-----------------------------------------#

                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                    tree.add_value('basal_area', math.pi*(tree.dbh/2)**2)  # normal (at 1.30m) section (cm2) calculation
                    tree.add_value('ba_ha', tree.basal_area*tree.expan/10000)  # basimetric area per ha (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is acumulated

                    #-----------------------------------HEIGHT-----------------------------------------#

                    if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                        tree.add_value('height', )

                    #------------------------------SLENDERNESS__N_CIRC-----------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%) calculation
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal (at 1.30m) circumference (cm) calculation

                    #-----------------------------------TREE FUNCTIONS-----------------------------------------#

                    self.crown(tree, plot, 'initialize')  # activate crown variables calculation

                    self.vol(tree, plot)  # activate volume variables calculation

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    self.merchantable(tree)  # activate wood uses variables calculation

                    self.biomass(tree)  # activate biomass variables calculation
                
                else:
                    other_trees += 1
    
            if other_trees != 0:
                print(' ')
                print(other_trees, 'of the total', total_trees, 'trees are from a different specie than the principal')
                print('That trees will be shown underlined at the output, and they will be maintained at simulations, not applying model equations over them.')
                print(' ')
                if other_trees == total_trees:
                    Warnings.specie_error_trees = 1

    
            self.vol_plot(plot, plot_trees)  # activate volume variables (plot) calculation

            self.canopy(plot, plot_trees)  # activate crown variables (plot) calculation

            self.merchantable_plot(plot, plot_trees)  # activate wood uses (plot) variables calculation

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables calculation  

            plot.add_value('DEAD_DENSITY', 0)  # change the value from '' to 0 in orde to print that information at the summary sheet
            plot.add_value('ING_DENSITY', 0)  # change the value from '' to 0 in orde to print that information at the summary sheet

        except Exception:
            self.catch_model_exception()


    def survival(self, time: int, plot: Plot, tree: Tree):
        """
        Tree survival/mortality function. 
        That function modifies the expan of the tree at the executions.
        Dead trees will be shown at the output with a "M" at the "status" column, with the "expan" value corresponding to the dead part.
        """

        if tree.specie == Model.specie_ifn_id:  # specie condition
            return 1
        else:
            return 1


    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Tree growth function.
        Function that update dbh and h by using growth equations, and also update age, g and v to the new situation
        """

        try:  # errors inside that construction will be annodbhced

            if old_tree.specie == Model.specie_ifn_id:  # specie condition

                new_tree.sum_value('tree_age', time)
            
                new_tree.sum_value("dbh", 0)

                new_tree.sum_value("height", 0)

                new_tree.add_value('basal_area', math.pi*(new_tree.dbh/2)**2)  # update basal area (cm2) 

                self.vol(new_tree, plot)  # update volume variables (dm3)

        except Exception:
            self.catch_model_exception()


    def ingrowth(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated are calculated. The next function will order how to divide that basal area on the different diametric classes.
        """

        try:  # errors inside that construction will be annodbhced

        except Exception:
            self.catch_model_exception()

        return 0


    def ingrowth_distribution(self, time: int, plot: Plot, area: float):
        """
        Tree diametric classes distribution.
        That function must return a list with different sublists for each diametric class, where the conditions to ingrowth function are written.
        That function has the aim to divide the ingrowth (added basal area of ingrowth function) in different proportions depending on the orders given.
        On the cases that a model hasn´t a good known distribution, just return None to share that ingrowth between all the trees of the plot.
        """

        try:  # errors inside that construction will be annodbhced

            distribution = []  # that list will contain the different diametric classes conditions to calculate the ingrowth distribution

            # for each diametric class: [dbh minimum, dbh maximum, proportion of basal area to add (between 0*area and 1*area)]
            # if your first diametric class doesn't start on 0, just create a cd_0 with the diametric range betwwen 0 and minimum of cd_1 without adding values
            # example: cd_0 = [0, 7.5, 0]  
            #          distribution.append(cd_0)
            # moreover, if your diametric distribution doesn't take into account the bigger tree dbh, just create another empty distribution
            # example: cd_x = [12.5, 100, 0]
            #          distribution.append(cd_x)

            # by doing this, you avoid possible errors at the simulator; if not, it's possible that an error will be found

        except Exception:
            self.catch_model_exception()

        return None


    def update_model(self, time: int, plot: Plot, trees: list):
        """
        Function that update trees and plot information once growth, survive and ingrowth functions was executed and the plot information was updated.
        The equations on that function are the same that in "initialize" function, so references are the same
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                        Running: BasicTreeModel model (xx). Plot:', plot.plot_id                     )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same of the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:  # errors inside that construction will be annodbhced

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # stablish an order to calculate tree variables
            bal: float = 0.0

            if 'YEAR' in PLOT_VARS:
                new_year = plot.year + time  # YEAR is automatically updated after the execution process
            if 'AGE' in PLOT_VARS:
                new_age = plot.age + time  # AGE is automatically updated after the execution process

            for tree in plot_trees:  # for each tree...

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    #-----------------------------------BASAL AREA-----------------------------------------#

                    tree.add_value('basal_area', math.pi*(tree.dbh/2)**2)  # normal (at 1.30m) section (cm2) calculation
                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                    tree.add_value('ba_ha', tree.basal_area*tree.expan/10000)  # basimetric area per ha (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is acumulated
                    
                    #------------------------------SLENDERNESS__N_CIRC-----------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%) calculation
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal (at 1.30m) circumference (cm) calculation

                    #-----------------------------------VOL_HA-----------------------------------------#

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    #-----------------------------------TREE FUNCTIONS-----------------------------------------#

                    self.crown(tree, plot, 'update_model')  # activate crown variables calculation
                    
                    self.merchantable(tree)  # activate wood uses variables calculation

                    self.biomass(tree)  # activate biomass variables calculation

            #-----------------------------------PLOT FUNCTIONS-----------------------------------------#

            self.vol_plot(plot, plot_trees)  # activate volume variables (plot) calculation

            self.canopy(plot, plot_trees)  # activate crown variables (plot) calculation

            self.merchantable_plot(plot, plot_trees)  # activate wood uses (plot) variables calculation

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables calculation 

        except Exception:
            self.catch_model_exception()


    def taper_over_bark(self, tree: Tree, hr: float):
        """
        Taper equation over bark function.
        Function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        """

        try:  # errors inside that construction will be annodbhced

        except Exception:
            self.catch_model_exception()


    def taper_under_bark(self, tree: Tree, hr: float):
        """
        Taper equation under bark function.
        Function that returns the taper equation to calculate the diameter (cm, under bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        """

        try:  # errors inside that construction will be annodbhced

        except Exception:
            self.catch_model_exception()


    def merchantable(self, tree: Tree):
        """
        Merchantable wood calculation (tree).
        Function needed to calcule the different comercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions, and is linked to taper_over_bark, indispensable function.
        That function is run by initialize and update_model functions.
        Data criteria to clasify the wood by different uses was obtained from:
        """
        
        try:  # errors inside that construction will be annodbhced

            ht = tree.height  # total height as ht to simplify
            # class_conditions has different lists for each usage, following that: [wood_usage, hmin/ht, dmin, dmax]
            # [WOOD USE NAME , LOG RELATIVE LENGTH RESPECT TOTAL TREE HEIGHT, MINIMUM DIAMETER, MAXIMUM DIAMETER]
            class_conditions = [] 

            # usage and merch_list are a dictionary and a list that are returned from merch_calculation
            # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
            usage, merch_list = TreeModel.merch_calculation(tree, class_conditions, BasicTreeModel)

            counter = -1
            for k,i in usage.items():
                counter += 1
                tree.add_value(k, merch_list[counter])  # add merch_list values to each usage

        except Exception:
            self.catch_model_exception()


    def merchantable_plot(self, plot: Plot, plot_trees):
        """
        Merchantable wood calculation (plot).
        Function needed to calcule the different comercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions, and uses the data obtained from trees.
        """

        try:  # errors inside that construction will be annodbhced

            plot_unwinding = plot_veneer = plot_saw_big = plot_saw_small = plot_saw_canter = plot_post = plot_stake = plot_chips =  0

            # for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                # if tree.specie == Model.specie_ifn_id:  # specie condition

                    # plot_unwinding += tree.unwinding*tree.expan
                    # plot_veneer += tree.veneer*tree.expan
                    # plot_saw_big += tree.saw_big*tree.expan
                    # plot_saw_small += tree.saw_small*tree.expan
                    # plot_saw_canter += tree.saw_canter*tree.expan
                    # plot_post += tree.post*tree.expan
                    # plot_stake += tree.stake*tree.expan
                    # plot_chips += tree.chips*tree.expan

            # plot.add_value('UNWINDING', plot_unwinding/1000)  # now, we add the plot value to each variable, changing the unit to m3/ha
            # plot.add_value('VENEER', plot_veneer/1000)
            # plot.add_value('SAW_BIG', plot_saw_big/1000)
            # plot.add_value('SAW_SMALL', plot_saw_small/1000)
            # plot.add_value('SAW_CANTER', plot_saw_canter/1000)
            # plot.add_value('POST', plot_post/1000)
            # plot.add_value('STAKE', plot_stake/1000)
            # plot.add_value('CHIPS', plot_chips/1000)

        except Exception:
            self.catch_model_exception()


    def crown(self, tree: Tree, plot: Plot, func):
        """
        Crown variables (tree).
        Function to calculate crown variables for each tree.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be annodbhced

            # if func == 'initialize':  # if that function is called from initilize, first we must check if that variables are available on the initial inventory

        except Exception:
            self.catch_model_exception()


    def canopy(self, plot: Plot, plot_trees):
        """
        Crown variables (plot).
        Function to calculate plot crown variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            #plot_expan = plot_lcw = plot_lcw2 = plot_fcc = 0

            #for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                #if tree.specie == Model.specie_ifn_id:  # specie condition

                    #plot_expan += tree.expan
                    #plot_lcw += tree.lcw*tree.expan
                    #plot_lcw2 += math.pow(tree.lcw, 2)*tree.expan
                    #plot_fcc += math.pi*(math.pow(tree.lcw, 2)/4)*tree.expan

            #plot.add_value('CROWN_MEAN_D', plot_lcw/plot_expan)
            #plot.add_value('CROWN_DOM_D', math.sqrt(plot_lcw2/plot_expan))
            #plot.add_value('CANOPY_COVER', plot_fcc/10000)

        except Exception:
            self.catch_model_exception()


    def vol(self, tree: Tree, plot: Plot):
        """
        Volume variables (tree).
        Function to calculate volume variables for each tree.
        That function is run by initialize and growth functions, and uses taper equations to calculate the values.
        """

        try:  # errors inside that construction will be annodbhced

            hr = np.arange(0, 1, 0.001)  # that line stablish the integrate conditions for volume calculation
            # dob = self.taper_over_bark(tree, hr)  # diameter over bark using taper equation (cm)
            # dub = self.taper_under_bark(tree, hr)  # diameter under/without bark using taper equation (cm)
            # fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
            # fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
            # tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
            # tree.add_value('bole_vol', math.pi * tree.height * 10 * integrate.simps(fub, hr))  # volume under bark using simpson integration (dm3)
            # tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)

        except Exception:
            self.catch_model_exception()


    def vol_plot(self, plot: Plot, plot_trees):
        """
        Volume variables (plot).
        Function to calculate plot volume variables by using tree information.
        That function is run by initialize and preocess_plot functions.
        """

        try:  # errors inside that construction will be annodbhced

            plot_vol = plot_bole_vol = plot_bark = 0

            #for tree in plot_trees:

                #if tree.specie == Model.specie_ifn_id:  # specie condition

                    #plot_vol += tree.expan*tree.vol
                    #plot_bole_vol += tree.expan*tree.bole_vol
            #plot_bark = plot_vol - plot_bole_vol

            #plot.add_value('VOL', plot_vol/1000)  # plot volume over bark (m3/ha)
            #plot.add_value('BOLE_VOL', plot_bole_vol/1000)  # plot volume under bark (m3/ha)
            #plot.add_value('BARK_VOL', plot_bark/1000)  # plot bark volume (m3/ha)

        except Exception:
            self.catch_model_exception()


    def biomass(self, tree: Tree):
        """
        Biomass variables (tree).
        Function to calculate biomass variables for each tree.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be annodbhced

            # tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
            # tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
            # tree.add_value('w_cork', w_cork)   # w_cork = fresh cork biomass (kg)
            # tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
            # tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches >7 cm (kg)
            # tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
            # tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches >2 cm (kg)
            # tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
            # tree.add_value('wb05', wb05)  # wb05 = thinniest branches (<0.5 cm) (kg)
            # tree.add_value('wl', wl)  # wl = leaves (kg)
            # tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches <2 cm and leaves (kg)
            # tree.add_value('wbl0_7', wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (kg)
            # tree.add_value('wr', wr)  # wr = roots (kg)
            # tree.add_value('wt', wt)  # wt = biomasa total (kg)

        except Exception:
            self.catch_model_exception()


    def biomass_plot(self, plot: Plot, plot_trees):
        """
        Biomass variables (plot).
        Function to calculate plot biomass variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be annodbhced

            plot_wsw = plot_wsb = plot_w_cork = plot_wthickb = plot_wstb = plot_wb2_7 = plot_wb2_t = plot_wthinb = plot_wb05 = plot_wl = plot_wtbl = plot_wbl0_7 = plot_wr = plot_wt =  0

            # for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                # if tree.specie == Model.specie_ifn_id:  # specie condition

                    # plot_wsw += tree.wsw*tree.expan
                    # plot_wsb += tree.wsb*tree.expan
                    # plot_w_cork += tree.w_cork*tree.expan
                    # plot_wthickb += tree.wthickb*tree.expan
                    # plot_wstb += tree.wstb*tree.expan
                    # plot_wb2_7 += tree.wb2_7*tree.expan
                    # plot_wb2_t += tree.wb2_t*tree.expan
                    # plot_wthinb += tree.wthinb*tree.expan
                    # plot_wb05 += tree.wb05*tree.expan
                    # plot_wl += tree.wl*tree.expan
                    # plot_wtbl += tree.wtbl*tree.expan
                    # plot_wbl0_7 += tree.wbl0_7*tree.expan
                    # plot_wr += tree.wr*tree.expan
                    # plot_wt += tree.wt*tree.expan

            # plot.add_value('WSW', plot_wsw/1000)  # Wsw  # wsw = stem wood (Tn/ha)
            # plot.add_value('WSB', plot_wsb/1000)  # Wsb  # wsb = stem bark (Tn/ha)
            # plot.add_value('W_CORK', plot_w_cork/1000)  # W Fresh Cork  # w_cork = fresh cork biomass (Tn/ha)
            # plot.add_value('WTHICKB', plot_wthickb/1000)  # Wthickb  # wthickb = Thick branches > 7 cm (Tn/ha)
            # plot.add_value('WSTB', plot_wstb/1000)  # Wstb  # wstb = wsw + wthickb, stem + branches >7 cm (Tn/ha)
            # plot.add_value('WB2_7', plot_wb2_7/1000)  # Wb2_7  # wb2_7 = branches (2-7 cm) (Tn/ha)
            # plot.add_value('WB2_T', plot_wb2_t/1000)  # Wb2_t  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn/ha)
            # plot.add_value('WTHINB', plot_wthinb/1000)  # Wthinb  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            # plot.add_value('WB05', plot_wb05/1000)  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            # plot.add_value('WL', plot_wl/1000)  # Wl  # wl = leaves (Tn/ha)
            # plot.add_value('WTBL', plot_wtbl/1000)  # Wtbl  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn/ha)
            # plot.add_value('WBL0_7', plot_wbl0_7/1000)  # Wbl0_7  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Tn/ha)
            # plot.add_value('WR', plot_wr/1000)  # Wr  # wr = roots (Tn/ha)
            # plot.add_value('WT', plot_wt/1000)  # Wt  # wt = biomasa total (Tn/ha)

        except Exception:
            self.catch_model_exception()


    def vars():
        """
        Control variables function.
        The aim of this function is to desactivate variables that are not calculated at the model and we don't want to show them at the output.
        It has the posibility to work over tree and plot variables.
        """
        
        #########################################################################################################################
        ############################################  PLOT variables ############################################################
        #########################################################################################################################


        # list of plot variables on the simulator that can be deleted without make errors
        # to delete them, just leave it at the list; to NOT delete them, comment it at the list or remove it from them

        delete_from_plot = [  

            'ID_SP1',  # IFN (Spanish National Forestal Inventory) ID specie 1 - mixed models
            'ID_SP2',  # IFN (Spanish National Forestal Inventory) ID specie 2 - mixed models

            # Basic plot variables measured
            "EXPAN",  # Expan  # expansion factor
            #'YEAR',  # year of the inventory
            #"AGE",  # Age  # (years)
            "SP1_PROPORTION",  # proportion of specie 1 on a mix plot - mixed models
            "SP2_PROPORTION",  # proportion of specie 2 on a mix plot - mixed models
            #"DENSITY",  # Density  # (nº trees/ha)
            "DENSITY_SP1",  # density of specie 1 on a mix plot - mixed models
            "DENSITY_SP2",  # density of specie 2 on a mix plot - mixed models
            #"DENSITY_CUT_VOLUME",  # stand density harvested volume (%)
            "DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            "ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

            # Basic plot variables calculated - basal area
            #"BASAL_AREA",  # Basal area  # (m2/ha)
            "BASAL_AREA_SP1",  # basal area of specie 1 on a mix plot - mixed models
            "BASAL_AREA_SP2",  # basal area of specie 2 on a mix plot - mixed models
            #"BA_MAX",  # BA Max  # (cm2)
            "BA_MAX_SP1",  # BA Max  # (cm2) of specie 1 on a mix plot - mixed models
            "BA_MAX_SP2",  # BA Max  # (cm2) of specie 2 on a mix plot - mixed models        
            #"BA_MIN",  # BA Min  # (cm2) 
            "BA_MIN_SP1",  # BA Min  # (cm2) of specie 1 on a mix plot - mixed models
            "BA_MIN_SP2",  # BA Min  # (cm2) of specie 2 on a mix plot - mixed models
            #"MEAN_BA",  # Mean BA  # (cm2)
            "MEAN_BA_SP1",  # Mean BA  # (cm2) of specie 1 on a mix plot - mixed models
            "MEAN_BA_SP2",  # Mean BA  # (cm2) of specie 2 on a mix plot - mixed models
            #"BA_CUT_VOLUME",  # Basal area harvested volume (%)
            "DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            "ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

            # Basic plot variables calculated - diameter
            #"DBH_MAX",  # D Max  # (cm)
            "DBH_MAX_SP1",  # D Max  # (cm) of specie 1 on a mix plot - mixed models
            "DBH_MAX_SP2",  # D Max  # (cm) of specie 2 on a mix plot - mixed models
            #"DBH_MIN",  # D Min  # (cm)
            "DBH_MIN_SP1",  # D Min  # (cm) of specie 1 on a mix plot - mixed models
            "DBH_MIN_SP2",  # D Min  # (cm) of specie 2 on a mix plot - mixed models
            #"MEAN_DBH",  # Mean dbh  # (cm)
            "MEAN_DBH_SP1",  # Mean dbh  # (cm) of specie 1 on a mix plot - mixed models
            "MEAN_DBH_SP2",  # Mean dbh  # (cm) of specie 2 on a mix plot - mixed models
            #"QM_DBH",  # Quadratic mean dbh  # (cm)
            "QM_DBH_SP1",  # quadratic mean dbh of specie 1 - mixed models
            "QM_DBH_SP2",  # quadratic mean dbh of specie 2 - mixed models
            #"DOMINANT_DBH",  # Dominant dbh  # (cm)
            "DOMINANT_DBH_SP1",  # dominant diameter os specie 1 (cm) on mixed models
            "DOMINANT_DBH_SP2",  # dominant diameter os specie 2 (cm) on mixed models     
            #"DOMINANT_SECTION",  # Dominant section (cm)
            "DOMINANT_SECTION_SP1",  # Dominant section (cm) of specie 1 on a mix plot - mixed models
            "DOMINANT_SECTION_SP2",  # Dominant section (cm) of specie 2 on a mix plot - mixed models

            # Basic plot variables calculated - height
            #"H_MAX",  # H Max  # (m)
            "H_MAX_SP1",  # H Max  # (m) of specie 1 on a mix plot - mixed models
            "H_MAX_SP2",  # H Max  # (m) of specie 2 on a mix plot - mixed models
            #"H_MIN",  # H Min  # (m)    
            "H_MIN_SP1",  # H Min  # (m) of specie 1 on a mix plot - mixed models
            "H_MIN_SP2",  # H Min  # (m) of specie 2 on a mix plot - mixed models
            #"MEAN_H",  # Mean height  # (m)
            "MEAN_H_SP1",  # Mean height  # (m) of specie 1 on a mix plot - mixed models
            "MEAN_H_SP2",  # Mean height  # (m) of specie 2 on a mix plot - mixed models
            #"DOMINANT_H",  # Dominant height  # (m)
            "DOMINANT_H_SP1",  # dominant height of specie 1 - mixed models
            "DOMINANT_H_SP2",  # dominant height of specie 2 - mixed models

            # Basic plot variables calculated - crown
            "CROWN_MEAN_D",  # Mean crown diameter  # (m)
            "CROWN_MEAN_D_SP1",  # Mean crown diameter (m) for specie 1  # (m)
            "CROWN_MEAN_D_SP2",  # Mean crown diameter (m) for specie 2  # (m)    
            "CROWN_DOM_D",  # Dominant crown diameter  # (m)
            "CROWN_DOM_D_SP1",  # Dominant crown diameter (m) for specie 1  # (m)
            "CROWN_DOM_D_SP2",  # Dominant crown diameter (m) for specie 2  # (m)    
            "CANOPY_COVER",  # Canopy cover  # (%)
            "CANOPY_COVER_SP1",  # Canopy cover (%) for specie 1  # (%)
            "CANOPY_COVER_SP2",  # Canopy cover (%) for specie 2  # (%)        

            # Basic plot variables calculated - plot
            #"SLENDERNESS_MEAN",  # slenderness calculated by using mean values of height and dbh (cm/cm)
            #"SLENDERNESS_DOM",  # slenderness calculated by using top height and dbh values (cm/cm)  
            #"REINEKE",  # Reineke Index  # Stand Density Index - SDI
            "REINEKE_SP1",  # reineke index for specie 1 on mixed models
            "REINEKE_SP2",  # reineke index for specie 2 on mixed models
            "REINEKE_MAX",  # maximum reineke index
            "REINEKE_MAX_SP1",  # maximum reineke index for specie 1 on mixed models
            "REINEKE_MAX_SP2",  # maximum reineke index for specie 2 on mixed models
            #"HART",  # Hart-Becking Index (S) calculated to simple rows 
            #"HART_STAGGERED",  # Hart-Becking Index (S) calculated to staggered rows 
            #"SI",  # Site index  # (m)
            #"REF_SI_AGE",  # SI reference age (years)
            #"REINEKE_VALUE" # r contstant value of SDI  to the specie of the model (-1.605 as default)

             # Plot variables calculated - volume and biomass
            "VOL",  # Volume  # (m3/ha)
            "BOLE_VOL",  # Bole Volume  # (m3/ha)
            "BARK_VOL",  # Bark Volumen  # (m3/ha) 
            "VOL_CUT_VOLUME",  # Volume harvested percentaje (%)
            "DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
            "ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - volume for mixed models
            "VOL_SP1",  # Volume  # (m3/ha)
            "BOLE_VOL_SP1",  # Bole Volume  # (m3/ha)
            "BARK_VOL_SP1",  # Bark Volumen  # (m3/ha) 
            "VOL_SP2",  # Volume  # (m3/ha)
            "BOLE_VOL_SP2",  # Bole Volume  # (m3/ha)
            "BARK_VOL_SP2",  # Bark Volumen  # (m3/ha)     

            # Plot variables calculated - wood uses
            "UNWINDING",  # Unwinding  # unwinding = useful volume for unwinding destiny (m3/ha)
            "VENEER",  # Veneer  # veneer = useful volume for veneer destiny (m3/ha)
            "SAW_BIG",  # Saw big  # saw_big = useful volume for big saw destiny (m3/ha)
            "SAW_SMALL",  # Saw small  # saw_small = useful volume for small saw destiny (m3/ha)
            "SAW_CANTER",  # Saw canter  # saw_canter = useful volume for canter saw destiny (m3/ha)
            "POST",  # Post  # post = useful volume for post destiny (m3/ha)
            "STAKE",  # Stake  # stake = useful volume for stake destiny (m3/ha)
            "CHIPS",  # Chips  # chips = useful volume for chips destiny (m3/ha)

            'UNWINDING_SP1',  # unwinding = useful volume for unwinding destiny (m3/ha)
            'VENEER_SP1',  # veneer = useful volume for veneer destiny (m3/ha)
            'SAW_BIG_SP1',  # saw_big = useful volume for big saw destiny (m3/ha)
            'SAW_SMALL_SP1',  # saw_small = useful volume for small saw destiny (m3/ha)
            'SAW_CANTER_SP1',  # saw_canter = useful volume for canter saw destiny (m3/ha)
            'POST_SP1',  # post = useful volume for post destiny (m3/ha)
            'STAKE_SP1',  # stake = useful volume for stake destiny (m3/ha)
            'CHIPS_SP1',  # chips = useful volume for chips destiny (m3/ha)
            
            'UNWINDING_SP2',  # unwinding = useful volume for unwinding destiny (m3/ha)
            'VENEER_SP2',  # veneer = useful volume for veneer destiny (m3/ha)
            'SAW_BIG_SP2',  # saw_big = useful volume for big saw destiny (m3/ha)
            'SAW_SMALL_SP2',  # saw_small = useful volume for small saw destiny (m3/ha)
            'SAW_CANTER_SP2',  # saw_canter = useful volume for canter saw destiny (m3/ha)
            'POST_SP2',  # post = useful volume for post destiny (m3/ha)
            'STAKE_SP2',  # stake = useful volume for stake destiny (m3/ha)
            'CHIPS_SP2',  # chips = useful volume for chips destiny (m3/ha)

            # Plot variables calculated - biomass
            "WSW",  # wsw = stem wood (Tn/ha)
            "WSB",  # wsb = stem bark (Tn/ha)
            "WSWB",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB",  # wstb = wsw + wthickb, stem + branches >7 cm (Tn/ha)
            "WB2_7",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T",  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn/ha)
            "WTHINB",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05",  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            "WB05_7",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB",  # wdb = dead branches biomass (Tn/ha)
            "WL",  # wl = leaves (Tn/ha)
            "WTBL",  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn/ha)
            "WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Tn/ha)
            "WR",  # wr = roots (Tn/ha)
            "WT",  # wt = biomasa total (Tn/ha)
            "DEAD_WT",  # WT of the dead trees after an execution (Tn/ha)
            "ING_WT",  # WT of the ingrowth trees after an execution (Tn/ha)

            # Plot variables calculated - biomass for mixed models
            "WSW_SP1",  # wsw = stem wood (Tn/ha)
            "WSB_SP1",  # wsb = stem bark (Tn/ha)
            "WSWB_SP1",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP1",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP1",  # wstb = wsw + wthickb, stem + branches >7 cm (Tn/ha)
            "WB2_7_SP1",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP1",  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn/ha)
            "WTHINB_SP1",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP1",  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            "WB05_7_SP1",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP1",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP1",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP1",  # wl = leaves (Tn/ha)
            "WTBL_SP1",  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn/ha)
            "WBL0_7_SP1",  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Tn/ha)
            "WR_SP1",  # wr = roots (Tn/ha)
            "WT_SP1",  # wt = biomasa total (Tn/ha)

            "WSW_SP2",  # wsw = stem wood (Tn/ha)
            "WSB_SP2",  # wsb = stem bark (Tn/ha)
            "WSWB_SP2",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP2",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP2",  # wstb = wsw + wthickb, stem + branches >7 cm (Tn/ha)
            "WB2_7_SP2",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP2",  # wb2_t = wb2_7 + wthickb; branches >2 cm (Tn/ha)
            "WTHINB_SP2",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP2",  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            "WB05_7_SP2",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP2",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP2",  # wl = leaves (Tn/ha)
            "WTBL_SP2",  # wtbl = wthinb + wl; branches <2 cm and leaves (Tn/ha)
            "WBL0_7_SP2",  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (Tn/ha)
            "WR_SP2",  # wr = roots (Tn/ha)
            "WT_SP2",  # wt = biomasa total (Tn/ha)

            # Quercus suber special variables
            "W_CORK",  # w_cork = fresh cork biomass (Tn/ha)
            "TOTAL_W_DEBARK",  # w cork accumulator to all the scenario (Tn)
            "TOTAL_V_DEBARK",  # v cork accumulator to all the scenario (m3)

            # Pinus pinea special variables
            "ALL_CONES",  # total of cones of the plot (anual mean)
            "SOUND_CONES",  # total sound (healthy) cones of the plot (anual mean)
            "SOUND_SEEDS",  # total sound (healthy) seeds of the plot (anual mean)
            "W_SOUND_CONES",  # weight of sound (healthy) cones (Tn/ha) (anual mean)
            "W_ALL_CONES",  # weight of all (healthy and not) cones (Tn/ha) (anual mean)

            # Mushrooms special variables
            "EDIBLE_MUSH",  # annual mushroom production of edible species (mean annual value) (kg/ha)
            "MARKETED_MUSH",  # annual mushroom production of marketed species (mean annual value) (kg/ha)
            "MARKETED_LACTARIUS",  # production of marketed Lactarius (mean annual value) (kg/ha)
         
        ]


        #########################################################################################################################
        ############################################  TREE variables ############################################################
        #########################################################################################################################


        # list of tree variables on the simulator that can be deleted without make errors
        # to delete them, just leave it at the list; to NOT delete them, comment it at the list or remove it from them

        delete_from_tree = [


            # Special TREE_IDs to work with the IFN data
            "TREE_ID_IFN3_2",
            "TREE_ID_IFN3",
            "TREE_ID_IFN2",
            "TREE_ID_compare", 

            # Remarkable variables and basic variables measured
            #"specie",
            #"tree_age",
            #"expan",  # expan  # expansion factor
            "dbh_1",  # dbh 1  # diameter mesasurement 1 (cm)
            "dbh_2",  # dbh 2  # diameter mesasurement 1 (cm)
            #"dbh",  # dbh  # diameter at breast height (cm)
            #"height",  # height  # total height (m)
            "stump_h",  # stump height  # (m)
            "bark_1",  # bark thickness 1  # bark thickness mesasurement 1 (mm)
            "bark_2",  # bark thickness 2  # bark thickness mesasurement 2 (mm)
            "bark",  # bark thickness  # mean bark thickness (mm)

           # Basic variables calculated
            #"basal_area",  # basal area  #  (cm2)
            "basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
            "basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
            #"bal",  # basal area acumulated  # (m2/ha)
            "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
            #"ba_ha",  # basal area per ha  # (m2/ha) 
            #"normal_circumference",  # normal circumference  # circumference at breast height (cm)
            #"slenderness",  # slenderness (cm/cm)
            
            # Crown variables
            "cr",  # crown ratio  # (%)
            "lcw",  # lcw  #  largest crown width (m)
            "hcb",  # hcb  # height crown base (m)
            "hlcw",  # hlcw  # height of largest crown width (m)

            # Volume variables
            "vol",  # volume  # volume with bark (dm3)
            "bole_vol",  # bole volume  # volume without bark (dm3)
            "bark_vol",  # bark vol  # volume of bark (dm3)
            "firewood_vol",  # fuelwood volume  # (dm3)
            "vol_ha",  # volume per ha  # volume with bark per hectare (m3/ha)

            # Wood uses variables
            "unwinding",  # unwinding  # unwinding = useful volume for unwinding destiny (dm3)
            "veneer",  # veneer  # veneer = useful volume for veneer destiny (dm3)
            "saw_big",  # saw big  # saw_big = useful volume for big saw destiny (dm3)
            "saw_small",  # saw small  # saw_small = useful volume for small saw destiny (dm3)
            "saw_canter",  # saw canter  # saw_canter = useful volume for canter saw destiny (dm3)
            "post",  # post  # post = useful volume for post destiny (dm3)
            "stake",  # stake  # stake = useful volume for stake destiny (dm3)
            "chips",  # chips  # chips = useful volume for chips destiny (dm3)

            # Biomass variables
            "wsw",  # wsw = stem wood (kg)
            "wsb",  # wsb = stem bark (kg)
            "wswb",  # wswb = stem wood and stem bark (kg)
            "w_cork",  # w_cork = fresh cork biomass (kg)
            "wthickb",  # wthickb = Thick branches > 7 cm (kg)
            "wstb",  # wstb = wsw + wthickb, stem + branches >7 cm (kg)
            "wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
            "wb2_t",  # wb2_t = wb2_7 + wthickb; branches >2 cm (kg)
            "wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
            "wb05",  # wb05 = thinniest branches (<0.5 cm) (kg)
            "wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
            "wb0_2",  # wb0_2 = branches < 2 cm (kg)
            "wdb",  # wdb = dead branches biomass (kg)
            "wl",  # wl = leaves (kg)
            "wtbl",  # wtbl = wthinb + wl; branches <2 cm and leaves (kg)
            "wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches <7 cm and leaves (kg)
            "wr",  # wr = roots (kg)
            "wt",  # wt = biomasa total (kg)

            # Quercus suber special variables
            "dbh_oc",  # dbh over cork  # dbh over cork (cm) - Quercus suber
            "h_debark",  # uncork height  # uncork height on main stem (m) - Quercus suber
            "nb",  # uncork boughs  # number of main bough stripped - Quercus suber
            "cork_cycle",  # cork cycle  # moment to obtain cork data; 0 to the moment just immediately before the stripping process
            "count_debark",  # number of debark treatments applied 
            "total_w_debark",  # w cork accumulator to all the scenario (kg)
            "total_v_debark",  # v cork accumulator to all the scenario (dm3)

            # Pinus pinea special variables
            "all_cones",  # number of all the cones of the tree (anual mean)
            "sound_cones",  # number of healthy cones in a tree (anual mean)
            "sound_seeds",  # total sound seeds of the tree (anual mean)
            "w_sound_cones",  # weight of sound (healthy) cones (kg) (anual mean)
            "w_all_cones",  # weight of all (healthy and not) cones (kg) (anual mean)

            # Tree general information
            "number_of_trees",
            "quality",
            "shape",
            "special_param",
            "remarks",
            "age_130",
            "social_class",
            "coord_x",
            "coord_y"
        ]

        Variables.remove_var_plot(delete_from_plot)
        Variables.remove_var_tree(delete_from_tree)
        
BasicTreeModel.vars()