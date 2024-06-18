# /usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
#
# Single tree growing model independent from distance, developed to
# Mixed stands of Pinus sylvestris and Quercus petraea located on Spain
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


class PsylvestrisQpetraeaMix(TreeModel):

    def __init__(self, configuration=None):
        super().__init__(name="PsylvestrisQpetraeaMix", version=1)


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
        
            Model.model_name = 'tree_template'  # set the model name to show it at the output
            Model.specie_ifn_id = ''  # Set the model specie ID to mark the trees of different species         
            Model.exec_time = 5  # recommended executions time to use that model
            Model.aplication_area = 'Spain'  # area recommended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = 'all'  # provenance regions recommended to use the model
            Model.model_type = 'under_development'  # SIMANFOR model type. It can be: ('' is neccesary)
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'link'  # link to model card in english
            Model.model_card_es = 'link'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps of information at the initial inventory
        SDImax equations:
            Doc.: de Prado, DR, San Martín R, Bravo F, de Aza CH (2020). Potential climatic influence on maximum stand carrying capacity for 15 Mediterranean coniferous and broadleaf species. Forest Ecology and Management, 460, 117824
            Ref.: de Prado et al (2020)
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('            Running: Pinus sylvestris - Quercus petraea mixed model (Spain). Plot:', plot.plot_id        )
        print('#--------------------------------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced

            self.model_info()
            plot.add_value('REINEKE_VALUE', -1.605)  # r constant value of SDI to the species of the model (-1.605 as default)
            other_trees = total_trees = 0  # variables to count the number of trees from a different species that the principal one and the total of trees

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            M = bal = bal_sp1 = bal_sp2 = g_sp1 = g_sp2 = N_sp1 = N_sp2 = dg_sp1 = dg_sp2 = beta0 = beta1 = 0
            dbh_sp1 = max_dbh_sp1 = max_h_sp1 = max_ba_sp1 = h_sp1 = dbh_sp2 = max_dbh_sp2 = max_h_sp2 = max_ba_sp2 = h_sp2 = 0
            min_dbh_sp1 = min_ba_sp1 = min_h_sp1 = min_dbh_sp2 = min_ba_sp2 = min_h_sp2 = 9999

            #------------------------------ MARTONNE INDEX ------------------------------#

            M = TreeModel.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))

            #---------------------------- TREES CALCULATION -----------------------------#

            # Specie 1 = Pinus sylvestris (21) 
            # Specie 2 = Quercus petraea (42) 

            # First of all, g and g/ha are calculated to order the trees by using that variable

            for tree in plot_trees:  # for each tree...

                tree.add_value('basal_area', math.pi*(tree.dbh/2)**2)  # basal area (cm2)
                tree.add_value('ba_ha', tree.basal_area*tree.expan/10000)  # basal area per ha (m2/ha)


            plot_trees: list[Tree] = plot.short_trees_on_list('ba_ha', DESC)  # establish an order to calculate tree variables


            for tree in plot_trees:  # for each tree...

                total_trees += 1

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                    #--------------------------------- BAL --------------------------------------#

                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)

                    tree.add_value('bal_intrasp', bal_sp1)  # bal value for specie 1 (m2/ha)
                    tree.add_value('bal_intersp', bal_sp2)  # bal value for specie 2 (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                    bal_sp1 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable

                    #-------------------------------- HEIGHT ------------------------------------#

                    #if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                    #    beta0 = 1.3877
                    #    h_sp1 = 1.3 + (beta0*(1/tree.dbh - 1/plot.dominant_dbh) + (1/(plot.dominant_h - 1.3))**(1/3)**(-3))
                    #    tree.add_value('height', h_sp1)

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal circumference (cm)

                    #------------------ ACCUMULATORS, MAX, MIN, MEAN VALUES ---------------------#

                    N_sp1 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                    dg_sp1 += math.pow(tree.dbh, 2)*tree.expan  # accumulator to calculate dg per specie
                    g_sp1 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable (m2/ha)
                    dbh_sp1 += tree.dbh*tree.expan  # accumulator to calculate mean dbh per specie
                    h_sp1 += tree.height*tree.expan  # accumulator to calculate mean height per specie
                    
                    max_dbh_sp1 = tree.dbh if tree.dbh > max_dbh_sp1 else max_dbh_sp1
                    min_dbh_sp1 = tree.dbh if tree.dbh < min_dbh_sp1 else min_dbh_sp1

                    max_h_sp1 = tree.height if tree.height > max_h_sp1 else max_h_sp1
                    min_h_sp1 = tree.height if tree.height < min_h_sp1 else min_h_sp1

                    max_ba_sp1 = tree.basal_area if tree.basal_area > max_ba_sp1 else max_ba_sp1
                    min_ba_sp1 = tree.basal_area if tree.basal_area < min_ba_sp1 else min_ba_sp1

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    #self.crown(tree, plot, 'initialize')  # activate crown variables

                    self.vol(tree, plot)  # activate volume variables

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    self.merchantable(tree, plot)  # activate wood uses variables

                    self.biomass(tree, plot)  # activate biomass variables
                

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    #--------------------------------- BAL --------------------------------------#
                    
                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)

                    tree.add_value('bal_intrasp', bal_sp2)  # bal value for specie 1 (m2/ha)
                    tree.add_value('bal_intersp', bal_sp1)  # bal value for specie 2 (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                    bal_sp2 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable

                    #-------------------------------- HEIGHT ------------------------------------#

                    #if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                    #    beta1 = - 0.3962*plot.qm_dbh_sp2 + 0.3045*M + 1.1670*plot.dominant_h_sp2
                    #    beta2 = - 9.1325
                    #    h_sp2 = 1.3 + (beta1*math.exp(beta2/tree.dbh))
                    #    tree.add_value('height', h_sp2)

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal circumference (cm)

                    #------------------ ACCUMULATORS, MAX, MIN, MEAN VALUES ---------------------#

                    N_sp2 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                    dg_sp2 += math.pow(tree.dbh, 2)*tree.expan  # accumulator to calculate dg per specie
                    g_sp2 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable (m2/ha)
                    dbh_sp2 += tree.dbh*tree.expan  # accumulator to calculate mean dbh per specie
                    h_sp2 += tree.height*tree.expan  # accumulator to calculate mean height per specie
                    
                    max_dbh_sp2 = tree.dbh if tree.dbh > max_dbh_sp2 else max_dbh_sp2
                    min_dbh_sp2 = tree.dbh if tree.dbh < min_dbh_sp2 else min_dbh_sp2

                    max_h_sp2 = tree.height if tree.height > max_h_sp2 else max_h_sp2
                    min_h_sp2 = tree.height if tree.height < min_h_sp2 else min_h_sp2

                    max_ba_sp2 = tree.basal_area if tree.basal_area > max_ba_sp2 else max_ba_sp2
                    min_ba_sp2 = tree.basal_area if tree.basal_area < min_ba_sp2 else min_ba_sp2

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    #self.crown(tree, plot, 'initialize')  # activate crown variables

                    self.vol(tree, plot)  # activate volume variables

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    self.merchantable(tree, plot)  # activate wood uses variables

                    self.biomass(tree, plot)  # activate biomass variables


                else:
                    other_trees += 1
    

            if other_trees != 0:
                print(' ')
                print(other_trees, 'of the total', total_trees, 'trees are from a different species than the principal')
                print('That trees will be shown underlined at the output, and they will be maintained at simulations, not applying model equations over them.')
                print(' ')
                if other_trees == total_trees:
                    Warnings.specie_error_trees = 1


            #-------------------------------- PLOTS -------------------------------------#

            #---------------------------- Ho by specie ----------------------------------#

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate plot variables

            selection_trees_sp1 = list()
            selection_trees_sp2 = list()
            tree_expansion_sp1 = tree_expansion_sp2 = 0

            for tree in plot_trees:  # for each tree...

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition
                    tree.add_value('basal_area_intrasp', g_sp1)  # add both basal area intra- and interspecific (m2/ha)
                    tree.add_value('basal_area_intersp', g_sp2)

                    if tree_expansion_sp1 < 100:  # select trees list, by species, to calculate Ho of each group
                        tree_expansion_sp1 += tree.expan
                        selection_trees_sp1.append(tree)

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    tree.add_value('basal_area_intrasp', g_sp2)  # add both basal area intra- and interspecific (m2/ha)
                    tree.add_value('basal_area_intersp', g_sp1)

                    if tree_expansion_sp2 < 100:  # select trees list, by species, to calculate Ho of each group
                        tree_expansion_sp2 += tree.expan
                        selection_trees_sp2.append(tree)


            plot.add_value('DOMINANT_H_SP1', Plot.get_dominant_height(plot, selection_trees_sp1))
            plot.add_value('DOMINANT_DBH_SP1', Plot.get_dominant_diameter(plot, selection_trees_sp1))
            plot.add_value('DOMINANT_SECTION_SP1', Plot.get_dominant_section(plot, selection_trees_sp1))
            plot.add_value('DOMINANT_H_SP2', Plot.get_dominant_height(plot, selection_trees_sp2))               
            plot.add_value('DOMINANT_DBH_SP2', Plot.get_dominant_diameter(plot, selection_trees_sp2))   
            plot.add_value('DOMINANT_SECTION_SP2', Plot.get_dominant_section(plot, selection_trees_sp2))            

            #--------------------- min, max, mean values per specie ---------------------#

            if N_sp1 != 0:  # if there are trees from that species, data is calculated; else, values will be empty
                plot.add_value('BA_MAX_SP1', max_ba_sp1)
                plot.add_value('DBH_MAX_SP1', max_dbh_sp1)
                plot.add_value('H_MAX_SP1', max_h_sp1)            
                plot.add_value('BA_MIN_SP1', min_ba_sp1)
                plot.add_value('DBH_MIN_SP1', min_dbh_sp1)
                plot.add_value('H_MIN_SP1', min_h_sp1)
                plot.add_value('MEAN_BA_SP1', g_sp1*10000/N_sp1)
                plot.add_value('MEAN_DBH_SP1', dbh_sp1/N_sp1)
                plot.add_value('MEAN_H_SP1', h_sp1/N_sp1)               

            if N_sp2 != 0:
                plot.add_value('BA_MAX_SP2', max_ba_sp2)
                plot.add_value('DBH_MAX_SP2', max_dbh_sp2)
                plot.add_value('H_MAX_SP2', max_h_sp2)            
                plot.add_value('BA_MIN_SP2', min_ba_sp2)
                plot.add_value('DBH_MIN_SP2', min_dbh_sp2)
                plot.add_value('H_MIN_SP2', min_h_sp2) 
                plot.add_value('MEAN_BA_SP2', g_sp2*10000/N_sp2)
                plot.add_value('MEAN_DBH_SP2', dbh_sp2/N_sp2)
                plot.add_value('MEAN_H_SP2', h_sp2/N_sp2)

            #-------------------- other calculations by specie --------------------------#

            plot.add_value('DENSITY_SP1', N_sp1)
            plot.add_value('DENSITY_SP2', N_sp2)

            if N_sp1 != 0:
                qm_dbh_sp1 = math.sqrt(dg_sp1/N_sp1)
            else:
                qm_dbh_sp1 = 0
            plot.add_value('QM_DBH_SP1', qm_dbh_sp1)

            if N_sp2 != 0:
                qm_dbh_sp2 = math.sqrt(dg_sp2/N_sp2)
            else:
                qm_dbh_sp2 = 0
            plot.add_value('QM_DBH_SP2', qm_dbh_sp2)        

            plot.add_value('BASAL_AREA_SP1', g_sp1)
            plot.add_value('BASAL_AREA_SP2', g_sp2)   


            #---------------------- Martonne, SDImax and SDI ----------------------------#

            # Calculate both SDImax values
            SDImax_1 = math.exp(12.579 + ((-1.7462 + 0.0007*M)*math.log(25)))
            plot.add_value('REINEKE_MAX_SP1', SDImax_1)
            SDImax_2 = math.exp(12.277 - 1.6777*math.log(25))
            plot.add_value('REINEKE_MAX_SP2', SDImax_2)


            # Calculate both SDI values
            if plot.qm_dbh_sp1 != 0:
                SDI_1 = plot.density_sp1*((25/plot.qm_dbh_sp1)**(-1.7462 + 0.0007*M))
            else:
                SDI_1 = 0
            plot.add_value('REINEKE_SP1', SDI_1)

            if plot.qm_dbh_sp2 != 0:
                SDI_2 = plot.density_sp2*((25/plot.qm_dbh_sp2)**(-1.6777))
            else:
                SDI_2 = 0
            plot.add_value('REINEKE_SP2', SDI_2)
         

            # Calculate species proportions
            plot.add_value('SP1_PROPORTION', plot.reineke_sp1/(plot.reineke_sp1 + (plot.reineke_sp2 * (plot.reineke_max_sp1/plot.reineke_max_sp2))))
            plot.add_value('SP2_PROPORTION', (plot.reineke_sp2 * (plot.reineke_max_sp1/plot.reineke_max_sp2))/(plot.reineke_sp1 + (plot.reineke_sp2 * (plot.reineke_max_sp1/plot.reineke_max_sp2))))         

            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables  


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

        if int(tree.specie) == int(plot.id_sp1):  # specie condition
            if plot.reineke_sp1 > plot.reineke_max_sp1:  # SDI condition
                return 0.98  # reduce a 2% of the tree expan (2% of the total plot density)
            else:
                return 1  # the tree survives

        elif int(tree.specie) == int(plot.id_sp2):  # specie condition
            if plot.reineke_sp2 > plot.reineke_max_sp2:  # SDI condition
                return 0.98  # reduce a 2% of the tree expan
            else:
                return 1  # the tree survives


    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Tree growth function.
        A function that updates dbh and h by using growth equations, and also update age, g, and v to the new situation.
        """

        try:  # errors inside that construction will be announced

            bai5_sp1 = bai5_sp2 = beta0 = beta1 = beta2 = h_sp1 = h_sp2 = 0

            new_tree.sum_value('tree_age', time)

            # Select the Martonne Index corresponding to the new year of the plot

            new_year = plot.year + time  # time is automatically updated after the execution process

            M = TreeModel.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))

            if int(old_tree.specie) == int(plot.id_sp1):  # specie 1 condition

                bai5_sp1 = math.exp(-0.0273 + 1.2849*math.log(old_tree.dbh) + 0.0264*old_tree.height - 0.0158*old_tree.basal_area_intrasp)
                new_tree.sum_value("basal_area", bai5_sp1)  # update basal area (cm2) 

                new_tree.add_value('dbh', 2*math.sqrt(new_tree.basal_area/math.pi))  # upload dbh (cm)

                beta0 = 1.3877
                h_sp1 = 1.3 + (beta0*(1/new_tree.dbh - 1/plot.dominant_dbh) + (1/(plot.dominant_h - 1.3))**(1/3))**(-3)
                new_tree.add_value("height", h_sp1)  # upload height (m)

                #self.vol(new_tree, plot)  # update volume variables (dm3)

            elif int(old_tree.specie) == int(plot.id_sp2):  # specie 2 condition

                bai5_sp2 = math.exp(-1.5479 - 0.0401*old_tree.dbh + 1.8118*math.log(old_tree.dbh) + 0.0827*old_tree.height - 0.0522*old_tree.basal_area_intrasp)
                new_tree.sum_value("basal_area", bai5_sp2)  # update basal area (cm2) 

                new_tree.add_value('dbh', 2*math.sqrt(new_tree.basal_area/math.pi))  # upload dbh (cm)

                beta1 = plot.qm_dbh_sp2**(- 0.3962)*M**(0.3045)*plot.dominant_h_sp2**(1.1670)
                beta2 = - 9.1325
                h_sp2 = 1.3 + (beta1*math.exp(beta2/new_tree.dbh))
                new_tree.add_value("height", h_sp2)  # upload height (m)

                #self.vol(new_tree, plot)  # update volume variables (dm3)

        except Exception:
            self.catch_model_exception()


    def ingrowth(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated is calculated. The next function will order how to divide that basal area into the different diametric classes.
        """

        #try:  # errors inside that construction will be announced

        #except Exception:
        #    self.catch_model_exception()

        return 0


    def ingrowth_distribution(self, time: int, plot: Plot, area: float):
        """
        Tree diametric classes distribution.
        That function must return a list with different sublists for each diametric class, where the conditions to ingrowth function are written.
        That function has the aim to divide the ingrowth (added basal area of ingrowth function) in different proportions depending on the orders given.
        In the cases that a model hasn´t a well-known distribution, just return None to share that ingrowth between all the trees of the plot.
        """

        try:  # errors inside that construction will be announced

            distribution = []  # that list will contain the different diametric classes conditions to calculate the ingrowth distribution

            # for each diametric class: [dbh minimum, dbh maximum, proportion of basal area to add (between 0*area and 1*area)]
            # if your first diametric class doesn't start on 0, just create a cd_0 with the diametric range between 0 and minimum of cd_1 without adding values
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
        A function that updates trees and plot information once growth, survival, and ingrowth functions were executed and the plot information was updated.
        The equations on that function are the same that in "initialize" function, so references are the same
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('            Running: Pinus sylvestris - Quercus petraea mixed model (Spain). Plot:', plot.plot_id        )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same as the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:  # errors inside that construction will be announced

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            M = bal = bal_sp1 = bal_sp2 = g_sp1 = g_sp2 = N_sp1 = N_sp2 = dg_sp1 = dg_sp2 = beta0 = beta1 = 0
            dbh_sp1 = max_dbh_sp1 = max_h_sp1 = max_ba_sp1 = h_sp1 = dbh_sp2 = max_dbh_sp2 = max_h_sp2 = max_ba_sp2 = h_sp2 = 0
            min_dbh_sp1 = min_ba_sp1 = min_h_sp1 = min_dbh_sp2 = min_ba_sp2 = min_h_sp2 = 9999

            if 'YEAR' in PLOT_VARS:
                new_year = plot.year + time  # YEAR is automatically updated after the execution process
            if 'AGE' in PLOT_VARS:
                new_age = plot.age + time  # AGE is automatically updated after the execution process

            #------------------------------ MARTONNE INDEX ------------------------------#

            M = TreeModel.choose_martonne(plot.plot_id, plot.year, (2020, 2040, 2060, 2080, 2100))

            #---------------------------- TREES CALCULATION -----------------------------#

            # Specie 1 = Pinus sylvestris (21) 
            # Specie 2 = Quercus petraea (42) 

            # First of all, g and g/ha are calculated to order the trees by using that variable

            for tree in plot_trees:  # for each tree...

                tree.add_value('basal_area', math.pi*(tree.dbh/2)**2)  # basal area (cm2)
                tree.add_value('ba_ha', tree.basal_area*tree.expan/10000)  # basal area per ha (m2/ha)


            plot_trees: list[Tree] = plot.short_trees_on_list('ba_ha', DESC)  # establish an order to calculate tree variables


            for tree in plot_trees:  # for each tree...

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                    #--------------------------------- BAL --------------------------------------#

                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)

                    tree.add_value('bal_intrasp', bal_sp1)  # bal value for specie 1 (m2/ha)
                    tree.add_value('bal_intersp', bal_sp2)  # bal value for specie 2 (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                    bal_sp1 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal circumference (cm)

                    #------------------ ACCUMULATORS, MAX, MIN, MEAN VALUES ---------------------#

                    N_sp1 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                    dg_sp1 += math.pow(tree.dbh, 2)*tree.expan  # accumulator to calculate dg per specie
                    g_sp1 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable (m2/ha)
                    dbh_sp1 += tree.dbh*tree.expan  # accumulator to calculate mean dbh per specie
                    h_sp1 += tree.height*tree.expan  # accumulator to calculate mean height per specie
                    
                    max_dbh_sp1 = tree.dbh if tree.dbh > max_dbh_sp1 else max_dbh_sp1
                    min_dbh_sp1 = tree.dbh if tree.dbh < min_dbh_sp1 else min_dbh_sp1

                    max_h_sp1 = tree.height if tree.height > max_h_sp1 else max_h_sp1
                    min_h_sp1 = tree.height if tree.height < min_h_sp1 else min_h_sp1

                    max_ba_sp1 = tree.basal_area if tree.basal_area > max_ba_sp1 else max_ba_sp1
                    min_ba_sp1 = tree.basal_area if tree.basal_area < min_ba_sp1 else min_ba_sp1

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    #self.crown(tree, plot, 'initialize')  # activate crown variables

                    self.vol(tree, plot)  # activate volume variables

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    self.merchantable(tree, plot)  # activate wood uses variables

                    self.biomass(tree, plot)  # activate biomass variables
                

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    #--------------------------------- BAL --------------------------------------#
                    
                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)

                    tree.add_value('bal_intrasp', bal_sp2)  # bal value for specie 1 (m2/ha)
                    tree.add_value('bal_intersp', bal_sp1)  # bal value for specie 2 (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                    bal_sp2 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal circumference (cm)

                    #------------------ ACCUMULATORS, MAX, MIN, MEAN VALUES ---------------------#

                    N_sp2 += tree.expan  # accumulator to calculate density per specie (trees/ha)
                    dg_sp2 += math.pow(tree.dbh, 2)*tree.expan  # accumulator to calculate dg per specie
                    g_sp2 += tree.basal_area*tree.expan/10000  # accumulator to calculate that plot variable (m2/ha)
                    dbh_sp2 += tree.dbh*tree.expan  # accumulator to calculate mean dbh per specie
                    h_sp2 += tree.height*tree.expan  # accumulator to calculate mean height per specie
                    
                    max_dbh_sp2 = tree.dbh if tree.dbh > max_dbh_sp2 else max_dbh_sp2
                    min_dbh_sp2 = tree.dbh if tree.dbh < min_dbh_sp2 else min_dbh_sp2

                    max_h_sp2 = tree.height if tree.height > max_h_sp2 else max_h_sp2
                    min_h_sp2 = tree.height if tree.height < min_h_sp2 else min_h_sp2

                    max_ba_sp2 = tree.basal_area if tree.basal_area > max_ba_sp2 else max_ba_sp2
                    min_ba_sp2 = tree.basal_area if tree.basal_area < min_ba_sp2 else min_ba_sp2

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    #self.crown(tree, plot, 'initialize')  # activate crown variables

                    self.vol(tree, plot)  # activate volume variables

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    self.merchantable(tree, plot)  # activate wood uses variables

                    self.biomass(tree, plot)  # activate biomass variables


            #-------------------------------- PLOTS -------------------------------------#

            #---------------------------- Ho by specie ----------------------------------#

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate plot variables

            selection_trees_sp1 = list()
            selection_trees_sp2 = list()
            tree_expansion_sp1 = tree_expansion_sp2 = 0

            for tree in plot_trees:  # for each tree...

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition
                    tree.add_value('basal_area_intrasp', g_sp1)  # add both basal area intra- and interspecific (m2/ha)
                    tree.add_value('basal_area_intersp', g_sp2)

                    if tree_expansion_sp1 < 100:  # select trees list, by species, to calculate Ho of each group
                        tree_expansion_sp1 += tree.expan
                        selection_trees_sp1.append(tree)

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    tree.add_value('basal_area_intrasp', g_sp2)  # add both basal area intra- and interspecific (m2/ha)
                    tree.add_value('basal_area_intersp', g_sp1)

                    if tree_expansion_sp2 < 100:  # select trees list, by species, to calculate Ho of each group
                        tree_expansion_sp2 += tree.expan
                        selection_trees_sp2.append(tree)


            plot.add_value('DOMINANT_H_SP1', Plot.get_dominant_height(plot, selection_trees_sp1))
            plot.add_value('DOMINANT_DBH_SP1', Plot.get_dominant_diameter(plot, selection_trees_sp1))
            plot.add_value('DOMINANT_SECTION_SP1', Plot.get_dominant_section(plot, selection_trees_sp1))
            plot.add_value('DOMINANT_H_SP2', Plot.get_dominant_height(plot, selection_trees_sp2))               
            plot.add_value('DOMINANT_DBH_SP2', Plot.get_dominant_diameter(plot, selection_trees_sp2))   
            plot.add_value('DOMINANT_SECTION_SP2', Plot.get_dominant_section(plot, selection_trees_sp2))            

            #--------------------- min, max, mean values per specie ---------------------#

            if N_sp1 != 0:  # if there are trees from that species, data is calculated; else, values will be empty
                plot.add_value('BA_MAX_SP1', max_ba_sp1)
                plot.add_value('DBH_MAX_SP1', max_dbh_sp1)
                plot.add_value('H_MAX_SP1', max_h_sp1)            
                plot.add_value('BA_MIN_SP1', min_ba_sp1)
                plot.add_value('DBH_MIN_SP1', min_dbh_sp1)
                plot.add_value('H_MIN_SP1', min_h_sp1)
                plot.add_value('MEAN_BA_SP1', g_sp1*10000/N_sp1)
                plot.add_value('MEAN_DBH_SP1', dbh_sp1/N_sp1)
                plot.add_value('MEAN_H_SP1', h_sp1/N_sp1)               

            if N_sp2 != 0:
                plot.add_value('BA_MAX_SP2', max_ba_sp2)
                plot.add_value('DBH_MAX_SP2', max_dbh_sp2)
                plot.add_value('H_MAX_SP2', max_h_sp2)            
                plot.add_value('BA_MIN_SP2', min_ba_sp2)
                plot.add_value('DBH_MIN_SP2', min_dbh_sp2)
                plot.add_value('H_MIN_SP2', min_h_sp2) 
                plot.add_value('MEAN_BA_SP2', g_sp2*10000/N_sp2)
                plot.add_value('MEAN_DBH_SP2', dbh_sp2/N_sp2)
                plot.add_value('MEAN_H_SP2', h_sp2/N_sp2)

            #-------------------- other calculations by specie --------------------------#

            plot.add_value('DENSITY_SP1', N_sp1)
            plot.add_value('DENSITY_SP2', N_sp2)

            if N_sp1 != 0:
                qm_dbh_sp1 = math.sqrt(dg_sp1/N_sp1)
            else:
                qm_dbh_sp1 = 0
            plot.add_value('QM_DBH_SP1', qm_dbh_sp1)

            if N_sp2 != 0:
                qm_dbh_sp2 = math.sqrt(dg_sp2/N_sp2)
            else:
                qm_dbh_sp2 = 0
            plot.add_value('QM_DBH_SP2', qm_dbh_sp2)        

            plot.add_value('BASAL_AREA_SP1', g_sp1)
            plot.add_value('BASAL_AREA_SP2', g_sp2)   


            #---------------------- Martonne, SDImax and SDI ----------------------------#

            # Calculate both SDImax values
            SDImax_1 = math.exp(12.579 + ((-1.7462 + 0.0007*M)*math.log(25)))
            plot.add_value('REINEKE_MAX_SP1', SDImax_1)
            SDImax_2 = math.exp(12.277 - 1.6777*math.log(25))
            plot.add_value('REINEKE_MAX_SP2', SDImax_2)


            # Calculate both SDI values
            if plot.qm_dbh_sp1 != 0:
                SDI_1 = plot.density_sp1*((25/plot.qm_dbh_sp1)**(-1.7462 + 0.0007*M))
            else:
                SDI_1 = 0
            plot.add_value('REINEKE_SP1', SDI_1)

            if plot.qm_dbh_sp2 != 0:
                SDI_2 = plot.density_sp2*((25/plot.qm_dbh_sp2)**(-1.6777))
         
            # Calculate species proportions         
            plot.add_value('SP1_PROPORTION', plot.reineke_sp1/(plot.reineke_sp1 + (plot.reineke_sp2 * (plot.reineke_max_sp1/plot.reineke_max_sp2))))
            plot.add_value('SP2_PROPORTION', (plot.reineke_sp2 * (plot.reineke_max_sp1/plot.reineke_max_sp2))/(plot.reineke_sp1 + (plot.reineke_sp2 * (plot.reineke_max_sp1/plot.reineke_max_sp2))))         


            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables  

        except Exception:
            self.catch_model_exception()


    def taper_over_bark(self, tree: Tree, plot: Plot, hr: float):
        """
        Taper equation over bark function.
        A function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source (Psyl):
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        Source (Qpet):
            Doc.: Ecuaciones de perfil para las especies de roble albar (Quercus petraea (Matt.) Liebl.) y rebollo (Quercus pyrenaica Willd) en la comarca de la “Castillería” en el Norte de la provincia de Palencia 
            Ref.: Manríquez-González et al, 2017
        """

        try:  # errors inside that construction will be announced

            if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                # a) Stud model

                # dob = (1 + 0.4959 * 2.7182818284 ** (-14.2598 * hr)) * 0.8474 * tree.dbh * pow((1 - hr), (0.6312 - 0.6361 * (1 - hr)))
                
                # b) Fang model

                ao = 0.000051
                a1 = 1.845867
                a2 = 1.045022
                b1 = 0.000011
                b2 = 0.000038
                b3 = 0.000030
                p1 = 0.093625
                p2 = 0.763750

                hst = 0.0  # stump height (m) --> 0.2 on merchantable function
                ht = tree.height
                h = ht - hst  # height from stump to comercial diameter (m)
                dbh = tree.dbh
                k = math.pi / 40000
                alpha1 = (1 - p1) ** (((b2 - b1) * k) / (b1 * b2))
                alpha2 = (1 - p2) ** (((b3 - b2) * k) / (b2 * b3))

                if isinstance(hr, float) == False:  # on the cases where hr is an array...
                    I1 = []  # we create two lists of values
                    I2 = []
                    for i in hr:  # for each hr value, we calculate the values of the other 2 parameters
                        if p1 <= i and i <= p2:
                            a = 1
                        else:
                            a = 0
                        if p2 <= i and i <= 1:
                            b = 1
                        else:
                            b = 0
                        I1.append(a)  # we add the parameters to the lists
                        I2.append(b)
                    I1 = np.array(I1)  # when the lists are full, we transform the list into an array to simplify the following calculations
                    I2 = np.array(I2)
                else:  # on the case we have only 1 value to hr, we add the values to the parameters directly
                    if p1 <= hr and hr <= p2:
                        I1 = 1
                    else:
                        I1 = 0
                    if p2 <= hr and hr <= 1:
                        I2 = 1
                    else:
                        I2 = 0


                beta = (b1 ** (1 - (I1 + I2))) * (b2 ** I1) * (b3 ** I2)
                ro = (1 - hst / ht) ** (k / b1)
                r1 = (1 - p1) ** (k / b1)
                r2 = (1 - p2) ** (k / b2)
                c1 = math.sqrt((ao * (dbh ** a1) * (h ** (a2 - (k / b1))) / (b1 * (ro - r1) + b2 * (r1 - alpha1 * r2) + b3 * alpha1 * r2)))

                if isinstance(hr, float) == False:  # on the cases where hr is an array...    
                    dob = []
                    counter = 0
                    for x in hr:  # for each hr value, we calculate the values of dob
                        d = (c1 * (math.sqrt(ht ** ((k - b1) / b1) * (1 - hr[counter]) ** ((k - beta[counter]) / beta[counter]) * alpha1 ** (I1[counter] + I2[counter]) * alpha2 ** (I2[counter]))))
                        dob.append(d)  # we add the value to a list
                        counter += 1
                    dob = np.array(dob)  # and transform the list to an array 
                else:  # on the case we have only 1 value to hr, we calculate dob directly
                    dob = (c1 * (math.sqrt(ht ** ((k - b1) / b1) * (1 - hr) ** ((k - beta) / beta) * alpha1 ** (I1 + I2) * alpha2 ** (I2))))
     

            elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                ht = tree.height
                dbh = tree.dbh
                dob = (1 + 0.558513*2.7182818284**(-25.933370*hr/ht))*(0.942294*dbh*((1 - hr/ht)**(1.312840 - 0.342491*(ht/dbh) - 1.239930*(1 - hr/ht))))

        except Exception:
            self.catch_model_exception()

        return dob  # diameter over bark (cm)


    def taper_under_bark(self, tree: Tree, plot: Plot, hr: float):
        """
        Taper equation under bark function.
        A function that returns the taper equation to calculate the diameter (cm, under bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source (Psyl):
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        """

        #try:  # errors inside that construction will be announced

            #if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

            #    dub = (1 + 0.3485 * 2.7182818284 ** (-23.9191 * hr)) * 0.7966 * tree.dbh * pow((1 - hr), (0.6094 - 0.7086 * (1 - hr)))

            #elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition


        #except Exception:
        #    self.catch_model_exception()

        #return dub    


    def merchantable(self, tree: Tree, plot: Plot):
        """
        Merchantable wood calculation (tree).
        A function needed to calculate the different commercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions and is linked to taper_over_bark, an indispensable function.
        That function is run by initialize and update_model functions.
        Data criteria to classify the wood by different uses were obtained from:
            Doc.: Rodriguez F (2009). Cuantificación de productos forestales en la planificación forestal:
                  Análisis de casos con cubiFOR. In Congresos Forestales
            Ref.: Rodriguez 2009        
        """
        
        try:  # errors inside that construction will be announced

            ht = tree.height  # the total height as ht to simplify
            # class_conditions have different lists for each usage, following that structure: [wood_usage, hmin/ht, dmin, dmax]
            # [WOOD USE NAME, LOG RELATIVE LENGTH RESPECT TOTAL TREE HEIGHT, MINIMUM DIAMETER, MAXIMUM DIAMETER]
            if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                class_conditions = [['unwinding', 3/ht, 40, 160], ['veneer', 3/ht, 40, 160], ['saw_big', 2.5/ht, 40, 200],
                                 ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28],
                                 ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]] 

            elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition            

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]

            # usage and merch_list are a dictionary and a list returned from merch_calculation function
            # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
            usage, merch_list = TreeModel.merch_calculation_mix(tree, plot, class_conditions, PsylvestrisQpetraeaMix)

            counter = -1
            for k,i in usage.items():
                counter += 1
                tree.add_value(k, merch_list[counter])  # add merch_list values to each usage

        except Exception:
            self.catch_model_exception()


    def merchantable_plot(self, plot: Plot, plot_trees):
        """
        Merchantable wood calculation (plot).
        A function needed to calculate the different commercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions and uses the data obtained from trees.
        """

        try:  # errors inside that construction will be announced

            plot_unwinding_sp1 = plot_veneer_sp1 = plot_saw_big_sp1 = plot_saw_small_sp1 = plot_saw_canter_sp1 = plot_post_sp1 = plot_stake_sp1 = plot_chips_sp1 =  0
            plot_unwinding_sp2 = plot_veneer_sp2 = plot_saw_big_sp2 = plot_saw_small_sp2 = plot_saw_canter_sp2 = plot_post_sp2 = plot_stake_sp2 = plot_chips_sp2 =  0

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                    plot_unwinding_sp1 += tree.unwinding*tree.expan
                    plot_veneer_sp1 += tree.veneer*tree.expan
                    plot_saw_big_sp1 += tree.saw_big*tree.expan
                    plot_saw_small_sp1 += tree.saw_small*tree.expan
                    plot_saw_canter_sp1 += tree.saw_canter*tree.expan
                    plot_post_sp1 += tree.post*tree.expan
                    plot_stake_sp1 += tree.stake*tree.expan
                    plot_chips_sp1 += tree.chips*tree.expan

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition 

                    # plot_unwinding_sp2 += tree.unwinding*tree.expan
                    # plot_veneer_sp2 += tree.veneer*tree.expan
                    plot_saw_big_sp2 += tree.saw_big*tree.expan
                    plot_saw_small_sp2 += tree.saw_small*tree.expan
                    plot_saw_canter_sp2 += tree.saw_canter*tree.expan
                    # plot_post_sp2 += tree.post*tree.expan
                    # plot_stake_sp2 += tree.stake*tree.expan
                    plot_chips_sp2 += tree.chips*tree.expan

            plot.add_value('UNWINDING_SP1', plot_unwinding_sp1/1000)  # now, we add the plot value to each variable, changing the units to m3/ha
            plot.add_value('VENEER_SP1', plot_veneer_sp1/1000)
            plot.add_value('SAW_BIG_SP1', plot_saw_big_sp1/1000)
            plot.add_value('SAW_SMALL_SP1', plot_saw_small_sp1/1000)
            plot.add_value('SAW_CANTER_SP1', plot_saw_canter_sp1/1000)
            plot.add_value('POST_SP1', plot_post_sp1/1000)
            plot.add_value('STAKE_SP1', plot_stake_sp1/1000)
            plot.add_value('CHIPS_SP1', plot_chips_sp1/1000)

            # plot.add_value('UNWINDING_SP2', plot_unwinding_sp2/1000)  # now, we add the plot value to each variable, changing the units to m3/ha
            # plot.add_value('VENEER_SP2', plot_veneer_sp2/1000)
            plot.add_value('SAW_BIG_SP2', plot_saw_big_sp2/1000)
            plot.add_value('SAW_SMALL_SP2', plot_saw_small_sp2/1000)
            plot.add_value('SAW_CANTER_SP2', plot_saw_canter_sp2/1000)
            # plot.add_value('POST_SP2', plot_post_sp2/1000)
            # plot.add_value('STAKE_SP2', plot_stake_sp2/1000)
            plot.add_value('CHIPS_SP2', plot_chips_sp2/1000)

            plot.add_value('UNWINDING', (plot_unwinding_sp1 + plot_unwinding_sp2)/1000)  # now, we add the plot value to each variable, changing the units to m3/ha
            plot.add_value('VENEER', (plot_veneer_sp1 + plot_veneer_sp2)/1000)
            plot.add_value('SAW_BIG', (plot_saw_big_sp1 + plot_saw_big_sp2)/1000)
            plot.add_value('SAW_SMALL', (plot_saw_small_sp1 + plot_saw_small_sp2)/1000)
            plot.add_value('SAW_CANTER', (plot_saw_canter_sp1 + plot_saw_canter_sp2)/1000)
            plot.add_value('POST', (plot_post_sp1 + plot_post_sp2)/1000)
            plot.add_value('STAKE', (plot_stake_sp1 + plot_stake_sp2)/1000)
            plot.add_value('CHIPS', (plot_chips_sp1 + plot_chips_sp2)/1000)

        except Exception:
            self.catch_model_exception()


    def crown(self, tree: Tree, plot: Plot, func):
        """
        Crown variables (tree).
        Function to calculate crown variables for each tree.
        That function is run by initialize and update_model functions.
        Crown equations (Psyl):
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008          
        """

        #try:  # errors inside that construction will be announced

        #    if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

        #        if func == 'initialize':  # if that function is called from initialize, first we must check if those variables are available on the initial inventory
        #            if tree.hlcw == 0 or tree.hlcw == '':  # if the tree hasn't height maximum crown-width (m) value, it is calculated
        #                if plot.basal_area != '' and plot.basal_area != 0:
        #                    tree.add_value('hlcw', tree.height / (1 + math.exp(
        #                    float(-0.0012 * tree.height * 10 - 0.0102 * tree.bal - 0.0168 * plot.basal_area))))
        #            if tree.hcb == 0 or tree.hcb == '':
        #                if plot.basal_area != '' and plot.basal_area != 0:
        #                    tree.add_value('hcb', tree.hlcw / (1 + math.exp(float(
        #                    1.2425 * (plot.basal_area/(tree.height*10)) + 0.0047 * plot.basal_area - 0.5725 * math.log(plot.basal_area) - 0.0082 * tree.bal))))
        #        else:
        #            if plot.basal_area != '' and plot.basal_area != 0:
        #                tree.add_value('hlcw', tree.height / (1 + math.exp(float(-0.0012 * tree.height * 10 - 0.0102 * tree.bal - 0.0168 * plot.basal_area))))
        #                tree.add_value('hcb', tree.hlcw / (1 + math.exp(float(1.2425 * (plot.basal_area/(tree.height*10)) + 0.0047 * plot.basal_area - 0.5725 * math.log(plot.basal_area) - 0.0082 * tree.bal))))
                
        #        if tree.hcb != 0 and tree.hcb != '':
        #            tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
        #            tree.add_value('lcw', (1 / 10.0) * (0.2518 * tree.dbh * 10) * math.pow(tree.cr, (0.2386 + 0.0046 * (tree.height - tree.hcb) * 10)))  # maximum crown-width (m)


        #    elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition


        #except Exception:
        #    self.catch_model_exception()


    def canopy(self, plot: Plot, plot_trees):
        """
        Crown variables (plot).
        Function to calculate plot crown variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            plot_expan_sp1 = plot_lcw_sp1 = plot_lcw2_sp1 = plot_fcc_sp1 = 0
            plot_expan_sp2 = plot_lcw_sp2 = plot_lcw2_sp2 = plot_fcc_sp2 = 0            

            #for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                #if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                    #plot_expan_sp1 += tree.expan
                    #plot_lcw_sp1 += tree.lcw*tree.expan
                    #plot_lcw2_sp1 += math.pow(tree.lcw, 2)*tree.expan
                    #plot_fcc_sp1 += math.pi*(math.pow(tree.lcw, 2)/4)*tree.expan

                #elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    #plot_expan_sp2 += tree.expan
                    #plot_lcw_sp2 += tree.lcw*tree.expan
                    #plot_lcw2_sp2 += math.pow(tree.lcw, 2)*tree.expan
                    #plot_fcc_sp2 += math.pi*(math.pow(tree.lcw, 2)/4)*tree.expan

            #if plot_expan_sp1 != 0:
                #plot.add_value('CROWN_MEAN_D_SP1', plot_lcw_sp1/plot_expan_sp1)
                #plot.add_value('CROWN_DOM_D_SP1', math.sqrt(plot_lcw2_sp1/plot_expan_sp1))
                #plot.add_value('CANOPY_COVER_SP1', plot_fcc_sp1/10000)
            
            #if plot_expan_sp2 != 0:
                #plot.add_value('CROWN_MEAN_D_SP2', plot_lcw_sp2/plot_expan_sp2)
                #plot.add_value('CROWN_DOM_D_SP2', math.sqrt(plot_lcw2_sp2/plot_expan_sp2))
                #plot.add_value('CANOPY_COVER_SP2', plot_fcc_sp2/10000)            

            #if (plot_expan_sp1 + plot_expan_sp2) != 0:
                #plot.add_value('CROWN_MEAN_D', (plot_lcw_sp1 + plot_lcw_sp2)/(plot_expan_sp1 + plot_expan_sp2))
                #plot.add_value('CROWN_DOM_D', math.sqrt((plot_lcw2_sp1 + plot_lcw2_sp2)/(plot_expan_sp1 + plot_expan_sp2)))
                #plot.add_value('CANOPY_COVER', (plot_fcc_sp1 + plot_fcc_sp2)/10000)

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
            dob = self.taper_over_bark(tree, plot, hr)  # diameter over bark using taper equation (cm)
            # dub = self.taper_under_bark(tree, plot, hr)  # diameter under/without bark using taper equation (cm)
            fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
            # fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
            tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
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

            plot_vol_sp1 = plot_bole_vol_sp1 = plot_bark_sp1 = 0
            plot_vol_sp2 = plot_bole_vol_sp2 = plot_bark_sp2 = 0

            for tree in plot_trees:

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                    plot_vol_sp1 += tree.expan*tree.vol
                    #plot_bole_vol_sp1 += tree.expan*tree.bole_vol
                    #plot_bark_sp1 = plot_vol_sp1 - plot_bole_vol_sp1

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    plot_vol_sp2 += tree.expan*tree.vol
                    #plot_bole_vol_sp2 += tree.expan*tree.bole_vol
                    #plot_bark_sp2 = plot_vol_sp2 - plot_bole_vol_sp2                   

            plot.add_value('VOL_SP1', plot_vol_sp1/1000)  # plot volume over bark (m3/ha)
            #plot.add_value('BOLE_VOL_SP1', plot_bole_vol_sp1/1000)  # plot volume under bark (m3/ha)
            #plot.add_value('BARK_VOL_SP1', plot_bark_sp1/1000)  # plot bark volume (m3/ha)

            plot.add_value('VOL_SP2', plot_vol_sp2/1000)  # plot volume over bark (m3/ha)
            #plot.add_value('BOLE_VOL_SP2', plot_bole_vol_sp2/1000)  # plot volume under bark (m3/ha)
            #plot.add_value('BARK_VOL_SP2', plot_bark_sp2/1000)  # plot bark volume (m3/ha)

            plot.add_value('VOL', plot.vol_sp1 + plot.vol_sp2)  # plot volume over bark (m3/ha)
            #plot.add_value('BOLE_VOL', plot.bole_vol_sp1 + plot.bole_vol_sp2)  # plot volume under bark (m3/ha)
            #plot.add_value('BARK_VOL', plot.bark_vol_sp1 + plot.bark_vol_sp2)  # plot bark volume (m3/ha)

        except Exception:
            self.catch_model_exception()


    def biomass(self, tree: Tree, plot: Plot):
        """
        Biomass variables (tree).
        Function to calculate biomass variables for each tree.
        That function is run by initialize and update_model functions.
        Biomass equations (Psyl):
            Doc.: Ruiz-Peinado R, del Rio M, Montero G (2011). New models for estimating the carbon sink capacity of Spanish softwood species. Forest Systems, 20(1), 176-188
            Ref.: Ruiz-Peinado et al, 2011
        Biomass equations (Qpet):
            Doc.: Manrique JM, Bravo F, del Peso C, Herrero C (2018). Ecuaciones de biomasa para roble albar (Quercus petraea (Matt.) Liebl.) y rebollo (Quercus pyrenaica Willd) en la comarca de la “Castillería” en el Norte de la Provincia de Palencia. En: 7º Congreso Forestal Español, SECF
            Ref.: Manrique et al, 2018            
        """

        try:  # errors inside that construction will be announced


            if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                wsw = 0.0154 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 37.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.540 * ((tree.dbh - 37.5) ** 2) - 0.0119 * ((tree.dbh - 37.5) ** 2) * tree.height) * Z
                wb2_7 = 0.0295 * (tree.dbh ** 2.742) * (tree.height ** (-0.899))
                wtbl = 0.530 * (tree.dbh ** 2.199) * (tree.height ** (-1.153))
                wr = 0.130 * (tree.dbh ** 2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                wstb = wthinb = 0

            elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                wstb = 0.001333*(tree.dbh**2)*tree.height
                wb2_7 = 0.006531*(tree.dbh**2)*tree.height - 0.07298*tree.dbh*tree.height
                wthinb = 0.023772*(tree.dbh**2)*tree.height
                wt = wstb + wb2_7 + wthinb
                wsw = wthickb = wtbl = wr = 0

            tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
            # tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
            # tree.add_value('w_cork', w_cork)   # fresh cork biomass (kg)
            tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
            tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
            # tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
            # tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
            # tree.add_value('wl', wl)  # wl = leaves (kg)
            tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            # tree.add_value('wbl0_7', wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
            tree.add_value('wr', wr)  # wr = roots (kg)
            tree.add_value('wt', wt)  # wt = total biomass (kg)

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
            plot_wsw_sp1 = plot_wsb_sp1 = plot_w_cork_sp1 = plot_wthickb_sp1 = plot_wstb_sp1 = plot_wb2_7_sp1 = plot_wb2_t_sp1 = plot_wthinb_sp1 = plot_wb05_sp1 = plot_wl_sp1 = plot_wtbl_sp1 = plot_wbl0_7_sp1 = plot_wr_sp1 = plot_wt_sp1 =  0
            plot_wsw_sp2 = plot_wsb_sp2 = plot_w_cork_sp2 = plot_wthickb_sp2 = plot_wstb_sp2 = plot_wb2_7_sp2 = plot_wb2_t_sp2 = plot_wthinb_sp2 = plot_wb05_sp2 = plot_wl_sp2 = plot_wtbl_sp2 = plot_wbl0_7_sp2 = plot_wr_sp2 = plot_wt_sp2 =  0

            for tree in plot_trees:  # for each tree...

                if int(tree.specie) == int(plot.id_sp1):  # specie 1 condition

                    plot_wsw_sp1 += tree.wsw*tree.expan
                    # plot_wsb_sp1 += tree.wsb*tree.expan
                    # plot_w_cork_sp1 += tree.w_cork*tree.expan
                    plot_wthickb_sp1 += tree.wthickb*tree.expan
                    # plot_wstb_sp1 += tree.wstb*tree.expan
                    plot_wb2_7_sp1 += tree.wb2_7*tree.expan
                    # plot_wb2_t_sp1 += tree.wb2_t*tree.expan
                    # plot_wthinb_sp1 += tree.wthinb*tree.expan
                    # plot_wb05_sp1 += tree.wb05*tree.expan
                    # plot_wl_sp1 += tree.wl*tree.expan
                    plot_wtbl_sp1 += tree.wtbl*tree.expan
                    # plot_wbl0_7_sp1 += tree.wbl0_7*tree.expan
                    plot_wr_sp1 += tree.wr*tree.expan
                    plot_wt_sp1 += tree.wt*tree.expan

                elif int(tree.specie) == int(plot.id_sp2):  # specie 2 condition

                    # plot_wsw_sp2 += tree.wsw*tree.expan
                    # plot_wsb_sp2 += tree.wsb*tree.expan
                    # plot_w_cork_sp2 += tree.w_cork*tree.expan
                    # plot_wthickb_sp2 += tree.wthickb*tree.expan
                    plot_wstb_sp2 += tree.wstb*tree.expan
                    plot_wb2_7_sp2 += tree.wb2_7*tree.expan
                    # plot_wb2_t_sp2 += tree.wb2_t*tree.expan
                    plot_wthinb_sp2 += tree.wthinb*tree.expan
                    # plot_wb05_sp2 += tree.wb05*tree.expan
                    # plot_wl_sp2 += tree.wl*tree.expan
                    # plot_wtbl_sp2 += tree.wtbl*tree.expan
                    # plot_wbl0_7_sp2 += tree.wbl0_7*tree.expan
                    # plot_wr_sp2 += tree.wr*tree.expan
                    plot_wt_sp2 += tree.wt*tree.expan

            plot.add_value('WSW_SP1', plot_wsw_sp1/1000)  # wsw = stem wood (Tn/ha)
            # plot.add_value('WSB_SP1', plot_wsb_sp1/1000)  # wsb = stem bark (Tn/ha)
            # plot.add_value('W_CORK_SP1', plot_w_cork_sp1/1000)  # fresh cork biomass (Tn/ha)
            plot.add_value('WTHICKB_SP1', plot_wthickb_sp1/1000)  # wthickb = Thick branches > 7 cm (Tn/ha)
            # plot.add_value('WSTB_SP1', plot_wstb_sp1/1000)  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            plot.add_value('WB2_7_SP1', plot_wb2_7_sp1/1000)  # wb2_7 = branches (2-7 cm) (Tn/ha)
            # plot.add_value('WB2_T_SP1', plot_wb2_t_sp1/1000)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            # plot.add_value('WTHINB_SP1', plot_wthinb_sp1/1000)  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            # plot.add_value('WB05_SP1', plot_wb05_sp1/1000)  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            # plot.add_value('WL_SP1', plot_wl_sp1/1000)  # wl = leaves (Tn/ha)
            plot.add_value('WTBL_SP1', plot_wtbl_sp1/1000)  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            # plot.add_value('WBL0_7_SP1', plot_wbl0_7_sp1/1000)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            plot.add_value('WR_SP1', plot_wr_sp1/1000)  # wr = roots (Tn/ha)
            plot.add_value('WT_SP1', plot_wt_sp1/1000)  # wt = total biomass (Tn/ha)

            # plot.add_value('WSW_SP2', plot_wsw_sp2/1000)  # wsw = stem wood (Tn/ha)
            # plot.add_value('WSB_SP2', plot_wsb_sp2/1000)  # wsb = stem bark (Tn/ha)
            # plot.add_value('W_CORK_SP2', plot_w_cork_sp2/1000)  # fresh cork biomass (Tn/ha)
            # plot.add_value('WTHICKB_SP2', plot_wthickb_sp2/1000)  # wthickb = Thick branches > 7 cm (Tn/ha)
            plot.add_value('WSTB_SP2', plot_wstb_sp2/1000)  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            plot.add_value('WB2_7_SP2', plot_wb2_7_sp2/1000)  # wb2_7 = branches (2-7 cm) (Tn/ha)
            # plot.add_value('WB2_T_SP2', plot_wb2_t_sp2/1000)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            plot.add_value('WTHINB_SP2', plot_wthinb_sp2/1000)  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            # plot.add_value('WB05_SP2', plot_wb05_sp2/1000)  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            # plot.add_value('WL_SP2', plot_wl_sp2/1000)  # wl = leaves (Tn/ha)
            # plot.add_value('WTBL_SP2', plot_wtbl_sp2/1000)  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            # plot.add_value('WBL0_7_SP2', plot_wbl0_7_sp2/1000)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            # plot.add_value('WR_SP2', plot_wr_sp2/1000)  # wr = roots (Tn/ha)
            plot.add_value('WT_SP2', plot_wt_sp2/1000)  # wt = total biomass (Tn/ha)

            plot.add_value('WSW', (plot_wsw_sp1 + plot_wsw_sp2)/1000)  # wsw = stem wood (Tn/ha)
            # plot.add_value('WSB', (plot_wsb_sp1 + plot_wsw_sp2)/1000)  # wsb = stem bark (Tn/ha)
            # plot.add_value('W_CORK', (plot_w_cork_sp1 + plot_w_cork_sp2)/1000)  # fresh cork biomass (Tn/ha)
            plot.add_value('WTHICKB', (plot_wthickb_sp1 + plot_wthickb_sp2)/1000)  # wthickb = Thick branches > 7 cm (Tn/ha)
            plot.add_value('WSTB', (plot_wstb_sp1 + plot_wstb_sp2)/1000)  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            plot.add_value('WB2_7', (plot_wb2_7_sp1 + plot_wb2_7_sp2)/1000)  # wb2_7 = branches (2-7 cm) (Tn/ha)
            # plot.add_value('WB2_T', (plot_wb2_t_sp1 + plot_wb2_t_sp2)/1000)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            plot.add_value('WTHINB', (plot_wthinb_sp1 + plot_wthinb_sp2)/1000)  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            # plot.add_value('WB05', (plot_wb05_sp1 + plot_wb05_sp2)/1000)  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            # plot.add_value('WL', (plot_wl_sp1 + plot_wl_sp2)/1000)  # wl = leaves (Tn/ha)
            plot.add_value('WTBL', (plot_wtbl_sp1 + plot_wtbl_sp2)/1000)  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            # plot.add_value('WBL0_7', (plot_wbl0_7_sp1 + plot_wbl0_7_sp2)/1000)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            plot.add_value('WR', (plot_wr_sp1 + plot_wr_sp2)/1000)  # wr = roots (Tn/ha)
            plot.add_value('WT', (plot_wt_sp1 + plot_wt_sp2)/1000)  # wt = total biomass (Tn/ha)

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
            "CROWN_MEAN_D",  # Mean crown diameter (m)
            "CROWN_MEAN_D_SP1",  # Mean crown diameter (m) for specie 1
            "CROWN_MEAN_D_SP2",  # Mean crown diameter (m) for specie 2    
            "CROWN_DOM_D",  # Dominant crown diameter (m)
            "CROWN_DOM_D_SP1",  # Dominant crown diameter (m) for specie 1
            "CROWN_DOM_D_SP2",  # Dominant crown diameter (m) for specie 2    
            "CANOPY_COVER",  # Canopy cover (%)
            "CANOPY_COVER_SP1",  # Canopy cover (%) for specie 1
            "CANOPY_COVER_SP2",  # Canopy cover (%) for specie 2        
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
            "BOLE_VOL",  # Volume under bark (m3/ha)
            "BARK_VOL",  # Bark Volume (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume harvested percentage (%)
            #"DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
            "ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - volume for mixed models
            #"VOL_SP1",  # Volume (m3/ha)
            "BOLE_VOL_SP1",  # Volume under bark (m3/ha)
            "BARK_VOL_SP1",  # Bark Volume (m3/ha) 
            #"VOL_SP2",  # Volume (m3/ha)
            "BOLE_VOL_SP2",  # Volume under bark (m3/ha)
            "BARK_VOL_SP2",  # Bark Volume (m3/ha)     

            # Plot variables calculated - wood uses
            #"UNWINDING",  # Unwinding = the useful wood volume unwinding destiny (m3/ha)
            #"VENEER",  # Veneer = the useful wood volume veneer destiny (m3/ha)
            #"SAW_BIG",  # Saw big =) the useful wood volume big saw destiny (m3/ha)
            #"SAW_SMALL",  # Saw small = the useful wood volume small saw destiny (m3/ha)
            #"SAW_CANTER",  # Saw canter = the useful wood volume canter saw destiny (m3/ha)
            #"POST",  # Post = the useful wood volume post destiny (m3/ha)
            #"STAKE",  # Stake = the useful wood volume stake destiny (m3/ha)
            #"CHIPS",  # Chips = the useful wood volume chips destiny (m3/ha)

            #'UNWINDING_SP1',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
            #'VENEER_SP1',  # veneer = the useful wood volume veneer destiny (m3/ha)
            #'SAW_BIG_SP1',  # saw_big = the useful wood volume big saw destiny (m3/ha)
            #'SAW_SMALL_SP1',  # saw_small = the useful wood volume small saw destiny (m3/ha)
            #'SAW_CANTER_SP1',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
            #'POST_SP1',  # post = the useful wood volume post destiny (m3/ha)
            #'STAKE_SP1',  # stake = the useful wood volume stake destiny (m3/ha)
            #'CHIPS_SP1',  # chips = the useful wood volume chips destiny (m3/ha)
            
            'UNWINDING_SP2',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
            'VENEER_SP2',  # veneer = the useful wood volume veneer destiny (m3/ha)
            #'SAW_BIG_SP2',  # saw_big = the useful wood volume big saw destiny (m3/ha)
            #'SAW_SMALL_SP2',  # saw_small = the useful wood volume small saw destiny (m3/ha)
            #'SAW_CANTER_SP2',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
            'POST_SP2',  # post = the useful wood volume post destiny (m3/ha)
            'STAKE_SP2',  # stake = the useful wood volume stake destiny (m3/ha)
            #'CHIPS_SP2',  # chips = the useful wood volume chips destiny (m3/ha)

            # Plot variables calculated - biomass
            #"WSW",  # wsw = stem wood (Tn/ha)
            "WSB",  # wsb = stem bark (Tn/ha)
            "WSWB",  # wswb = stem wood and stem bark (Tn/ha)
            #"WTHICKB",  # wthickb = Thick branches > 7 cm (Tn/ha)
            #"WSTB",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            #"WB2_7",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            #"WTHINB",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB",  # wdb = dead branches biomass (Tn/ha)
            "WL",  # wl = leaves (Tn/ha)
            #"WTBL",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            #"WR",  # wr = roots (Tn/ha)
            #"WT",  # wt = total biomass (Tn/ha)
            #"DEAD_WT",  # WT of the dead trees after an execution (Tn/ha)
            "ING_WT",  # WT of the ingrowth trees after an execution (Tn/ha)

            # Plot variables calculated - biomass for mixed models
            #"WSW_SP1",  # wsw = stem wood (Tn/ha)
            "WSB_SP1",  # wsb = stem bark (Tn/ha)
            "WSWB_SP1",  # wswb = stem wood and stem bark (Tn/ha)
            #"WTHICKB_SP1",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP1",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            #"WB2_7_SP1",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP1",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB_SP1",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP1",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7_SP1",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP1",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP1",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP1",  # wl = leaves (Tn/ha)
            #"WTBL_SP1",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7_SP1",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            #"WR_SP1",  # wr = roots (Tn/ha)
            #"WT_SP1",  # wt = total biomass (Tn/ha)

            "WSW_SP2",  # wsw = stem wood (Tn/ha)
            "WSB_SP2",  # wsb = stem bark (Tn/ha)
            "WSWB_SP2",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP2",  # wthickb = Thick branches > 7 cm (Tn/ha)
            #"WSTB_SP2",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            #"WB2_7_SP2",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP2",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            #"WTHINB_SP2",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP2",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7_SP2",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP2",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP2",  # wl = leaves (Tn/ha)
            "WTBL_SP2",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7_SP2",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            "WR_SP2",  # wr = roots (Tn/ha)
            #"WT_SP2",  # wt = total biomass (Tn/ha)

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

            # Auxiliar variables for future models - 08/03/2023
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
            'SAW_BIG_LIFEREBOLLO',
            'SAW_SMALL_LIFEREBOLLO',
            'STAVES_INTONA',
            'BOTTOM_STAVES_INTONA',
            'WOOD_PANELS_GAMIZ',
            'MIX_GARCIA_VARONA',
            'CARBON',
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
            #"height",  # total tree height (m)
            "stump_h",   # stump height (m))
            "bark_1",  # bark thickness, measurement 1 (mm)
            "bark_2",  # bark thickness, measurement 2 (mm)
            "bark",  # mean bark thickness (mm)

           # Basic variables calculated
            #"basal_area",   # basal area (cm2)
            #"basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
            #"basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
            #"bal",  # cumulative basal area (m2/ha)
            #"bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            #"bal_intersp",  # intraspecific bal (m2/ha) for mixed models
            #"ba_ha",  # basal area per ha (m2/ha) 
            #"normal_circumference",  # circumference at breast height (cm)
            #"slenderness",  # slenderness (cm/cm)
            
            # Crown variables
            "cr",  # crown ratio (%)
            "lcw",  #  largest crown width (m)
            "hcb",  # height of the crown base (m)
            "hlcw",  # height of the largest crown width (m)
            "cpa",  # crown projection area (m2)
            "crown_vol",  # crown volume (m3)

            # Volume variables
            #"vol",  # volume over bark (dm3)
            "bole_vol",  # volume under bark (dm3)
            "bark_vol",  # bark volume (dm3)
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
            #"wsw",  # wsw = stem wood (kg)
            "wsb",  # wsb = stem bark (kg)
            "wswb",  # wswb = stem wood and stem bark (kg)
            "w_cork",  # fresh cork biomass (kg)
            #"wthickb",  # wthickb = Thick branches > 7 cm (kg)
            #"wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            #"wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
            "wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            #"wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
            "wb05",  # wb05 = thinnest branches (< 0.5 cm) (kg)
            "wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
            "wb0_2",  # wb0_2 = branches < 2 cm (kg)
            "wdb",  # wdb = dead branches biomass (kg)
            "wl",  # wl = leaves (kg)
            #"wtbl",  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            "wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
            #"wr",  # wr = roots (kg)
            #"wt",  # wt = total biomass (kg)
            
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

            # Auxiliar variables for future models - 08/03/2023
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
            'saw_big_liferebollo',
            'saw_small_liferebollo',
            'staves_intona',
            'bottom_staves_intona',
            'wood_panels_gamiz',
            'mix_garcia_varona',
            'carbon',
        ]

        Variables.remove_var_plot(delete_from_plot)
        Variables.remove_var_tree(delete_from_tree)
        
PsylvestrisQpetraeaMix.vars()