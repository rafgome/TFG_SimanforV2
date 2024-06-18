#!/usr/bin/env python
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from engine import Engine
from util.tools import Tools
from simulation.inventory import Inventory
from engine.engine import DEFAULT_CONFIG

from models import TreeModel
from models import HarvestModel
from models import LoadModel
from models import StandModel
from data import Plot
from data import Tree
from data import DESC
from data.general import Area, Model, Warnings
from data import SearchCriteria
from data import OrderCriteria
from scenario import Operation
from data.variables import TREE_VARS, PLOT_VARS, MODEL_VARS

from models.trees.equations_mixed_models import MixedEquations
from models.trees.equations_tree_models import TreeEquations
from models.trees.equations_tree_biomass import TreeBiomass
from models.trees.equations_tree_volume import TreeVolume

from data import GREATEREQUAL
from data import LESS
from data import EQUAL
from data.variables import CUTS_DICT

import logging
import math

class BasicEngine(Engine):

    def __init__(self, configuration):

        if configuration is None:
            configuration = DEFAULT_CONFIG

        self.__processes = None
        self.__threads_per_worker = None
        self.__num_workers = None
        self.__memory_limit = None

    @property
    def processes(self):
        return self.__processes

    @property
    def threads_per_worker(self):
        return self.__threads_per_worker

    @property
    def num_workers(self):
        return self.____num_workers

    @property
    def memory_limit(self):
        return self.__memory_limit

    def execute_function(self, function, parameters):
        return self.__client.submit(function, **parameters)

    def map_function(self, function, parameters):
        return self.__client.map(function, **parameters)

    def gather_function(self, function, parameters):
        return self.__client.gather(function, **parameters)

    def apply_harvest_model(self, inventory: Inventory, model: HarvestModel, operation: Operation):
        """
        Function executed by engine file when the process selected at the scenario is a cut on a tree model.
        """

        result_inventory: inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        operation.add_variable('time', 0)  # time on HARVEST operation must be always 0    

        for plot in inventory.plots:

            if 'AGE' in PLOT_VARS:
                plot_age = plot.age
            else:
                plot_age = 0

            if min <= plot_age <= max:  # execute the function only if the age of the plot are between the stablished range of the scenario (or default range)

                try:
                    # set by default values
                    cut_criteria = "PERCENTOFTREES" if operation.get_variable('cut_down') == None else operation.get_variable('cut_down')
                    preserve_trees_value = 15 if operation.get_variable('preserve_trees') == None else operation.get_variable('preserve_trees')
                    species_harvest = '' if operation.get_variable('species') == None else operation.get_variable('species')
                    volume_target = 'plot' if operation.get_variable('volume_target') == None else operation.get_variable('volume_target')

                    # apply harvest model
                    new_plot = model.apply_model(plot, operation.get_variable('time'), operation.get_variable('volumen'),
                                                 preserve_trees_value, species_harvest, volume_target, cut_criteria)

                    # update tree bal
                    TreeEquations.get_bal(new_plot.trees)
                    if 'bal_intrasp' in TREE_VARS:
                        MixedEquations.get_bal_per_sp(new_plot.trees, new_plot)

                    # update basal area and volume per ha
                    for tree in new_plot.trees:
                        TreeEquations.set_g_ha(tree)
                        if 'vol_ha' in TREE_VARS and 'vol' in TREE_VARS:
                            if tree.vol != '':  # sometimes, I don't know why, that value is empty and the simulation fails
                                tree.add_value('vol_ha', tree.expan * tree.vol / 1000)  # update vol/ha value
                            else:
                                tree.add_value('vol_ha', '')

                    # update general plot variables
                    new_plot.recalculate()

                    # when models for mixed stands are used, then variables should be updated
                    if 'ID_SP1' in PLOT_VARS and 'ID_SP2' in PLOT_VARS and new_plot.id_sp1 != '' and new_plot.id_sp2 != '':
                        # get Martonne
                        M = TreeEquations.choose_martonne(new_plot.plot_id, new_plot.year, (2020, 2040, 2060, 2080, 2100))
                        # reorder trees by dbh
                        list_of_trees: list[Tree] = new_plot.short_trees_on_list('dbh', DESC)
                        # calculate stand variables by species
                        MixedEquations.get_stand_by_sp(list_of_trees, new_plot, M)

                    # set 0 to death and ingrowth variables
                    new_plot.cut_vars()

                    # update plot variables without distinguishing between tree species
                    TreeBiomass.set_w_carbon_plot(new_plot, new_plot.trees)
                    TreeVolume.set_plot_vol(new_plot, new_plot.trees)
                    TreeVolume.set_plot_merch(new_plot, new_plot.trees)
                    TreeEquations.set_diversity_indexes(new_plot, new_plot.trees)

                    #update plot variables distinguishing between tree species
                    if 'ID_SP1' in PLOT_VARS and 'ID_SP2' in PLOT_VARS and new_plot.id_sp1 != '' and new_plot.id_sp2 != '':
                        TreeBiomass.set_w_carbon_plot_sp(new_plot, new_plot.trees)
                        TreeVolume.set_plot_vol_sp(new_plot, new_plot.trees)
                        TreeVolume.set_plot_merch_sp(new_plot, new_plot.trees)

                    result_inventory.add_plot(new_plot)

                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

            else:
                Tools.print_log_line('Plot ' + str(plot.id) + ' was not added', logging.INFO)
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
                print('That cut was not realised because the plot age on this step, which is', plot_age,'years, are not between the minimum age of', min,'years and the maximum of', max, 'years established at the scenario file')
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')

                #new_plot = model.apply_model(plot, operation.get_variable('time'), 0)
                #new_plot.cut_vars()  # set 0 to death and ingrowth variables
                #result_inventory.add_plot(new_plot)
                plot.cut_vars()
                result_inventory.add_plot(plot)

        return result_inventory

    def apply_harvest_stand_model(self, inventory: Inventory, model: StandModel, operation: Operation):
        """
        Function executed by engine file when the process selected at the scenario is a cut on a stand model.
        """

        result_inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        operation.add_variable('time', 0)  # time on HARVEST operation must be always 0  

        for plot in inventory.plots:

            if 'AGE' in PLOT_VARS:
                plot_age = plot.age
            else:
                plot_age = 0

            if min <= plot_age <= max:  # execute the function only if the age of the plot are between the stablished range of the scenario (or default range)
                
                new_plot = Plot()
                new_plot.clone(plot)

                try:
                    cut_criteria = CUTS_DICT[operation.get_variable('cut_down')]
                    model.harvest(plot, new_plot, cut_criteria, 
                        operation.get_variable('volumen'), operation.get_variable('time'), min, max)
                    # model.harvest(plot, new_plot, cut_criteria, 
                    # operation.get_variable('intensity'), operation.get_variable('time'), min, max)

                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                result_inventory.add_plot(new_plot)

            else:
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
                print('That cut was not realised because the plot age on this step, which is', plot_age,'years, are not between the minimum age of', min,'years and the maximum of', max, 'years established at the scenario file')              
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')

                new_plot = Plot()
                new_plot.clone(plot)
                result_inventory.add_plot(new_plot)

        return result_inventory

    def apply_initialize_tree_model(self, inventory: Inventory, model: TreeModel, operation: Operation):
        """
        Function executed by engine file when the process selected at the scenario is the initialization on a tree model.
        """

        result_inventory = Inventory()

        operation.add_variable('time', 0)  # time on initialize operation must be always 0  

        for plot in inventory.plots:

            if 'AGE' in PLOT_VARS:
                if plot.age == '' :
                    plot.add_value('AGE', 0) 
            if 'YEAR' in PLOT_VARS:
                if plot.year == '' :
                    plot.add_value('YEAR', 0)   

            Plot.from_plot_to_area(plot)  # move information from Plot to Area

            new_plot = Plot()
            new_plot.clone(plot, True)  # full = True also includes trees created by ingrowth

            try:
                model.initialize(new_plot)
            except Exception as e:
                Tools.print_log_line(str(e), logging.ERROR)

            new_plot.recalculate()

            result_inventory.add_plot(new_plot)
          
        Plot.eliminate_from_plot()  # eliminate information from PLOT_VARS already copied on AREA_VARS

        return result_inventory

    def apply_initialize_stand_model(self, inventory: Inventory, model: StandModel, operation: Operation):
        """
        Function executed by engine file when the process selected at the scenario is the initialization on a stand model.
        """

        result_inventory = Inventory()

        operation.add_variable('time', 0)  # time on initialize operation must be always 0  

        for plot in inventory.plots:

            if 'AGE' in PLOT_VARS:
                if plot.age == '' :
                    plot.add_value('AGE', 0) 
            if 'YEAR' in PLOT_VARS:
                if plot.year == '' :
                    plot.add_value('YEAR', 0)  

            Plot.from_plot_to_area(plot)  # move information from Plot to Area            

            new_plot = Plot()
            new_plot.clone(plot, True)  # full = True also includes trees created by ingrowth

            try:
                model.initialize(new_plot)
            except Exception as e:
                Tools.print_log_line(str(e), logging.ERROR)

            # new_plot.recalculate()  # in that case, recalculate is not needed beacuse plot variables available for each model are programmed on the stand model file

            result_inventory.add_plot(new_plot)

        Plot.eliminate_from_plot()  # eliminate information from PLOT_VARS already copied on AREA_VARS

        return result_inventory

    def apply_tree_model(self, inventory: Inventory, model: TreeModel, operation: Operation):
        """
        Function executed by engine file when the process selected at the scenario is an execution on a tree model.
        That function contains the calculation on the survive, growth and ingrowth functions planned at the tree model.
        """

        result_inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        for plot in inventory.plots:
            
            if 'AGE' in PLOT_VARS:
                plot_age = plot.age
            else:
                plot_age = 0

            dead_trees = list()  # dead tree list, with status = M
            alive_trees = list()  # alive tree list after expan recalculation, with status = None
            ingrowth_trees = list()  # ingrowth tree list, with status = I
            alive_ing_trees = list()  # alive trees after add ingrowth expan, with status = None
            growth_trees = list()  # tree list after growth process, with status = None
            original_growth_trees = list()  # trees with the original expan but with the dbh modified by growth function, to use on ingrowth function, status = None
            final_trees = list()  # alive trees after survive, growth and ingrowth calculations, with status = None

            if min <= plot_age <= max:  # execute the function only if the age of the plot are between the stablished range of the scenario (or default range)

                new_plot = Plot()
                new_plot.clone(plot, full=True)  # full = True also includes trees created by ingrowth
                    
                search_criteria = SearchCriteria()
                search_criteria.add_criteria('status', None, EQUAL)  # choose only alive trees

                original_trees = Tree.get_sord_and_order_tree_list(plot.trees, search_criteria=search_criteria)  # import tree information


###############################################################################################################
##################################################### SURVIVE ###########################################################
###############################################################################################################


                dead_tree = dead_n = dead_ba = dead_vol = dead_wt = 0  # declare variables to use at survive calculations

                for tree in original_trees:  # for each tree..

                    survival_ratio: float = 0.0

                    try:  # import the value from the survival function at the model
                        survival_ratio = model.survival(operation.get_variable('time'), new_plot, tree)
                    except Exception as e:
                        Tools.print_log_line(str(e), logging.ERROR)

                    # Models of only 1 specie
                    if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                        if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                            if survival_ratio == 1:  # if the tree completely survival...

                                new_tree_alive = Tree()
                                new_tree_alive.clone(tree)                       
                                alive_trees.append(new_tree_alive)  # we add the tree to the list with no changes

                            elif survival_ratio == 0:  # if the tree is totally dead...
                            
                                new_tree_dead = Tree()
                                new_tree_dead.clone(tree)   
                                new_tree_dead.add_value('status', 'M')  # set "M" status to recognise dead trees on the output                                                      
                                dead_trees.append(new_tree_dead)  # we add the tree to the dead trees list 

                                # temporal variables to calculate plot information about dead trees
                                dead_tree = new_tree_dead.expan
                                dead_n += new_tree_dead.expan
                                if new_tree_dead.basal_area == '':
                                    new_tree_dead.add_value('basal_area', 0)
                                #dead_ba += (dead_tree*plot.basal_area/plot.density)*10000  # calculate dead basal area accumulated in cm2
                                dead_ba += dead_tree*new_tree_dead.basal_area
                                if new_tree_dead.vol == '':
                                    new_tree_dead.add_value('vol', 0)
                                dead_vol += dead_tree*new_tree_dead.vol  # calculate dead volume accumulated in dm3
                                if new_tree_dead.wt == '':
                                    new_tree_dead.add_value('wt', 0)
                                dead_wt += dead_tree*new_tree_dead.wt  # calculate dead biomass accumulated in kg

                            elif survival_ratio > 0 and survival_ratio < 1:  # if the survival ratio in the tree model exist (>0), next lines modify the "expan" of alive and dead trees

                                new_tree_alive = Tree()
                                new_tree_alive.clone(tree)
                                new_tree_alive.add_value('expan', survival_ratio*new_tree_alive.expan)  # recalculation of alive trees "expan"

                                new_tree_dead = Tree()
                                new_tree_dead.clone(tree)
                                new_tree_dead.add_value('status', 'M')  # set "M" status to recognise dead trees on the output      
                                new_tree_dead.add_value('expan', (1 - survival_ratio)*new_tree_dead.expan)  # calculation of dead trees "expan"
                                
                                # temporal variables to calculate plot information about dead trees
                                dead_tree = new_tree_dead.expan
                                dead_n += new_tree_dead.expan
                                if new_tree_dead.basal_area == '':
                                    new_tree_dead.add_value('basal_area', 0)
                                #dead_ba += (dead_tree*new_plot.basal_area/new_plot.density)*10000  # calculate dead basal area accumulated in cm2
                                dead_ba += dead_tree*new_tree_dead.basal_area                               
                                if new_tree_dead.vol == '':
                                    new_tree_dead.add_value('vol', 0)
                                dead_vol += dead_tree*new_tree_dead.vol  # calculate dead volume accumulated in dm3
                                if new_tree_dead.wt == '':
                                    new_tree_dead.add_value('wt', 0)
                                dead_wt += dead_tree*new_tree_dead.wt  # calculate dead biomass accumulated in kg

                                alive_trees.append(new_tree_alive)  # update alive trees information
                                dead_trees.append(new_tree_dead)  # update dead trees information

                            else:  # if the value is wrong and it is not between 0 and 1
                                
                                break  # we jump the tree

                        else:  # to trees of different specie as the model

                            new_tree_alive = Tree()
                            new_tree_alive.clone(tree)
                            alive_trees.append(new_tree_alive)  # update alive trees information

                    # Models of more than 1 specie
                    elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                        if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model
   
                            if survival_ratio == 1:  # if the tree completely survival...

                                new_tree_alive = Tree()
                                new_tree_alive.clone(tree)                       
                                alive_trees.append(new_tree_alive)  # we add the tree to the list with no changes

                            elif survival_ratio == 0:  # if the tree is totally dead...
                            
                                new_tree_dead = Tree()
                                new_tree_dead.clone(tree)   
                                new_tree_dead.add_value('status', 'M')  # set "M" status to recognise dead trees on the output                                                      
                                dead_trees.append(new_tree_dead)  # we add the tree to the dead trees list 

                                # temporal variables to calculate plot information about dead trees
                                dead_tree = new_tree_dead.expan
                                dead_n += new_tree_dead.expan
                                if new_tree_dead.basal_area == '':
                                    new_tree_dead.add_value('basal_area', 0)
                                #dead_ba += (dead_tree*plot.basal_area/plot.density)*10000  # calculate dead basal area accumulated in cm2
                                dead_ba += dead_tree*new_tree_dead.basal_area                              
                                if new_tree_dead.vol == '':
                                    new_tree_dead.add_value('vol', 0)
                                dead_vol += dead_tree*new_tree_dead.vol  # calculate dead volume accumulated in dm3
                                if new_tree_dead.wt == '':
                                    new_tree_dead.add_value('wt', 0)
                                dead_wt += dead_tree*new_tree_dead.wt  # calculate dead biomass accumulated in kg

                            elif survival_ratio > 0 and survival_ratio < 1:  # if the survival ratio in the tree model exist (>0), next lines modify the "expan" of alive and dead trees

                                new_tree_alive = Tree()
                                new_tree_alive.clone(tree)
                                new_tree_alive.add_value('expan', survival_ratio*new_tree_alive.expan)  # recalculation of alive trees "expan"

                                new_tree_dead = Tree()
                                new_tree_dead.clone(tree)
                                new_tree_dead.add_value('status', 'M')  # set "M" status to recognise dead trees on the output      
                                new_tree_dead.add_value('expan', (1 - survival_ratio)*new_tree_dead.expan)  # calculation of dead trees "expan"
                                
                                # temporal variables to calculate plot information about dead trees
                                dead_tree = new_tree_dead.expan
                                dead_n += new_tree_dead.expan
                                if new_tree_dead.basal_area == '':
                                    new_tree_dead.add_value('basal_area', 0)
                                #dead_ba += (dead_tree*new_plot.basal_area/new_plot.density)*10000  # calculate dead basal area accumulated in cm2
                                dead_ba += dead_tree*new_tree_dead.basal_area                           
                                if new_tree_dead.vol == '':
                                    new_tree_dead.add_value('vol', 0)
                                dead_vol += dead_tree*new_tree_dead.vol  # calculate dead volume accumulated in dm3
                                if new_tree_dead.wt == '':
                                    new_tree_dead.add_value('wt', 0)
                                dead_wt += dead_tree*new_tree_dead.wt  # calculate dead biomass accumulated in kg

                                alive_trees.append(new_tree_alive)  # update alive trees information
                                dead_trees.append(new_tree_dead)  # update dead trees information

                            else:  # if the value is wrong and it is not between 0 and 1
                                
                                break  # we jump the tree

                        else:  # to trees of different specie as the model

                            new_tree_alive = Tree()
                            new_tree_alive.clone(tree)
                            alive_trees.append(new_tree_alive)  # update alive trees information

                if dead_tree != 0:  # if it exist some mortality at the plot...
                    dead_ba = dead_ba/10000  # set basal area at m2/ha
                    dead_vol = dead_vol/1000  # set volume at m3/ha
                    dead_wt = dead_wt/1000  # set biomass at Tn/ha
                    
                    new_plot.add_value('DEAD_DENSITY', dead_n)  # upload plot information about dead tree density
                    new_plot.add_value('DEAD_BA', dead_ba)  # upload plot information about dead tree basal area
                    new_plot.add_value('DEAD_VOL', dead_vol)  # upload plot information about dead tree volume
                    new_plot.add_value('DEAD_WT', dead_wt)  # upload plot information about dead tree biomass
                    

###############################################################################################################
##################################################### GROWTH ############################################################
###############################################################################################################


                if dead_tree != 0 and new_plot.density == new_plot.dead_density:  # if it is not alive trees, we don't continue with the calculation
                    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
                    print('All your trees are DEAD, so no more calculations are needed.')
                    print('If you made it consciously, the process is correct; if not, check the calculations of "survive" function at your model.')    
                    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
                else:

                    for tree in alive_trees:  # for each alive tree.. 

                        try:  # once mortality is calculated, only alive trees are send to the growth function of the model
                            model.growth(operation.get_variable('time'), new_plot, tree, tree)
                        except Exception as e:
                            Tools.print_log_line(str(e), logging.ERROR)

                        growth_trees.append(tree)  # we save the information of trees after growth in a new list

                        original_tree_growth = Tree()
                        original_tree_growth.clone(tree)
                        original_tree_growth.add_value('dbh', tree.dbh)  # substitute old dbh value by the new one, with no modifications of expan value
                        original_tree_growth.add_value('dbh_i', tree.dbh_i)  # substitute old dbh value by the new one, with no modifications of expan value
                        original_tree_growth.add_value('height', tree.height)  # substitute old h value by the new one, with no modifications of expan value
                        original_tree_growth.add_value('height_i', tree.height_i)  # substitute old dbh value by the new one, with no modifications of expan value
                        original_tree_growth.add_value('tree_age', tree.tree_age)  # substitute old age value by the new one, with no modifications of expan value
                        original_tree_growth.add_value('basal_area', tree.basal_area)  # substitute old g value by the new one, with no modifications of expan value
                        original_tree_growth.add_value('basal_area_i', tree.basal_area_i)  # substitute old dbh value by the new one, with no modifications of expan value
                        if 'bark' in TREE_VARS:
                            original_tree_growth.add_value('bark', tree.bark)  # substitute old bark value by the new one, with no modifications of expan value  
                        if 'vol' in TREE_VARS:
                            original_tree_growth.add_value('vol', tree.vol)  # substitute old vol value by the new one, with no modifications of expan value                                        
                        if 'bole_vol' in TREE_VARS:
                            original_tree_growth.add_value('bole_vol', tree.bole_vol)  # substitute old bole vol value by the new one, with no modifications of expan value   
                        if 'bark_vol' in TREE_VARS:
                            original_tree_growth.add_value('bark_vol', tree.bark_vol)  # substitute old bark vol value by the new one, with no modifications of expan value

                        original_growth_trees.append(original_tree_growth)  # temporal list with older expan but new dbh, to use it at ingrowth function


###############################################################################################################
#################################################### INGROWTH ###########################################################
###############################################################################################################


                new_area_basimetrica = distribution = 0  

                try:  # obtain ingrowth value (m2/ha)
                    new_area_basimetrica = model.ingrowth(operation.get_variable('time'), new_plot)
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                # if the model hasn't ingrowth, the process finish here

                if new_area_basimetrica > 0:  # if it is ingrowth...

                    try:  # obtain ingrowth distribution by diameter classes
                        distribution = model.ingrowth_distribution(operation.get_variable('time'), new_plot, new_area_basimetrica)
                    except Exception as e:
                        Tools.print_log_line(str(e), logging.ERROR)

                    order_criteria = OrderCriteria()  
                    order_criteria.add_criteria('dbh')  # stablish an order to work with the trees

                    tree_ingrowth: Tree = Tree.get_sord_and_order_tree_list(original_growth_trees, order_criteria=order_criteria)  # import original trees with dbh modified
                    tree_alive_ing: Tree = Tree.get_sord_and_order_tree_list(growth_trees, order_criteria=order_criteria)  # import trees after survival and growth functions

                    trees_expan = trees_ba = ing_tree = ing_n = ing_ba = ing_vol = ing_wt = 0 


                    #--# TWO POSSIBLE CASES: #--#
                    # - if it is not an ingrowth distribution function (return None), ingrowth expan will be shared between all the trees of the plot
                    # - if it is an ingrowth distribution function, ingrowth expan will be shared at the % stablished on the model for each diameter class                  


                    #--# CASE 1 #--#

                    # No distribution

                    if distribution == None:  

                        for tree in tree_ingrowth:  # for each tree...
                            
                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                                if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                                    trees_expan += tree.expan  # we calculate density...
                                    trees_ba += tree.basal_area*tree.expan/10000  # ... and basal area

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                                if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model
           
                                    trees_expan += tree.expan  # we calculate density...
                                    trees_ba += tree.basal_area*tree.expan/10000  # ... and basal area


                        expan_add = new_area_basimetrica*trees_expan/trees_ba  # we calculate the amount of expan to add
                        sum_expan = []  # that list will save the values of expan ingrowth to add to the alive trees (needed because we will work with 2 lists)

                        for tree in tree_ingrowth:  # for each tree...

                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                                if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                                    new_tree_ing = Tree()  # trees that will be shown with status = I
                                    new_tree_ing.clone(tree)
                                    new_tree_ing.add_value('status', 'I')
                                    new_tree_ing.add_value('bal', 0)  # set bal value as 0                                
                                    new_tree_ing.add_value('expan', (expan_add/new_plot.density)*new_tree_ing.expan)  # we add the corresponding value
                                    new_tree_ing.add_value('ba_ha', new_tree_ing.expan*new_tree_ing.basal_area/10000)  # update g/ha value
                                    new_tree_ing.add_value('vol_ha', new_tree_ing.expan*new_tree_ing.vol/1000)  # update vol/ha value                                
                                    sum_expan.append(new_tree_ing.expan)

                                    # temporal variables to calculate plot information about ingrowth trees
                                    ing_tree = new_tree_ing.expan  # calculate expan ingrowth per tree 
                                    ing_n += new_tree_ing.expan  # calculate expan accumulated ingrowth
                                    if new_tree_ing.basal_area == '':
                                        new_tree_ing.add_value('basal_area', 0)
                                    ing_ba += ing_tree*new_tree_ing.basal_area  # calculate basal area accumulated ingrowth in cm2
                                    if 'vol' in TREE_VARS:
                                        if new_tree_ing.vol == '':
                                            new_tree_ing.add_value('vol', 0)                            
                                        ing_vol += ing_tree*new_tree_ing.vol  # calculate volume accumulated ingrowth in dm3
                                    if 'wt' in TREE_VARS:
                                        if new_tree_ing.wt == '':
                                            new_tree_ing.add_value('wt', 0)                            
                                        ing_wt += ing_tree*new_tree_ing.wt  # calculate biomass accumulated ingrowth in kg

                                    ingrowth_trees.append(new_tree_ing)  # we add trees with status = I to a new list

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                                if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model
           
                                    new_tree_ing = Tree()  # trees that will be shown with status = I
                                    new_tree_ing.clone(tree)
                                    new_tree_ing.add_value('status', 'I')
                                    new_tree_ing.add_value('bal', 0)  # set bal value as 0                                
                                    new_tree_ing.add_value('expan', (expan_add/new_plot.density)*new_tree_ing.expan)  # we add the corresponding value
                                    new_tree_ing.add_value('ba_ha', new_tree_ing.expan*new_tree_ing.basal_area/10000)  # update g/ha value
                                    new_tree_ing.add_value('vol_ha', new_tree_ing.expan*new_tree_ing.vol/1000)  # update vol/ha value                                
                                    sum_expan.append(new_tree_ing.expan)

                                    # temporal variables to calculate plot information about ingrowth trees
                                    ing_tree = new_tree_ing.expan  # calculate expan ingrowth per tree 
                                    ing_n += new_tree_ing.expan  # calculate expan accumulated ingrowth
                                    if new_tree_ing.basal_area == '':
                                        new_tree_ing.add_value('basal_area', 0)
                                    ing_ba += ing_tree*new_tree_ing.basal_area  # calculate basal area accumulated ingrowth in cm2
                                    if 'vol' in TREE_VARS:
                                        if new_tree_ing.vol == '':
                                            new_tree_ing.add_value('vol', 0)                            
                                        ing_vol += ing_tree*new_tree_ing.vol  # calculate volume accumulated ingrowth in dm3
                                    if 'wt' in TREE_VARS:
                                        if new_tree_ing.wt == '':
                                            new_tree_ing.add_value('wt', 0)                            
                                        ing_wt += ing_tree*new_tree_ing.wt  # calculate biomass accumulated ingrowth in kg

                                    ingrowth_trees.append(new_tree_ing)  # we add trees with status = I to a new list


                        count_sum_expan = 0  # variable needed to move over the values of expan ingrowth
                        for tree in tree_alive_ing:

                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                                if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                                    new_tree_alive = Tree()  # alive trees modified by survival and growth functions
                                    new_tree_alive.clone(tree)
                                    new_tree_alive.add_value('expan', sum_expan[count_sum_expan] + new_tree_alive.expan)  # we add the expan calculated before
                                    count_sum_expan += 1

                                    alive_ing_trees.append(new_tree_alive)  # after modified expan by ingrowth, we add the tree to the list

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                                if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model

                                    new_tree_alive = Tree()  # alive trees modified by survival and growth functions
                                    new_tree_alive.clone(tree)
                                    new_tree_alive.add_value('expan', sum_expan[count_sum_expan] + new_tree_alive.expan)  # we add the expan calculated before
                                    count_sum_expan += 1

                                    alive_ing_trees.append(new_tree_alive)  # after modified expan by ingrowth, we add the tree to the list


                    #--# CASE 2 #--#

                    # ingrowth distribution function available at the model

                    else:  

                        # STEP 1: check if all the CDs has trees to include the ingrowth

                        # create variables to control trees in CD and a list of CD
                        trees_in_k = trees_out_k = 0
                        available_trees = [True] * len(distribution)

                        # check if there are trees in all the needed cd to include expan
                        for index, k in enumerate(distribution):  # index = order value; k = sublist

                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':

                                for tree in tree_ingrowth:

                                    if int(tree.specie) == int(
                                        Model.specie_ifn_id):  # to trees of the same specie as the model

                                        if tree.dbh >= k[0] and tree.dbh < k[1]:

                                            trees_in_k += 1

                                        else:

                                            trees_out_k += 1

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2' in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':

                                for tree in tree_ingrowth:

                                    if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(
                                            plot.id_sp2):  # to trees of the same specie as the model

                                        if tree.dbh >= k[0] and tree.dbh < k[1]:

                                            trees_in_k += 1

                                        else:

                                            trees_out_k += 1

                            # if no trees in a certain CD class
                            if trees_in_k == 0:

                                # the class is mark as False
                                available_trees[index] = False

                            # reset variables
                            trees_in_k = trees_out_k = 0


                        # STEP 2: calculate the amount of ingrowth to add on each CD using existing trees as reference


                        sum_n = sum_g = sum_vol = sum_wt = 0
                        count = 0

                        for tree in tree_ingrowth:  # for each tree...

                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                                if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                                    for k in distribution:  # for each diametric class established at the model

                                        if tree.dbh >= distribution[count][0] and tree.dbh < distribution[count][1]:
                                        # if diameter are between the diameter limits, their value are used to next calculation. If not, the data will be saved and the distribution
                                        # will be moved to the next diameter class
                                            sum_n += tree.expan  # sum of the expan
                                            sum_g += tree.expan*tree.basal_area/10000  # sum of the basal area (m2/ha)
                                            break

                                        else:  # when diameter condition stop to be agreed...

                                            distribution[count].append(sum_n)  # we add expan of the diametric class to distribution list
                                            distribution[count].append(sum_g)  # we add basal area of the diametric class to distribution list
                                            if distribution[count][4] != 0:
                                                N_add = (distribution[count][3]/distribution[count][4])*distribution[count][2]  # we calculate the expan to add for each diametric class
                                            else:
                                                N_add = 0
                                            distribution[count].append(N_add)  # we add expan to add for each diametric class to distribution list
                                            count += 1  # we move to the next sublist of distribution (next diametric class)
                                            sum_n = sum_g = sum_vol = sum_wt = 0  # we start to count again

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                                if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model

                                    for k in distribution:  # for each diametric class stablished at the model

                                        if tree.dbh >= distribution[count][0] and tree.dbh < distribution[count][1]:
                                        # if diameter are between the diameter limits, their value are used to next calculation. If not, the data will be saved and the distribution
                                        # will be moved to the next diameter class
                                            sum_n += tree.expan  # sum of the expan
                                            sum_g += tree.expan*tree.basal_area/10000  # sum of the basal area (cm2)
                                            break

                                        else:  # when diameter condition stop to be agrred...

                                            distribution[count].append(sum_n)  # we add expan of the diametric class to distribution list
                                            distribution[count].append(sum_g)  # we add basal area of the diametric class to distribution list
                                            if distribution[count][4] != 0:
                                                N_add = (distribution[count][3]/distribution[count][4])*distribution[count][2]  # we calculate the expan to add for each diametric class
                                            else:
                                                N_add = 0
                                            distribution[count].append(N_add)  # we add expan to add for each diametric class to distribution list
                                            count += 1  # we move to the next sublist of distribution (next diametric class)
                                            sum_n = sum_g = sum_vol = sum_wt = 0  # we start to count again


                        distribution[count].append(sum_n)  # we add expan of the diametric class to distribution list
                        distribution[count].append(sum_g)  # we add basal area of the diametric class to distribution list
                        if distribution[count][4] != 0:
                            N_add = (distribution[count][3]/distribution[count][4])*distribution[count][2]  # we calculate the expan to add for each diametric class
                        else:
                            N_add = 0
                        distribution[count].append(N_add)  # we add expan to add for each diametric class to distribution list

                        # at this point, each distribution sublist (each CD) has the next information:
                        # [min_dbh, max_dbh, G_to_add, N_cd, G_cd, N_to_add]


                        # STEP 3: create the trees with status 'I'


                        sum_expan = []  # that list will save the values of expan ingrowth to add to the alive trees (needed because we will work with 2 lists)

                        for tree in tree_ingrowth:

                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                                if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                                    for index, k in enumerate(distribution):  # for each diametric class...

                                        if available_trees[index] == False and k[2] != 0:  # when no trees in CD and it's needed to include ingrowth...

                                            # tree cloned (as a template) giving a special ID
                                            new_tree_ing = Tree()  # trees that will be shown with status = I
                                            new_tree_ing.create_new_from_clone(tree, n_code='new')

                                            # set new information for the tree with status = I
                                            # TODO: los cálculos con este ingrowth no van a salir bien, creo que no se contabilizará WT y V añadido
                                            # TODO: añadir a masas mixtas
                                            new_tree_ing.add_value('status', 'I')
                                            new_tree_ing.add_value('dbh', (k[0] + k[1])/2)
                                            new_tree_ing.add_value('basal_area', math.pi * (new_tree_ing.dbh / 2) ** 2)
                                            new_tree_ing.add_value('expan', (1/new_tree_ing.basal_area) * k[2] * 10000)  # we add the corresponding value

                                            new_tree_ing.add_value('height', 0)
                                            new_tree_ing.add_value('bal', 0)  # set bal value as 0
                                            new_tree_ing.add_value('ba_ha', new_tree_ing.expan*new_tree_ing.basal_area/10000)  # update g/ha value
                                            new_tree_ing.add_value('vol', 0)
                                            new_tree_ing.add_value('vol_ha', 0)  # update vol/ha value

                                            # temporal variables to calculate plot information about ingrowth trees
                                            ing_tree = new_tree_ing.expan  # calculate expan ingrowth per tree
                                            ing_n += new_tree_ing.expan  # calculate expan accumulated ingrowth
                                            if new_tree_ing.basal_area == '':
                                                new_tree_ing.add_value('basal_area', 0)
                                            ing_ba += ing_tree*new_tree_ing.basal_area  # calculate basal area accumulated ingrowth in cm2
                                            if 'vol' in TREE_VARS:
                                                if new_tree_ing.vol == '':
                                                    new_tree_ing.add_value('vol', 0)
                                                ing_vol += ing_tree*new_tree_ing.vol  # calculate volume accumulated ingrowth in dm3
                                            if 'wt' in TREE_VARS:
                                                if new_tree_ing.wt == '':
                                                    new_tree_ing.add_value('wt', 0)
                                                ing_wt += ing_tree*new_tree_ing.wt  # calculate biomass accumulated ingrowth in kg

                                            ingrowth_trees.append(new_tree_ing)  # añado los árboles con status = I a una nueva lista

                                            # repeat the process for tree with status ''

                                            # tree cloned (as a template) giving a special ID
                                            new_tree_alive = Tree()
                                            new_tree_alive.create_new_from_clone(tree, n_code='same')

                                            # set new information for the tree with status = ''
                                            # TODO: los cálculos con este ingrowth no van a salir bien, creo que no se contabilizará WT y V añadido
                                            # TODO: añadir a masas mixtas
                                            new_tree_alive.add_value('status', '')
                                            new_tree_alive.add_value('dbh', (k[0] + k[1])/2)
                                            new_tree_alive.add_value('basal_area', math.pi * (new_tree_alive.dbh / 2) ** 2)
                                            new_tree_alive.add_value('expan', (1/new_tree_alive.basal_area) * k[2] * 10000)  # we add the corresponding value

                                            new_tree_alive.add_value('height', 0)
                                            new_tree_alive.add_value('bal', 0)  # set bal value as 0
                                            new_tree_alive.add_value('ba_ha', new_tree_alive.expan*new_tree_alive.basal_area/10000)  # update g/ha value
                                            new_tree_alive.add_value('vol', 0)
                                            new_tree_alive.add_value('vol_ha', 0)  # update vol/ha value

                                            alive_ing_trees.append(new_tree_alive)  # add trees to the new list

                                            # deactive this as the expan is already added
                                            available_trees[index] = True


                                        if tree.dbh >= k[0] and tree.dbh < k[1]:  # if diameter condition are between the limits...

                                            new_tree_ing = Tree()  # trees that will be shown with status = I
                                            new_tree_ing.clone(tree)
                                            new_tree_ing.add_value('status', 'I')
                                            new_tree_ing.add_value('bal', 0)  # set bal value as 0
                                            if k[3] != 0:
                                                new_tree_ing.add_value('expan', (k[5]/k[3])*new_tree_ing.expan)  # we add the corresponding value
                                            else:
                                                new_tree_ing.add_value('expan', 0)
                                            new_tree_ing.add_value('ba_ha', new_tree_ing.expan*new_tree_ing.basal_area/10000)  # update g/ha value
                                            new_tree_ing.add_value('vol_ha', new_tree_ing.expan*new_tree_ing.vol/1000)  # update vol/ha value
                                            sum_expan.append(new_tree_ing.expan)  # we save that value in order to add it to alive trees

                                            # temporal variables to calculate plot information about ingrowth trees
                                            ing_tree = new_tree_ing.expan  # calculate expan ingrowth per tree
                                            ing_n += new_tree_ing.expan  # calculate expan accumulated ingrowth
                                            if new_tree_ing.basal_area == '':
                                                new_tree_ing.add_value('basal_area', 0)
                                            ing_ba += ing_tree*new_tree_ing.basal_area  # calculate basal area accumulated ingrowth in cm2
                                            if 'vol' in TREE_VARS:
                                                if new_tree_ing.vol == '':
                                                    new_tree_ing.add_value('vol', 0)
                                                ing_vol += ing_tree*new_tree_ing.vol  # calculate volume accumulated ingrowth in dm3
                                            if 'wt' in TREE_VARS:
                                                if new_tree_ing.wt == '':
                                                    new_tree_ing.add_value('wt', 0)
                                                ing_wt += ing_tree*new_tree_ing.wt  # calculate biomass accumulated ingrowth in kg

                                            ingrowth_trees.append(new_tree_ing)  # añado los árboles con status = I a una nueva lista

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                                if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model

                                    for k in distribution:  # for each diametric class...

                                        if tree.dbh >= k[0] and tree.dbh < k[1]:  # if diameter condition are between the limits...

                                            new_tree_ing = Tree()  # trees that will be shown with status = I
                                            new_tree_ing.clone(tree)
                                            new_tree_ing.add_value('status', 'I')
                                            new_tree_ing.add_value('bal', 0)  # set bal value as 0
                                            if k[3] != 0:
                                                new_tree_ing.add_value('expan', (k[5]/k[3])*new_tree_ing.expan)  # we add the corresponding value
                                            else:
                                                new_tree_ing.add_value('expan', 0)
                                            new_tree_ing.add_value('ba_ha', new_tree_ing.expan*new_tree_ing.basal_area/10000)  # update g/ha value
                                            new_tree_ing.add_value('vol_ha', new_tree_ing.expan*new_tree_ing.vol/1000)  # update vol/ha value
                                            sum_expan.append(new_tree_ing.expan)  # we save that value in order to add it to alive trees

                                            # temporal variables to calculate plot information about dead trees
                                            ing_tree = new_tree_ing.expan  # calculate expan ingrowth per tree
                                            ing_n += new_tree_ing.expan  # calculate expan accumulated ingrowth
                                            if new_tree_ing.basal_area == '':
                                                new_tree_ing.add_value('basal_area', 0)
                                            ing_ba += ing_tree*new_tree_ing.basal_area  # calculate basal area accumulated ingrowth in cm2
                                            if 'vol' in TREE_VARS:
                                                if new_tree_ing.vol == '':
                                                    new_tree_ing.add_value('vol', 0)
                                                ing_vol += ing_tree*new_tree_ing.vol  # calculate volume accumulated ingrowth in dm3
                                            if 'wt' in TREE_VARS:
                                                if new_tree_ing.wt == '':
                                                    new_tree_ing.add_value('wt', 0)
                                                ing_wt += ing_tree*new_tree_ing.wt  # calculate biomass accumulated ingrowth in kg

                                            ingrowth_trees.append(new_tree_ing)  # añado los árboles con status = I a una nueva lista


                        # STEP 4: modify the expan of the trees with status ''


                        count_sum_expan = 0  # variable needed to move over the values of expan ingrowth
                        for tree in tree_alive_ing:

                            # Models of only 1 specie
                            if 'SPECIE_IFN_ID' in MODEL_VARS and Model.specie_ifn_id != '':
                                if int(tree.specie) == int(Model.specie_ifn_id):  # to trees of the same specie as the model

                                    for k in distribution:

                                        if tree.dbh >= k[0] and tree.dbh < k[1]:

                                            new_tree_alive = Tree()  # alive trees modified by survival and growth functions
                                            new_tree_alive.clone(tree)
                                            new_tree_alive.add_value('expan', sum_expan[count_sum_expan] + new_tree_alive.expan)  # we add the expan calculated before

                                            alive_ing_trees.append(new_tree_alive)  # add trees to the new list
                                            count_sum_expan += 1

                            # Models of more than 1 specie
                            elif 'ID_SP1' in PLOT_VARS and 'ID_SP2'  in PLOT_VARS and plot.id_sp1 != '' and plot.id_sp2 != '':
                                if int(tree.specie) == int(plot.id_sp1) or int(tree.specie) == int(plot.id_sp2):  # to trees of the same specie as the model

                                    for k in distribution:

                                        if tree.dbh >= k[0] and tree.dbh < k[1]:

                                            new_tree_alive = Tree()  # alive trees modified by survival and growth functions
                                            new_tree_alive.clone(tree)
                                            new_tree_alive.add_value('expan', sum_expan[count_sum_expan] + new_tree_alive.expan)  # we add the expan calculated before

                                            alive_ing_trees.append(new_tree_alive)  # add trees to the new list
                                            count_sum_expan += 1

                    new_plot.add_value('ING_DENSITY', ing_n)  # upload plot information about added tree density                       
                    new_plot.add_value('ING_BA', ing_ba/10000)  # upload plot information about added tree basal area                    
                    new_plot.add_value('ING_VOL', ing_vol/1000)  # upload plot information about added tree volume                     
                    new_plot.add_value('ING_WT', ing_wt/1000)  # upload plot information about added tree biomass                        
                    
                else:  # if there is no ingrowth...

                    alive_ing_trees = growth_trees.copy()  # we copy the modified information to send to the growth function

                    new_plot.add_value('ING_DENSITY', 0)  # upload plot information about added tree density                       
                    new_plot.add_value('ING_BA', 0)  # upload plot information about added tree basal area                    
                    new_plot.add_value('ING_VOL', 0)  # upload plot information about added tree volume                     
                    new_plot.add_value('ING_WT', 0)  # upload plot information about added tree biomass  


                dead_trees = self.delete_info(dead_trees)  # delete variables not needed on the output
                ingrowth_trees = self.delete_info(ingrowth_trees)

                final_trees.extend(dead_trees)  # add dead trees, status = M
                final_trees.extend(ingrowth_trees)  # add ingrowth trees, status = I
                final_trees.extend(alive_ing_trees)  # add alive trees, status = None

                new_plot.add_trees(final_trees)  # we add all the trees to the next plot, in order to show it at the output

###############################################################################################################
########################################## RECALCULATE AND UPDATE_MODEL #################################################
###############################################################################################################

                new_plot.recalculate()  # recalculate the stand variables after survive, ingrowth and growth

                try:  # once expan recalculations are finished, the next function to realice is update_model
                    model.update_model(operation.get_variable('time'), new_plot, final_trees)  # we send final_trees list to this process
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                if 'AGE' in PLOT_VARS:  # that code updates the age of the stand
                    new_plot.sum_value('AGE', operation.get_variable('time'))
                if 'YEAR' in PLOT_VARS:  # that code updates the year of the stand
                    new_plot.sum_value('YEAR', operation.get_variable('time'))

                result_inventory.add_plot(new_plot)  # once we finish with one plot, we add it to the inventory and continue with the next one

            else:
                Tools.print_log_line('Plot ' + str(plot.id) + ' was not added', logging.INFO)
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
                print('That execution was not realised because the plot age on this step, which is', plot_age,'years, are not between the minimum age of', min,'years and the maximum of', max, 'years established at the scenario file')
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')

                result_inventory.add_plot(plot)

        return result_inventory  # we return the total inventory

    def apply_tree_stand_model(self, inventory: Inventory, model: StandModel, operation: Operation):
        """
        Function executed by engine file when the process selected at the scenario is an execution on a stand model.
        """

        result_inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        for plot in inventory.plots:

            if 'AGE' in PLOT_VARS:
                plot_age = plot.age
            else:
                plot_age = 0

            if min <= plot_age <= max:  # execute the function only if the age of the plot are between the stablished range of the scenario (or default range)
                
                new_plot = Plot()
                new_plot.clone(plot)

                try:
                    model.growth(plot, new_plot, operation.get_variable('time'))
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                if 'AGE' in PLOT_VARS:  # that code updates the age of the stand
                    new_plot.sum_value('AGE', operation.get_variable('time'))
                if 'YEAR' in PLOT_VARS:  # that code updates the year of the stand
                    new_plot.sum_value('YEAR', operation.get_variable('time'))

                result_inventory.add_plot(new_plot)

            else:
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
                print('That execution was not realised because the plot age on this step, which is', plot_age,'years, are not between the minimum age of', min,'years and the maximum of', max, 'years established at the scenario file')
                print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')

                new_plot = Plot()
                new_plot.clone(plot)
                result_inventory.add_plot(new_plot)

        return result_inventory

    def apply_load_model(self, file_path: str, model: LoadModel, operation: Operation):
        """
        Function that loads the information of the initial inventory
        """

        operation.add_variable('time', 0)  # time on LOAD operation must be always 0    

        return model.apply_model(file_path, operation.get_variable('init'))

    def close(self):
        return 0


    def delete_info(self, list_of_trees: list):
        """
        Function that delete non useful variables content.
        It is used for dead and ingrowth trees.
        """

        trees_updated = list()  # list of cleaned trees

        TO_PRESERVE = [  # variables to preserve
        # IDs
        "INVENTORY_ID",
        "PLOT_ID",
        "TREE_ID",
        # Remarkable variables
        "specie",
        "expan",
        "status"
        ]

        TO_DELETE = [i for i in TREE_VARS if i not in TO_PRESERVE]  # delete other variables

        for tree in list_of_trees:
            for variable in TO_DELETE:
                tree.add_value(variable, 0)  # '' is not allowed, I don't know why
            trees_updated.append(tree)

        return trees_updated
