# /usr/bin/env python3
#
# Python file structure developed by iuFOR, in collaboration with Sngular (https://www.sngular.com/es/)
# Main developers:
#   - Felipe Bravo Oviedo (iuFOR)
#   - Ángel Cristóbal Ordóñez Alonso (iuFOR)
#   - Aitor Vázquez Veloso (iuFOR)
#   - Moisés Martínez (Sngular)
#   - Spiros Michalakopoulos (Sngular)
#   - Pepe Cáceres (Sngular)
#
# Single tree growing model independent from distance, developed to
# Pure stands of Pinus sylvestris located on Sistema Ibérico y Central (Spain)
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


class PinusSylvestrisSIM(TreeModel):


    def __init__(self, configuration=None):
        super().__init__(name="Pinus sylvestris - Sistema Ibérico Meridional", version=1)


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
        
            Model.model_name = 'Psylvestris__sim__v01'  # set the model name to show it at the output
            Model.specie_ifn_id = 21  # Set the model specie ID to mark the trees of different species         
            Model.exec_time = 5  # recommended executions time to use that model
            Model.aplication_area = 'Sistema Ibérico Meridional (Spain)'  # area recommended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = '8, 9, 12, 13, 14'  # provenance regions recommended to use the model
            Model.model_type = 'tree_independent'  # SIMANFOR model type. It can be: ('' is neccesary)
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'link'  # link to model card in english
            Model.model_card_es = 'link'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps of information at the initial inventory
        Height/Diameter equation:
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        Reineke Index value:
            Doc.: del Río M, Montero G, Bravo F (2001). Analysis of diameter–density relationships and self-thinning in non-thinned even-aged Scots pine stands. Forest Ecology and Management, 142(1-3), 79-87
            Ref.: del Río et al (2001)
            Doc.: del Río M, López E, Montero G (2006). Manual de gestión para masas procedentes de repoblación de Pinus pinaster Ait., Pinus sylvestris L. y Pinus nigra Arn. en Castilla y León (No. 634.9560946 R585). Junta de Castilla y León, Castilla y León (España). Consejería de Medio Ambiente Ministerio de Educación y Ciencia, Madrid (España) Instituto Nacional de Investigación y Tecnología Agraria y Alimentaria, Madrid (España)
            Ref.: del Rio et al, 2006
            Doc.: del Río M, Montero G (2011). Modelo de simulación de claras en masas de Pinus sylvestris L. Monografias INIA: Forestal n. 3
            Ref.: del Río and Montero, 2011
        SI equation:
            Doc.: Rojo A, Montero, G (1996). El pino silvestre en la Sierra de Guadarrama MAPA.
            Ref.: Rojo and Montero, 1996
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('          Running: Pinus sylvestris model (Sistema Ibérico Meridional). Plot:', plot.plot_id         )
        print('#--------------------------------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced
            
            self.model_info()            
            plot.add_value('REINEKE_VALUE', -1.75)  # r constant value of SDI to the species of the model (-1.605 as default)  
            other_trees = total_trees = 0  # variables to count the number of trees from a different species that the principal one and the total of trees

            #-----------------------------------SITE_INDEX-----------------------------------------#

            if plot.si == 0 or plot.si == '':  # OJO, revisar la publicación, faltan cosas           
                t2 = 100  # SI reference age (years)
                t = t2/10  # Si reference age (decades) to use it on SI equation
                plot.add_value('REF_SI_AGE', t2)  
                SI = ((plot.dominant_h/10)*0.8534446)/(pow((1 - math.exp(float(- 0.270*t))), 2.2779))  # SI (dam)
                plot.add_value('SI', SI*10)  # Site Index (m) calculation

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

                    #-------------------------------- HEIGHT ------------------------------------#

                    if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                        tree.add_value('height', (13 + (
                                    27.0392 + 1.4853 * plot.dominant_h * 10 - 0.1437 * plot.qm_dbh * 10) * math.exp(
                            -8.0048 / math.sqrt(tree.dbh * 10))) / 10)

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height * 100 / tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal circumference (cm)

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    self.crown(tree, plot, 'initialize')  # activate crown variables

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

            self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

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
        Source:
            Doc.: Bravo-Oviedo A, Sterba H, del Río M, Bravo F (2006). Competition-induced mortality for
                  Mediterranean Pinus pinaster Ait. and P. sylvestris L. Forest Ecology and Management, 222(1-3), 88-98
            Ref.: Bravo-Oviedo et al, 2006
        """

        #if tree.specie == Model.specie_ifn_id:  # specie condition
        #    cvdbh = math.sqrt(pow(plot.qm_dbh, 2) - pow(plot.mean_dbh, 2)) / plot.mean_dbh
        #    return (1 / (1 + math.exp(
        #    -6.8548 + (9.792 / tree.dbh) + 0.121 * tree.bal * cvdbh + 0.037 * plot.si)))

        #else:
        return 1


    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Tree growth function.
        A function that updates dbh and h by using growth equations, and also update age, g, and v to the new situation.
        Source:
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        """

        try:  # errors inside that construction will be announced

            if old_tree.specie == Model.specie_ifn_id:  # specie condition

                new_tree.sum_value('tree_age', time)

                if plot.si == 0:
                    dbhg5: float = 0
                else:
                    dbhg5: float = math.exp(-0.37110 + 0.2525 * math.log(old_tree.dbh * 10) + 0.7090 * math.log(
                        (old_tree.cr + 0.2) / 1.2) + 0.9087 * math.log(plot.si) - 0.1545 * math.sqrt(
                        plot.basal_area) - 0.0004 * (old_tree.bal * old_tree.bal / math.log(old_tree.dbh * 10)))
                new_tree.sum_value("dbh", 1.70 + dbhg5 / 10)


                if dbhg5 == 0:
                    htg5: float = 0
                else:
                    htg5: float = math.exp(3.1222 - 0.4939 * math.log(dbhg5 * 10) + 1.3763 * math.log(
                    plot.si) - 0.0061 * old_tree.bal + 0.1876 * math.log(old_tree.cr))
                new_tree.sum_value("height", 1.14 + htg5 / 100)

                new_tree.add_value('basal_area', math.pi*(new_tree.dbh/2)**2)  # update basal area (cm2) 

                self.vol(new_tree, plot)  # update volume variables (dm3)

        except Exception:
            self.catch_model_exception()            


    def ingrowth(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated is calculated. The next function will order how to divide that basal area into the different diametric classes.
        Source:
            Doc.: Bravo F, Pando V, Ordóñez C, Lizarralde I (2008). Modelling ingrowth in mediterranean pine forests: a case study from scots pine (Pinus sylvestris L.) and mediterranean maritime pine (Pinus pinaster Ait.) stands in Spain. Forest Systems, 17(3), 250-260.
            Ref.: Bravo et al, 2008
        """

        prob_ingrowth: float = 1/(1 + math.exp( - (8.2739 - 0.3022*plot.qm_dbh)))

        if prob_ingrowth >= 0.50:
            ba_added = 5.7855 - 0.1703*plot.qm_dbh
            if ba_added < 0:
                return 0
            else:
                return ba_added  # m2/ha
        else:
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

            cd_1 = [0, 12.5, 0.0384*area]  # creating the first diametric class
            distribution.append(cd_1)  # adding the first diametric class to the distribution list

            if 'IFN' in Area.plot_type[plot.plot_id] or 'SNFI' in Area.plot_type[plot.plot_id]:
            # technical ingrowth only added on IFN plots
            
                cd_2 = [12.5, 22.5, 0.2718*area]
                distribution.append(cd_2)

                cd_3 = [22.5, 100, 0.6898*area]
                distribution.append(cd_3)

            else:

                cd_2 = [12.5, 100, 0]
                distribution.append(cd_2)

        except Exception:
            self.catch_model_exception()

        return distribution  # return distribution list
        # on the case you don't know how to share the ingrowth basal area on your plot, just return None


    def update_model(self, time: int, plot: Plot, trees: list):
        """
        A function that updates trees and plot information once growth, survival, and ingrowth functions were executed and the plot information was updated.
        The equations on that function are the same that in "initialize" function, so references are the same
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('          Running: Pinus sylvestris model (Sistema Ibérico Meridional). Plot:', plot.plot_id         )
        print('#--------------------------------------------------------------------------------------------------#')

        if time != Model.exec_time:  # if the user time is not the same as the execution model time, a warning message will be notified
            print('BE CAREFUL! That model was developed to', Model.exec_time,'year execution, and you are trying to make a', time, 'years execution!')
            print('Please, change your execution conditions to the recommended (', Model.exec_time, 'years execution). If not, the output values will be not correct.')
            # that variable must be activated just in case if the execution time of the user is not the same as the model
            Warnings.exec_error = 1  # that variable value must be 1 to notify the error at the output

        try:  # errors inside that construction will be announced

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            bal: float = 0.0

            if 'YEAR' in PLOT_VARS:
                new_year = plot.year + time  # YEAR is automatically updated after the execution process
            if 'AGE' in PLOT_VARS:
                new_age = plot.age + time  # AGE is automatically updated after the execution process

            for tree in plot_trees:  # for each tree...

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    #-----------------------------------BASAL_AREA-----------------------------------------#

                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                    tree.add_value('basal_area', math.pi * (tree.dbh / 2) ** 2)  # normal section (cm2)
                    tree.add_value('ba_ha', tree.basal_area * tree.expan / 10000)  # basal area per ha (m2/ha)
                    bal += tree.basal_area * tree.expan / 10000  # then, that value is accumulated

                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height * 100 / tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi * tree.dbh)  # normal circumference (cm)

                    #-------------------------------------VOL_HA-------------------------------------------#

                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                    #--------------------------- TREE FUNCTIONS ---------------------------------#  

                    self.crown(tree, plot, 'update_model')  # activate crown variables
                    
                    self.merchantable(tree)  # activate wood uses variables

                    self.biomass(tree)  # activate biomass variables

            #---------------------------------PLOT_FUNCTIONS---------------------------------------#

            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables 

        except Exception:
            self.catch_model_exception()


    def taper_over_bark(self, tree: Tree, hr: float):
        """
        Taper equation over bark function.
        A function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source:
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        """

        try:  # errors inside that construction will be announced

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
     
        except Exception:
            self.catch_model_exception()

        return dob  # diameter over bark (cm)


    def taper_under_bark(self, tree: Tree, hr: float):
        """
        Taper equation under bark function.
        A function that returns the taper equation to calculate the diameter (cm, under bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source:
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        """

        try:  # errors inside that construction will be announced

            dub = (1 + 0.3485 * 2.7182818284 ** (-23.9191 * hr)) * 0.7966 * tree.dbh * pow((1 - hr), (0.6094 - 0.7086 * (1 - hr)))

        except Exception:
            self.catch_model_exception()

        return dub        


    def merchantable(self, tree: Tree):
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
            class_conditions = [['unwinding', 3/ht, 40, 160], ['veneer', 3/ht, 40, 160], ['saw_big', 2.5/ht, 40, 200],
                                 ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28],
                                 ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]] 

            # usage and merch_list are a dictionary and a list returned from merch_calculation function
            # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
            usage, merch_list = TreeModel.merch_calculation(tree, class_conditions, PinusSylvestrisSIM)

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
        Crown equations:
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
        """

        try:  # errors inside that construction will be announced

            if func == 'initialize':  # if that function is called from initialize, first we must check if those variables are available on the initial inventory
                if tree.hlcw == 0 or tree.hlcw == '':  # if the tree hasn't height maximum crown-width (m) value, it is calculated
                    if plot.basal_area != '' and plot.basal_area != 0:                    
                        tree.add_value('hlcw', tree.height / (1 + math.exp(
                        float(-0.0012 * tree.height * 10 - 0.0102 * tree.bal - 0.0168 * plot.basal_area))))
                if tree.hcb == 0 or tree.hcb == '':
                    if plot.basal_area != '' and plot.basal_area != 0:
                        tree.add_value('hcb', tree.hlcw / (1 + math.exp(float(
                        1.2425 * (plot.basal_area/(tree.height*10)) + 0.0047 * plot.basal_area - 0.5725 * math.log(plot.basal_area) - 0.0082 * tree.bal))))
            else:
                if plot.basal_area != '' and plot.basal_area != 0:                
                    tree.add_value('hlcw', tree.height / (1 + math.exp(float(-0.0012 * tree.height * 10 - 0.0102 * tree.bal - 0.0168 * plot.basal_area))))
                    tree.add_value('hcb', tree.hlcw / (1 + math.exp(float(1.2425 * (plot.basal_area/(tree.height*10)) + 0.0047 * plot.basal_area - 0.5725 * math.log(plot.basal_area) - 0.0082 * tree.bal))))

            if tree.hcb != '' and tree.hcb != 0:
                tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
                tree.add_value('lcw', (1 / 10.0) * (0.2518 * tree.dbh * 10) * math.pow(tree.cr, (0.2386 + 0.0046 * (tree.height - tree.hcb) * 10)))  # maximum crown-width (m)

        except Exception:
            self.catch_model_exception()


    def canopy(self, plot: Plot, plot_trees):
        """
        Crown variables (plot).
        Function to calculate plot crown variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            plot_expan = plot_lcw = plot_lcw2 = plot_fcc = 0

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                if tree.specie == Model.specie_ifn_id:  # specie condition

                    plot_expan += tree.expan
                    plot_lcw += tree.lcw*tree.expan
                    plot_lcw2 += math.pow(tree.lcw, 2)*tree.expan
                    plot_fcc += math.pi*(math.pow(tree.lcw, 2)/4)*tree.expan

            plot.add_value('CROWN_MEAN_D', plot_lcw/plot_expan)
            plot.add_value('CROWN_DOM_D', math.sqrt(plot_lcw2/plot_expan))
            plot.add_value('CANOPY_COVER', plot_fcc/10000)

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
            Ref.: Ruiz-Peinado et al. 2011
        """

        try:  # errors inside that construction will be announced

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
            #"DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
            #"ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

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
            #"DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
            #"ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

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
            #"CROWN_MEAN_D",  # Mean crown diameter (m)
            "CROWN_MEAN_D_SP1",  # Mean crown diameter (m) for specie 1
            "CROWN_MEAN_D_SP2",  # Mean crown diameter (m) for specie 2    
            #"CROWN_DOM_D",  # Dominant crown diameter (m)
            "CROWN_DOM_D_SP1",  # Dominant crown diameter (m) for specie 1
            "CROWN_DOM_D_SP2",  # Dominant crown diameter (m) for specie 2    
            #"CANOPY_COVER",  # Canopy cover (%)
            "CANOPY_COVER_SP1",  # Canopy cover (%) for specie 1
            "CANOPY_COVER_SP2",  # Canopy cover (%) for specie 2        

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
            #"REINEKE_VALUE" # r constant value of SDI to the species of the model (-1.605 as default)

             # Plot variables calculated - volume and biomass
            #"VOL",  # Volume (m3/ha)
            #"BOLE_VOL",  # Volume under bark (m3/ha)
            #"BARK_VOL",  # Bark Volume (m3/ha) 
            #"VOL_CUT_VOLUME",  # Volume harvested percentage (%)
            #"DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
            #"ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

            # Plot variables calculated - volume for mixed models
            "VOL_SP1",  # Volume (m3/ha)
            "BOLE_VOL_SP1",  # Volume under bark (m3/ha)
            "BARK_VOL_SP1",  # Bark Volume (m3/ha) 
            "VOL_SP2",  # Volume (m3/ha)
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
            #"DEAD_WT",  # WT of the dead trees after an execution (Tn/ha)
            #"ING_WT",  # WT of the ingrowth trees after an execution (Tn/ha)

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


        ###############################################################################################################
        ######################################## TREE variables #######################################################
        ###############################################################################################################


        # list of tree variables on the simulator that can be deleted without make errors
        # to delete them, just leave it on the list; to NOT delete them, comment it at the list or remove it from them

        delete_from_tree = [


            # Special TREE_IDs to work with the IFN data
            #"TREE_ID_IFN3_2",
            #"TREE_ID_IFN3",
            #"TREE_ID_IFN2",
            #"TREE_ID_compare", 

            # Remarkable variables and basic variables measured
            #"specie",
            #"tree_age",
            #"expan",  # expansion factor
            "dbh_1",  # dbh measurement 1 (cm)
            "dbh_2",  # dbh measurement 2 (cm)
            #"dbh",  # diameter at breast height (cm)
            #"height",  # total tree height (m)
            #"stump_h",   # stump height (m))
            "bark_1",  # bark thickness, measurement 1 (mm)
            "bark_2",  # bark thickness, measurement 2 (mm)
            "bark",  # mean bark thickness (mm)

           # Basic variables calculated
            #"basal_area",   # basal area (cm2)
            "basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
            "basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
            #"bal",  # cumulative basal area (m2/ha)
            "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
            "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
            #"ba_ha",  # basal area per ha (m2/ha) 
            #"normal_circumference",  # circumference at breast height (cm)
            #"slenderness",  # slenderness (cm/cm)
            
            # Crown variables
            #"cr",  # crown ratio (%)
            #"lcw",  #  largest crown width (m)
            #"hcb",  # height of the crown base (m)
            #"hlcw",  # height of the largest crown width (m)

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
            "coord_y"
        ]

        Variables.remove_var_plot(delete_from_plot)
        Variables.remove_var_tree(delete_from_tree)
        
PinusSylvestrisSIM.vars()
