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

from models.stand_model import StandModel
from data import Tree
from data import Plot
from data import DESC
from data import ASC
from data.general import Area, Model, Warnings
from data.variables import TREE_VARS, PLOT_VARS, AREA_VARS, MODEL_VARS, WARNING_VARS, CUTS_DICT
from data.variables import Variables

import math
import sys
import logging
import numpy as np
import os


# xx model (place, Spain), version 01
# Written by iuFOR
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (University of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, University of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/

# Stand models in Simanfor are make up of 3 functions
#            -> initialize()             <--- for setting up initial variables and calculate productivity of the area: SI = site index
#            -> growth()       <--- for calculus of stand variables variations after a simulation of "time" years
#            -> harvest()   <--- for simulate thinning behabiour of stands variables

class StandTemplate(StandModel):

    def __init__(self, configuration=None):
        super().__init__(name="StandTemplate", version=1)


    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def model_info(self):
        """
        Function to set the model information at the at the output.
        It will be runned by initialize function once.
        """

        try:  # errors inside that construction will be annodbhced

            Model.model_name = 'stand_template'  # set the model name to show it at the output
            Model.specie_ifn_id = 999  # Set the model specie ID to mark the trees of different species
            Model.exec_time = 999  # recommended executions time to use that model
            Model.aplication_area = 'none'  # area reccomended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = 'example'  # provenance regions reccomended to use the model
            Model.model_type = 'under_development'  # SIMANFOR model type. It can be: '' are neccesary
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'link'  # link to model card in english
            Model.model_card_es = 'link'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()

    ### initial function. Only run after importing inventory    
    ## "plot" are variables of the plot in database
    ## This function is the more suitable for calculate Site Index, constant value along all simulation
    ##
    def initialize(self, plot: Plot):
        """
        Function that update the gaps on the information with the inventory data
        Site Index equation:
            Doc.: 
            Ref.: 
        Volume equation:
            Doc.: 
            Ref.:      
        Reineke Index equation: standard value
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                          Running: Xstand model (XX). Plot:', plot.plot_id                           )
        print('#--------------------------------------------------------------------------------------------------#')

        try:

            self.model_info()
            plot.add_value('REINEKE_VALUE', -1.605)  # r contstant value of SDI  to the specie of the model (-1.605 as default)  

            if Area.specie_ifn_id != Model.specie_ifn_id:
                print()
                print('BE CAREFUL! You are trying to run that model of xxxxxxxxxxxxxxx with an inventory of another specie.')
                print('Please, check the variable "SPECIE_IFN_ID" on your inventory and insert the right value (', Model.specie_ifn_id, ') or try to use another inventory/model.')
                print()
                Warnings.specie_error = 1  # Variable needed to notify an specie error at the output
                
        #-----------------------------------FIRST: calculate PLOT data by using TREE data-----------------------------------------#

            tree_expansion: float = 0.0

            expansion_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC) 
            selection_trees = list()

            for tree in expansion_trees:   
                if tree_expansion < 100:
                    tree_expansion += tree.expan
                    selection_trees.append(tree)
                else:
                    break

            plot_expan = plot_ba = plot_h = 0

            for tree in expansion_trees:

                plot_expan += tree.expan
                plot_ba += tree.basal_area*tree.expan
                plot_h += tree.height*tree.expan

            # From here, silence all the variables that are not needed to realise the calculations of initialize

            if plot.basal_area == 0 or plot.basal_area == '':
                plot.add_value('BASAL_AREA', plot_ba/10000)
            if plot.dominant_h == 0 or plot.dominant_h == '':
                plot.add_value('DOMINANT_H', plot.get_dominant_height(selection_trees))
            if plot.density == 0 or plot.density == '':
                plot.add_value('DENSITY', plot_expan)
            if plot.mean_h == 0 or plot.mean_h == '':
                plot.add_value('MEAN_H', plot_h/plot_expan)


        #-----------------------------------SECOND: calculate PLOT data by using PLOT data-----------------------------------------#

            # Site Index
            if plot.si == 0 or plot.si == '':
                t2 =  # SI reference age (years)
                plot.add_value('REF_SI_AGE', t2)   
                plot.add_value('SI', SI)  # store Site Index in database

            # Quadratic mean diameter
            dg = 
            plot.add_value('QM_DBH', dg)

            # Basal Area
            G = 
            plot.add_value('BASAL_AREA', G)

            # Mean Diameter
            mean_dbh =
            plot.add_value('MEAN_DBH', mean_dbh) 

            # Mean Height
            if plot.mean_dbh != 0 and plot.dominant_dbh != 0:
                mean_h = 
                plot.add_value('MEAN_H', mean_h) 

            # Slenderness
            plot.add_value('SLENDERNESS_DOM', plot.dominant_h*100/plot.dominant_dbh)
            plot.add_value('SLENDERNESS_MEAN', plot.mean_h*100/plot.mean_dbh)  

            # Initial Volume
            V = 
            plot.add_value('VOL', V)  # store initial stand volume in database
        
            # Reineke Index
            if plot.qm_dbh != 0:
                SDI = plot.density*pow(25/plot.qm_dbh, plot.reineke_value)  # Reineke density index
                plot.add_value('REINEKE', SDI)  # store Reineke index in database

            # Hart index
            if plot.dominant_h != 0 and plot.density != 0:
                S = 10000/(plot.dominant_h*math.sqrt(plot.density))  # Hart-Becking Index (S) calculated to simple rows 
                plot.add_value('HART', S)  # Store Hart index in database
                S_staggered = (10000/plot.dominant_h)*math.sqrt(2/(plot.density*math.sqrt(3)))  # Hart-Becking Index (S) calculated to staggered rows 
                plot.add_value('HART_STAGGERED', S_staggered)  # Store Hart index in database

        except Exception:
            self.catch_model_exception()


    ### simulation function. run in every simulation process to simulate growth. Change of stand variables after "time" years
    ##  old_plot are variables in initial state
    ##  new_plot are variables after "time" years
    ## 
    def growth(self, old_plot: Plot, new_plot: Plot, time: int):
        """
        Function that includes the equations needed in the executions.
        BE CAREFUL!! Is not needed to store the new plot age on the 'AGE' variable, the simulator will do it by his own.
        Dominant Height equation:
            Doc.: 
            Ref.: 
        Basal Area Growth equation:
            Doc.: 
            Ref.: 
        Survive equation:
            Doc.: 
            Ref.: 
        Volume equation:
            Doc.: 
            Ref.: 
        Quadratic Mean Diameter --> standard equation
        Reineke Index equation: standard value
        Hart Index equation --> standard equation
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                          Running: Xstand model (XX). Plot:', old_plot.plot_id                           )
        print('#--------------------------------------------------------------------------------------------------#')


        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same of the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:

            # BE CAREFUL!! Is not needed to store the new plot age and time variables, the simulator will do it by his own.
            # if you need to use the "actualised" age or time, just create another new variable to do it.
            if 'YEAR' in PLOT_VARS:
                new_year = old_plot.year + time  # YEAR is automatically updated after the execution process
            if 'AGE' in PLOT_VARS:
                new_age = old_plot.age + time  # AGE is automatically updated after the execution process

            # Dominant Height
            Xo = 
            Ho = 
            new_plot.add_value('DOMINANT_H', Ho)  # store Dominant height in database

            # Mortality
            N = 
            new_plot.add_value('DENSITY', N)  # store trees per hectare in database
            new_plot.add_value('DEAD_DENSITY', old_plot.density - new_plot.density)  # Nº of dead trees after an execution (nº trees/ha)
            new_plot.add_value('DEAD_BA', old_plot.basal_area*new_plot.dead_density/old_plot.density)

            # Quadratic Mean Diameter
            dg = 
            new_plot.add_value('QM_DBH', dg)

            # Basal Area        
            G = 
            new_plot.add_value('BASAL_AREA', G)  # store basal area in database

            # Volume
            V = 
            new_plot.add_value('VOL', V)  # store total stand volume with bark in database

            # Mean Diameter
            mean_dbh = 
            new_plot.add_value('MEAN_DBH', mean_dbh) 

            # Mean Height
            if new_plot.mean_dbh != 0 and new_plot.dominant_dbh != 0:
                mean_h = 
                new_plot.add_value('MEAN_H', mean_h)  # store mean height in database

            # Slenderness
            new_plot.add_value('SLENDERNESS_DOM', new_plot.dominant_h*100/new_plot.dominant_dbh)
            new_plot.add_value('SLENDERNESS_MEAN', new_plot.mean_h*100/new_plot.mean_dbh)  

            # Reineke Index
            if new_plot.qm_dbh != 0:
                SDI = new_plot.density*pow(25/new_plot.qm_dbh, old_plot.reineke_value)  # Reineke density index
                new_plot.add_value('REINEKE', SDI)  # store Reineke index in database

            # Hart index
            if new_plot.dominant_h != 0 and new_plot.density != 0:
                S = 10000/(new_plot.dominant_h*math.sqrt(new_plot.density))  # Hart-Becking Index (S) calculated to simple rows 
                new_plot.add_value('HART', S)  # Store Hart index in database
                S_staggered = (10000/new_plot.dominant_h)*math.sqrt(2/(new_plot.density*math.sqrt(3)))  # Hart-Becking Index (S) calculated to staggered rows 
                new_plot.add_value('HART_STAGGERED', S_staggered)  # Store Hart index in database   

            new_plot.add_value('DENSITY_CUT_VOLUME', 0)  # stand density harvested volume (%)
            new_plot.add_value('BA_CUT_VOLUME', 0)  # stand basal area harvested volume (%)
            new_plot.add_value('VOL_CUT_VOLUME', 0)  # stand volume harvested volume (%)

        except Exception:
            self.catch_model_exception()


    ###  calculus of variables changes after thinning
    ##  old_plot are variables before thinning
    ##  new_plot are variables after thinning
    ## 
    def harvest( self, old_plot: Plot, new_plot: Plot, #cut_down, 
                             cut_criteria, volume, time, 
                             min_age, max_age):
        """
        Function that includes the equations needed in the cuts.
        Harvest equations:
            Doc.: 
            Ref.: 
        Reineke Index equation (value):
            Doc.: 
            Ref.: 
        Hart Index equation --> standard equation
        """

        # trimType values: ( ByTallest, BySmallest, Systematic ) --> Thinning types
        # cutDownType values: ( PercentOfTrees, Volume, Area )   --> Variable used to evaluate the thinning
        # volume ---> value: (% of "Variable" reduced after the thinning) 

        print('#------------------------------------------------------------------------------------------------- #')
        print('                          Running: Xstand model (XX). Plot:', old_plot.plot_id                           )
        print('#--------------------------------------------------------------------------------------------------#')


        if time != 0:
            print('BE CAREFUL! When you plan a HARVEST the time must be 0, and you wrote a', time, 'years for the harvest period!')
            print('Please, change your time value to 0 and run your scenario again.')
            # that variable must be activated just in case if the time of the cut is different to 0
            Warnings.cut_error = 1  # that variable value must be 1 to notify the error at the output


        try:

            value = volume

            # Thinning parameters
            if cut_criteria == CUTS_DICT['PERCENTOFTREES']:
                tpuN = value/100  # ratio of thinning trees per hectare and total before thinning
                N = (1 - tpuN)*old_plot.density  # trees per hectare after thinning
                
                if N != 0:
                    G = old_plot.basal_area*N/old_plot.density
                    MTBA = G*10000/N  # Mean Tree Basal Area
                    dg  = 2*math.sqrt(MTBA/math.pi)  # Quadratic mean diameter
                    MTBA = math.pi*pow(dg/2, 2)  # average mean basal area
                    V =   # equation to calculate volume
                else:
                    G = dg = V = 0

                      
            elif cut_criteria == CUTS_DICT['AREA']:
                tpuBA = value/100  # ratio of thinning basal area and total before thinning
                G = (1 - tpuBA)*old_plot.basal_area  # basal area after thinning
                
                if G != 0:
                    N = old_plot.density*G/old_plot.basal_area
                    MTBA = G*10000/N  # Mean Tree Basal Area
                    dg  = 2*math.sqrt(MTBA/math.pi)  # Quadratic mean diameter
                    V =   # equation to calculate volume
                else:
                    N = dg = V = 0


            elif cut_criteria == CUTS_DICT['VOLUME']:
                tpuVOL = value/100  # ratio of thinning volume and total before thinning
                V = (1 - tpuVOL)*old_plot.vol  # volume after thinning
                
                if V != 0:
                    G = old_plot.basal_area*V/old_plot.vol  # equation to calculate stand basal area
                    N = old_plot.density*V/old_plot.vol
                    MTBA = G*10000/N  # Mean Tree Basal Area
                    dg = 2*math.sqrt(MTBA/math.pi)  # equation to calculate quadratic mean diameter
                else:
                    G = dg = N = 0

            
            new_plot.add_value('DENSITY', N)  # store trees per hectare in database
            new_plot.add_value('QM_DBH', dg)  # store quadratic mean diameter
            new_plot.add_value('BASAL_AREA', G)  # store basal area in database
            new_plot.add_value('VOL', V)  # store total stand volume with bark in database

            new_plot.add_value('DENSITY_CUT_VOLUME', 1 - new_plot.density/old_plot.density)  # stand density harvested volume (%)
            new_plot.add_value('BA_CUT_VOLUME', 1 - new_plot.basal_area/old_plot.basal_area)  # stand basal area harvested volume (%)
            new_plot.add_value('VOL_CUT_VOLUME', 1 - new_plot.vol/old_plot.vol)  # stand volume harvested volume (%)

            new_plot.add_value('DEAD_DENSITY', 0)  # Nº of dead trees after an cut (nº trees/ha)
            new_plot.add_value('DEAD_BA', 0)            

            # Reineke Index
            if new_plot.qm_dbh != 0:
                SDI = new_plot.density*pow(25/new_plot.qm_dbh, old_plot.reineke_value)  # Reineke density index
            else:
                SDI = 0
            new_plot.add_value('REINEKE', SDI)  # store Reineke index in database

            # Hart index
            if new_plot.density != 0:
                S = 10000/(new_plot.dominant_h*math.sqrt(new_plot.density))  # Hart-Becking Index (S) calculated to simple rows 
                S_staggered = (10000/new_plot.dominant_h)*math.sqrt(2/(new_plot.density*math.sqrt(3)))  # Hart-Becking Index (S) calculated to staggered rows                 
            else:
                S = S_staggered = 0
            new_plot.add_value('HART', S)  # Store Hart index in database
            new_plot.add_value('HART_STAGGERED', S_staggered)  # Store Hart index in database   

        except Exception:
            self.catch_model_exception()


    def vars():
        """
        That function will add some needed variables to the output, calculated during the model, and it will remove another variables that are not needed.
        It can only be added variable to tree, but no to the plot (it will return an error).
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
            #"DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            "ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

            # Basic plot variables calculated - basal area
            #"BASAL_AREA",  # Basal area  # (m2/ha)
            "BASAL_AREA_SP1",  # basal area of specie 1 on a mix plot - mixed models
            "BASAL_AREA_SP2",  # basal area of specie 2 on a mix plot - mixed models
            "BA_MAX",  # BA Max  # (cm2)
            "BA_MAX_SP1",  # BA Max  # (cm2) of specie 1 on a mix plot - mixed models
            "BA_MAX_SP2",  # BA Max  # (cm2) of specie 2 on a mix plot - mixed models        
            "BA_MIN",  # BA Min  # (cm2) 
            "BA_MIN_SP1",  # BA Min  # (cm2) of specie 1 on a mix plot - mixed models
            "BA_MIN_SP2",  # BA Min  # (cm2) of specie 2 on a mix plot - mixed models
            "MEAN_BA",  # Mean BA  # (cm2)
            "MEAN_BA_SP1",  # Mean BA  # (cm2) of specie 1 on a mix plot - mixed models
            "MEAN_BA_SP2",  # Mean BA  # (cm2) of specie 2 on a mix plot - mixed models
            #"BA_CUT_VOLUME",  # Basal area harvested volume (%)
            #"DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            "ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

            # Basic plot variables calculated - diameter
            "DBH_MAX",  # D Max  # (cm)
            "DBH_MAX_SP1",  # D Max  # (cm) of specie 1 on a mix plot - mixed models
            "DBH_MAX_SP2",  # D Max  # (cm) of specie 2 on a mix plot - mixed models
            "DBH_MIN",  # D Min  # (cm)
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
            "DOMINANT_SECTION",  # Dominant section (cm)
            "DOMINANT_SECTION_SP1",  # Dominant section (cm) of specie 1 on a mix plot - mixed models
            "DOMINANT_SECTION_SP2",  # Dominant section (cm) of specie 2 on a mix plot - mixed models

            # Basic plot variables calculated - height
            "H_MAX",  # H Max  # (m)
            "H_MAX_SP1",  # H Max  # (m) of specie 1 on a mix plot - mixed models
            "H_MAX_SP2",  # H Max  # (m) of specie 2 on a mix plot - mixed models
            "H_MIN",  # H Min  # (m)    
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
            #"VOL",  # Volume  # (m3/ha)
            "BOLE_VOL",  # Bole Volume  # (m3/ha)
            "BARK_VOL",  # Bark Volumen  # (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume harvested percentaje (%)
            #"DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
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
            "bal",  # basal area acumulated  # (m2/ha)
            "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
            "ba_ha",  # basal area per ha  # (m2/ha) 
            "normal_circumference",  # normal circumference  # circumference at breast height (cm)
            "slenderness",  # slenderness (cm/cm)
            
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
        
StandTemplate.vars()