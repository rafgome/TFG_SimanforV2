#!/usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
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
from .equations import Equations

import math
import sys
import logging
import numpy as np
import os

# Master model (Spain), version 01
# Written by iuFOR
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (dbhiversity of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, dbhiversity of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/


class MasterModel(TreeModel):

    def __init__(self, configuration=None):
        super().__init__(name="MasterModel", version=1)


    def catch_model_exception(self):  # that Function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def model_info(self):
        """
        Function to set the model information at the output.
        It will be run by initialize function once.
        """

        Model.model_name = 'master_model'  # set the model name to show it at the output
        Model.specie_ifn_id = 'all'  # Set the model specie ID to mark the trees of different species        
        Model.exec_time = 999  # recommended executions time to use that model
        Model.aplication_area = 'none'  # area recommended to use the model
        Model.valid_prov_reg = 'example'  # provenance regions recommended to use the model
        Model.model_type = 'tree_independent'  # SIMANFOR model type. It can be: ('' is neccesary)
        # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
        Model.model_card_en = 'link'  # link to model card in english
        Model.model_card_es = 'link'  # link to model card in spanish


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps of information at the initial inventory
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                             Running: Master model. Plot:', plot.plot_id                             )
        print('#--------------------------------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced

            self.model_info()
            
            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            bal: float = 0

            for tree in plot_trees:  # for each tree...

                #-----------------------------------BASAL_AREA-----------------------------------------#

                tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal section (cm2)
                tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basal area per ha (m2/ha)
                bal += tree.basal_area * tree.expan / 10000  # then, that value is accumulated

                #-------------------------------- HEIGHT ------------------------------------#

                if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                    ht = Equations.height(self, plot, tree)
                    tree.add_value('height', ht)

                #-------------------------------- OTHERS ------------------------------------#

                tree.add_value('slenderness', tree.height * 100 / tree.dbh)  # height/diameter ratio (%)
                tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal circumference (cm)

                #-----------------------------------CROWN------------------------------------------#

                Equations.crown(self, plot, tree)

                #----------------------------------VOLUME------------------------------------------#

                hr = np.arange(0, 1, 0.001)  # that line establish the integrated conditions for volume calculation
                dob = Equations.taper_over_bark(self, tree, plot, hr)
                dub = Equations.taper_under_bark(self, tree, plot, hr)
                Equations.vol(self, plot, tree, dob, dub, hr)
                
                tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha) 

                #-------------------------------MERCHANTABLE--------------------------------------#

                class_conditions = Equations.merchantable(self, plot, tree)  # import the class_conditions list
                self.merchantable(tree, plot, class_conditions)  # activate wood uses variables

                #----------------------------------BIOMASS-----------------------------------------#

                Equations.biomass(self, plot, tree)

            #----------------------------------PLOT_VOL-----------------------------------------#

            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #----------------------------------CANOPY_PLOT-----------------------------------------#

            self.canopy(plot, plot_trees)  # activate crown variables (plot) merch_calculation

            #--------------------------------PLOT_MERCHANTABLE---------------------------------------#

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)
        
            #----------------------------------PLOT_BIOMASS-----------------------------------------#

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables 

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

        return Equations.survival(self, time, plot, tree)


    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Tree growth function.
        A function that updates dbh and h by using growth equations, and also update age, g, and v to the new situation.
        """

        return Equations.growth(self, time, plot, old_tree, new_tree)


    def ingrowth(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated is calculated. The next function will order how to divide that basal area into the different diametric classes.
        """
        return 0


    def ingrowth_distribution(self, time: int, plot: Plot, area: float):
        """
        Tree diametric classes distribution.
        That function must return a list with different sublists for each diametric class, where the conditions to ingrowth function are written.
        That function has the aim to divide the ingrowth (added basal area of ingrowth function) in different proportions depending on the orders given.
        In the cases that a model hasn´t a well-known distribution, just return None to share that ingrowth between all the trees of the plot.
        """

        distribution = []  # that list will contain the different diametric classes conditions to calculate the ingrowth distribution

            # for each diametric class: [dbh minimum, dbh maximum, proportion of basal area to add (between 0*area and 1*area)]
            # if your first diametric class doesn't start on 0, just create a cd_0 with the diametric range between 0 and minimum of cd_1 without adding values
            # example: cd_0 = [0, 7.5, 0]  
            #          distribution.append(cd_0)
            # moreover, if your diametric distribution doesn't take into account the bigger tree dbh, just create another empty distribution
            # example: cd_x = [12.5, 100, 0]
            #          distribution.append(cd_x)

            # by doing this, you avoid possible errors at the simulator; if not, it's possible that an error will be found

        return None


    def update_model(self, time: int, plot: Plot, trees: list):
        """
        A function that updates trees and plot information once growth, survival, and ingrowth functions were executed and the plot information was updated.
        The equations on that function are the same that in "initialize" function, so references are the same
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                             Running: Master model. Plot:', plot.plot_id                             )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same as the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:  # errors inside that construction will be announced

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            bal: float = 0.0

            for tree in plot_trees:  # for each tree...

                #-----------------------------------BASAL_AREA-----------------------------------------#

                tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal section (cm2)
                tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basal area per ha (m2/ha)
                bal += tree.basal_area * tree.expan / 10000  # then, that value is accumulated

                #--------------------------------HEIGHT_PPINEA-------------------------------------------#
                
                if tree.specie == 23:  # if the tree is Pinus pinea, we need to calculate the height in a special way...
                    tree.add_value('height', 0)  # restablish the height value
                    ht = Equations.height(self, plot, tree)  # calculate it again with the updated data
                    tree.add_value('height', ht)

                #-------------------------------- OTHERS ------------------------------------#

                tree.add_value('slenderness', tree.height * 100 / tree.dbh)  # height/diameter ratio (%)
                tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal circumference (cm)

                #-----------------------------------CROWN------------------------------------------#

                Equations.crown(self, plot, tree)

                #----------------------------------VOLUME------------------------------------------#

                hr = np.arange(0, 1, 0.001)  # that line establish the integrated conditions for volume calculation
                dob = Equations.taper_over_bark(self, tree, plot, hr)
                dub = Equations.taper_under_bark(self, tree, plot, hr)
                Equations.vol(self, plot, tree, dob, dub, hr)
               
                tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)               

                #-------------------------------MERCHANTABLE--------------------------------------#

                class_conditions = Equations.merchantable(self, plot, tree)  # import the class_conditions list
                self.merchantable(tree, plot, class_conditions)  # activate wood uses variables

                #----------------------------------BIOMASS-----------------------------------------#

                Equations.biomass(self, plot, tree)

            #----------------------------------PLOT_VOL-----------------------------------------#

            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #----------------------------------PLOT_CROWN-----------------------------------------#

            self.canopy(plot, plot_trees)  # activate crown variables (plot) merch_calculation

            #--------------------------------PLOT_MERCHANTABLE---------------------------------------#

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)
        
            #----------------------------------PLOT_BIOMASS-----------------------------------------#

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables 

        except Exception:
            self.catch_model_exception()


    def taper_over_bark(self, tree, plot, hr):
        """
        Taper equation over bark function.
        A function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        """

        dob = Equations.taper_over_bark(self, tree, plot, hr)
        return dob


    def taper_under_bark(self, tree, plot, hr):
        """
        Taper equation under bark function.
        A function that returns the taper equation to calculate the diameter (cm, under bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        """

        dub = Equations.taper_under_bark(self, tree, plot, hr)
        return dub
                        

    def merchantable(self, tree, plot, class_conditions):
        """
        Merchantable wood calculation (tree).
        A function needed to calculate the different commercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions and is linked to taper_over_bark, an indispensable function.
        That function is run by initialize and update_model functions.
        Data criteria to classify the wood by different uses were obtained from:
        """
 
        try:  # errors inside that construction will be announced

            ht = tree.height  # the total height as ht to simplify

            # usage and merch_list are a dictionary and a list returned from merch_calculation function
            # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using

            if class_conditions != []:  # only calculate the merchantable classes if the tree has a list to do it
                usage, merch_list = TreeModel.merch_calculation_master(self, tree, plot, class_conditions, MasterModel)

                counter = -1
                for k,i in usage.items():
                    counter += 1
                    tree.add_value(k, merch_list[counter])  # add merch_list values to each usage
            else:
                usage = {}

            # add 0 to the empty uses to calculate the plot merchantable classes
            if 'unwinding' not in usage:
                tree.add_value('unwinding', 0)
            if 'veneer' not in usage:
                tree.add_value('veneer', 0)
            if 'saw_big' not in usage:
                tree.add_value('saw_big', 0)
            if 'saw_canter' not in usage:
                tree.add_value('saw_canter', 0)
            if 'saw_small' not in usage:
                tree.add_value('saw_small', 0)
            if 'post' not in usage:
                tree.add_value('post', 0)
            if 'stake' not in usage:
                tree.add_value('stake', 0)
            if 'chips' not in usage:
                tree.add_value('chips', 0)

        except Exception:
            self.catch_model_exception()


    def merchantable_plot(self, plot: Plot, plot_trees):
        """
        Merchantable wood calculation (plot).
        A function needed to calculate the different commercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions and uses the data obtained from trees.
        """

        try:  # errors inside that construction will be announced

            plot_unwinding = plot_veneer = plot_saw_big = plot_saw_small = plot_saw_canter = plot_post = plot_stake = plot_chips =  0

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                plot_unwinding += tree.unwinding*tree.expan
                plot_veneer += tree.veneer*tree.expan
                plot_saw_big += tree.saw_big*tree.expan
                plot_saw_small += tree.saw_small*tree.expan
                plot_saw_canter += tree.saw_canter*tree.expan
                plot_post += tree.post*tree.expan
                plot_stake += tree.stake*tree.expan
                plot_chips += tree.chips*tree.expan

            plot.add_value('UNWINDING', plot_unwinding/1000)  # now, we add the plot value to each variable, changing the units to m3/ha
            plot.add_value('VENEER', plot_veneer/1000)
            plot.add_value('SAW_BIG', plot_saw_big/1000)
            plot.add_value('SAW_SMALL', plot_saw_small/1000)
            plot.add_value('SAW_CANTER', plot_saw_canter/1000)
            plot.add_value('POST', plot_post/1000)
            plot.add_value('STAKE', plot_stake/1000)
            plot.add_value('CHIPS', plot_chips/1000)

        except Exception:
            self.catch_model_exception()


    def crown(self, tree: Tree, plot: Plot, func):
        """
        Crown variables (tree).
        Function to calculate crown variables for each tree.
        That function is run by initialize and update_model functions.
        """

        # if func == 'initialize':  # if that function is called from initialize, first we must check if those variables are available on the initial inventory


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
        That function is run by initialize and growth functions and uses taper equations to calculate the values.
        """

        try:  # errors inside that construction will be announced

            hr = np.arange(0, 1, 0.001)  # that line establish the integrated conditions for volume calculation
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
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            #plot_vol = plot_bole_vol = plot_bark = 0

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

        try:  # errors inside that construction will be announced

            # tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
            # tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
            # tree.add_value('w_cork', w_cork)   # fresh cork biomass (kg)
            # tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
            # tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            # tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
            # tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            # tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
            # tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
            # tree.add_value('wl', wl)  # wl = leaves (kg)
            # tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            # tree.add_value('wbl0_7', wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
            # tree.add_value('wr', wr)  # wr = roots (kg)
            # tree.add_value('wt', wt)  # wt = total biomass (kg)

        except Exception:
            self.catch_model_exception()


    def biomass_plot(self, plot: Plot, plot_trees):
        """
        Biomass variables (plot).
        Function to calculate plot biomass variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            plot_wsw = plot_wsb = plot_w_cork = plot_wthickb = plot_wstb = plot_wb2_7 = plot_wb2_t = plot_wthinb = plot_wb05 = plot_wl = plot_wtbl = plot_wbl0_7 = plot_wr = plot_wt =  0

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                plot_wsw += tree.wsw*tree.expan
                plot_wsb += tree.wsb*tree.expan
                plot_w_cork += tree.w_cork*tree.expan
                plot_wthickb += tree.wthickb*tree.expan
                plot_wstb += tree.wstb*tree.expan
                plot_wb2_7 += tree.wb2_7*tree.expan
                plot_wb2_t += tree.wb2_t*tree.expan
                plot_wthinb += tree.wthinb*tree.expan
                plot_wb05 += tree.wb05*tree.expan                
                plot_wl += tree.wl*tree.expan
                plot_wtbl += tree.wtbl*tree.expan
                plot_wbl0_7 += tree.wbl0_7*tree.expan
                plot_wr += tree.wr*tree.expan
                plot_wt += tree.wt*tree.expan

            plot.add_value('WSW', plot_wsw/1000)  # wsw = stem wood (Tn/ha)
            plot.add_value('WSB', plot_wsb/1000)  # wsb = stem bark (Tn/ha)
            plot.add_value('W_CORK', plot_w_cork/1000)  # fresh cork biomass (Tn/ha)
            plot.add_value('WTHICKB', plot_wthickb/1000)  # wthickb = Thick branches > 7 cm (Tn/ha)
            plot.add_value('WSTB', plot_wstb/1000)  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            plot.add_value('WB2_7', plot_wb2_7/1000)  # wb2_7 = branches (2-7 cm) (Tn/ha)
            plot.add_value('WB2_T', plot_wb2_t/1000)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            plot.add_value('WTHINB', plot_wthinb/1000)  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            plot.add_value('WB05', plot_wb05/1000)  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            plot.add_value('WL', plot_wl/1000)  # wl = leaves (Tn/ha)
            plot.add_value('WTBL', plot_wtbl/1000)  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            plot.add_value('WBL0_7', plot_wbl0_7/1000)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            plot.add_value('WR', plot_wr/1000)  # wr = roots (Tn/ha)
            plot.add_value('WT', plot_wt/1000)  # wt = total biomass (Tn/ha)
          
        except Exception:
            self.catch_model_exception()


    def vars():
        """
        Control variables function.
        The aim of this function is to deactivate variables that are not calculated at the model and we don't want to show them at the output.
        It has the possibility to work over trees and plot variables.
        """

        ###############################################################################################################
        ######################################## PLOT variables #######################################################
        ###############################################################################################################


        # list of plot variables on the simulator that can be deleted without make errors
        # to delete them, just leave it on the list; to NOT delete them, comment it at the list or remove it from them

        delete_from_plot = [  

            # Basic plot variables measured
            "EXPAN",  # plot expansion factor

            # Basic plot variables calculated - density
            #"DENSITY_CUT_VOLUME",  # stand density harvested volume (%)
            #"DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            #"ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

            # Basic plot variables calculated - basal area
            #"BA_MAX",  # Maximal Basal Area (cm2)
            #"BA_MIN",  # Minimal Basal Area (cm2)
            #"MEAN_BA",  # Mean Basal Area (cm2)
            #"BA_CUT_VOLUME",  # Basal area harvested volume (%)
            #"DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            #"ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

            # Basic plot variables calculated - diameter
            #"DBH_MAX",  # Maximal Diameter (cm)
            #"DBH_MIN",  # Minimal Diameter (cm)
            #"DOMINANT_SECTION",  # Dominant section (cm)

            # Basic plot variables calculated - height
            #"H_MAX",  # Maximal Height (m)
            #"H_MIN",  # Minimal Height (m)

            # Basic plot variables calculated - crown
            #"CROWN_MEAN_D",  # Mean crown diameter (m)
            #"CROWN_DOM_D",  # Dominant crown diameter (m)
            #"CANOPY_COVER",  # Canopy cover (%)

            # Basic plot variables calculated - plot
            #"SLENDERNESS_MEAN",  # slenderness calculated by using mean values of height and dbh (cm/cm)
            #"SLENDERNESS_DOM",  # slenderness calculated by using top height and dbh values (cm/cm)  
            #"REINEKE",  # Reineke Index or Stand Density Index - SDI
            #"REINEKE_VALUE"  # r contstant value of SDI  to the specie of the model (-1.605 as default)
            #"HEGYI_RADIUS",  # radius value to calculate the Hegyi competition index (m)    
            #"HART",  # Hart-Becking Index (S) calculated to simple rows 
            #"HART_STAGGERED",  # Hart-Becking Index (S) calculated to staggered rows 

             # Plot variables calculated - volume and biomass
            #"VOL",  # Volume (m3/ha)
            #"BOLE_VOL",  # Volume under bark (m3/ha)
            #"BARK_VOL",  # Bark Volume (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume harvested percentage (%)
            #"DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
            #"ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - wood uses
            #"UNWINDING",  # Unwinding = the useful wood volume unwinding destiny (m3/ha)
            #"VENEER",  # Veneer = the useful wood volume veneer destiny (m3/ha)
            #"SAW_BIG",  # Saw big =) the useful wood volume big saw destiny (m3/ha)
            #"SAW_SMALL",  # Saw small = the useful wood volume small saw destiny (m3/ha)
            #"SAW_CANTER",  # Saw canter = the useful wood volume canter saw destiny (m3/ha)
            #"POST",  # Post = the useful wood volume post destiny (m3/ha)
            #"STAKE",  # Stake = the useful wood volume stake destiny (m3/ha)
            #"CHIPS",  # Chips = the useful wood volume chips destiny (m3/ha)

            # Plot variables calculated - biomass
            #"WSW",  # wsw = stem wood (Tn/ha)
            #"WSB",  # wsb = stem bark (Tn/ha)
            #"WSWB",  # wswb = stem wood and stem bark (Tn/ha)
            #"W_CORK",  # fresh cork biomass (Tn/ha)
            #"WTHICKB",  # wthickb = Thick branches > 7 cm (Tn/ha)
            #"WSTB",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            #"WB2_7",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            #"WB2_T",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            #"WTHINB",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            #"WB05",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            #"WB05_7",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            #"WB0_2",  # wb0_2 = branches < 2 cm (Tn/ha)
            #"WDB",  # wdb = dead branches biomass (Tn/ha)
            #"WL",  # wl = leaves (Tn/ha)
            #"WTBL",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            #"WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            #"WR",  # wr = roots (Tn/ha)
            #"WT",  # wt = total biomass (Tn/ha)
            #"DEAD_WT",  # WT of the dead trees after an execution (Tn/ha)
            #"ING_WT",  # WT of the ingrowth trees after an execution (Tn/ha)

            # Pinus pinea special variables
            #"ALL_CONES",  # total of cones of the plot (anual mean)
            #"SOUND_CONES",  # total sound (healthy) cones of the plot (anual mean)
            #"SOUND_SEEDS",  # total sound (healthy) seeds of the plot (anual mean)
            #"W_SOUND_CONES",  # weight of sound (healthy) cones (Tn/ha) (anual mean)
            #"W_ALL_CONES",  # weight of all (healthy and not) cones (Tn/ha) (anual mean)

            # Mushrooms special variables
            #"EDIBLE_MUSH",  # annual mushroom production of edible species (mean annual value) (kg/ha)
            #"MARKETED_MUSH",  # annual mushroom production of marketed species (mean annual value) (kg/ha)
            #"MARKETED_LACTARIUS"  # production of marketed Lactarius (mean annual value) (kg/ha)
           
        ]


        ###############################################################################################################
        ######################################## TREE variables #######################################################
        ###############################################################################################################


        # list of tree variables on the simulator that can be deleted without make errors
        # to delete them, just leave it on the list; to NOT delete them, comment it at the list or remove it from them

        delete_from_tree = [

            # Special TREE_IDs to work with the IFN data
            "TREE_ID_IFN3_2",
            "TREE_ID_IFN3",
            "TREE_ID_IFN2",
            "TREE_ID_compare", 

            # Remarkable variables
            #"tree_age",
            #"bearing",  # bearing from the tree to the central point of the plot ('rumbo')
            #"distance",  # distance from the tree to the central point of the plot    

            # Basic variables measured
            #"dbh_1",  # dbh measurement 1 (cm)
            #"dbh_2",  # dbh measurement 2 (cm)
            #"stump_h",   # stump height (m))
            #"bark_1",  # bark thickness, measurement 1 (mm)
            #"bark_2",  # bark thickness, measurement 2 (mm)
            #"bark",  # mean bark thickness (mm)

           # Basic variables calculated
            #"ba_ha",  # basal area per ha (m2/ha) 
            #"normal_circumference",  # circumference at breast height (cm)
            #"slenderness",  # slenderness (cm/cm)
            
            # Crown variables
            #"cr",  # crown ratio (%)
            #"lcw",  #  largest crown width (m)
            #"hcb",  # height of the crown base (m)
            #"hlcw",  # height of the largest crown width (m)
            #"cpa",  # crown projection area (m2)
            #"crown_vol",  # crown volume (m3)

            # Volume variables
            #"vol",  # volume over bark (dm3)
            #"bole_vol",  # volume under bark (dm3)
            #"bark_vol",  # bark volume (dm3)
            #"firewood_vol",  # firewood volume (dm3)
            #"vol_ha",  # volume over bark per hectare (m3/ha)

            # Wood uses variables
            #"unwinding",  # unwinding = the useful wood volume unwinding destiny (dm3)
            #"veneer",  # veneer = the useful wood volume veneer destiny (dm3)
            #"saw_big",  # saw_big = the useful wood volume big saw destiny (dm3)
            #"saw_small",  # saw_small = the useful wood volume small saw destiny (dm3)
            #"saw_canter",  # saw_canter = the useful wood volume canter saw destiny (dm3)
            #"post",  # post = the useful wood volume post destiny (dm3)
            #"stake",  # stake = the useful wood volume stake destiny (dm3)
            #"chips",  # chips = the useful wood volume chips destiny (dm3)

            # Biomass variables
            #"wsw",  # wsw = stem wood (kg)
            #"wsb",  # wsb = stem bark (kg)
            #"wswb",  # wswb = stem wood and stem bark (kg)
            #"w_cork",  # fresh cork biomass (kg)
            #"wthickb",  # wthickb = Thick branches > 7 cm (kg)
            #"wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            #"wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
            #"wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            #"wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
            #"wb05",  # wb05 = thinnest branches (< 0.5 cm) (kg)
            #"wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
            #"wb0_2",  # wb0_2 = branches < 2 cm (kg)
            #"wdb",  # wdb = dead branches biomass (kg)
            #"wl",  # wl = leaves (kg)
            #"wtbl",  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            #"wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
            #"wr",  # wr = roots (kg)
            #"wt",  # wt = total biomass (kg)
            
            # Competition information
            #"hegyi",  # Hegyi competition index calculation

            # Quercus suber special variables
            #"dbh_oc",  # dbh over cork (cm) - Quercus suber
            #"h_debark",  # uncork height on the main stem (m) - Quercus suber
            #"nb",  # number of the main boughs stripped - Quercus suber
            #"cork_cycle",  # moment to obtain cork data; 0 to the moment just immediately before the stripping process

            # Pinus pinea special variables
            #"all_cones",  # number of all the cones of the tree (anual mean)
            #"sound_cones",  # number of healthy cones in a tree (anual mean)
            #"sound_seeds",  # total sound seeds of the tree (anual mean)
            #"w_sound_cones",  # weight of sound (healthy) cones (kg) (anual mean)
            #"w_all_cones",  # weight of all (healthy and not) cones (kg) (anual mean)
    
            # Basic variables on hegyi subplot
            "bal_intrasp_hegyi",  # intraspecific bal (m2/ha) inside hegyi subplot of each tree
            "bal_intersp_hegyi",  # interspecific bal (m2/ha) inside hegyi subplot of each tree
            "bal_ratio_intrasp_hegyi",  # intraspecific bal ratio (0 to 1) inside hegyi subplot of each tree
            "bal_ratio_intersp_hegyi",  # interspecific bal ratio (0 to 1) inside hegyi subplot of each tree
            "bal_total_hegyi",  # total bal (m2/ha) inside hegyi subplot of each tree
            "g_intrasp_hegyi",  # intraspecific basal area (m2/ha) inside hegyi subplot of each tree
            "g_intersp_hegyi",  # interspecific basal area (m2/ha) inside hegyi subplot of each tree
            "g_ratio_intrasp_hegyi",  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
            "g_ratio_intersp_hegyi",  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
            "g_total_hegyi",  # total basal area (m2/ha) inside hegyi subplot of each tree
            "n_intrasp_hegyi",  # intraspecific density (trees/ha) inside hegyi subplot of each tree
            "n_intersp_hegyi",  # interspecific density (trees/ha) inside hegyi subplot of each tree
            "n_ratio_intrasp_hegyi",  # intraspecific density ratio (0 to 1) inside hegyi subplot of each tree
            "n_ratio_intersp_hegyi",  # interspecific density ratio (0 to 1) inside hegyi subplot of each tree
            "n_total_hegyi",  # total density (trees/ha) inside hegyi subplot of each tree

            # Tree general information
            "number_of_trees",
            "quality",
            "shape",
            "special_param",
            "remarks",
            "age_130",
            "social_class",
            "coord_x",
            "coord_y",
            "coord_z"
        ]

        Variables.remove_var_plot(delete_from_plot)
        Variables.remove_var_tree(delete_from_tree)

#MasterModel.vars()