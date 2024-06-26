# /usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
#
# Single tree growing model independent from distance, developed to
# Pure stands of Pinus pinea located on Cataluña (Spain)
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


class PinusPineaCataluña(TreeModel):


    global dbh_list  # that variable is needed to catch the data of old and new dbh on grow function, to be used on update_model
    dbh_list = []


    def __init__(self, configuration=None):
        super().__init__(name="Pinus pinea - Cataluña", version=1)


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
        
            Model.model_name = 'Ppinea__cat_v01'  # set the model name to show it at the output
            Model.specie_ifn_id = 23  # Set the model specie ID to mark the trees of different species        
            Model.exec_time = 5  # recommended executions time to use that model
            Model.aplication_area = 'Cataluña (Spain)'  # area recommended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = '6, 7'  # provenance regions recommended to use the model
            Model.model_type = 'tree_independent'  # SIMANFOR model type. It can be: ('' is neccesary)
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'https://github.com/simanfor/modelos/blob/main/arbol/Ppinea_cat_EN.pdf'  # link to model card in english
            Model.model_card_es = 'https://github.com/simanfor/modelos/blob/main/arbol/Ppinea_cat_ES.pdf'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def P9010_distribution(self, plot: Plot, tree: Tree):
        """
        That function is only needed on Pinus pinea model.
        It is needed to calculate the difference between the 90th and 10th percentiles from the diametric distribution (cm),
        which is a parameter useful on the h/d equation of Calama and Montero (2004).
        """

        try:  # errors inside that construction will be announced

            # That model includes this function because it is needed in orden to calculate the difference between 10 and 90 diametric distribution percentiles (cm)

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            P9010_list = []
            for tree in plot_trees:  # add all the trees dbh to a list
                P9010_list.append(tree.dbh)

            x = len(P9010_list)
            x_up = int(0.9*x)
            x_down = int(0.1*x)
            P9010_clean = P9010_list[x_down:x_up]  # reduce the list leaving the trees between 10% an 90% of diametric distribution
            P9010 = max(P9010_list) - min(P9010_list)  # obtain the difference between them, which is the value of P9010

        except Exception:
            self.catch_model_exception()

        return P9010  # that variable will return the difference between the 90th and 10th percentiles from the diametric distribution (cm)


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps of information at the initial inventory
        Height/Diameter equation:
            Doc.: Calama R, Montero G (2004). Interregional nonlinear height diameter model with random coefficients for stone pine in Spain. Canadian Journal of Forest Research, 34(1), 150-163
            Ref.: Calama and Montero, 2004
        Reineke Index value:
            Doc.: Aguirre A, Condés S, del Río M (2017) Variación de las líneas de máxima densidad de las principales especies de pino a lo largo del gradiente estacional de la Península Ibérica. 7 Congreso Forestal Español
            Ref.: Aguirre et al, 2017              
        SI equation:
            a)
            Doc.: Calama R, Cañadas N, Montero G (2003). Inter-regional variability in site index models for even-aged stands of stone pine (Pinus pinea L.) in Spain. Annals of Forest Science, 60(3), 259-269
            Ref.: Calama et al, 2003
            b)
            Doc.: Casanueva GM, Ponce RA (2007). Patrón de crecimiento en altura dominante en masas naturales y artificiales de Pinus pinea L.: comparación a través de modelos dinámicos. Cuadernos de la SECF, (23)
            Ref.: Casanueva and Ponce, 2007
            c)
            Doc.: Cañadas MN, Calama R, Güemes GCG (2005). Modelo de calidad de estación para Pinus pinea L. en las masas del sistema central (Valles del Tiétar y Alberche), mediante aplicación de la metodología propuesta por Goelz & Burk (1992). In Congresos Forestales
            Ref.: Cañadas et al, 2005
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                     Running: Pinus pinea model (Cataluña). Plot:', plot.plot_id                     )
        print('#--------------------------------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced
            
            self.model_info()            
            plot.add_value('REINEKE_VALUE', -2.1518)  # r constant value of SDI to the species of the model (-1.605 as default) 
            other_trees = total_trees = 0  # variables to count the number of trees from a different species that the principal one and the total of trees

            global P9010  # the explanation of that variable is on P9010_distribution function
            P9010 = 0  # define the variable that later we will use

            #-----------------------------------SI -----------------------------------------#
          
            # a)
            if plot.si == 0 or plot.si == '':            
                T2 = 100  # SI reference age (years)
                plot.add_value('REF_SI_AGE', T2)  
                if plot.dominant_h != 0 and plot.dominant_h != '':  # to not obtain an error because of math.log(0)                 
                    SI = math.exp(4.1437 + (math.log(plot.dominant_h) - 4.1437) * ((T2 / plot.age) ** (- 0.3935)))
                else:
                    SI = 0
                    
            # b)
            #a = 0.005994
            #m1 = 14.08433
            #m2 = -12.0075
            #Xo = (math.log(plot.dominant_h) - m1) / (m2 + math.log(1 - math.exp(-a * plot.age)))
            #t = 80  # Age when we want to obtain the Site Index (years)
            #SI = math.exp(m1 + m2 * Xo) * ((1 - math.exp(-a * t)) ** Xo)

            # c)
            #Hj = plot.dominant_h
            #tj = plot.age
            #ti = 80  # Age when we want to obtain the Site Index (years)
            #b1 = 0.252147664
            #b2 = 1.225418697
            #b3 = 0.498226472
            #b4 = 0.785418166
            #SI = 1.3 + (Hj - 1.3) * ((1 - math.exp(- b1 * ((Hj / tj) ** b2) * (tj ** b3) * ti)) / (
            #            1 - math.exp(- b1 * ((Hj / tj) ** b2) * (tj ** b3) * tj)))**b4

                plot.add_value('SI', SI)  # Site Index (m) calculation 

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            bal: float = 0
            
            for tree in plot_trees:  # for each tree...

                total_trees += 1

                if tree.specie == Model.specie_ifn_id:  # specie condition
                    
                    #-----------------------------------BASAL_AREA-----------------------------------------#

                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                    tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal section (cm2)
                    tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basal area per ha (m2/ha)
                    bal += tree.basal_area * tree.expan / 10000  # then, that value is accumulated

                    if P9010 == 0:  # condition needed to only calculate that variable once
                        P9010 = self.P9010_distribution(plot, tree)  # that line is needed to activate the calculation of P9010, needed later

                    #-------------------------------- HEIGHT ------------------------------------#

                    if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                        K = 1  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia
                        tree.add_value('height', 1.3 + math.exp((1.7306 + 0.0882 * plot.dominant_h - 0.0062 * P9010 - 0.0936*K) + (
                                        - 25.2776 + 1.6999 * math.log(plot.density) + 4.743*K) / (tree.dbh + 1)))

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height * 100 / tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal circumference (cm)

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    #elf.crown(tree, plot, 'initialize')  # activate crown variables

                    self.vol(tree, plot)  # activate volume variables

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    self.merchantable(tree)  # activate wood uses variables

                    self.biomass(tree)  # activate biomass variables
                
                else:
                    other_trees += 1
    
            if other_trees != 0:
                print(' ')
                print(other_trees, 'of the total', total_trees, 'trees are from a different species than the principal')
                print('That trees will be shown underlined at the output, and they will be maintained at simulations, not applying model equations over them.')
                print(' ')
                if other_trees == total_trees:
                    Warnings.specie_error_trees = 1


            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables  

            #-----------------------------------Update QM_DBH and calculate cones production-----------------------------------------#     

            plot_expan = plot_dbh2 = 0
            for tree in plot_trees:
                plot_expan += tree.expan
                plot_dbh2 += math.pow(tree.dbh, 2)*tree.expan

            plot.add_value('QM_DBH', math.sqrt(plot_dbh2/plot_expan))  # upload qmd value before cones calculation

            for tree in plot_trees:
                    self.cones(tree, plot)  # activate cones variables calculation
            self.cones_plot(plot, plot_trees)  # activate cones (plot) variables calculation  

            
            #plot.add_value('DEAD_DENSITY', 0)  # change the value from '' to 0 in orde to print that information at the summary sheet
            #plot.add_value('ING_DENSITY', 0)  # change the value from '' to 0 in orde to print that information at the summary sheet

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
        A function that updates dbh and h by using growth equations, and also update age, g, and v to the new situation.
        Source of diameter growing equation:
            Doc.: Calama R, Montero G (2005). Multilevel linear mixed model for tree diameter increment in stone pine (Pinus pinea): a calibrating approach. Silva Fenn, 39(1), 37-54
            Ref.: Calama and Montero, 2005
        Source for height/diameter equation: (update_model)
            Doc.: Calama R, Montero G (2004). Interregional nonlinear height diameter model with random coefficients for stone pine in Spain. Canadian Journal of Forest Research, 34(1), 150-163
            Ref.: Calama and Montero, 2004
        SI equation (Hdom_new): (update_model)
            Doc.: Calama R, Cañadas N, Montero G (2003). Inter-regional variability in site index models for even-aged stands of stone pine (Pinus pinea L.) in Spain. Annals of Forest Science, 60(3), 259-269
            Ref.: Calama et al, 2003
        """

        try:  # errors inside that construction will be announced

            if old_tree.specie == Model.specie_ifn_id:  # specie condition

                new_tree.sum_value('tree_age', time)

                cat = 1  # cat = 1 if the analysis is for Catalonia; 0 for Spain in general
                if plot.si == 0:
                    dbhg5 = 0
                else:
                    dbhg5 = math.exp(2.2451 - 0.2615 * math.log(old_tree.dbh) - 0.0369 * plot.dominant_h - 0.1368 * math.log(
                        plot.density) + 0.0448 * plot.si + 0.1984 * (
                                             old_tree.dbh / plot.qm_dbh) - 0.5542 * cat + 0.0277 * cat * plot.si) - 1
                new_tree.sum_value("dbh", dbhg5)

                dbh_list.append([old_tree.dbh, new_tree.dbh])  # that variable is needed to used dbh values on update_model

                # The h/d calculations are written on update_model

                new_tree.add_value('basal_area', math.pi*(new_tree.dbh/2)**2)  # update basal area (cm2) 

                self.vol(new_tree, plot)  # update volume variables (dm3)

        except Exception:
            self.catch_model_exception()


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
        print('                     Running: Pinus pinea model (Cataluña). Plot:', plot.plot_id                     )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same as the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:  # errors inside that construction will be announced

            dbh_list.sort(reverse = True)  # we need to sort the list from higher to lower dbh, as plot_trees does it
            global P9010  # the explanation of that variable is on P9010_distribution function
            P9010 = 0  # leave the variable value as 0 to calculate it again on that execution
            count = 0  # counter needed to dbh_list

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            bal: float = 0.0

            if 'YEAR' in PLOT_VARS:
                new_year = plot.year + time  # YEAR is automatically updated after the execution process
            if 'AGE' in PLOT_VARS:
                new_age = plot.age + time  # AGE is automatically updated after the execution process

            for tree in plot_trees:  # for each tree...

                if tree.specie == Model.specie_ifn_id:  # specie condition

                     #-----------------------------------BASAL_AREA-----------------------------------------#

                    tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal section (cm2)
                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                    tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basal area per ha (m2/ha)
                    bal += tree.basal_area * tree.expan / 10000  # then, that value is accumulated 

                    if P9010 == 0:  # condition needed to only calculate that variable once
                        P9010 = self.P9010_distribution(plot, tree)  # that line is neede to activate the calculation of P9010, needed later
                        # Hdom_new is a SI equation used to predict the Dominant Height 5 years later (execution)
                        Hdom_new = math.exp(4.1437 + (math.log(plot.dominant_h) - 4.1437) * pow(((new_age + 5)/new_age), - 0.3935))  # that variable need to be calculated again only once
                   
                    K = 1  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia
                    
                    old_height = 1.3 + math.exp((1.7306 + 0.0882 * plot.dominant_h - 0.0062 * P9010 - 0.0936*K) + (
                                - 25.2776 + 1.6999 * math.log(plot.density) + 4.743*K) / (dbh_list[count][0] + 1))  # height calculation before execution (m)
                    new_height = 1.3 + math.exp((1.7306 + 0.0882 * (Hdom_new) - 0.0062 * P9010 - 0.0936*K) + (
                                - 25.2776 + 1.6999 * math.log(plot.density) + 4.743*K) / (dbh_list[count][1] + 1))  # height calculation after execution (m)
                    ht = tree.height * new_height / old_height  # obtaining the new height of the tree by comparing values
                    tree.add_value('height', ht)  # adding new tree height value (m)
                    count += 1  # add 1 value to move the variable to the next tree position

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height * 100 / tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal circumference (cm)

                    #-------------------------------------VOL_HA-------------------------------------------#

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    self.cones(tree, plot)  # activate cones variables calculation

                    #self.crown(tree, plot, 'update_model')  # activate crown variables
                    
                    self.merchantable(tree)  # activate wood uses variables

                    self.biomass(tree)  # activate biomass variables

            #---------------------------------PLOT_FUNCTIONS---------------------------------------#

            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables 

            self.cones_plot(plot, plot_trees)  # activate cones (plot) variables calculation  

            #-----------------------------------Dominant Height-----------------------------------------#

            # On this model, we didn't update height values on grow function, so Dominant Height was calculates by using the height values before the execution
            # In order to correct that value, we add the calculation methodology used on SIMANFOR project to update that value after the height values update

            plot.add_value('DOMINANT_H', -plot.dominant_h)  # Dominant Height is calculated befores update_model, so we eliminate this value to recalculate it with
            tree_expansion: float = 0.0  # the new tree.height values
            selection_trees = list()

            for tree in plot_trees:  # for each tree on the list (ordered by dbh), we calculate how many trees are needed to Dominant Height calculation
                if tree_expansion < 100:
                    tree_expansion += tree.expan
                    selection_trees.append(tree)
                else:
                    break

            acumulate: float = 0
            result: float = 0

            for tree in selection_trees:  # for each selected tree, we calculate the relative weight for each of them on the Dominant Height value
                if acumulate + tree.expan < 100:
                    result += tree.height * tree.expan
                    acumulate += tree.expan
                else:
                    result += (100 - acumulate) * tree.height
            dom_h = result / 100

            plot.add_value('DOMINANT_H', dom_h)  # adding new Dominant Height value to the plot


            plot_expan = plot_h = max_h = min_h = 0
            for tree in plot_trees:  # recalculate plot height variables is needed, because h after growth is calculated on update_model instead of growth function

                plot_expan += tree.expan
                plot_h += tree.height*tree.expan
                max_h = tree.height if tree.height > max_h else max_h
                min_h = tree.height if tree.height < min_h else min_h
                
            if plot_expan != 0:
                plot.add_value('MEAN_H', plot_h/plot_expan)        
            plot.add_value('H_MAX', max_h)
            plot.add_value('H_MIN', min_h)


            number = len(dbh_list)
            while number > 0:  # that loop leaves the dbh_list empty to the next execution 
                dbh_list.pop(0)
                number -= 1

        except Exception:
            self.catch_model_exception()


    def taper_over_bark(self, tree: Tree, hr: float):
        """
        Taper equation over bark function.
        A function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source:
            Doc.: Rodríguez F, Lizarralde I (2015). Comparison of stem taper equations for eight major tree species in the Spanish Plateau. Forest systems, 24(3), 2
            Ref.: Rodriguez and Lizarralde, 2015
        """

        try:  # errors inside that construction will be announced

            # a) Stud model

            # alpha10 = 1.176657
            # alpha11 = 0.006518
            # alpha2 = 0.886843
            # alpha3 = 0.214083
            # alpha4 = 14.671320
            # alpha50 = 0
            # alpha51 = 0.979925
            # dob = (1 + alpha3*2.7182818284 ** (- alpha4*hr))*alpha50 + alpha51*tree.dbh*((1 - hr)**(alpha10 + alpha11*((100*tree.height)/tree.dbh) + alpha2*(1 - hr)))
            
            # b) Fang model

            ao = 0.000067
            a1 = 1.698754
            a2 = 1.210604
            b1 = 0.000006
            b2 = 0.000033
            b3 = 0.000026
            p1 = 0.021072
            p2 = 0.475953

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

        except Exception:
            self.catch_model_exception()

        return dob  # diameter over bark (cm)


    def taper_under_bark(self, tree: Tree, hr: float):
        """
        Taper equation under bark function.
        A function that returns the taper equation to calculate the diameter (cm, under bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source:
            Doc.: Calama R, Montero G (2006). Stand and tree-level variability on stem form and tree volume in Pinus pinea L.: a multilevel random components approach. Forest Systems, 15(1), 24-41
            Ref.: Calama and Montero, 2006
        """

        try:  # errors inside that construction will be announced

            beta1 = 1.0972
            beta2 = -2.8505
            H = tree.height*10  # dm
            dubmm = tree.dbh * 10 * ((H - hr*H) / (H - 13)) + beta1 * (
                        ((H ** 1.5 - (hr*H) ** 1.5) * (hr*H - 13)) / H ** 1.5) + beta2 * (
                               ((H - (hr*H)) ** 4) * (hr*H - 13) / (H ** 4))
            dub = dubmm*0.1  # mm to cm

        except Exception:
            self.catch_model_exception()

        return dub  # diameter under bark (cm)


    def merchantable(self, tree: Tree):
        """
        Merchantable wood calculation (tree).
        A function needed to calculate the different commercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions and is linked to taper_over_bark, an indispensable function.
        That function is run by initialize and update_model functions.
        Data criteria to classify the wood by different uses were obtained from:
            Doc.: Rodríguez F (2009). Cuantificación de productos forestales en la planificación forestal: Análisis de casos con cubiFOR. In Congresos Forestales
            Ref.: Rodríguez, 2009
        """
 
        try:  # errors inside that construction will be announced

            ht = tree.height  # the total height as ht to simplify
            # class_conditions have different lists for each usage, following that structure: [wood_usage, hmin/ht, dmin, dmax]
            # [WOOD USE NAME, LOG RELATIVE LENGTH RESPECT TOTAL TREE HEIGHT, MINIMUM DIAMETER, MAXIMUM DIAMETER]
            class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            # usage and merch_list are a dictionary and a list returned from merch_calculation function
            # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
            usage, merch_list = TreeModel.merch_calculation(tree, class_conditions, PinusPineaCataluña)

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

            plot_unwinding = plot_veneer = plot_saw_big = plot_saw_small = plot_saw_canter = plot_post = plot_stake = plot_chips =  0

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    # plot_unwinding += tree.unwinding*tree.expan
                    # plot_veneer += tree.veneer*tree.expan
                    plot_saw_big += tree.saw_big*tree.expan
                    plot_saw_small += tree.saw_small*tree.expan
                    plot_saw_canter += tree.saw_canter*tree.expan
                    # plot_post += tree.post*tree.expan
                    # plot_stake += tree.stake*tree.expan
                    plot_chips += tree.chips*tree.expan

            # plot.add_value('UNWINDING', plot_unwinding/1000)  # now, we add the plot value to each variable, changing the units to m3/ha
            # plot.add_value('VENEER', plot_veneer/1000)
            plot.add_value('SAW_BIG', plot_saw_big/1000)
            plot.add_value('SAW_SMALL', plot_saw_small/1000)
            plot.add_value('SAW_CANTER', plot_saw_canter/1000)
            # plot.add_value('POST', plot_post/1000)
            # plot.add_value('STAKE', plot_stake/1000)
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

            plot_expan = plot_lcw = plot_lcw2 = plot_fcc = 0

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
            dob = self.taper_over_bark(tree, hr)  # diameter over bark using taper equation (cm)
            dub = self.taper_under_bark(tree, hr)  # diameter under/without bark using taper equation (cm)
            fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
            fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
            tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
            tree.add_value('bole_vol', math.pi * tree.height * 10 * integrate.simps(fub, hr))  # volume under bark using simpson integration (dm3)
            tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)

        except Exception:
            self.catch_model_exception()


    def vol_plot(self, plot: Plot, plot_trees):
        """
        Volume variables (plot).
        Function to calculate plot volume variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            plot_vol = plot_bole_vol = plot_bark = 0

            for tree in plot_trees:

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    plot_vol += tree.expan*tree.vol
                    plot_bole_vol += tree.expan*tree.bole_vol
            plot_bark = plot_vol - plot_bole_vol

            plot.add_value('VOL', plot_vol/1000)  # plot volume over bark (m3/ha)
            plot.add_value('BOLE_VOL', plot_bole_vol/1000)  # plot volume under bark (m3/ha)
            plot.add_value('BARK_VOL', plot_bark/1000)  # plot bark volume (m3/ha)

        except Exception:
            self.catch_model_exception()


    def biomass(self, tree: Tree):
        """
        Biomass variables (tree).
        Function to calculate biomass variables for each tree.
        That function is run by initialize and update_model functions.
        Biomass equations:
            Doc.: Ruiz-Peinado R, del Rio M, Montero G (2011). New models for estimating the carbon sink capacity of Spanish softwood species. Forest Systems, 20(1), 176-188
            Ref.: Ruiz-Peinado et al, 2011
        """

        try:  # errors inside that construction will be announced

            wsw = 0.0224 * (tree.dbh ** 1.923) * (tree.height ** 1.0193)
            if tree.dbh <= 22.5:
                Z = 0
            else:
                Z = 1
            wthickb = (0.247 * ((tree.dbh - 22.5) ** 2)) * Z
            wb2_7 = 0.0525 * (tree.dbh ** 2)
            wtbl = 21.927 + 0.0707 * (tree.dbh ** 2) - 2.827 * tree.height
            wr = 0.117 * (tree.dbh ** 2)
            wt = wsw + wb2_7 + wthickb + wtbl + wr

            tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
            # tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
            # tree.add_value('w_cork', w_cork)   # fresh cork biomass (kg)
            tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
            # tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
            # tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            # tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
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

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    plot_wsw += tree.wsw*tree.expan
                    # plot_wsb += tree.wsb*tree.expan
                    # plot_w_cork += tree.w_cork*tree.expan
                    plot_wthickb += tree.wthickb*tree.expan
                    # plot_wstb += tree.wstb*tree.expan
                    plot_wb2_7 += tree.wb2_7*tree.expan
                    # plot_wb2_t += tree.wb2_t*tree.expan
                    # plot_wthinb += tree.wthinb*tree.expan
                    # plot_wb05 += tree.wb05*tree.expan                    
                    # plot_wl += tree.wl*tree.expan
                    plot_wtbl += tree.wtbl*tree.expan
                    # plot_wbl0_7 += tree.wbl0_7*tree.expan
                    plot_wr += tree.wr*tree.expan
                    plot_wt += tree.wt*tree.expan

            plot.add_value('WSW', plot_wsw/1000)  # wsw = stem wood (Tn/ha)
            # plot.add_value('WSB', plot_wsb/1000)  # wsb = stem bark (Tn/ha)
            # plot.add_value('W_CORK', plot_w_cork/1000)  # fresh cork biomass (Tn/ha)
            plot.add_value('WTHICKB', plot_wthickb/1000)  # wthickb = Thick branches > 7 cm (Tn/ha)
            # plot.add_value('WSTB', plot_wstb/1000)  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            plot.add_value('WB2_7', plot_wb2_7/1000)  # wb2_7 = branches (2-7 cm) (Tn/ha)
            # plot.add_value('WB2_T', plot_wb2_t/1000)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            # plot.add_value('WTHINB', plot_wthinb/1000)  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            # plot.add_value('WB05', plot_wb05/1000)  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            # plot.add_value('WL', plot_wl/1000)  # wl = leaves (Tn/ha)
            plot.add_value('WTBL', plot_wtbl/1000)  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            # plot.add_value('WBL0_7', plot_wbl0_7/1000)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            plot.add_value('WR', plot_wr/1000)  # wr = roots (Tn/ha)
            plot.add_value('WT', plot_wt/1000)  # wt = total biomass (Tn/ha)
            
        except Exception:
            self.catch_model_exception()


    def cones(self, tree: Tree, plot: Plot):
        """
        Function to calculate cones and pinyons variables for each tree.
        That function is run by initialize and update_model functions.
        Weight of all the cones:
            Doc.: Calama R, Gordo FJ, Mutke S, Montero G (2008). An empirical ecological-type model for predicting stone pine (Pinus pinea L.) cone production in the Northern Plateau (Spain). Forest Ecology and Management, 255(3-4), 660-673
            Ref.: Calama et al, 2008
        Cones and pinyons calculations:
            Doc.: Calama R, Montero G (2007). Cone and seed production from stone pine (Pinus pinea L.) stands in Central Range (Spain). European Journal of Forest Research, 126(1), 23-35
            Ref.: Calama and Montero (2007)
        """
        
        try:  # errors inside that construction will be announced

            if plot.qm_dbh != 0:
                # Silvicultural model
                wc = math.exp(0.7408 + 4.7407*tree.basal_area/10000 + 0.5081*tree.dbh/plot.qm_dbh - 0.2611*math.log(plot.density) + 0.0350*plot.si) - 1  # weight of all (healthy and not) cones (kg) (anual mean)

                # Hybrid model
                # wr = winter rainfall wr (average value for long-term data series, in mm per year)
                # wc = math.log(1.2745 + 4.9892*tree.basal_area/10000 + 0.4821*tree.dbh/plot.qm_dbh - 0.2636*math.log(plot.density) + 0.0357*plot.si + 0.0177*wr - 0.0034*Model.altitude) - 1

                # Ecological-type model
                # UN = natural unit
                # wc = math.log(1.4796 + 4.2383*tree.basal_area/10000 + 0.5539*tree.dbh/plot.qm_dbh - 0.2320*math.log(plot.density) + UN) - 1

            Ln = 0.2641 + 0.6492*tree.basal_area/10000 - 0.0310*math.log(plot.density)  # Ln = cone production variable
            # Ln = math.log(Nh + 1)/10
            Nh = math.exp(Ln*10) - 1  # Nh is the number of healthy cones in a tree  (anual mean)
            Mw = 0.1301 + 0.01199*plot.si  # Mw = mean weight of cones for the tree in that year (kg)
            Np100 = 0.3068 + 1.3448*Mw + 0.4142*Ln  # Np100 = Number of pinyons per cone / 100
            Np = Np100*100  # Np = Number of pinyons per cone
            Em = 0.2368 - 0.4151*Mw  # Em = rate of empty cones
            Sc = 100*Np100*(1 - Em)  # Sc = expected number of sound seeds per cone (semillas sanas) viable for germination
            Sc_total = Sc*Nh  # total sound seeds of the tree (anual mean)
            wsc = Nh*Mw  # weight of sound (healthy) cones (kg) (anual mean)
            all_cones = wc/Mw  # number of all the cones of the tree (anual mean)

            tree.add_value('all_cones', all_cones)  # number of all the cones of the tree (anual mean)
            tree.add_value('sound_cones', Nh)  # number of healthy cones in a tree  (anual mean)
            tree.add_value('sound_seeds', Sc_total)  # total sound seeds of the tree (anual mean)
            tree.add_value('w_sound_cones', wsc)  # weight of sound (healthy) cones (kg) (anual mean)
            tree.add_value('w_all_cones', wc)  # weight of all (healthy and not) cones (kg) (anual mean)

        except Exception:
            self.catch_model_exception()


    def cones_plot(self, plot: Plot, plot_trees):
        """
        Function to calculate some volume variables of the plot.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            plot_all_cones = plot_sound_cones = plot_sound_seeds = plot_wsc = plot_wc = 0

            for tree in plot_trees:

                plot_all_cones += tree.all_cones*tree.expan
                plot_sound_cones += tree.sound_cones*tree.expan
                plot_sound_seeds +=  tree.sound_seeds*tree.expan
                plot_wsc += tree.w_sound_cones*tree.expan
                plot_wc += tree.w_all_cones*tree.expan

            plot.add_value('ALL_CONES', plot_all_cones)  # total of cones of the plot (anual mean)
            plot.add_value('SOUND_CONES', plot_sound_cones)  # total sound (healthy) cones of the plot (anual mean)
            plot.add_value('SOUND_SEEDS', plot_sound_seeds)  # total sound (healthy) seeds of the plot (anual mean)
            plot.add_value('W_SOUND_CONES', plot_wsc/1000)  # weight of sound (healthy) cones (Tn/ha) (anual mean)
            plot.add_value('W_ALL_CONES', plot_wc/1000)  # weight of all (healthy and not) cones (Tn/ha) (anual mean)

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
            "DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            "ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

            # Basic plot variables calculated - basal area
            #"BASAL_AREA",  # Basal area (m2/ha)
            "BASAL_AREA_SP1",  # basal area of specie 1 on a mix plot - mixed models
            "BASAL_AREA_SP2",  # basal area of specie 2 on a mix plot - mixed models
            #"BA_MAX",  # Maximal Basal Area (cm2)
            "BA_MAX_SP1",  # Maximal Basal Area (cm2) of specie 1 on a mix plot - mixed models
            "BA_MAX_SP2",  # Maximal Basal Area (cm2) of specie 2 on a mix plot - mixed models        
            #"BA_MIN",  # Minimal Basal Area (cm2) 
            "BA_MIN_SP1",  # Minimal Basal Area (cm2) of specie 1 on a mix plot - mixed models
            "BA_MIN_SP2",  # Minimal Basal Area (cm2) of specie 2 on a mix plot - mixed models
            #"MEAN_BA",  # Mean Basal Area (cm2)
            "MEAN_BA_SP1",  # Mean Basal Area (cm2) of specie 1 on a mix plot - mixed models
            "MEAN_BA_SP2",  # Mean Basal Area (cm2) of specie 2 on a mix plot - mixed models
            #"BA_CUT_VOLUME",  # Basal area harvested volume (%)
            "DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            "ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

            # Basic plot variables calculated - diameter
            #"DBH_MAX",  # Maximal Diameter (cm)
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
            #"DOMINANT_SECTION",  # Dominant section (cm)
            "DOMINANT_SECTION_SP1",  # Dominant section (cm) of specie 1 on a mix plot - mixed models
            "DOMINANT_SECTION_SP2",  # Dominant section (cm) of specie 2 on a mix plot - mixed models

            # Basic plot variables calculated - height
            #"H_MAX",  # Maximal Height (m)
            "H_MAX_SP1",  # Maximal Height (m) of specie 1 on a mix plot - mixed models
            "H_MAX_SP2",  # Maximal Height (m) of specie 2 on a mix plot - mixed models
            #"H_MIN",  # Minimal Height (m)    
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
            #"SLENDERNESS_DOM",  # slenderness calculated by using top height and dbh values (cm/cm)  
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
            #"VOL",  # Volume (m3/ha)
            #"BOLE_VOL",  # Volume under bark (m3/ha)
            #"BARK_VOL",  # Bark Volume (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume harvested percentage (%)
            "DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
            "ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - volume for mixed models
            "VOL_SP1",  # Volume (m3/ha)
            "BOLE_VOL_SP1",  # Volume under bark (m3/ha)
            "BARK_VOL_SP1",  # Bark Volume (m3/ha) 
            "VOL_SP2",  # Volume (m3/ha)
            "BOLE_VOL_SP2",  # Volume under bark (m3/ha)
            "BARK_VOL_SP2",  # Bark Volume (m3/ha)     

            # Plot variables calculated - wood uses
            "UNWINDING",  # Unwinding = the useful wood volume unwinding destiny (m3/ha)
            "VENEER",  # Veneer = the useful wood volume veneer destiny (m3/ha)
            #"SAW_BIG",  # Saw big =) the useful wood volume big saw destiny (m3/ha)
            #"SAW_SMALL",  # Saw small = the useful wood volume small saw destiny (m3/ha)
            #"SAW_CANTER",  # Saw canter = the useful wood volume canter saw destiny (m3/ha)
            "POST",  # Post = the useful wood volume post destiny (m3/ha)
            "STAKE",  # Stake = the useful wood volume stake destiny (m3/ha)
            #"CHIPS",  # Chips = the useful wood volume chips destiny (m3/ha)

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
            #"WSW",  # wsw = stem wood (Tn/ha)
            "WSB",  # wsb = stem bark (Tn/ha)
            "WSWB",  # wswb = stem wood and stem bark (Tn/ha)
            #"WTHICKB",  # wthickb = Thick branches > 7 cm (Tn/ha)
            "WSTB",  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            #"WB2_7",  # wb2_7 = branches (2-7 cm) (Tn/ha)
            "WB2_T",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            "WTHINB",  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            "WB05",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            "WB05_7",  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            "WB0_2",  # wb0_2 = branches < 2 cm (Tn/ha)
            "WDB",  # wdb = dead branches biomass (Tn/ha)
            "WL",  # wl = leaves (Tn/ha)
            #"WTBL",  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            "WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            #"WR",  # wr = roots (Tn/ha)
            #"WT",  # wt = total biomass (Tn/ha)
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
            "WB05_SP1",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
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
            "WB05_SP2",  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
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
            #"ALL_CONES",  # total of cones of the plot (anual mean)
            #"SOUND_CONES",  # total sound (healthy) cones of the plot (anual mean)
            #"SOUND_SEEDS",  # total sound (healthy) seeds of the plot (anual mean)
            #"W_SOUND_CONES",  # weight of sound (healthy) cones (Tn/ha) (anual mean)
            #"W_ALL_CONES",  # weight of all (healthy and not) cones (Tn/ha) (anual mean)

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
            "basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
            "basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
            #"bal",  # cumulative basal area (m2/ha)
            "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
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
            #"bole_vol",  # volume under bark (dm3)
            #"bark_vol",  # bark volume (dm3)
            "firewood_vol",  # firewood volume (dm3)
            #"vol_ha",  # volume over bark per hectare (m3/ha)

            # Wood uses variables
            "unwinding",  # unwinding = the useful wood volume unwinding destiny (dm3)
            "veneer",  # veneer = the useful wood volume veneer destiny (dm3)
            #"saw_big",  # saw_big = the useful wood volume big saw destiny (dm3)
            #"saw_small",  # saw_small = the useful wood volume small saw destiny (dm3)
            #"saw_canter",  # saw_canter = the useful wood volume canter saw destiny (dm3)
            "post",  # post = the useful wood volume post destiny (dm3)
            "stake",  # stake = the useful wood volume stake destiny (dm3)
            #"chips",  # chips = the useful wood volume chips destiny (dm3)

            # Biomass variables
            #"wsw",  # wsw = stem wood (kg)
            "wsb",  # wsb = stem bark (kg)
            "wswb",  # wswb = stem wood and stem bark (kg)
            "w_cork",  # fresh cork biomass (kg)
            #"wthickb",  # wthickb = Thick branches > 7 cm (kg)
            "wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            #"wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
            "wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            "wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
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
        
PinusPineaCataluña.vars()