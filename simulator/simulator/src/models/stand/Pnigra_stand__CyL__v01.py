# /usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
#
# Stand dinamic model, developed to
# Pure stands of Pinus nigra located on Castilla y León (Spain)
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


class PinusNigraCyL(StandModel):

    def __init__(self, configuration=None):
        super().__init__(name="Sylves", version=1)


    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def model_info(self):
        """
        Function to set the model information at the output.
        It will be run by initialize function once.
        """

        try:  # errors inside that construction will be announced

            Model.model_name = 'Pnigra_stand__CyL__v01'  # set the model name to show it at the output
            Model.specie_ifn_id = 25  # Set the model specie ID to mark the trees of different species         
            Model.exec_time = 5  # recommended executions time to use that model
            Model.aplication_area = 'Castilla y León (Spain)'  # area recommended to use the model
            Model.valid_prov_reg = '9, 10, 11'  # provenance regions recommended to use the model
            Model.model_type = 'stand_model'  # SIMANFOR model type. It can be: ('' is neccesary)
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'https://github.com/simanfor/modelos/blob/main/masa/Pnigra_cyl_stand_EN.pdf'  # link to model card in english
            Model.model_card_es = 'https://github.com/simanfor/modelos/blob/main/masa/Pnigra_cyl_stand_ES.pdf'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps in the information with the inventory data
        Site Index equation:
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait. Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León, 1-102
            Ref.: del Río et al, 2006
        Volume equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012
        Mean Height equation:
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait. Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León, 1-102
            Ref.: del Río et al, 2006
        Mean Diameter equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Minimum Diameter equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Reineke Index equation (value):
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait., Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León (No. 634.9560946 R585). Junta de Castilla y León, Castilla y León (España). Consejería de Medio Ambiente Ministerio de Educación y Ciencia, Madrid (España) Instituto Nacional de Investigación y Tecnología Agraria y Alimentaria, Madrid (España)
            Ref.: del Rio et al, 2006
        Hart Index equation --> standard equation
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                Running: Pinus nigra stand model (Castilla y León). Plot:', plot.plot_id             )
        print('#--------------------------------------------------------------------------------------------------#')

        try:

            self.model_info()
            plot.add_value('REINEKE_VALUE', -1.621)  # r constant value of SDI to the species of the model (-1.605 as default)    
            
            if Area.specie_ifn_id[plot.plot_id] != Model.specie_ifn_id:
                print()
                print('BE CAREFUL! You are trying to run that model of Pinus nigra with an inventory of another specie.')
                print('Please, check the variable "SPECIE_IFN_ID" on your inventory and insert the right value (', Model.specie_ifn_id, ') or try to use another inventory/model.')
                print()
                Warnings.specie_error = 1  # Variable needed to notify an specie error at the output
                
#-------------------- If plot data is not available, tree data is used to calculate it --------------------------#

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
            #    plot_h += tree.height*tree.expan

            # From here, silence all the variables that are not needed to realize the calculations of initialize

            if plot.basal_area == 0 or plot.basal_area == '':
                plot.add_value('BASAL_AREA', plot_ba/10000)
            if plot.dominant_h == 0 or plot.dominant_h == '':
                plot.add_value('DOMINANT_H', plot.get_dominant_height(selection_trees))
            if plot.density == 0 or plot.density == '':
                plot.add_value('DENSITY', plot_expan)
            #if plot.mean_h == 0 or plot.mean_h == '':
            #    plot.add_value('MEAN_H', plot_h/plot_expan)


#-------------------- Plot data calculation after having all the needed input variables -------------------------#

            # Site Index
            if plot.si == 0 or plot.si == '':
                t2 = 50  # SI reference age (years)
                plot.add_value('REF_SI_AGE', t2)   
                ec01 = pow(plot.dominant_h / 29.7954, 1/1.5162)
                ec02 = pow (1 -  ec01, t2/plot.age)
                plot.add_value('SI', 29.7954 * pow(1 - ec02, 1.5162))
               
            # Initial Volume Over Bark             
            parB0  = 1.69
            parB1  = 0.0604
            parB2  = -48.8
            parB3  = 0.982
            V = math.exp(parB0 + parB1*plot.si + parB2/plot.age + parB3*math.log(plot.basal_area))
            plot.add_value('VOL', V) 
                
            # Quadratic Mean Diameter:      
            if plot.density != 0:
                MTBA = plot.basal_area*10000/plot.density  # Mean Tree Basal Area
                dg = 2*math.sqrt(MTBA/math.pi)  # Quadratic Mean Diameter
                plot.add_value('QM_DBH', dg)  # store quadratic mean diameter

            # Mean Diameter
            parC1 = 0.0021
            parC2 = 0.00168
            parC3 = 0.0595
            mean_dbh = plot.qm_dbh*(1 - 1/(1 + math.exp(parC1*plot.si + parC2*plot.density + parC3*plot.qm_dbh)))
            plot.add_value('MEAN_DBH', mean_dbh)

            # Minimum Diameter
            parD1 = -0.0288
            parD2 = 0.0334
            min_dbh = plot.mean_dbh*(1 - 1/(1 + math.exp(parD1*plot.qm_dbh + parD2*plot.si)))
            plot.add_value('DBH_MIN', min_dbh)

            # Mean Height
            parA0 = 0.1456
            parA1 = 0.9626
            mean_h = parA0 + parA1*plot.dominant_h
            plot.add_value('MEAN_H', mean_h)

            # Slenderness
            plot.add_value('SLENDERNESS_MEAN', plot.mean_h*100/plot.mean_dbh)  

            # Reineke Index
            if plot.qm_dbh != 0:
                SDI = plot.density * pow(25 / plot.qm_dbh, plot.reineke_value)  # Reineke density index
                plot.add_value('REINEKE', SDI)  # store Reineke index in database

            # Hart Index
            if plot.dominant_h != 0 and plot.density != 0:
                S = 10000/(plot.dominant_h*math.sqrt(plot.density))  # Hart-Becking Index (S) calculated to simple rows 
                plot.add_value('HART', S)  # Store Hart index in database
                S_staggered = (10000/plot.dominant_h)*math.sqrt(2/(plot.density*math.sqrt(3)))  # Hart-Becking Index (S) calculated to staggered rows 
                plot.add_value('HART_STAGGERED', S_staggered)  # Store Hart index in database

            plot.add_value('DEAD_DENSITY', 0)  # variable needed to be printed at the summary sheet

        except Exception:
            self.catch_model_exception()


    def growth(self, old_plot: Plot, new_plot: Plot, time: int):
        """
        A function that includes the equations needed in the executions.
        BE CAREFUL!! Is not needed to store the new plot age and year on 'AGE' and 'YEAR' variables, the simulator will do it by his own.
        Dominant Height equation:
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait. Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León, 1-102
            Ref.: del Río et al, 2006
        Basal Area Growth equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Mean Height equation:
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait. Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León, 1-102
            Ref.: del Río et al, 2006
        Survive equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Mean Diameter equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Minimum Diameter equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Volume equation:
            Doc.: Mora JV, del Rio M, Bravo-Oviedo A (2012). Dynamic growth and yield model for Black pine stands in Spain. Forest systems, 21(3), 439-445
            Ref.: Mora et al, 2012 
        Reineke Index equation (value):
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait., Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León (No. 634.9560946 R585). Junta de Castilla y León, Castilla y León (España). Consejería de Medio Ambiente Ministerio de Educación y Ciencia, Madrid (España) Instituto Nacional de Investigación y Tecnología Agraria y Alimentaria, Madrid (España)
            Ref.: del Rio et al, 2006            
        Quadratic Mean Diameter --> standard equation
        Hart Index equation --> standard equation
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                Running: Pinus nigra stand model (Castilla y León). Plot:', old_plot.plot_id             )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same as the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:

            # BE CAREFUL!! Is not needed to store the new plot age and time variables, the simulator will do it by his own.
            # if you need to use the "actualized" age or time, just create another new variable to do it.
            if 'YEAR' in PLOT_VARS:
                new_year = old_plot.year + time  # YEAR is automatically updated after the execution process
            if 'AGE' in PLOT_VARS:
                new_age = old_plot.age + time  # AGE is automatically updated after the execution process

            # Dominant Height              
            ec01 = pow(old_plot.dominant_h / 29.7954, 1 / 1.5162)
            ec02 = pow (1 -  ec01, new_age/old_plot.age)
            new_plot.add_value('DOMINANT_H', 29.7954 * pow(1 - ec02, 1.5162))
            
            # Basal Area
            parA1 = 3.88
            parA2 = 0.0475
            G = math.exp(math.log(old_plot.basal_area)*old_plot.age/new_age + parA1*(1 - old_plot.age/new_age) + parA2*(1 - old_plot.age/new_age)*old_plot.si)
            new_plot.add_value('BASAL_AREA', G)

            # Volume Over Bark     
            parB0 = 1.69
            parB1 = 0.0604
            parB2 = -48.8
            parB3 = 0.982         
            parB4 = 3.81
            parB5 = 0.0466
            V = math.exp(parB0 + parB1*old_plot.si + parB2/new_age + parB3*(old_plot.age/new_age)*math.log(old_plot.basal_area) + parB4*(1 - old_plot.age/new_age) + parB5*(1 - old_plot.age/new_age))
            new_plot.add_value('VOL', V)

            # Mean Height
            parA0 = 0.1456
            parA1 = 0.9626
            mean_h = parA0 + parA1*new_plot.dominant_h
            new_plot.add_value('MEAN_H', mean_h)
                
            # Mortality 
            parA0 = 0.417
            parA1 = -0.00003
            parA2 = 1.57
            N = pow(pow(old_plot.density, parA0) + parA1*old_plot.si*(pow(new_age, parA2) - pow(old_plot.age, parA2)), 1/parA0)
            new_plot.add_value('DENSITY', N)
            new_plot.add_value('DEAD_DENSITY', old_plot.density - new_plot.density)  # Nº of dead trees after an execution (nº trees/ha)
            new_plot.add_value('DEAD_BA', old_plot.basal_area*new_plot.dead_density/old_plot.density)
            parB0  = 1.69
            parB1  = 0.0604
            parB2  = -48.8
            parB3  = 0.982
            V_dead = math.exp(parB0 + parB1*old_plot.si + parB2/old_plot.age + parB3*math.log(new_plot.dead_ba))
            new_plot.add_value('DEAD_VOL', V_dead)  # store dead volume in database            
            
            # Quadratic Mean Diameter        
            if new_plot.density != 0:
                MTBA = new_plot.basal_area*10000/new_plot.density  # Mean Tree Basal Area
                dg = 2*math.sqrt(MTBA/math.pi)  # Quadratic Mean Diameter
                new_plot.add_value('QM_DBH', dg)    
                
            # Mean Diameter
            parC1 = 0.0021
            parC2 = 0.00168
            parC3 = 0.0595
            mean_dbh = new_plot.qm_dbh*(1 - 1/(1 + math.exp(parC1*old_plot.si + parC2*new_plot.density + parC3*new_plot.qm_dbh)))
            new_plot.add_value('MEAN_DBH', mean_dbh)

            # Slenderness
            slenderness_mean = new_plot.mean_h*100/new_plot.mean_dbh
            new_plot.add_value('SLENDERNESS_MEAN', slenderness_mean)             
                
            # Minimum Diameter
            parD1 = -0.0288
            parD2 = 0.0334
            min_dbh = new_plot.mean_dbh*(1 - 1/(1 + math.exp(parD1*new_plot.qm_dbh + parD2*old_plot.si)))
            new_plot.add_value('DBH_MIN', min_dbh)

            # Reineke Index
            if new_plot.qm_dbh != 0:
                SDI = new_plot.density*pow(25/new_plot.qm_dbh, old_plot.reineke_value)  # Reineke density index
                new_plot.add_value('REINEKE', SDI)  # store Reineke index in database

            # Hart Index
            if new_plot.dominant_h != 0 and new_plot.density != 0:
                S = 10000/(new_plot.dominant_h*math.sqrt(new_plot.density))  # Hart-Becking Index (S) calculated to simple rows 
                new_plot.add_value('HART', S)  # Store Hart index in database
                S_staggered = (10000/new_plot.dominant_h)*math.sqrt(2/(new_plot.density*math.sqrt(3)))  # Hart-Becking Index (S) calculated to staggered rows 
                new_plot.add_value('HART_STAGGERED', S_staggered)  # Store Hart index in database   

            new_plot.add_value('DENSITY_CUT_VOLUME', 0)  # stand density harvested volume (trees/ha)
            new_plot.add_value('BA_CUT_VOLUME', 0)  # stand basal area harvested volume (m2/ha)
            new_plot.add_value('VOL_CUT_VOLUME', 0)  # stand volume harvested volume (m3/ha)
            new_plot.add_value('WT_CUT_VOLUME', 0)  # stand biomass harvested volume (t/ha)

        except Exception:
            self.catch_model_exception()


    def harvest(self, old_plot: Plot, new_plot: Plot, cut_criteria, volume, time, min_age, max_age):
        """
        A function that includes the equations needed in the cuts.
        Harvest equations developed by using the initialize equations.  
        Reineke Index equation (value) --> standard value
        Hart Index equation --> standard equation
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                Running: Pinus nigra stand model (Castilla y León). Plot:', old_plot.plot_id             )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != 0:
            print('BE CAREFUL! When you plan a HARVEST the time must be 0, and you wrote a', time, 'years for the harvest period!')
            print('Please, change your time value to 0 and run your scenario again.')
            # that variable must be activated just in case if the time of the cut is different to 0
            Warnings.cut_error = 1  # that variable value must be 1 to notify the error at the output

        try:

            value = volume

            # Parameter for volume equation
            b0  = 1.69
            b1  = 0.0604
            b2  = -48.8
            b3  = 0.982

            
            if cut_criteria == CUTS_DICT['PERCENTOFTREES']:
                tpuN = value/100  # ratio of thinning trees per hectare and total before thinning
                N = (1 - tpuN)*old_plot.density  # trees per hectare after thinning
                
                if N != 0:                
                    G = old_plot.basal_area*N/old_plot.density
                    Ge = old_plot.basal_area - G  # Removed basal area
                    dg = 1.35 + 0.979*old_plot.qm_dbh + 0.859*(Ge/old_plot.basal_area)*old_plot.qm_dbh
                    V = math.exp(b0 + b1*old_plot.si + b2/old_plot.age + b3*math.log(G))  # equation to calculate volume
                    Vcut = V - old_plot.vol
                    V = V - 2*Vcut
                else:
                    G = dg = V = 0


            elif cut_criteria == CUTS_DICT['AREA']:
                tpuBA = value/100  # ratio of thinning basal area and total before thinning
                G = (1 - tpuBA)*old_plot.basal_area  # basal area after thinning
                
                if G != 0:  
                    N = old_plot.density*G/old_plot.basal_area
                    Ge = old_plot.basal_area - G  # Removed basal area
                    dg = 1.35 + 0.979*old_plot.qm_dbh + 0.859*(Ge/old_plot.basal_area)*old_plot.qm_dbh
                    V = math.exp(b0 + b1*old_plot.si + b2/old_plot.age + b3*math.log(G))  # equation to calculate volume
                    Vcut = V - old_plot.vol
                    V = V - 2*Vcut
                else:
                    N = dg = V = 0     


            elif cut_criteria == CUTS_DICT['VOLUME']:
                tpuVOL = value/100  # ratio of thinning volume and total before thinning
                V = (1 - tpuVOL)*old_plot.vol  # volume after thinning
                
                if V != 0:
                    G = math.exp((math.log(V) - b0 - b1*old_plot.si - b2/old_plot.age)/b3)
                    N = old_plot.density*G/old_plot.basal_area
                    Ge = old_plot.basal_area - G  # Removed basal area
                    dg = 1.35 + 0.979*old_plot.qm_dbh + 0.859*(Ge/old_plot.basal_area)*old_plot.qm_dbh
                else:
                    G = dg = N = 0


            new_plot.add_value('DENSITY', N)  # update plot density after the cut
            new_plot.add_value('QM_DBH', dg)  # update plot quadratic mean diameter after the cut
            new_plot.add_value('BASAL_AREA', G)  # update plot basal area after the cut
            new_plot.add_value('VOL', V)  # update plot volume over bark after the cut

            new_plot.add_value('DENSITY_CUT_VOLUME', old_plot.density - new_plot.density)  # stand density harvested (trees/ha)
            new_plot.add_value('BA_CUT_VOLUME', old_plot.basal_area - new_plot.basal_area)  # stand basal area harvested (m2/ha)
            new_plot.add_value('VOL_CUT_VOLUME', old_plot.vol - new_plot.vol)  # stand volume harvested (m3/ha)
            #new_plot.add_value('WT_CUT_VOLUME', old_plot.wt - new_plot.wt)  # stand biomass harvested (t/ha)

            new_plot.add_value('DEAD_DENSITY', 0)  # Nº of dead trees after an cut (nº trees/ha)
            new_plot.add_value('DEAD_BA', 0)  # Dead basal area
            new_plot.add_value('DEAD_VOL', 0)
            #new_plot.add_value('DEAD_WT', 0)  # Dead biomass

            # Mean Height, Mean Diameter, Minimum Diameter and Slenderness
            parA0 = 0.1456
            parA1 = 0.9626
            parC1 = 0.0021
            parC2 = 0.00168
            parC3 = 0.0595
            parD1 = -0.0288
            parD2 = 0.0334
            if new_plot.qm_dbh != 0:
                mean_h = parA0 + parA1*new_plot.dominant_h
                mean_dbh = new_plot.qm_dbh*(1 - 1/(1 + math.exp(parC1*old_plot.si + parC2*new_plot.density + parC3*new_plot.qm_dbh)))
                min_dbh = mean_dbh*(1 - 1/(1 + math.exp(parD1*new_plot.qm_dbh + parD2*old_plot.si)))
            else:
                mean_h = mean_dbh = min_dbh = 0
            new_plot.add_value('DBH_MIN', min_dbh)
            new_plot.add_value('MEAN_DBH', mean_dbh)
            new_plot.add_value('MEAN_H', mean_h) 

            if new_plot.qm_dbh != 0:
                slenderness_mean = new_plot.mean_h*100/new_plot.mean_dbh 
            else:
                slenderness_mean = 0
            new_plot.add_value('SLENDERNESS_MEAN', slenderness_mean)             
            
            # Reineke Index
            if new_plot.qm_dbh != 0:
                SDI = new_plot.density*pow(25/new_plot.qm_dbh, old_plot.reineke_value)  # Reineke density index
            else:
                SDI = 0
            new_plot.add_value('REINEKE', SDI)  # store Reineke index in database

            # Hart Index
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

        ###############################################################################################################
        ######################################## PLOT variables #######################################################
        ###############################################################################################################


        # list of plot variables on the simulator that can be deleted without make errors
        # to delete them, just leave it on the list; to NOT delete them, comment it at the list or remove it from them

        delete_from_plot = [  

            'ID_SP1',  # IFN (Spanish National Forestal Inventory) ID specie 1 - mixed models
            'ID_SP2',  # IFN (Spanish National Forestal Inventory) ID specie 2 - mixed models

            # Basic plot variables measured
            "EXPAN",  # plot expansion factor
            #'YEAR',  # year of the inventory
            #"AGE",  # plot age (years)
            "SP1_PROPORTION",  # proportion of specie 1 on a mix plot - mixed models
            "SP2_PROPORTION",  # proportion of specie 2 on a mix plot - mixed models
            #"DENSITY",  # plot density (nº trees/ha)
            "DENSITY_SP1",  # density of specie 1 on a mix plot - mixed models
            "DENSITY_SP2",  # density of specie 2 on a mix plot - mixed models
            #"DENSITY_CUT_VOLUME",  # stand density harvested volume (%)
            #"DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            "ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

            # Basic plot variables calculated - basal area
            #"BASAL_AREA",  # Basal area (m2/ha)
            "BASAL_AREA_SP1",  # basal area of specie 1 on a mix plot - mixed models
            "BASAL_AREA_SP2",  # basal area of specie 2 on a mix plot - mixed models
            "BA_MAX",  # Maximal Basal Area (cm2)
            "BA_MAX_SP1",  # Maximal Basal Area (cm2) of specie 1 on a mix plot - mixed models
            "BA_MAX_SP2",  # Maximal Basal Area (cm2) of specie 2 on a mix plot - mixed models        
            "BA_MIN",  # Minimal Basal Area (cm2) 
            "BA_MIN_SP1",  # Minimal Basal Area (cm2) of specie 1 on a mix plot - mixed models
            "BA_MIN_SP2",  # Minimal Basal Area (cm2) of specie 2 on a mix plot - mixed models
            "MEAN_BA",  # Mean Basal Area (cm2)
            "MEAN_BA_SP1",  # Mean Basal Area (cm2) of specie 1 on a mix plot - mixed models
            "MEAN_BA_SP2",  # Mean Basal Area (cm2) of specie 2 on a mix plot - mixed models
            #"BA_CUT_VOLUME",  # Basal area harvested volume (%)
            #"DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            "ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

            # Basic plot variables calculated - diameter
            "DBH_MAX",  # Maximal Diameter (cm)
            "DBH_MAX_SP1",  # Maximal Diameter (cm) of specie 1 on a mix plot - mixed models
            "DBH_MAX_SP2",  # Maximal Diameter (cm) of specie 2 on a mix plot - mixed models
            #"DBH_MIN",  # Minimal Diameter (cm)
            "DBH_MIN_SP1",  # Minimal Diameter (cm) of specie 1 on a mix plot - mixed models
            "DBH_MIN_SP2",  # Minimal Diameter (cm) of specie 2 on a mix plot - mixed models
            #"MEAN_DBH",  # Mean Diameter (cm)
            "MEAN_DBH_SP1",  # Mean Diameter (cm) of specie 1 on a mix plot - mixed models
            "MEAN_DBH_SP2",  # Mean Diameter (cm) of specie 2 on a mix plot - mixed models
            #"QM_DBH",  # Quadratic mean dbh (cm)
            "QM_DBH_SP1",  # quadratic mean dbh of specie 1 - mixed models
            "QM_DBH_SP2",  # quadratic mean dbh of specie 2 - mixed models
            #"DOMINANT_DBH",  # Dominant Diameter (cm)
            "DOMINANT_DBH_SP1",  # dominant diameter os specie 1 (cm) on mixed models
            "DOMINANT_DBH_SP2",  # dominant diameter os specie 2 (cm) on mixed models     
            "DOMINANT_SECTION",  # Dominant section (cm)
            "DOMINANT_SECTION_SP1",  # Dominant section (cm) of specie 1 on a mix plot - mixed models
            "DOMINANT_SECTION_SP2",  # Dominant section (cm) of specie 2 on a mix plot - mixed models

            # Basic plot variables calculated - height
            "H_MAX",  # Maximal Height (m)
            "H_MAX_SP1",  # Maximal Height (m) of specie 1 on a mix plot - mixed models
            "H_MAX_SP2",  # Maximal Height (m) of specie 2 on a mix plot - mixed models
            "H_MIN",  # Minimal Height (m)    
            "H_MIN_SP1",  # Minimal Height (m) of specie 1 on a mix plot - mixed models
            "H_MIN_SP2",  # Minimal Height (m) of specie 2 on a mix plot - mixed models
            #"MEAN_H",  # Mean height (m)
            "MEAN_H_SP1",  # Mean height (m) of specie 1 on a mix plot - mixed models
            "MEAN_H_SP2",  # Mean height (m) of specie 2 on a mix plot - mixed models
            #"DOMINANT_H",  # Dominant height (m)
            "DOMINANT_H_SP1",  # dominant height of specie 1 - mixed models
            "DOMINANT_H_SP2",  # dominant height of specie 2 - mixed models

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
            "SLENDERNESS_DOM",  # slenderness calculated by using top height and dbh values (cm/cm)  
            #"REINEKE",  # Reineke Index or Stand Density Index - SDI
            "REINEKE_SP1",  # reineke index for specie 1 on mixed models
            "REINEKE_SP2",  # reineke index for specie 2 on mixed models
            "REINEKE_MAX",  # maximal reineke index
            "REINEKE_MAX_SP1",  # maximal reineke index for specie 1 on mixed models
            "REINEKE_MAX_SP2",  # maximal reineke index for specie 2 on mixed models
            #"HART",  # Hart-Becking Index (S) calculated to simple rows 
            #"HART_STAGGERED",  # Hart-Becking Index (S) calculated to staggered rows 
            #"SI",  # Site index (m)
            #"REF_SI_AGE",  # SI reference age (years)
            #"REINEKE_VALUE"  # r contstant value of SDI  to the specie of the model (-1.605 as default)
            "HEGYI_RADIUS",  # radius value to calculate the Hegyi competition index (m)

             # Plot variables calculated - volume and biomass
            #"VOL",  # Volume Over Bark (m3/ha)
            "BOLE_VOL",  # Volume Over Bark under bark (m3/ha)
            "BARK_VOL",  # Bark Volume (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume Over Bark harvested percentage (%)
            #"DEAD_VOL",  # Volume Over Bark of dead trees after an execution (m3/ha)
            "ING_VOL",  # Volume Over Bark of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - volume for mixed models
            "VOL_SP1",  # Volume Over Bark (m3/ha)
            "BOLE_VOL_SP1",  # Volume Over Bark under bark (m3/ha)
            "BARK_VOL_SP1",  # Bark Volume (m3/ha) 
            "VOL_SP2",  # Volume Over Bark (m3/ha)
            "BOLE_VOL_SP2",  # Volume Over Bark under bark (m3/ha)
            "BARK_VOL_SP2",  # Bark Volume (m3/ha)     

            # Plot variables calculated - wood uses
            "UNWINDING",  # Unwinding = the useful wood volume unwinding destiny (m3/ha)
            "VENEER",  # Veneer = the useful wood volume veneer destiny (m3/ha)
            "SAW_BIG",  # Saw big =) the useful wood volume big saw destiny (m3/ha)
            "SAW_SMALL",  # Saw small = the useful wood volume small saw destiny (m3/ha)
            "SAW_CANTER",  # Saw canter = the useful wood volume canter saw destiny (m3/ha)
            "POST",  # Post = the useful wood volume post destiny (m3/ha)
            "STAKE",  # Stake = the useful wood volume stake destiny (m3/ha)
            "CHIPS",  # Chips = the useful wood volume chips destiny (m3/ha)

            'UNWINDING_SP1',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
            'VENEER_SP1',  # veneer = the useful wood volume veneer destiny (m3/ha)
            'SAW_BIG_SP1',  # saw_big = the useful wood volume big saw destiny (m3/ha)
            'SAW_SMALL_SP1',  # saw_small = the useful wood volume small saw destiny (m3/ha)
            'SAW_CANTER_SP1',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
            'POST_SP1',  # post = the useful wood volume post destiny (m3/ha)
            'STAKE_SP1',  # stake = the useful wood volume stake destiny (m3/ha)
            'CHIPS_SP1',  # chips = the useful wood volume chips destiny (m3/ha)
            
            'UNWINDING_SP2',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
            'VENEER_SP2',  # veneer = the useful wood volume veneer destiny (m3/ha)
            'SAW_BIG_SP2',  # saw_big = the useful wood volume big saw destiny (m3/ha)
            'SAW_SMALL_SP2',  # saw_small = the useful wood volume small saw destiny (m3/ha)
            'SAW_CANTER_SP2',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
            'POST_SP2',  # post = the useful wood volume post destiny (m3/ha)
            'STAKE_SP2',  # stake = the useful wood volume stake destiny (m3/ha)
            'CHIPS_SP2',  # chips = the useful wood volume chips destiny (m3/ha)

            # Plot variables calculated - biomass
            "WSW",  # wsw = stem wood (Tn/ha)
            "WSB",  # wsb = stem bark (Tn/ha)
            "WSWB",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            "WB2_7",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05",  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            "WB05_7",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB",  # wdb = dead branches biomass (Tn/ha)
            "WL",  # wl = leaves (Tn/ha)
            "WTBL",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            "WR",  # wr = roots (Tn/ha)
            "WT",  # wt = total biomass (Tn/ha)
            "WT_CUT_VOLUME",  # WT of the cut trees after a cut process (%)
            "DEAD_WT",  # WT of the dead trees after an execution (Tn/ha)
            "ING_WT",  # WT of the ingrowth trees after an execution (Tn/ha)

            # Plot variables calculated - biomass for mixed models
            "WSW_SP1",  # wsw = stem wood (Tn/ha)
            "WSB_SP1",  # wsb = stem bark (Tn/ha)
            "WSWB_SP1",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP1",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP1",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            "WB2_7_SP1",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP1",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB_SP1",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP1",  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            "WB05_7_SP1",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP1",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP1",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP1",  # wl = leaves (Tn/ha)
            "WTBL_SP1",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7_SP1",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            "WR_SP1",  # wr = roots (Tn/ha)
            "WT_SP1",  # wt = total biomass (Tn/ha)

            "WSW_SP2",  # wsw = stem wood (Tn/ha)
            "WSB_SP2",  # wsb = stem bark (Tn/ha)
            "WSWB_SP2",  # wswb = stem wood and stem bark (Tn/ha)
            "WTHICKB_SP2",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB_SP2",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            "WB2_7_SP2",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T_SP2",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB_SP2",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05_SP2",  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
            "WB05_7_SP2",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2_SP2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB_SP2",  # wdb = dead branches biomass (Tn/ha)
            "WL_SP2",  # wl = leaves (Tn/ha)
            "WTBL_SP2",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7_SP2",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            "WR_SP2",  # wr = roots (Tn/ha)
            "WT_SP2",  # wt = total biomass (Tn/ha)

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
            'UNWINDING_SP3',
            'VENEER_SP3',
            'SAW_BIG_SP3',
            'SAW_SMALL_SP3',
            'SAW_CANTER_SP3',
            'POST_SP3',
            'STAKE_SP3',
            'CHIPS_SP3',
            'VOL_SP3',
            'BOLE_VOL_SP3',
            'BARK_VOL_SP3',
            'CARBON_STEM_SP1',
            'CARBON_BRANCHES_SP1',
            'CARBON_ROOTS_SP1',
            'CARBON_SP1',
            'CARBON_STEM_SP2',
            'CARBON_BRANCHES_SP2',
            'CARBON_ROOTS_SP2',
            'CARBON_SP2',
            'CARBON_STEM_SP3',
            'CARBON_BRANCHES_SP3',
            'CARBON_ROOTS_SP3',
            'CARBON_SP3',
            'WS_SP3',
            'WB_SP3',
            'WR_SP3',
            'WT_SP3',
            'WS_SP2',
            'WB_SP2',
            'WS_SP1',
            'WB_SP1',
            'CARBON_STEM',
            'CARBON_BRANCHES',
            'CARBON_ROOTS',
            'WB',
            'WS',
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
            'SP3_N_PROPORTION',
            'SP2_N_PROPORTION',
            'SP1_N_PROPORTION',
            'BASAL_AREA_SP3',
            'QM_DBH_SP3',
            'DENSITY_SP3',
            'MEAN_H_SP3',
            'H_MIN_SP3',
            'H_MAX_SP3',
            'MEAN_DBH_SP3',
            'DBH_MIN_SP3',
            'DBH_MAX_SP3',
            'MEAN_BA_SP3',
            'BA_MIN_SP3',
            'BA_MAX_SP3',
            'DOMINANT_SECTION_SP3',
            'DOMINANT_DBH_SP3',
            'DOMINANT_H_SP3',
            'CARBON_HEARTWOOD',
            'CARBON_SAPWOOD',
            'CARBON_BARK',
            'DEADWOOD_INDEX_CESEFOR_G',
            'DEADWOOD_INDEX_CESEFOR_V',
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
            "bearing",  # bearing from the tree to the central point of the plot ('rumbo')
            "distance",  # distance from the tree to the central point of the plot    
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
            "basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
            "basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
            "bal",  # cumulative basal area (m2/ha)
            "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
            "ba_ha",  # basal area per ha (m2/ha) 
            "normal_circumference",  # circumference at breast height (cm)
            "slenderness",  # slenderness (cm/cm)
            
            # Crown variables
            "cr",  # crown ratio (%)
            "lcw",  #  largest crown width (m)
            "hcb",  # height of the crown base (m)
            "hlcw",  # height of the largest crown width (m)
            "cpa",  # crown projection area (m2)
            "crown_vol",  # crown volume (m3)

            # Volume Over Bark variables
            "vol",  # volume over bark (dm3)
            "bole_vol",  # volume under bark (dm3)
            "bark_vol",  # bark volume (dm3)
            "firewood_vol",  # firewood volume (dm3)
            "vol_ha",  # volume over bark per hectare (m3/ha)

            # Wood uses variables
            "unwinding",  # unwinding = the useful wood volume unwinding destiny (dm3)
            "veneer",  # veneer = the useful wood volume veneer destiny (dm3)
            "saw_big",  # saw_big = the useful wood volume big saw destiny (dm3)
            "saw_small",  # saw_small = the useful wood volume small saw destiny (dm3)
            "saw_canter",  # saw_canter = the useful wood volume canter saw destiny (dm3)
            "post",  # post = the useful wood volume post destiny (dm3)
            "stake",  # stake = the useful wood volume stake destiny (dm3)
            "chips",  # chips = the useful wood volume chips destiny (dm3)

            # Biomass variables
            "wsw",  # wsw = stem wood (kg)
            "wsb",  # wsb = stem bark (kg)
            "wswb",  # wswb = stem wood and stem bark (kg)
            "w_cork",  # fresh cork biomass (kg)
            "wthickb",  # wthickb = Thick branches > 7 cm (kg)
            "wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            "wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
            "wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            "wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
            "wb05",  # wb05 = thinniest branches (<0.5 cm) (kg)
            "wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
            "wb0_2",  # wb0_2 = branches < 2 cm (kg)
            "wdb",  # wdb = dead branches biomass (kg)
            "wl",  # wl = leaves (kg)
            "wtbl",  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            "wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
            "wr",  # wr = roots (kg)
            "wt",  # wt = total biomass (kg)
            
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
            'carbon_stem',
            'carbon_branches',
            'carbon_roots',
            'wb',
            'ws',
            'carbon_heartwood',
            'carbon_sapwood',
            'carbon_bark',
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
        
PinusNigraCyL.vars()