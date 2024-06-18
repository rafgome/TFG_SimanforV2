# /usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
#
# Single tree growing model independent from distance, developed to
# Mixed stands of different species located in Spain
# Version 01
#
# Model adaptation and equations transcription developed by iuFOR:
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (University of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, University of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/
#
# Use the following reference to cite the use of this model in your own work:
# 
#
# ==============================================================================
# TODO: cambiar los encabezados de todos los archivos

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

from models.trees.equations_mixed_models import MixedEquations
from models.trees.equations_tree_models import TreeEquations
from models.trees.equations_tree_biomass import TreeBiomass
from models.trees.equations_tree_volume import TreeVolume

import math
import sys
import logging
import numpy as np
import os


class MixedModelsSpain(TreeModel):

    def __init__(self, configuration=None):
        super().__init__(name="MixedModelsSpain", version=1)


    def catch_model_exception(self):  # that Function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def model_info(self):
        """
        Function to set the model information at the output.
        It will be run by initialize function once.
        """

        try:  # errors inside that construction will be announced
            # TODO: completar
            Model.model_name = 'tree_template'  # set the model name to show it at the output
            Model.specie_ifn_id = ''  # Set the model specie ID to mark the trees of different species         
            Model.exec_time = 5  # recommended executions time to use that model
            Model.aplication_area = 'Spain'  # area recommended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = 'all'  # provenance regions recommended to use the model
            Model.model_type = 'tree_independent'  # SIMANFOR model type. It can be: ('' is neccesary)
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'link'  # link to model card in english
            Model.model_card_es = 'link'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps of information at the initial inventory.
        """

        try:  # errors inside that construction will be announced

            # print running message
            MixedEquations.print_run_info(plot)

            # print model information
            self.model_info()

            # get Reineke value (0 is the default)
            plot.add_value('REINEKE_VALUE', TreeEquations.get_reineke_value(0))

            # establish an order to calculate tree variables
            list_of_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables

            # get martonne aridity index if data is available on the inventory
            # TODO: list of years is temporally written like this
            M = TreeEquations.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))

            # calculate basal areas
            for tree in list_of_trees:

                TreeEquations.set_g(tree)  # tree basal area (cm2)
                TreeEquations.set_g_ha(tree)  # basal area per ha (m2/ha)

            # reorder trees to calculate bal
            list_of_trees: list[Tree] = plot.short_trees_on_list('ba_ha', DESC)  # establish an order to calculate tree variables

            # calculate bal variables per species
            MixedEquations.get_bal_per_sp(list_of_trees, plot)

            # calculate size variables
            for tree in list_of_trees:

                # calculate heights if needed
                if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated

                    MixedEquations.apply_hd_model(plot, tree)

                # calculate additional tree size variables
                TreeEquations.set_slenderness(tree)
                TreeEquations.set_circumference(tree)

            # reorder trees by dbh
            list_of_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)

            # calculate stand variables by species
            MixedEquations.get_stand_by_sp(list_of_trees, plot, M)

            # calculate biodiversity indexes
            plot.add_value('SHANNON', TreeEquations.get_shannon_index(plot, list_of_trees))
            plot.add_value('SIMPSON', TreeEquations.get_simpson_index(plot, list_of_trees))
            plot.add_value('MARGALEF', TreeEquations.get_margalef_index(plot, list_of_trees))
            plot.add_value('PIELOU', TreeEquations.get_pielou_index(plot, list_of_trees))

            # calculate other extra variables
            for tree in list_of_trees:
            #     # activate crown variables
            #     self.crown(tree, plot, 'initialize')
            #
                # activate volume variables
                TreeVolume.set_tree_vol(tree)

                # activate wood uses variables
                TreeVolume.set_tree_merch(tree)
                # activate biomass variables
                TreeBiomass.set_w_carbon_trees(tree)

            #
            # # activate crown variables (plot)
            # self.canopy(plot, list_of_trees)
            #

            # activate volume variables (plot)
            TreeVolume.set_plot_vol(plot, list_of_trees)
            TreeVolume.set_plot_vol_sp(plot, list_of_trees)

            # # activate wood uses variables (plot)
            TreeVolume.set_plot_merch(plot, list_of_trees)
            TreeVolume.set_plot_merch_sp(plot, list_of_trees)

            # # activate biomass (plot) variables
            # self.biomass_plot(plot, list_of_trees)
            TreeBiomass.set_w_carbon_plot(plot, list_of_trees)
            TreeBiomass.set_w_carbon_plot_sp(plot, list_of_trees)

            plot.add_value('DEAD_DENSITY', 0)  # change the value from '' to 0 in order to print that information at the summary sheet
            plot.add_value('ING_DENSITY', '')  # change the value from '' to 0 in order to print that information at the summary sheet


        except Exception:
            self.catch_model_exception()


    def survival(self, time: int, plot: Plot, tree: Tree):
        """
        Tree survival/mortality function. 
        That function modifies the expan of the tree at the executions.
        Dead trees will be shown at the output with a "M" at the "status" column, with the "expan" value corresponding to the dead part.
        """

        try:  # errors inside that construction will be announced

            # get the survival rate for each tree based on the species combination
            survival_rate = MixedEquations.apply_survival_model(tree, plot)

        except Exception:
            self.catch_model_exception()

        return survival_rate


    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Tree growth function.
        A function that updates dbh and h by using growth equations, and also update age, g, and v to the new situation.
        """

        try:  # errors inside that construction will be announced

            # TODO: meter aquí un check del time (Irene necesita 10 años, lo mismo en survival e ingrowth)
            # get tree growth for each tree based on the species combination
            MixedEquations.apply_growth_model(time, plot, old_tree, new_tree)

        except Exception:
            self.catch_model_exception()


    def ingrowth(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated is calculated. The next function will order how to divide that basal area into the different diametric classes.
        """

        try:  # errors inside that construction will be announced

            ingrowth = MixedEquations.apply_ingrowth_model(time, plot)

        except Exception:
            self.catch_model_exception()

        return ingrowth


    def ingrowth_distribution(self, time: int, plot: Plot, area: float):
        """
        Tree diametric classes distribution.
        That function must return a list with different sublists for each diametric class, where the conditions to ingrowth function are written.
        That function has the aim to divide the ingrowth (added basal area of ingrowth function) in different proportions depending on the orders given.
        In the cases that a model hasn´t a well-known distribution, just return None to share that ingrowth between all the trees of the plot.
        """

        try:  # errors inside that construction will be announced

            # that list will contain the different diametric classes conditions to calculate the ingrowth distribution
            distribution = MixedEquations.apply_ingrowth_distribution(time, plot, area)

        except Exception:
            self.catch_model_exception()

        return distribution


    def update_model(self, time: int, plot: Plot, trees: list):
        """
        A function that updates trees and plot information once growth, survival, and ingrowth functions were
        executed and the plot information was updated. The equations on that function are the same that in
        "initialize" function, so references are the same
        """

        try:  # errors inside that construction will be announced

            # print running message
            MixedEquations.print_run_info(plot)

            # check the time value provided by the user
            TreeEquations.check_projection_time(time)

            # both will be automatically updated by SIMANFOR, here variables are temporally available (if needed)
            new_plot_year, new_plot_age = TreeEquations.update_year_and_age(plot, time)

            # establish an order to calculate tree variables
            list_of_trees: list[Tree] = plot.short_trees_on_list('dbh',
                                                                 DESC)  # establish an order to calculate tree variables

            # get martonne aridity index if data is available on the inventory
            # TODO: list of years is temporally written like this
            M = TreeEquations.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))

            # calculate basal areas
            for tree in list_of_trees:
                TreeEquations.set_g(tree)  # tree basal area (cm2)
                TreeEquations.set_g_ha(tree)  # basal area per ha (m2/ha)

            # reorder trees to calculate bal
            list_of_trees: list[Tree] = plot.short_trees_on_list('ba_ha',
                                                                 DESC)  # establish an order to calculate tree variables

            # calculate bal variables per species
            MixedEquations.get_bal_per_sp(list_of_trees, plot)

            # calculate size variables
            for tree in list_of_trees:

                # calculate additional tree size variables
                TreeEquations.set_slenderness(tree)
                TreeEquations.set_circumference(tree)

            # reorder trees by dbh
            list_of_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)

            # calculate stand variables by species
            MixedEquations.get_stand_by_sp(list_of_trees, plot, M)

            # calculate other extra variables
            for tree in list_of_trees:
            #
            #     # activate crown variables
            #     self.crown(tree, plot, 'update_model')

                # activate volume variables
                TreeVolume.set_tree_vol(tree)

                # activate wood uses variables
                TreeVolume.set_tree_merch(tree)

                # activate biomass variables
                TreeBiomass.set_w_carbon_trees(tree)

            # # activate crown variables (plot)
            # self.canopy(plot, list_of_trees)

            # activate volume variables (plot)
            TreeVolume.set_plot_vol(plot, list_of_trees)
            TreeVolume.set_plot_vol_sp(plot, list_of_trees)

            # activate wood uses variables (plot)
            TreeVolume.set_plot_merch(plot, list_of_trees)
            TreeVolume.set_plot_merch_sp(plot, list_of_trees)

            # activate biomass (plot) variables
            TreeBiomass.set_w_carbon_plot(plot, list_of_trees)
            TreeBiomass.set_w_carbon_plot_sp(plot, list_of_trees)

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

            #'ID_SP1',  # IFN (Spanish National Forestal Inventory) ID specie 1 - mixed models
            #'ID_SP2',  # IFN (Spanish National Forestal Inventory) ID specie 2 - mixed models

            # Basic plot variables measured
            "EXPAN",  # plot expansion factor
            #'YEAR',  # year of the inventory
            #"AGE",  # plot age (years)
            #"SP1_PROPORTION",  # proportion of specie 1 on a mix plot - mixed models
            #"SP2_PROPORTION",  # proportion of specie 2 on a mix plot - mixed models
            #"DENSITY",  # plot density (nº trees/ha)
            #"DENSITY_SP1",  # density of specie 1 on a mix plot - mixed models
            #"DENSITY_SP2",  # density of specie 2 on a mix plot - mixed models
            #"DENSITY_CUT_VOLUME",  # stand density harvested volume (%)
            #"DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            "ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

            # Basic plot variables calculated - basal area
            #"BASAL_AREA",  # Basal area (m2/ha)
            #"BASAL_AREA_SP1",  # basal area of specie 1 on a mix plot - mixed models
            #"BASAL_AREA_SP2",  # basal area of specie 2 on a mix plot - mixed models
            #"BA_MAX",  # Maximal Basal Area (cm2)
            #"BA_MAX_SP1",  # Maximal Basal Area (cm2) of specie 1 on a mix plot - mixed models
            #"BA_MAX_SP2",  # Maximal Basal Area (cm2) of specie 2 on a mix plot - mixed models        
            #"BA_MIN",  # Minimal Basal Area (cm2) 
            #"BA_MIN_SP1",  # Minimal Basal Area (cm2) of specie 1 on a mix plot - mixed models
            #"BA_MIN_SP2",  # Minimal Basal Area (cm2) of specie 2 on a mix plot - mixed models
            #"MEAN_BA",  # Mean Basal Area (cm2)
            #"MEAN_BA_SP1",  # Mean Basal Area (cm2) of specie 1 on a mix plot - mixed models
            #"MEAN_BA_SP2",  # Mean Basal Area (cm2) of specie 2 on a mix plot - mixed models
            #"BA_CUT_VOLUME",  # Basal area harvested volume (%)
            #"DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            "ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

            # Basic plot variables calculated - diameter
            #"DBH_MAX",  # Maximal Diameter (cm)
            #"DBH_MAX_SP1",  # Maximal Diameter (cm) of specie 1 on a mix plot - mixed models
            #"DBH_MAX_SP2",  # Maximal Diameter (cm) of specie 2 on a mix plot - mixed models
            #"DBH_MIN",  # Minimal Diameter (cm)
            #"DBH_MIN_SP1",  # Minimal Diameter (cm) of specie 1 on a mix plot - mixed models
            #"DBH_MIN_SP2",  # Minimal Diameter (cm) of specie 2 on a mix plot - mixed models
            #"MEAN_DBH",  # Mean Diameter (cm)
            #"MEAN_DBH_SP1",  # Mean Diameter (cm) of specie 1 on a mix plot - mixed models
            #"MEAN_DBH_SP2",  # Mean Diameter (cm) of specie 2 on a mix plot - mixed models
            #"QM_DBH",  # Quadratic mean dbh (cm)
            #"QM_DBH_SP1",  # quadratic mean dbh of specie 1 - mixed models
            #"QM_DBH_SP2",  # quadratic mean dbh of specie 2 - mixed models
            #"DOMINANT_DBH",  # Dominant Diameter (cm)
            #"DOMINANT_DBH_SP1",  # dominant diameter os specie 1 (cm) on mixed models
            #"DOMINANT_DBH_SP2",  # dominant diameter os specie 2 (cm) on mixed models     
            #"DOMINANT_SECTION",  # Dominant section (cm)
            #"DOMINANT_SECTION_SP1",  # Dominant section (cm) of specie 1 on a mix plot - mixed models
            #"DOMINANT_SECTION_SP2",  # Dominant section (cm) of specie 2 on a mix plot - mixed models

            # Basic plot variables calculated - height
            #"H_MAX",  # Maximal Height (m)
            #"H_MAX_SP1",  # Maximal Height (m) of specie 1 on a mix plot - mixed models
            #"H_MAX_SP2",  # Maximal Height (m) of specie 2 on a mix plot - mixed models
            #"H_MIN",  # Minimal Height (m)    
            #"H_MIN_SP1",  # Minimal Height (m) of specie 1 on a mix plot - mixed models
            #"H_MIN_SP2",  # Minimal Height (m) of specie 2 on a mix plot - mixed models
            #"MEAN_H",  # Mean height (m)
            #"MEAN_H_SP1",  # Mean height (m) of specie 1 on a mix plot - mixed models
            #"MEAN_H_SP2",  # Mean height (m) of specie 2 on a mix plot - mixed models
            #"DOMINANT_H",  # Dominant height (m)
            #"DOMINANT_H_SP1",  # dominant height of specie 1 - mixed models
            #"DOMINANT_H_SP2",  # dominant height of specie 2 - mixed models

            # Basic plot variables calculated - crown
            #"CROWN_MEAN_D",  # Mean crown diameter (m)
            #"CROWN_MEAN_D_SP1",  # Mean crown diameter (m) for specie 1
            #"CROWN_MEAN_D_SP2",  # Mean crown diameter (m) for specie 2    
            #"CROWN_DOM_D",  # Dominant crown diameter (m)
            #"CROWN_DOM_D_SP1",  # Dominant crown diameter (m) for specie 1
            #"CROWN_DOM_D_SP2",  # Dominant crown diameter (m) for specie 2    
            #"CANOPY_COVER",  # Canopy cover (%)
            #"CANOPY_COVER_SP1",  # Canopy cover (%) for specie 1
            #"CANOPY_COVER_SP2",  # Canopy cover (%) for specie 2        
            "CANOPY_VOL",  # Canopy volume (m3)   
            "CANOPY_VOL_SP1",  # Canopy volume (m3) for specie 1
            "CANOPY_VOL_SP2",  # Canopy volume (m3) for specie 2        

            # Basic plot variables calculated - plot
            #"SLENDERNESS_MEAN",  # slenderness calculated by using mean values of height and dbh (cm/cm)
            #"SLENDERNESS_DOM",  # slenderness calculated by using top height and dbh values (cm/cm)  
            #"REINEKE",  # Reineke Index or Stand Density Index - SDI
            #"REINEKE_SP1",  # reineke index for specie 1 on mixed models
            #"REINEKE_SP2",  # reineke index for specie 2 on mixed models
            "REINEKE_MAX",  # maximal reineke index
            #"REINEKE_MAX_SP1",  # maximal reineke index for specie 1 on mixed models
            #"REINEKE_MAX_SP2",  # maximal reineke index for specie 2 on mixed models
            #"HART",  # Hart-Becking Index (S) calculated to simple rows 
            #"HART_STAGGERED",  # Hart-Becking Index (S) calculated to staggered rows 
            "SI",  # Site index (m)
            "REF_SI_AGE",  # SI reference age (years)
            #"REINEKE_VALUE"  # r contstant value of SDI  to the specie of the model (-1.605 as default)
            "HEGYI_RADIUS",  # radius value to calculate the Hegyi competition index (m)

             # Plot variables calculated - volume and biomass
            #"VOL",  # Volume (m3/ha)
            #"BOLE_VOL",  # Volume under bark (m3/ha)
            #"BARK_VOL",  # Bark Volume (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume harvested percentage (%)
            #"DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
            "ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - volume for mixed models
            #"VOL_SP1",  # Volume (m3/ha)
            #"BOLE_VOL_SP1",  # Volume under bark (m3/ha)
            #"BARK_VOL_SP1",  # Bark Volume (m3/ha) 
            #"VOL_SP2",  # Volume (m3/ha)
            #"BOLE_VOL_SP2",  # Volume under bark (m3/ha)
            #"BARK_VOL_SP2",  # Bark Volume (m3/ha)     

            # Plot variables calculated - wood uses
            #"UNWINDING",  # Unwinding = the useful wood volume unwinding destiny (m3/ha)
            #"VENEER",  # Veneer = the useful wood volume veneer destiny (m3/ha)
            #"SAW_BIG",  # Saw big =) the useful wood volume big saw destiny (m3/ha)
            #"SAW_SMALL",  # Saw small = the useful wood volume small saw destiny (m3/ha)
            #"SAW_CANTER",  # Saw canter = the useful wood volume canter saw destiny (m3/ha)
            #"POST",  # Post = the useful wood volume post destiny (m3/ha)
            #"STAKE",  # Stake = the useful wood volume stake destiny (m3/ha)
            #"CHIPS",  # Chips = the useful wood volume chips destiny (m3/ha)

            # 'UNWINDING_SP1',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
            # 'VENEER_SP1',  # veneer = the useful wood volume veneer destiny (m3/ha)
            #'SAW_BIG_SP1',  # saw_big = the useful wood volume big saw destiny (m3/ha)
            #'SAW_SMALL_SP1',  # saw_small = the useful wood volume small saw destiny (m3/ha)
            #'SAW_CANTER_SP1',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
            # 'POST_SP1',  # post = the useful wood volume post destiny (m3/ha)
            # 'STAKE_SP1',  # stake = the useful wood volume stake destiny (m3/ha)
            #'CHIPS_SP1',  # chips = the useful wood volume chips destiny (m3/ha)
            
            #'UNWINDING_SP2',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
            #'VENEER_SP2',  # veneer = the useful wood volume veneer destiny (m3/ha)
            #'SAW_BIG_SP2',  # saw_big = the useful wood volume big saw destiny (m3/ha)
            #'SAW_SMALL_SP2',  # saw_small = the useful wood volume small saw destiny (m3/ha)
            #'SAW_CANTER_SP2',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
            #'POST_SP2',  # post = the useful wood volume post destiny (m3/ha)
            #'STAKE_SP2',  # stake = the useful wood volume stake destiny (m3/ha)
            #'CHIPS_SP2',  # chips = the useful wood volume chips destiny (m3/ha)

            # Plot variables calculated - biomass
            "WSW",  # wsw = stem wood (Tn/ha)
            "WSB",  # wsb = stem bark (Tn/ha)
            "WSWB",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            "WB2_7",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB",  # wdb = dead branches biomass (Tn/ha)
            "WL",  # wl = leaves (Tn/ha)
            "WTBL",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            # "WR",  # wr = roots (Tn/ha)
            # "WT",  # wt = total biomass (Tn/ha)
            # "WT_CUT_VOLUME",  # WT of the cut trees after a cut process (%)
            # "DEAD_WT",  # WT of the dead trees after an execution (Tn/ha)
            # "ING_WT",  # WT of the ingrowth trees after an execution (Tn/ha)

            # Plot variables calculated - biomass for mixed models
            "WSW_SP1",  # wsw = stem wood (Tn/ha)
            "WSB_SP1",  # wsb = stem bark (Tn/ha)
            "WSWB_SP1",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP1",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP1",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            "WB2_7_SP1",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP1",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB_SP1",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP1",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7_SP1",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP1",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP1",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP1",  # wl = leaves (Tn/ha)
            "WTBL_SP1",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7_SP1",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            # "WR_SP1",  # wr = roots (Tn/ha)
            # "WT_SP1",  # wt = total biomass (Tn/ha)
            "WSW_SP2",  # wsw = stem wood (Tn/ha)
            "WSB_SP2",  # wsb = stem bark (Tn/ha)
            "WSWB_SP2",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP2",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP2",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            "WB2_7_SP2",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP2",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB_SP2",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP2",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7_SP2",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP2",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP2",  # wl = leaves (Tn/ha)
            "WTBL_SP2",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7_SP2",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            # "WR_SP2",  # wr = roots (Tn/ha)
            # "WT_SP2",  # wt = total biomass (Tn/ha)

            # Quercus suber special variables
            "W_CORK",  # fresh cork biomass (Tn/ha)
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
            "MUSHROOM_PRODUCTIVITY",  # total fresh-weight mushroom productivity (kg fw/ha)

            # Cistus ladanifer special variables
            'TIME_AT',  # Time_AT  # time after treatment (years)
            'B_EDULIS',  # B_edulis  # annual yield of B. edulis sporocarps (kg/ha*year)
            'MYCOD',  # MycoD  # Shannon diversity index of mycorrhizal taxa
            'MYCOP',  # MycoP  # Annual mushroom yield from all mycorrhizal species (kg/ha*year)
            'SAPROD',  # SaproD  # Shannon diversity index of saprotrophic fungi
            'SAPROP',  # SaproP  # annual mushroom yield of saprotrophic species (kg/ha*year)

            # Auxiliar variables for future models - 11/08/2023
            'PLOT_VAR1',
            'PLOT_VAR2',
            'PLOT_VAR3',
            'PLOT_VAR4',
            'PLOT_VAR5',
            'PLOT_VAR6',
            'PLOT_VAR7',
            'PLOT_VAR8',
            'PLOT_VAR9',
            'PLOT_VAR10',
            'PLOT_VAR11',
            'PLOT_VAR12',
            'PLOT_VAR13',
            'PLOT_VAR14',
            'PLOT_VAR15',
            'PLOT_VAR16',
            'PLOT_VAR17',
            'PLOT_VAR18',
            'PLOT_VAR19',
            'PLOT_VAR20',
            'PLOT_VAR21',
            'PLOT_VAR22',
            'PLOT_VAR23',
            'PLOT_VAR24',
            'PLOT_VAR25',
            'PLOT_VAR26',
            'PLOT_VAR27',
            'PLOT_VAR28',
            'PLOT_VAR29',
            'PLOT_VAR30',
            'PLOT_VAR31',
            'PLOT_VAR32',
            'PLOT_VAR33',
            'PLOT_VAR34',
            'PLOT_VAR35',
            'PLOT_VAR36',
            'PLOT_VAR37',
            'PLOT_VAR38',
            'PLOT_VAR39',
            'PLOT_VAR40',
            'PLOT_VAR41',
            'PLOT_VAR42',
            'PLOT_VAR43',
            'PLOT_VAR44',
            'PLOT_VAR45',
            'PLOT_VAR46',
            'PLOT_VAR47',
            'PLOT_VAR48',
            # 'UNWINDING_SP3',
            # 'VENEER_SP3',
            # 'SAW_BIG_SP3',
            # 'SAW_SMALL_SP3',
            # 'SAW_CANTER_SP3',
            # 'POST_SP3',
            # 'STAKE_SP3',
            # 'CHIPS_SP3',
            #'VOL_SP3',
            #'BOLE_VOL_SP3',
            #'BARK_VOL_SP3',
            # 'CARBON_STEM_SP1',
            # 'CARBON_BRANCHES_SP1',
            # 'CARBON_ROOTS_SP1',
            # 'CARBON_SP1',
            # 'CARBON_STEM_SP2',
            # 'CARBON_BRANCHES_SP2',
            # 'CARBON_ROOTS_SP2',
            # 'CARBON_SP2',
            # 'CARBON_STEM_SP3',
            # 'CARBON_BRANCHES_SP3',
            # 'CARBON_ROOTS_SP3',
            # 'CARBON_SP3',
            # 'WS_SP3',
            # 'WB_SP3',
            # 'WR_SP3',
            # 'WT_SP3',
            # 'WS_SP2',
            # 'WB_SP2',
            # 'WS_SP1',
            # 'WB_SP1',
            # 'CARBON_STEM',
            # 'CARBON_BRANCHES',
            # 'CARBON_ROOTS',
            # 'WB',
            # 'WS',
            'ZPCUM9',
            'ZPCUM8',
            'ZPCUM7',
            'ZPCUM6',
            'ZPCUM5',
            'ZPCUM4',
            'ZPCUM3',
            'ZPCUM2',
            'ZPCUM1',
            'ZQ95',
            'ZQ90',
            'ZQ85',
            'ZQ80',
            'ZQ75',
            'ZQ70',
            'ZQ65',
            'ZQ60',
            'ZQ55',
            'ZQ50',
            'ZQ45',
            'ZQ40',
            'ZQ35',
            'ZQ30',
            'ZQ25',
            'ZQ20',
            'ZQ15',
            'ZQ10',
            'ZQ5',
            'PZABOVE2',
            'PZABOVEZMEAN',
            'ZENTROPY',
            'ZKURT',
            'ZSKEW',
            'ZSD',
            'ZMEAN',
            'ZMAX',
            # 'SP3_N_PROPORTION',
            # 'SP2_N_PROPORTION',
            # 'SP1_N_PROPORTION',
            # 'BASAL_AREA_SP3',
            # 'QM_DBH_SP3',
            # 'DENSITY_SP3',
            # 'MEAN_H_SP3',
            # 'H_MIN_SP3',
            # 'H_MAX_SP3',
            # 'MEAN_DBH_SP3',
            # 'DBH_MIN_SP3',
            # 'DBH_MAX_SP3',
            # 'MEAN_BA_SP3',
            # 'BA_MIN_SP3',
            # 'BA_MAX_SP3',
            # 'DOMINANT_SECTION_SP3',
            # 'DOMINANT_DBH_SP3',
            # 'DOMINANT_H_SP3',
            # 'CARBON_HEARTWOOD',
            # 'CARBON_SAPWOOD',
            # 'CARBON_BARK',
            'DEADWOOD_INDEX_CESEFOR_G',
            'DEADWOOD_INDEX_CESEFOR_V',
            'SAW_BIG_LIFEREBOLLO',
            'SAW_SMALL_LIFEREBOLLO',
            'STAVES_INTONA',
            'BOTTOM_STAVES_INTONA',
            'WOOD_PANELS_GAMIZ',
            'MIX_GARCIA_VARONA',
            # 'CARBON',
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

            # Remarkable variables and basic variables measured
            #"specie",
            #"tree_age",
            #"bearing",  # bearing from the tree to the central point of the plot ('rumbo')
            #"distance",  # distance from the tree to the central point of the plot    
            #"expan",  # expansion factor
            "dbh_1",  # dbh measurement 1 (cm)
            "dbh_2",  # dbh measurement 2 (cm)
            #"dbh",  # diameter at breast height (cm)
            #'dbh_i",  # increment dbh (cm)
            #"height",  # total tree height (m)
            #"height_i",  # increment tree height (m)
            "stump_h",   # stump height (m))
            "bark_1",  # bark thickness, measurement 1 (mm)
            "bark_2",  # bark thickness, measurement 2 (mm)
            "bark",  # mean bark thickness (mm)

           # Basic variables calculated
            #"basal_area",   # basal area (cm2)
            #"basal_area_i",   # increment basal area (cm2)
            #"basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
            #"basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
            #"bal",  # cumulative basal area (m2/ha)
            #"bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            #"bal_intersp",  # intraspecific bal (m2/ha) for mixed models
            #"ba_ha",  # basal area per ha (m2/ha) 
            #"normal_circumference",  # circumference at breast height (cm)
            #"slenderness",  # slenderness (cm/cm)
            
            # Crown variables
            #"cr",  # crown ratio (%)
            #"lcw",  #  largest crown width (m)
            #"hcb",  # height of the crown base (m)
            #"hlcw",  # height of the largest crown width (m)
            "cpa",  # crown projection area (m2)
            "crown_vol",  # crown volume (m3)

            # Volume variables
            #"vol",  # volume over bark (dm3)
            #"bole_vol",  # volume under bark (dm3)
            #"bark_vol",  # bark volume (dm3)
            "firewood_vol",  # firewood volume (dm3)
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
            # "wsw",  # wsw = stem wood (kg)
            # "wsb",  # wsb = stem bark (kg)
            # "wswb",  # wswb = stem wood and stem bark (kg)
            # "w_cork",  # fresh cork biomass (kg)
            # "wthickb",  # wthickb = Thick branches > 7 cm (kg)
            # "wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            # "wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
            # "wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            # "wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
            # "wb05",  # wb05 = thinnest branches (< 0.5 cm) (kg)
            # "wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
            # "wb0_2",  # wb0_2 = branches < 2 cm (kg)
            # "wdb",  # wdb = dead branches biomass (kg)
            # "wl",  # wl = leaves (kg)
            # "wtbl",  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            # "wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
            # "wr",  # wr = roots (kg)
            # "wt",  # wt = total biomass (kg)
            
            # Competition information
            "hegyi",  # Hegyi competition index calculation

            # Quercus suber special variables
            "dbh_oc",  # dbh over cork (cm) - Quercus suber
            "h_debark",  # uncork height on the main stem (m) - Quercus suber
            "nb",  # number of the main boughs stripped - Quercus suber
            "cork_cycle",  # moment to obtain cork data; 0 to the moment just immediately before the stripping process
            "count_debark",  # number of debarking treatments applied 
            "total_w_debark",  # w cork accumulator to all the scenario (kg)
            "total_v_debark",  # v cork accumulator to all the scenario (dm3)

            # Pinus pinea special variables
            "all_cones",  # number of all the cones of the tree (anual mean)
            "sound_cones",  # number of healthy cones in a tree (anual mean)
            "sound_seeds",  # total sound seeds of the tree (anual mean)
            "w_sound_cones",  # weight of sound (healthy) cones (kg) (anual mean)
            "w_all_cones",  # weight of all (healthy and not) cones (kg) (anual mean)
    
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

            # Vorest model variables
            'w_voronoi',  # weights used to construct the Voronoi diagrams 
            'neighbours_mean_dbh',  # mean dbh of the neighbour trees     
            'ogs',  # occupied growing space of tree i in year t, computed as the area of the weighted Voronoi region of the tree i restricted by the range of its zone of influence (radius) at time t
            'ags',  # area in its surroundings not occupied by neighboring trees and therefore available to that tree to search for light
            'pgs',  # potential growing space of tree i in year t estimated as the crown projection area of an open grown tree of the same dbh
            'rel_area',  # ratio of the occupied growing space (OGS) of a tree and its potential growing space (PGS) and it is used as a surrogate for the growing capacity of a tree

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
            "coord_z",

            # Auxiliar variables for future models - 11/08/2023
            'tree_var1',
            'tree_var2',
            'tree_var3',
            'tree_var4',
            'tree_var5',
            'tree_var6',
            'tree_var7',
            'tree_var8',
            'tree_var9',
            'tree_var10',
            'tree_var11',
            'tree_var12',
            'tree_var13',
            'tree_var14',
            'tree_var15',
            'tree_var16',
            'tree_var17',
            'tree_var18',
            'tree_var19',
            'tree_var20',
            'tree_var21',
            'tree_var22',
            'tree_var23',
            'tree_var24',
            'tree_var25',
            'tree_var26',
            'tree_var27',
            'tree_var28',
            'tree_var29',
            'tree_var30',
            'tree_var31',
            'tree_var32',
            'tree_var33',
            'tree_var34',
            'tree_var35',
            'tree_var36',
            'tree_var37',
            'tree_var38',
            'tree_var39',
            'tree_var40',
            'tree_var41',
            'tree_var42',
            'tree_var43',
            'tree_var44',
            'tree_var45',
            'tree_var46',
            'tree_var47',
            'tree_var48',
            # 'carbon_stem',
            # 'carbon_branches',
            # 'carbon_roots',
            # 'wb',
            # 'ws',
            # 'carbon_heartwood',
            # 'carbon_sapwood',
            # 'carbon_bark',
            'saw_big_liferebollo',
            'saw_small_liferebollo',
            'staves_intona',
            'bottom_staves_intona',
            'wood_panels_gamiz',
            'mix_garcia_varona',
            # 'carbon',
        ]

        Variables.remove_var_plot(delete_from_plot)
        Variables.remove_var_tree(delete_from_tree)
        
MixedModelsSpain.vars()
