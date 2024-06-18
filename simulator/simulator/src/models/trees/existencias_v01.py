# /usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
#
# Single tree growing model independent from distance, developed to
# Pure stands of specie located on location (Spain)
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

from models.trees.equations_tree_models import TreeEquations

import math
import sys
import logging
import numpy as np
import os


class Existencias(TreeModel):

    def __init__(self, configuration=None):
        super().__init__(name="Existencias", version=1)


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
        
            Model.model_name = 'existencias_v01'  # set the model name to show it at the output
            Model.specie_ifn_id = ''  # Set the model specie ID to mark the trees of different species         
            Model.exec_time = 0  # recommended executions time to use that model
            Model.aplication_area = 'Spain'  # area recommended to use the model; just write 'none' if it is not defined yet
            Model.valid_prov_reg = ''  # provenance regions recommended to use the model
            Model.model_type = 'tree_independent'  # SIMANFOR model type. It can be: ('' is neccesary)
            # 'under_development' - 'tree_independent' - 'tree_dependent' - 'stand_model' - 'size-class models'
            Model.model_card_en = 'https://github.com/simanfor/modelos/blob/main/existencias/existencias_EN.pdf'  # link to model card in english
            Model.model_card_es = 'https://github.com/simanfor/modelos/blob/main/existencias/existencias_ES.pdf'  # link to model card in spanish

        except Exception:
            self.catch_model_exception()


    def initialize(self, plot: Plot):
        """
        A function that updates the gaps of information at the initial inventory
        Source:
            Doc.:
            Ref.:
        """

        print('#------------------------------------------------------------------------------------------------- #')
        print('                        Running: Existencias model (Spain). Plot:', plot.plot_id                     )
        print('#--------------------------------------------------------------------------------------------------#')

        try:  # errors inside that construction will be announced

            self.model_info()
            plot.add_value('REINEKE_VALUE', -1.605)  # r constant value of SDI to the species of the model (-1.605 as default)
            other_trees = total_trees = 0  # variables to count the number of trees from a different species that the principal one and the total of trees

            #-----------------------------------SITE_INDEX-----------------------------------------#

            #if plot.si == 0 or plot.si == '':
            #    t2 =   # age to estimate the SI and Dominant_diamter (years)
            #    plot.add_value('REF_SI_AGE', t2)  
            #    SI = 
            #    plot.add_value('SI', SI)  # Site Index (m) calculation

            plot_trees: list[Tree] = plot.short_trees_on_list('dbh', DESC)  # establish an order to calculate tree variables
            bal: float = 0

            for tree in plot_trees:  # for each tree...

                total_trees += 1

                #if tree.specie == Model.specie_ifn_id:  # specie condition

                #-----------------------------------BASAL_AREA-----------------------------------------#

                tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                tree.add_value('basal_area', math.pi*(tree.dbh/2)**2)  # normal section (cm2)
                tree.add_value('ba_ha', tree.basal_area*tree.expan/10000)  # basal area per ha (m2/ha)
                bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated

                #-------------------------------- HEIGHT ------------------------------------#

                #if tree.height == 0 or tree.height == '':  # if the tree hasn't height (m) value, it is calculated
                #    tree.add_value('height', )

                #-------------------------------- OTHERS ------------------------------------#

                tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%)
                tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal circumference (cm)

                #--------------------------- TREE FUNCTIONS ---------------------------------#  

                #self.crown(tree, plot, 'initialize')  # activate crown variables

                self.vol(tree, plot)  # activate volume variables

                if tree.vol == '':
                    tree.add_value('vol_ha', '')
                else:
                    tree.add_value('vol_ha', tree.vol*tree.expan/1000)  # volume over bark per ha (m3/ha)

                self.merchantable(tree)  # activate wood uses variables

                self.biomass(tree)  # activate biomass variables
                
                #else:
                #    other_trees += 1
    
            #if other_trees != 0:
            #    print(' ')
            #    print(other_trees, 'of the total', total_trees, 'trees are from a different species than the principal')
            #    print('That trees will be shown underlined at the output, and they will be maintained at simulations, not applying model equations over them.')
            #    print(' ')
            #    if other_trees == total_trees:
            #        Warnings.specie_error_trees = 1

    
            self.vol_plot(plot, plot_trees)  # activate volume variables (plot)

            #self.canopy(plot, plot_trees)  # activate crown variables (plot)

            self.merchantable_plot(plot, plot_trees)  # activate wood uses variables (plot)

            self.biomass_plot(plot, plot_trees)  # activate biomass (plot) variables  

            # get diversity indexes
            plot.add_value('SHANNON', TreeEquations.get_shannon_index(plot, plot_trees))
            plot.add_value('SIMPSON', TreeEquations.get_simpson_index(plot, plot_trees))
            plot.add_value('MARGALEF', TreeEquations.get_margalef_index(plot, plot_trees))
            plot.add_value('PIELOU', TreeEquations.get_pielou_index(plot, plot_trees))

            Warnings.specie_error_trees = Warnings.specie_error = 0  # no red color on the tree sheet


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
        A function that updates dbh and h by using growth equations, and also update age, g, and v to the new situation.
        """

        try:  # errors inside that construction will be announced

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
        incorporated is calculated. The next function will order how to divide that basal area into the different diametric classes.
        """

        try:  # errors inside that construction will be announced
            None
        except Exception:
            self.catch_model_exception()

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
        print('                        Running: Existencias model (xx). Plot:', plot.plot_id                     )
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

                    tree.add_value('basal_area', math.pi*(tree.dbh/2)**2)  # normal section (cm2)
                    tree.add_value('bal', bal)  # the first tree must receive 0 value (m2/ha)
                    tree.add_value('ba_ha', tree.basal_area*tree.expan/10000)  # basal area per ha (m2/ha)
                    bal += tree.basal_area*tree.expan/10000  # then, that value is accumulated
                    
                    #-------------------------------- OTHERS ------------------------------------#

                    tree.add_value('slenderness', tree.height*100/tree.dbh)  # height/diameter ratio (%)
                    tree.add_value('normal_circumference', math.pi*tree.dbh)  # normal circumference (cm)

                    #-------------------------------------VOL_HA-------------------------------------------#

                    if tree.vol == '':
                        tree.add_value('vol_ha', '')
                    else:
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


    def taper_over_bark_Fang(self, tree: Tree, hr: float):
        """
        Taper equation over bark function using the Fang model.
        A function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Sources:
            Doc.: Bravo, F., Álvarez González, J. G., Rio, M. D., Barrio, M., Bonet Lledos, J. A., Bravo Oviedo, A., ... & Diéguez Aranda, U. (2011). Growth and yield models in Spain: historical overview, contemporary examples and perspectives. Forest Systems, 2011, vol. 20, núm. 2, p. 315-328.
            Ref.: Bravo et al., 2011
            Doc.: Diéguez-Aranda, U., Alboreca, A. R., Castedo-Dorado, F., González, J. Á., Barrio-Anta, M., Crecente-Campo, F., ... & Balboa-Murias, M. A. (2009). Herramientas selvícolas para la gestión forestal sostenible en Galicia. Forestry, 82, 1-16.
            Ref.: Diéguez-Aranda et al., 2009
            Doc.: López-Sánchez C A (2009). Estado selvícola y modelos de crecimiento y gestión de plantaciones de Pseudotsuga menziesii (Mirb.) Franco en España (Doctoral dissertation, Doctoral thesis. Universidad de Santiago de Compostela, Lugo.
            Ref.: López-Sánchez, 2009
            Doc.: Rodríguez, F., & Torre, I. L. (2015). Comparison of stem taper equations for eight major tree species in the Spanish Plateau. Forest systems, 24(3), 2.
            Ref.: Rodriguez & Torre, 2015
        """

        try:  # errors inside that construction will be announced

            # values = (ao, a1, a2, b1, b2, b3, p1, p2) values to Fang model over bark
            values = list  # it will be changed to boolean if no equations are available

            
            ########################################################################################


            # if tree.specie == 3:  # Frangula alnus

            # elif tree.specie == 11:  # Ailanthus altissima

            # elif tree.specie == 12:  # Malus sylvestris

            # elif tree.specie == 13:  # Celtis australis

            # elif tree.specie == 14:  # Taxus baccata

            # elif tree.specie == 15:  # Crataegus spp.

            # elif tree.specie == 16:  # Pyrus spp.

            # elif tree.specie in (17, 217, 317, 917):  # Cedrus spp. - Cedrus atlantica, C. deodara, C. libani, C. spp.

            if tree.specie == 21:  # Pinus sylvestris

                values = (0.000051, 1.845867, 1.045022, 0.000011, 0.000038, 0.000030, 0, 0)
                # Rodriguez & Torre, 2015

                # values = (6.421e-5, 1.817, 1.001, 1.357e-5, 3.059e-5, 2.699e-5, 0.08199, 0.6237)
                # Diéguez-Aranda et al., 2009                

            # elif tree.specie == 22:  # Pinus uncinata

            elif tree.specie == 23:  # Pinus pinea
            
                values = (0.000067, 1.698754, 1.210604, 0.000006, 0.000033, 0.000026, 0.021072, 0.475953)
                # Rodriguez & Torre, 2015

            # elif tree.specie == 24:  # Pinus halepensis

            elif tree.specie == 25:  # Pinus nigra

                values = (0.000049, 1.982808, 0.905147, 0.000014, 0.000036, 0.000029, 0.091275, 0.781990)
                # Rodriguez & Torre, 2015

            elif tree.specie == 26:  # Pinus pinaster
                
                values = (0.000048, 1.929098, 0.976356, 0.000010, 0.000035, 0.000033, 0.064157, 0.681476)
                # Rodriguez & Torre, 2015

                # values = (3.974e-5, 1.876, 1.079, 1.003e-5, 3.695e-5, 2.910e-5, 0.1013, 0.7233)
                # Diéguez-Aranda et al., 2009

            # elif tree.specie == 27:  # Pinus canariensis

                # Bravo et al., 2011

            elif tree.specie == 28:  # Pinus radiata

                #values = (0.000058, 1.829097, 1.007844, 0.000009, 0.000033, 0.000030, 0, 0)
                # CESEFOR

                values = (4.851e-5, 1.883, 1.004, 8.702e-6, 3.302e-5, 2.899e-5, 0.06526, 0.6560)
                # Diéguez-Aranda et al., 2009                

            # elif tree.specie == 31:  # Abies alba

            # elif tree.specie == 32:  # Abies pinsapo

            # elif tree.specie == 33:  # Picea abies

            elif tree.specie == 34:  # Pseudotsuga menziesii

                values = (8.560e-5, 1.771, 0.9510, 9.340e-6, 3.169e-5, 2.786e-5, 0.07362, 0.5397)
                # Diéguez-Aranda et al., 2009                   

                values = (0.00008564, 1.775, 0.9510, 0.000009340, 0.00003169, 0.00002786, 0.07362, 0.5397)
                # López-Sánchez, 2009

            # elif tree.specie in (36, 236, 336, 436, 936):  # Cupressus spp. - C. sempervirens, C. arizonica, C. lusitanica, C. macrocarpa, C. spp.
            
            # elif tree.specie == 37:  # Juniperus communis          
                                    
            elif tree.specie == 38:  # Juniperus thurifera

                values = (0.000074, 1.86289, 0.901233, 0.000001, 0.000028, 0.000037, 0.008578, 0.711639)
                # Rodriguez & Torre, 2015

            # elif tree.specie == 39:  # Juniperus phoenica

            elif tree.specie == 41:  # Quercus robur

                values = (4.618e-5, 1.771, 1.165, 5.159e-6, 3.157e-5, 2.553e-5, 0.04025, 0.5184)
                # Diéguez-Aranda et al., 2009                      

            # elif tree.specie == 42:  # Quercus petraea

            elif tree.specie == 43:  # Quercus pyrenaica

                values = (0.000051, 1.867810, 0.989625, 0.000007, 0.000030, 0.000032, 0.047757, 0.825279)
                # Rodriguez & Torre, 2015

            # elif tree.specie == 44:  # Quercus faginea

            # elif tree.specie == 45:  # Quercus ilex

            # elif tree.specie == 46:  # Quercus suber

            # elif tree.specie == 47:  # Quercus canariensis

            # elif tree.specie == 51:  # Populus alba

            # elif tree.specie == 52:  # Populus tremula

            # elif tree.specie == 54:  # Alnus glutinosa

            # elif tree.specie == 55:  # Fraxinus angustifolia

            # elif tree.specie in (55, 255, 355, 955):  # Fraxinus spp. - F. angustifolia, F. excelsior, F. omus, F. spp.                                                
            
            # elif tree.specie in (56, 256, 356, 956):  # Ulmus spp. - U. minor, U. glabra, U. pumila, U. spp.
            
            # elif tree.specie in (57, 257, 357, 457, 557, 657, 757, 857, 858, 957):  # Salix spp. - S. spp., S. alba, S. atrocinerea, S. babylonica, S. cantabrica, S. caprea, S. eleagnos, S. fragilis, S. canariensis, S. purpurea

            elif tree.specie == 61:  # Eucalyptus globulus

                values = (4.896e-5, 1.679, 1.186, 4.901e-6, 3.246e-5, 4.156e-5, 0.04503, 0.8364)
                # Diéguez-Aranda et al., 2009

            # elif tree.specie == 62:  # Eucalyptus camaldulensis

            elif tree.specie == 64:  # Eucalyptus nittens

                values = (5.024e-5, 1.823, 1.046, 5.700e-6, 3.074e-5, 2.797e-5, 0.03111, 0.5643)
                # Diéguez-Aranda et al., 2009
            
            # elif tree.specie == 65:  # Ilex aquifolium
            
            # elif tree.specie == 66:  # Olea europaea

            # elif tree.specie == 67:  # Ceratonia siliqua

            # elif tree.specie == 68:  # Arbutus unedo

            elif tree.specie == 71:  # Fagus sylvatica

                values = (0.000120, 2.036193, 0.799343, 0.000015, 0.000033, 0.005194, 0.074439, 0.873445)
                # Rodriguez & Torre, 2015

            elif tree.specie == 72:  # Castanea sativa

                values = (0.00005542, 1.914, 0.936, 0.000009869, 0.00003362, 0.00002667, 0.07191, 0.5590)
                # Bravo et al., 2011

            # elif tree.specie in (73, 273, 373):  # Betula spp. - B. spp., B. alba, B. pendula
            
            # elif tree.specie == 74:  # Corylus avellana
            
            # elif tree.specie == 75:  # Juglans regia
            
            # elif tree.specie in (76, 276, 376, 476, 576, 676, 976):  # Acer spp. - A. campestre, A. monspessulanum, A. negundo, A. opalus, A. pseudoplatanus, A. platanoides, A. spp.
            
            # elif tree.specie in (78, 278, 378, 478, 578, 678, 778):  # Sorbus spp. - S. spp., S. aria, S. aucuparia, S. domestica, S. torminalis, S. latifolia, S. chamaemespilus

            # elif tree.specie in (95, 295, 395, 495, 595):  # Prunus spp. - P. spp, P.spinosa, P. avium, P. lusitanica, P. padus

            # elif tree.specie == 97:  # Sambucus nigra
            
            elif tree.specie == 258:  # Populus x canadensis/euroamericana

                values = (0.000044, 1.872438, 1.023328, 0.000013, 0.000028, 0.000026, 0.032326, 0.645012)
                # Rodriguez & Torre, 2015

            elif tree.specie == 273:  # Betula alba

                values = (5.991e-5, 1.925, 0.8637, 5.266e-6, 2.838e-5, 2.428e-5, 0.04425, 0.9984)
                # Diéguez-Aranda et al., 2009

            else:  # no volume equation available
                
                values = False
            
            # TODO: incluir ecuaciones IFN4, anexo 19: https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/temas/inventarios-nacionales/documentador_sig_tcm30-536622.pdf

            ########################################################################################


            dob = TreeModel.Fang_taper(tree, hr, values)


        except Exception:
            self.catch_model_exception()

        return dob  # diameter over bark (cm)


    def taper_over_bark_others(self, tree: Tree, hr: float):
        """
        Taper equation over bark function using the Stud, D'Aquitaine or other model.
        A function that returns the taper equation to calculate the diameter (cm, over bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        """

        try:  # errors inside that construction will be announced

            dbh = tree.dbh
            ht = tree.height
            h = hr


            if tree.specie == 24:  # Pinus halepensis

                a1 = 0.4893
                a2 = 1.9362
                a3 = 0.0559
                # rwb = radius with bark (cm)
                A = (a1 * tree.dbh) / (1 - 2.7182818284**(a3 * (1.3 - tree.height)))
                B = (tree.dbh / 2 - a1 * tree.dbh) * (1 - (1 / (1 - 2.7182818284**(a2 * (1.3 - tree.height)))))
                C = 2.7182818284**(-a2*hr*tree.height) * (((tree.dbh / 2 - a1 * tree.dbh) * 2.7182818284**(1.3 * a2)) / (1 - 2.7182818284**(a2 * (1.3 - tree.height))))
                D = 2.7182818284**(a3*hr*tree.height) * ((a1 * tree.dbh * 2.7182818284**(-a3 * tree.height)) / (1 - 2.7182818284**(a3 * (1.3 - tree.height))))
                rwb = A + B + C - D
                dob = rwb*2
                # Saldaña, 2010

            elif tree.specie == 42:  # Quercus petraea

                dob = (1 + 0.558513*2.7182818284**(-25.933370*h/ht))*(0.942294*dbh*((1 - h/ht)**(1.312840 - 0.342491*(ht/dbh) - 1.239930*(1 - h/ht))))
                # Manríquez-González et al., 2017

            elif tree.specie == 43:  # Quercus pyrenaica

                dob = (1 + 0.558513*2.7182818284**(-25.933370*h/ht))*(0.942294*dbh*((1 - h/ht)**(1.312840 - 0.342491*(ht/dbh) - 1.239930*(1 - h/ht))))
                # Manríquez-González et al., 2017


        except Exception:
            self.catch_model_exception()

        return dob  # diameter over bark (cm)


    def taper_under_bark(self, tree: Tree, hr: float):
        """
        Taper equation under bark function.
        A function that returns the taper equation to calculate the diameter (cm, under bark) at different heights.
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually.
        Source:
            Doc.: López-Sánchez C A (2009). Estado selvícola y modelos de crecimiento y gestión de plantaciones de Pseudotsuga menziesii (Mirb.) Franco en España (Doctoral dissertation, Doctoral thesis. Universidad de Santiago de Compostela, Lugo.
            Ref.: López-Sánchez, 2009        
        """

        try:  # errors inside that construction will be announced
            

            if tree.specie == 21:  # Pinus sylvestris

                dub = (1 + 0.3485 * 2.7182818284 ** (-23.9191 * hr)) * 0.7966 * tree.dbh * pow((1 - hr), (0.6094 - 0.7086 * (1 - hr)))


            elif tree.specie == 23:  # Pinus pinea

                beta1 = 1.0972
                beta2 = -2.8505
                H = tree.height*10  # dm
                dubmm = tree.dbh * 10 * ((H - hr*H) / (H - 13)) + beta1 * (
                            ((H ** 1.5 - (hr*H) ** 1.5) * (hr*H - 13)) / H ** 1.5) + beta2 * (
                                   ((H - (hr*H)) ** 4) * (hr*H - 13) / (H ** 4))
                dub = dubmm*0.1  # mm to cm


            elif tree.specie == 26:  # Pinus pinaster

                dub = (1 + 2.4771 * 2.7182818284 ** (-5.0779 * hr)) * 0.2360 * tree.dbh * pow((1 - hr), (0.4733 - 3.0371 * (1 - hr)))
        

            # elif tree.specie == 28:  # Pinus radiata

                #a1 = 0.6665
                #a11 = 0.002472
                #a2 = -0.7668
                #a3 = 0.18857
                #a4 = 11.4727
                #a5 = 0.90117

                #h = tree.height*100  # height in cm
                #z = hr*tree.height*100  # relative height in cm

                #dub = a5*tree.dbh*((1 - z/h)**(a1 + a11*h/tree.dbh + a2*(1 - z/h))) * (1 + a3*(2.7182818284**(-a4*z/h)))


            elif tree.specie == 34:  # Pseudotsuga menziesii

                values = (0.00005695, 1.741, 1.072, 0.000009823, 0.00003246, 0.00002745, 0.06750, 0.5149)
                dub = TreeModel.Fang_taper(tree, hr, values)


        except Exception:
            self.catch_model_exception()

        return dub  # diameter under bark (cm)


    def vol(self, tree: Tree, plot: Plot):
        """
        Volume variables (tree).
        Function to calculate volume variables for each tree.
        That function is run by initialize and growth functions and uses taper equations to calculate the values.
        Sources:
            Doc.: Badía M, Rodríguez F, Broto M (2001). Modelos del perfil del árbol. Aplicación al pino radiata (Pinus radiata D. Don). In Congresos Forestales
            Ref.: Badía et al, 2001
            Doc.: Calama R, Montero G (2006). Stand and tree-level variability on stem form and tree volume in Pinus pinea L.: a multilevel random components approach. Forest Systems, 15(1), 24-41
            Ref.: Calama and Montero, 2006
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp           
            Ref.: Lizarralde 2008
            Doc.: Manrique-González, J., Bravo, F., del Peso, C., Herrero, C., Rodríguez, F., 2017. Ecuaciones de perfil para las especies de roble albar (Quercus petraea (Matt.) Liebl.) y rebollo (Quercus pyrenaica Willd) en la comarca de la “Castillería” en el Norte de la provincia de Palencia. 7º Congreso Forestal Español (póster).  http://7cfe.congresoforestal.es/sites/default/files/comunicaciones/776.pdf
            Ref.: Manrique-González et al., 2017
        """

        try:  # errors inside that construction will be announced


            not_Fang = False  # change to True when it is needed to use a model different from Fang
            dub = False  # chage to True when an under bark volume equation is available



            if tree.specie == 21:  # Pinus sylvestris
             
                dub = True
                # Lizarralde, 2008

            # elif tree.specie == 22:  # Pinus uncinata

            elif tree.specie == 23:  # Pinus pinea
            
                dub = True  
                # Calama and Montero, 2006

            elif tree.specie == 24:  # Pinus halepensis

                not_Fang = True
                # Saldaña, 2010

            # elif tree.specie == 25:  # Pinus nigra

            elif tree.specie == 26:  # Pinus pinaster
                
                dub = True
                # Lizarralde, 2008

            # elif tree.specie == 27:  # Pinus canariensis

                # Bravo et al., 2011

            #elif tree.specie == 28:  # Pinus radiata
          
                # dub = True   # predictions are higher than vob
                # Badía et al, 2001

            # elif tree.specie == 31:  # Abies alba

            # elif tree.specie == 32:  # Abies pinsapo

            elif tree.specie == 34:  # Pseudotsuga menziesii                

                dub = True
                # López-Sánchez, 2009

            # elif tree.specie == 38:  # Juniperus thurifera

            # elif tree.specie == 41:  # Quercus robur                    

            elif tree.specie == 42:  # Quercus petraea

                not_Fang = True
                # Manríquez-González et al., 2017

            # elif tree.specie == 43:  # Quercus pyrenaica

                # not_Fang = True
                # Manríquez-González et al., 2017

            # elif tree.specie == 44:  # Quercus faginea

            # elif tree.specie == 45:  # Quercus ilex

            # elif tree.specie == 46:  # Quercus suber

            # elif tree.specie == 47:  # Quercus canariensis

            # elif tree.specie == 54:  # Alnus glutinosa

            # elif tree.specie == 55:  # Fraxinus angustifolia

            # elif tree.specie == 61:  # Eucalyptus globulus

            # elif tree.specie == 64:  # Eucalyptus nittens

            # elif tree.specie == 66:  # Olea europaea

            # elif tree.specie == 67:  # Ceratonia siliqua

            # elif tree.specie == 71:  # Fagus sylvatica

            # elif tree.specie == 72:  # Castanea sativa

            # elif tree.specie == 258:  # Populus x canadensis/euroamericana

            # elif tree.specie == 273:  # Betula alba
    

            #######################################################################################################


            hr = np.arange(0, 1, 0.001)  # that line establish the integrated conditions for volume calculation


            # Volume over bark
            if not_Fang == False:  # Fang model 

                dob = self.taper_over_bark_Fang(tree, hr)  # diameter over bark using taper equation (cm)

            else:  # not_Fang model

                dob = self.taper_over_bark_others(tree, hr)  # diameter over bark using taper equation (cm)


            if type(dob) != int:  # dob must be a list of values

                fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)                
                tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)

            else:  # if it is int, then not equations are available

                tree.add_value('vol', '')


            # Volume under bark
            if dub == True:

                dub = self.taper_under_bark(tree, hr)  # diameter under/without bark using taper equation (cm)
                fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
                tree.add_value('bole_vol', math.pi * tree.height * 10 * integrate.simps(fub, hr))  # volume under bark using simpson integration (dm3)
                tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)

            else:

                tree.add_value('bole_vol', '')
                tree.add_value('bark_vol', '')

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
            vol_plot = vol_plot_bole = True  # variable to decide if plot volume can be calculated


            for tree in plot_trees:  # check if all trees have volume variables calculated

                # volume over bark
                if tree.vol == '':
                    vol_plot = False

                else:   
                    plot_vol += tree.expan*tree.vol

                # volume under bark
                if tree.bole_vol == '':
                    vol_plot_bole = False
                else:
                    plot_bole_vol += tree.expan*tree.bole_vol


            if vol_plot == True:
                plot.add_value('VOL', plot_vol/1000)  # plot volume over bark (m3/ha)
                plot.add_value('BOLE_VOL', '')  # plot volume under bark (m3/ha)
                plot.add_value('BARK_VOL', '')  # plot bark volume (m3/ha)

                if vol_plot_bole == True:
                    plot_bark = plot_vol - plot_bole_vol

                    plot.add_value('BOLE_VOL', plot_bole_vol/1000)  # plot volume under bark (m3/ha)
                    plot.add_value('BARK_VOL', plot_bark/1000)  # plot bark volume (m3/ha)

            else:

                plot.add_value('VOL', '')  # plot volume over bark (m3/ha)


        except Exception:
            self.catch_model_exception()


    def merchantable(self, tree: Tree):
        """
        Merchantable wood calculation (tree).
        A function needed to calculate the different commercial volumes of wood depending on the destiny of that.
        That function is run by initialize and update_model functions and is linked to taper_over_bark, an indispensable function.
        That function is run by initialize and update_model functions.
        Data criteria to classify the wood by different uses were obtained from:
            Doc.: Fernández-Manso A, Sarmiento A (2004). El pino radiata (Pinus radiata). Manual de gestión forestal sostenible. Junta de Castilla y León.
            Ref.: Fernández-Manso et al, 2004
            Doc.: Rodríguez F (2009). Cuantificación de productos forestales en la planificación forestal: Análisis de casos con cubiFOR. In Congresos Forestales
            Ref.: Rodríguez, 2009

        """
        
        try:  # errors inside that construction will be announced

            ht = tree.height  # the total height as ht to simplify
            # class_conditions have different lists for each usage, following that structure: [wood_usage, hmin/ht, dmin, dmax]
            # [WOOD USE NAME, LOG RELATIVE LENGTH RESPECT TOTAL TREE HEIGHT, MINIMUM DIAMETER, MAXIMUM DIAMETER]
            

            ########################################################################################


            if tree.specie == 3:  # Frangula alnus

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 11:  # Ailanthus altissima

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 12:  # Malus sylvestris

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 13:  # Celtis australis

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 14:  # Taxus baccata

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 15:  # Crataegus spp.

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 16:  # Pyrus spp.

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (17, 217, 317, 917):  # Cedrus spp. - Cedrus atlantica, C. deodara, C. libani, C. spp.

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 21:  # Pinus sylvestris

                class_conditions = [['unwinding', 3/ht, 40, 160], ['veneer', 3/ht, 40, 160], ['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 22:  # Pinus uncinata


            elif tree.specie == 23:  # Pinus pinea
            
                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 24:  # Pinus halepensis

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 25:  # Pinus nigra

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 26:  # Pinus pinaster
                
                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 27:  # Pinus canariensis

                # Bravo et al., 2011


            elif tree.specie == 28:  # Pinus radiata

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
                #  Fernández-Manso et al, 2004
                

            # elif tree.specie == 31:  # Abies alba


            # elif tree.specie == 32:  # Abies pinsapo


            elif tree.specie == 33:  # Picea abies

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 34:  # Pseudotsuga menziesii

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (36, 236, 336, 436, 936):  # Cupressus spp. - C. sempervirens, C. arizonica, C. lusitanica, C. macrocarpa, C. spp.

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16]]


            elif tree.specie == 37:  # Juniperus communis

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16]]


            elif tree.specie == 38:  # Juniperus thurifera

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16]]


            elif tree.specie == 39:  # Juniperus phoenica

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16]]


            elif tree.specie == 41:  # Quercus robur

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 42:  # Quercus petraea

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 43:  # Quercus pyrenaica

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 44:  # Quercus faginea

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 45:  # Quercus ilex

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 46:  # Quercus suber

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 47:  # Quercus canariensis


            elif tree.specie == 51:  # Populus alba

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 52:  # Populus tremula

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 54:  # Alnus glutinosa

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (55, 255, 355, 955):  # Fraxinus spp. - F. angustifolia, F. excelsior, F. omus, F. spp.

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (56, 256, 356, 956):  # Ulmus spp. - U. minor, U. glabra, U. pumila, U. spp.

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (57, 257, 357, 457, 557, 657, 757, 857, 858, 957):  # Salix spp. - S. spp., S. alba, S. atrocinerea, S. babylonica, S. cantabrica, S. caprea, S. eleagnos, S. fragilis, S. canariensis, S. purpurea

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 61:  # Eucalyptus globulus
 

            elif tree.specie == 62:  # Eucalyptus camaldulensis

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 64:  # Eucalyptus nittens


            elif tree.specie == 65:  # Ilex aquifolium

                class_conditions = [['saw_canter', 2.5/ht, 15, 28]]


            elif tree.specie == 66:  # Olea europaea

                class_conditions = [['unwinding', 1.2/ht, 20, 160], ['veneer', 1.2/ht, 20, 160], ['saw_canter', 2.5/ht, 12, 28], ['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 67:  # Ceratonia siliqua


            elif tree.specie == 68:  # Arbutus unedo

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 71:  # Fagus sylvatica

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 72:  # Castanea sativa

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (73, 273, 373):  # Betula spp. - B. spp., B. alba, B. pendula

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 74:  # Corylus avellana

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 75:  # Juglans regia

                class_conditions = [['unwinding', 1.2/ht, 20, 160], ['veneer', 1.2/ht, 20, 160], ['saw_canter', 2.5/ht, 12, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (76, 276, 376, 476, 576, 676, 976):  # Acer spp. - A. campestre, A. monspessulanum, A. negundo, A. opalus, A. pseudoplatanus, A. platanoides, A. spp.

                class_conditions = [['unwinding', 1.2/ht, 20, 160], ['veneer', 1.2/ht, 20, 160], ['saw_canter', 2.5/ht, 12, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (78, 278, 378, 478, 578, 678, 778):  # Sorbus spp. - S. spp., S. aria, S. aucuparia, S. domestica, S. torminalis, S. latifolia, S. chamaemespilus

                class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]


            elif tree.specie in (95, 295, 395, 495, 595):  # Prunus spp. - P. spp, P.spinosa, P. avium, P. lusitanica, P. padus

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 97:  # Sambucus nigra

                class_conditions = [['chips', 1/ht, 5, 1000000]]


            elif tree.specie == 258:  # Populus x canadensis/euroamericana

                class_conditions = [['unwinding', 1.2/ht, 20, 160], ['veneer', 1.2/ht, 20, 160], ['saw_canter', 2.5/ht, 12, 28], ['chips', 1/ht, 5, 1000000]]


            # elif tree.specie == 273:  # Betula alba


            else:  # no volume equation available
                
                class_conditions = []
            

            ########################################################################################


            if type(class_conditions) != bool:  # if it is a merchantable limit available...

                # usage and merch_list are a dictionary and a list returned from merch_calculation function
                # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
                usage, merch_list = TreeModel.merch_calculation_all_species(tree, class_conditions, Existencias)

            else:

                usage = merch_list = 0

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

            plot_unwinding = plot_veneer = plot_saw_big = plot_saw_small = plot_saw_canter = plot_post = plot_stake = plot_chips = 0

            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                if type(tree.unwinding) != str:
                    plot_unwinding += tree.unwinding*tree.expan/1000
                if type(tree.veneer) != str:
                    plot_veneer += tree.veneer*tree.expan/1000
                if type(tree.saw_big) != str:
                    plot_saw_big += tree.saw_big*tree.expan/1000
                if type(tree.saw_small) != str:    
                    plot_saw_small += tree.saw_small*tree.expan/1000
                if type(tree.saw_canter) != str:    
                    plot_saw_canter += tree.saw_canter*tree.expan/1000
                if type(tree.post) != str:    
                    plot_post += tree.post*tree.expan/1000
                if type(tree.stake) != str:
                    plot_stake += tree.stake*tree.expan/1000
                if type(tree.chips) != str:
                    plot_chips += tree.chips*tree.expan/10000

            if plot_unwinding != 0:
                plot.add_value('UNWINDING', plot_unwinding)  # now, we add the plot value to each variable, changing the units to m3/ha
            if plot_veneer != 0:
                plot.add_value('VENEER', plot_veneer)
            if plot_saw_big != 0:
                plot.add_value('SAW_BIG', plot_saw_big)
            if plot_saw_small != 0:
                plot.add_value('SAW_SMALL', plot_saw_small)
            if plot_saw_canter != 0:
                plot.add_value('SAW_CANTER', plot_saw_canter)
            if plot_post != 0:
                plot.add_value('POST', plot_post)
            if plot_stake != 0:
                plot.add_value('STAKE', plot_stake)
            if plot_chips != 0:
                plot.add_value('CHIPS', plot_chips)

        except Exception:
            self.catch_model_exception()


    def crown(self, tree: Tree, plot: Plot, func):
        """
        Crown variables (tree).
        Function to calculate crown variables for each tree.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced

            #if func == 'initialize':  # if that function is called from initialize, first we must check if those variables are available on the initial inventory
            None
        except Exception:
            self.catch_model_exception()


    def canopy(self, plot: Plot, plot_trees):
        """
        Crown variables (plot).
        Function to calculate plot crown variables by using tree information.
        That function is run by initialize and update_model functions.
        """

        try:  # errors inside that construction will be announced
            None
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


    def biomass(self, tree: Tree):
        """
        Biomass variables (tree).
        Function to calculate biomass variables for each tree.
        That function is run by initialize and update_model functions.
        Source: 
            Doc.: Diéguez-Aranda U, Rojo A, Castedo-Dorado F, et al (2009). Herramientas selvícolas para la gestión forestal sostenible en Galicia. Forestry, 82, 1-16
            Ref.: Diéguez-Aranda et al. 2009
            Doc.: Ruiz-Peinado R, del Rio M, Montero G (2011). New models for estimating the carbon sink capacity of Spanish softwood species. Forest Systems, 20(1), 176-188
            Ref.: Ruiz-Peinado et al, 2011
            Doc.: Ruiz-Peinado R, Montero G, Del Rio M (2012). Biomass models to estimate carbon stocks for hardwood tree species. Forest systems, 21(1), 42-52
            Ref.: Ruiz-Peinado et al, 2012
        """

        try:  # errors inside that construction will be announced

            wsw = wsb = wswb = w_cork = wthickb = wstb = wb2_7 = wb2_t = wthinb = wb05 = ''
            wb05_7 = wb0_2 = wdb = wdb = wl = wtbl = wbl0_7 = wr = wt = ''


            #######################################################################################################


            if tree.specie == 21:  # Pinus sylvestris

                # España
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
                # Ruiz-Peinado et al, 2011

                # Galicia
                #wswb = 0.02321*(tree.dbh**2.708)
                #wthickb = 3.7e-7*(tree.dbh**4.804)
                #wb2_7 = 0.02036*(tree.dbh**2.141)
                #wb0_2 = 0.1432*(tree.dbh**1.510)
                #wl = 0.1081*(tree.dbh**1.510)
                #wr = 0.01089*(tree.dbh**2.628)
                #wt = wstb + wthickb + wb2_7 + wb0_2 + wl + wr
                # Diéguez-Aranda et al. 2009

            elif tree.specie == 22:  # Pinus uncinata

                wsw = 0.0203*(tree.dbh**2)*tree.height
                wb2_t = 0.0379*(tree.dbh**2)
                wtbl = 2.740*tree.dbh - 2.641*tree.height
                wr = 0.193*(tree.dbh**2)
                wt = wsw + wb2_t + wtbl + wr
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 23:  # Pinus pinea
            
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
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 24:  # Pinus halepensis

                wsw = 0.0139 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 27.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (3.926 * (tree.dbh - 27.5)) * Z
                wb2_7 = 4.257 + 0.00506 * (tree.dbh ** 2) * tree.height - 0.0722 * tree.dbh * tree.height
                wtbl = 6.197 + 0.00932 * (tree.dbh ** 2) * tree.height - 0.0686 * tree.dbh * tree.height
                wr = 0.0785 * (tree.dbh ** 2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 25:  # Pinus nigra

                wsw = 0.0403 * (tree.dbh**1.838) * (tree.height**0.945)  # Stem wood (kg)
                if tree.dbh <= 32.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.228 * ((tree.dbh - 32.5)**2)) * Z  # wthickb = branches > 7 cm biomass (kg)
                wb2_7 = 0.0521*(tree.dbh**2)  # wb2_7 = branches (2-7 cm) biomass (kg)
                wtbl = 0.0720*(tree.dbh**2)  # Thin branches + Leaves (<2 cm) biomass (kg)
                wr = 0.0189*(tree.dbh**2.445)  # Roots biomass (kg)
                wt = wsw + wb2_7 + wthickb + wtbl + wr  # Total biomass (kg)
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 26:  # Pinus pinaster
                
                # España
                wsw = 0.0278 * (tree.dbh ** 2.115) * (tree.height ** 0.618)
                wb2_t = 0.000381 * (tree.dbh ** 3.141)
                wtbl = 0.0129 * (tree.dbh ** 2.320)
                wr = 0.00444 * (tree.dbh ** 2.804)
                wt = wsw + wb2_t + wtbl + wr
                # Ruiz-Peinado et al, 2011

                # Galicia
                #wstb = 0.3882 + 0.01149*(tree.dbh**2)*tree.height
                #wsb = 0.0079*(tree.dbh**2.098)*(tree.height**0.466)
                #wb2_7 = 3.202 - 0.01484*(tree.dbh**2) - 0.4228*tree.height + 0.00279*(tree.dbh**2)*tree.height
                #wthinb = 0.09781*(tree.dbh**2.288)*(tree.height**(-0.9648))
                #wb05 = 0.00188*(tree.dbh**2.154)
                #wl = 0.005*(tree.dbh**2.383)
                #wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl
                # Diéguez-Aranda et al. 2009

            elif tree.specie == 27:  # Pinus canariensis

                wsw = 0.0249*((tree.dbh**2)*tree.height)**0.975
                if tree.dbh <= 32.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.634*((tree.dbh - 32.5)**2))*Z
                wb2_7 = 0.00162*(tree.dbh**2)*tree.height
                wtbl = 0.0844*(tree.dbh**2) - 0.0731*(tree.height**2)
                wr = 0.155*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 28:  # Pinus radiata

                # España
                wstb = 0.01230*(tree.dbh**1.604)*(tree.height**1.413)
                wsb = 0.003600*(tree.dbh**2.656)
                wb2_7 = 1.938 + 0.001065*(tree.dbh**2)*tree.height
                wthinb = 0.03630*(tree.dbh**2.609)*(tree.height**(-0.9417)) 
                wb05 = 0.007800*(tree.dbh**1.961)
                wl = 0.04230*(tree.dbh**1.714)
                wr = 0.06174*(tree.dbh**2.144)
                wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl + wr

                # Galicia
                #wstb = 0.01230*(tree.dbh**1.604)*(tree.height**1.413)
                #wsb = 0.003600*(tree.dbh**2.656)
                #wb2_7 = 1.938 + 0.001065*(tree.dbh**2)*tree.height
                #wthinb = 0.03630*(tree.dbh**2.609)*(tree.height**(-0.9417)) 
                #wb05 = 0.007800*(tree.dbh**1.961)
                #wl = 0.04230*(tree.dbh**1.714)
                #wr = 0.06174*(tree.dbh**2.144)
                #wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl + wr
                # Diéguez-Aranda et al. 2009

            elif tree.specie == 31:  # Abies alba

                wsw = 0.0189*(tree.dbh**2)*tree.height
                wb2_t = 0.0584*(tree.dbh**2)
                wtbl = 0.0371*(tree.dbh**2) + 0.968*tree.height
                wr = 0.101*(tree.dbh**2)
                wt = wsw + wb2_t + wtbl + wr
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 32:  # Abies pinsapo

                wsw = 0.00960*(tree.dbh**2)*tree.height
                if tree.dbh <= 32.5:
                    Z=0
                else:
                    Z=1
                wthickb = ((1.637*((tree.dbh - 32.5)**2) - 0.0719*(tree.dbh - 32.5)**2)*tree.height)*Z
                w2_7 = 0.00344*(tree.dbh**2)*tree.height
                wtbl = 0.131*tree.dbh*tree.height
                wt = wsw + w2_7 + wthickb + wtbl
                # Ruiz-Peinado et al, 2011

            # elif tree.specie == 34:  # Pseudotsuga menziesii


            elif tree.specie == 38:  # Juniperus thurifera

                wsw = 0.32*(tree.dbh**2)*tree.height + 0.217*tree.dbh*tree.height
                if tree.dbh <= 22.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.107*((tree.dbh - 22.5)**2))*Z
                wb2_7 = 0.00792*(tree.dbh**2)*tree.height
                wtbl = 0.273*tree.dbh*tree.height
                wr = 0.0767*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 41:  # Quercus robur

                # Galicia
                #wsw = -5.714 + 0.01823*(tree.dbh**2)*tree.height
                #wsb = -1.5 + 0.03154*(tree.dbh**2) + 0.00111*(tree.dbh**2)*tree.height
                #wthickb = 3.427e-9*((tree.dbh**2)*tree.height)**2.310
                #wb2_7 = 4.268 + 0.003410*(tree.dbh**2)*tree.height
                #wthinb = 0.03851*(tree.dbh**1.784) 
                #wb05 = 1.379 + 0.00024*(tree.dbh**2)*tree.height
                #wl = 0.01985*((tree.dbh**2)*tree.height)**0.7375
                #wr = 0.01160*((tree.dbh**2)*tree.height)**0.9625
                #wt = wsw + wsb + wthickb + wb2_7 + wthinb + wb05 + wl + wr
                # Diéguez-Aranda et al. 2009

                # España
                wsw = -5.714 + 0.01823*(tree.dbh**2) * tree.height
                wsb = -1.500 + 0.03154*(tree.dbh**2) + 0.001110 * (tree.dbh**2) * tree.height
                wthickb = 3.427e-9*(((tree.dbh**2) * tree.height) ** 2.310)
                wb2_7 = 4.268 + 0.003410*(tree.dbh**2) * tree.height
                wthinb = 0.03851*(tree.dbh**1.784) + 1.379 
                wb05 = 0.00024*(tree.dbh**2) * tree.height
                wl = 0.01985*(((tree.dbh**2) * tree.height) ** 0.7375)
                wr = 0.01160*((tree.dbh**2)*tree.height) ** 0.9625
                wt = wsw + wsb + wb2_7 + wthickb + wthinb + wb05 + wl + wr


            elif tree.specie == 42:  # Quercus petraea

                wstb = 0.001333*(tree.dbh**2)*tree.height
                wb2_7 = 0.006531*(tree.dbh**2)*tree.height - 0.07298*tree.dbh*tree.height
                wthinb = 0.023772*(tree.dbh**2)*tree.height
                wt = wstb + wb2_7 + wthinb


            elif tree.specie == 43:  # Quercus pyrenaica

                wstb = 0.0261 * (tree.dbh ** 2) * tree.height
                wb2_7 = - 0.0260 * (tree.dbh ** 2) + 0.536 * tree.height + 0.00538 * (tree.dbh ** 2) * tree.height
                wthinb = 0.898 * tree.dbh - 0.445 * tree.height
                wr = 0.143 * (tree.dbh ** 2)
                wt = wstb + wb2_7 + wthinb + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 44:  # Quercus faginea

                wsw = 0.154*(tree.dbh**2)
                wthickb = 0.0861*(tree.dbh**2)
                wb2_7 = 0.127*(tree.dbh**2) - 0.00598*(tree.dbh**2)*tree.height
                wtbl = 0.0726*(tree.dbh**2) - 0.00275*(tree.dbh**2)*tree.height
                wr = 0.169*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 45:  # Quercus ilex

                wsw = 0.143*(tree.dbh**2)
                if tree.dbh <= 12.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.0684*((tree.dbh - 12.5)**2)*tree.height)*Z
                wb2_7 = 0.0898*(tree.dbh**2)
                wtbl = 0.0824*(tree.dbh**2)
                wr = 0.254*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 46:  # Quercus suber

                wsw = 0.00525*(tree.dbh**2)*tree.height + 0.278*tree.dbh*tree.height
                wthickb = 0.0135*(tree.dbh**2)*tree.height
                wb2_7 = 0.127*tree.dbh*tree.height
                wtbl = 0.0463*tree.dbh*tree.height
                wr = 0.0829*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2012

                if 'h_debark' in TREE_VARS and 'dbh_oc' in TREE_VARS and 'nb' in TREE_VARS:
                    
                    if isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float) and isinstance(tree.nb, float):

                        pbhoc = (tree.dbh_oc*math.pi) / 100  # perimeter at breast height outside cork (m)
                        pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
                        shs = tree.h_debark  # stripped height in the stem (m)
                        nb = tree.nb + 1  # number of stripped main bough + 1

                        if tree.cork_cycle == 0:  # To use inmediately before the stripping process
                            if nb == 1 and shs != 0:
                                tree.add_value('w_cork', math.exp(2.3665 + 2.2722*math.log(pbhoc) + 0.4473*math.log(shs)))
                            elif nb != 1 and shs != 0:
                                tree.add_value('w_cork', math.exp(2.1578 + 1.5817*math.log(pbhoc) + 0.5062*math.log(nb) + 0.6680*math.log(shs)))
                            else:    
                                tree.add_value('w_cork', 0)

                        elif tree.cork_cycle == 1:  # To use after the stripping process or in a intermediate age of the cork cycle production
                            if nb == 1 and shs != 0:
                                tree.add_value('w_cork', math.exp(2.7506 + 1.9174*math.log(pbhic) + 0.4682*math.log(shs)))
                            elif nb != 1 and shs != 0:
                                tree.add_value('w_cork', math.exp(2.2137 + 0.9588*math.log(shs) + 0.6546*math.log(nb)))
                            else:    
                                tree.add_value('w_cork', 0)
                        else:    
                            tree.add_value('w_cork', 0)

                    elif isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float) and not isinstance(tree.nb, float):

                        pbhoc = (tree.dbh_oc*math.pi) / 100  # perimeter at breast height outside cork (m)
                        pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
                        shs = tree.h_debark  # stripped height in the stem (m)
                        nb = 1  # number of stripped main bough + 1

                        if tree.cork_cycle == 0 and shs != 0:  # To use inmediately before the stripping process
                            tree.add_value('w_cork', math.exp(2.3665 + 2.2722*math.log(pbhoc) + 0.4473*math.log(shs)))
                        elif tree.cork_cycle == 1 and shs != 0:  # To use after the stripping process or in a intermediate age of the cork cycle production
                            tree.add_value('w_cork', math.exp(2.7506 + 1.9174*math.log(pbhic) + 0.4682*math.log(shs)))
                        else:    
                            tree.add_value('w_cork', 0)

                    else:
                        
                        tree.add_value('w_cork', 0)

            elif tree.specie == 47:  # Quercus canariensis

                wsw = 0.0126*(tree.dbh**2)*tree.height
                wthickb = 0.103*(tree.dbh**2)
                wbl0_7 = 0.167*tree.dbh*tree.height
                wr = 0.135*(tree.dbh**2)
                wt = wsw + wbl0_7 + wthickb + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 54:  # Alnus glutinosa

                wsw = 0.0191*(tree.dbh**2)*tree.height
                wb2_t = 0.0512*(tree.dbh**2)
                wtbl = 0.0567*tree.dbh*tree.height
                wr = 0.214*(tree.dbh**2)
                wt = wsw + wb2_t + wtbl + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 55:  # Fraxinus angustifolia

                wsw = 0.0296*(tree.dbh**2)*tree.height
                if tree.dbh <= 12.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.231*((tree.dbh - 12.5)**2))*Z
                wb2_7 = 0.0925*(tree.dbh**2)
                wthinb = 2.005*tree.dbh
                wr = 0.359*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wthinb + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 61:  # Eucalyptus globulus

                # Galicia
                wstb = 0.01308*(tree.dbh**1.870)*(tree.height**1.172)
                wsb = 0.01010*(tree.dbh**2.484)
                wb05_7 = 0.003685*(tree.dbh**2.654)
                wb05 = 0.01258*(tree.dbh**1.705)
                wl = 0.02949*(tree.dbh**1.917)
                wt = wstb + wsb + wb05_7 + wb05 + wl
                # Diéguez-Aranda et al. 2009

                # España
                #wstb = 0.0221*(tree.dbh**2)*tree.height
                #wb2_7 = 0.154*(tree.dbh**1.668)
                #wtbl = 0.180*(((tree.dbh**2)*tree.height)**0.587)
                #wt = wstb + wb2_7 + wtbl 
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 64:  # Eucalyptus nittens

                # Sin ecuaciones de copa
                wstb = 0.0094*(tree.dbh**2.033)*(tree.height**1.056)
                wsb = 0.01342*(tree.dbh**2.361)
                wb2_7 = 0.000059*(tree.dbh**3.760)
                wthinb = 0.01280*(tree.dbh**1.858)
                wb05 = 0.000922*(tree.dbh**2.632)
                wl = 0.0053*(tree.dbh**2.393)
                wdb = 0.1451*(tree.dbh**1.403)
                wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl + wdb
                # Diéguez-Aranda et al. 2009
                
                # Con ecuaciones de copa
                #wstb = 0.1495*(tree.dbh**2.052)*(tree.height**0.8946)
                #wsb = 0.03190*(tree.dbh**2.108)
                #wb2_7 = 0.000822*(tree.dbh**2.644)*(tree.lcw**0.7627)
                #wthinb = 0.03005*(tree.dbh**1.590)
                #wb05 = 0.006230*(tree.dbh**1.949)*(tree.lcw**0.2189)
                #wl = 0.0168*(tree.dbh**1.516)*((tree.height - tree.hcb)**0.7747)
                #wdb = 0.007933*(tree.dbh**1.279)*(tree.hbc**1.254)
                #wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl + wdb
                # Diéguez-Aranda et al. 2009

            elif tree.specie == 66:  # Olea europaea

                wsw = 0.0114*(tree.dbh**2)*tree.height
                wthickb = 0.0108*(tree.dbh**2)*tree.height
                wb2_7 = 1.672*tree.dbh
                wtbl = 0.0354*(tree.dbh**2) + 1.187*tree.height
                wr = 0.147*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 67:  # Ceratonia siliqua

                wsw = 0.142*(tree.dbh**1.974)
                wthickb = 0.104*(tree.dbh**2)
                wb2_7 = 0.0538*(tree.dbh**2)
                wtbl = 0.151*(tree.dbh**2) - 0.00740*(tree.dbh**2)*tree.height
                wr = 0.335*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 71:  # Fagus sylvatica

                wsw = 0.0676 * (tree.dbh ** 2) + 0.0182 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 22.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.830*((tree.dbh - 22.5)**2) - 0.0248*((tree.dbh - 22.5)**2)*tree.height) * Z
                wb2_7 = 0.0792*(tree.dbh**2)
                wthinb = 0.0930*(tree.dbh**2) - 0.00226*(tree.dbh**2) * tree.height
                wr = 0.106*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wthinb + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 72:  # Castanea sativa

                wsw = 0.0142*(tree.dbh**2)*tree.height
                if tree.dbh <= 12.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.223*((tree.dbh - 12.5)**2))*Z
                wb2_7 = 0.230*tree.dbh*tree.height
                wthinb = 0.221*tree.dbh*tree.height
                wr = 0.0211*(tree.dbh**2.804)
                wt = wsw + wb2_7 + wthickb + wthinb + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 258:  # Populus x canadensis/euroamericana

                wsw = 0.0130*(tree.dbh**2)*tree.height
                if tree.dbh <= 22.5:
                    Z=0
                else:
                    Z=1
                wthickb = (0.538*((tree.dbh - 22.5)**2) - 0.0130*((tree.dbh - 22.5)**2)*tree.height)*Z
                wb2_7 = 0.385*(tree.dbh**2)
                wtbl = 0.0774*(tree.dbh**2) - 0.00198*(tree.dbh**2)*tree.height
                wr = 0.122*(tree.dbh**2)
                wt = wsw + wb2_7 + wthickb + wtbl + wr
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 273:  # Betula alba

                wsw = 0.1485*(tree.dbh**2.223)
                wsb = 0.03010*(tree.dbh**2.186)
                wthickb = 1.515*math.exp(0.09040*tree.dbh)
                wb2_7 = 0.1374*(tree.dbh**1.760)
                wthinb = 0.05*(tree.dbh**1.618)
                wb05 = 0.03720*(tree.dbh**1.581)
                wl = 0.03460*(tree.dbh**1.645)
                wr = 1.042*(tree.dbh**1.254)
                wt = wsw + wsb + wthickb + wb2_7 + wthinb + wb05 + wl + wr
                # Diéguez-Aranda et al. 2009

            #######################################################################################################


            tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
            tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
            tree.add_value('wswb', wswb)   # wswb = stem wood and stem bark (Tn/ha)  
            tree.add_value('w_cork', w_cork)   # fresh cork biomass (kg)
            tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
            tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
            tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
            tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
            tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
            tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
            tree.add_value('wb05_7', wb05_7)  # wb05 = thinnest branches (< 0.5 cm) (kg)
            tree.add_value('wb0_2', wb0_2)  # wb05 = thinnest branches (< 0.5 cm) (kg)                        
            tree.add_value('wdb', wdb)  # wb05 = thinnest branches (< 0.5 cm) (kg)            
            tree.add_value('wl', wl)  # wl = leaves (kg)
            tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
            tree.add_value('wbl0_7', wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
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
            
            plot_wsw = plot_wsb = plot_wswb = plot_w_cork = plot_wthickb = plot_wstb = plot_wb2_7 = plot_wb2_t = plot_wthinb = plot_wb05 = plot_wb05_7 = plot_wb0_2 = plot_wdb = plot_wl = plot_wtbl = plot_wbl0_7 = plot_wr = plot_wt = 0
            wsw = wsb = wswb = w_cork = wthickb = wstb = wb2_7 = wb2_t = wthinb = wb05 = wb05_7 = wb0_2 = wdb = wl = wtbl = wbl0_7 = wr = wt = True  # variable to decide if plot biomass can be calculated


            #######################################################################################################


            for tree in plot_trees:  # for each tree, we are going to add the simple values to the plot value

                if tree.wsw == '':
                    wsw = False
                else:   
                    plot_wsw += tree.wsw*tree.expan/1000
                
                if tree.wsb == '':
                    wsb = False
                else:   
                    plot_wsb += tree.wsb*tree.expan/1000

                if tree.wswb == '':
                    wswb = False
                else:
                    plot_wswb += tree.wswb*tree.expan/1000

                if tree.w_cork == '':
                    w_cork = False
                else:
                    plot_w_cork += tree.w_cork*tree.expan/1000

                if tree.wthickb == '':
                    wthickb = False
                else:                
                    plot_wthickb += tree.wthickb*tree.expan/1000
                
                if tree.wstb == '':
                    wstb = False
                else:
                    plot_wstb += tree.wstb*tree.expan/1000
                
                if tree.wb2_7 == '':
                    wb2_7 = False
                else:                
                    plot_wb2_7 += tree.wb2_7*tree.expan/1000
                
                if tree.wb2_t == '':
                    wb2_t = False
                else:
                    plot_wb2_t += tree.wb2_t*tree.expan/1000
                
                if tree.wthinb == '':
                    wthinb = False
                else:
                    plot_wthinb += tree.wthinb*tree.expan/1000

                if tree.wb05 == '':
                    wb05 = False
                else:
                    plot_wb05 += tree.wb05*tree.expan/1000
                
                if tree.wb05_7 == '':
                    wb05_7 = False
                else:
                    plot_wb05_7 += tree.wb05_7*tree.expan/1000

                if tree.wb0_2 == '':
                    wb0_2 = False
                else:
                    plot_wb0_2 += tree.wb0_2*tree.expan/1000

                if tree.wdb == '':
                    wdb = False
                else:
                    plot_wdb += tree.wdb*tree.expan/1000

                if tree.wl == '':
                    wl = False
                else:
                    plot_wl += tree.wl*tree.expan/1000

                if tree.wtbl == '':
                    wtbl = False
                else:
                    plot_wtbl += tree.wtbl*tree.expan/1000
                
                if tree.wbl0_7 == '':
                    wbl0_7 = False
                else:
                    plot_wbl0_7 += tree.wbl0_7*tree.expan/1000

                if tree.wr == '':
                    wr = False
                else:
                    plot_wr += tree.wr*tree.expan/1000

                if tree.wt == '':
                    wt = False
                else:
                    plot_wt += tree.wt*tree.expan/1000
            

            #######################################################################################################


            if wsw == True:
                plot.add_value('WSW', plot_wsw)  # wsw = stem wood (Tn/ha)
            if wsb == True:
                plot.add_value('WSB', plot_wsb)  # wsb = stem bark (Tn/ha)
            if wswb == True:                
                plot.add_value('WSWB', plot_wswb)  # wswb = stem wood and stem bark (Tn/ha)          
            if w_cork == True:
                plot.add_value('W_CORK', plot_w_cork)  # fresh cork biomass (Tn/ha)
            if wthickb == True:                
                plot.add_value('WTHICKB', plot_wthickb)  # wthickb = Thick branches > 7 cm (Tn/ha)
            if wstb == True:              
                plot.add_value('WSTB', plot_wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
            if wb2_7 == True:                
                plot.add_value('WB2_7', plot_wb2_7)  # wb2_7 = branches (2-7 cm) (Tn/ha)
            if wb2_t == True:                
                plot.add_value('WB2_T', plot_wb2_t)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
            if wthinb == True:                
                plot.add_value('WTHINB', plot_wthinb)  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
            if wb05 == True:               
                plot.add_value('WB05', plot_wb05)  # wb05 = thinnest branches (< 0.5 cm) (Tn/ha)
            if wb05_7 == True:                
                plot.add_value('WB05_7', plot_wb05_7)  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
            if wb0_2 == True:                
                plot.add_value('WB0_2', plot_wb0_2)  # wb0_2 = branches < 2 cm (Tn/ha)
            if wdb == True:                
                plot.add_value('WDB', plot_wdb)  # wdb = dead branches biomass (Tn/ha)
            if wl == True:                
                plot.add_value('WL', plot_wl)  # wl = leaves (Tn/ha)
            if wtbl == True:                
                plot.add_value('WTBL', plot_wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
            if wbl0_7 == True:                
                plot.add_value('WBL0_7', plot_wbl0_7)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
            if wr == True:             
                plot.add_value('WR', plot_wr)  # wr = roots (Tn/ha)
            if wt == True:                
                plot.add_value('WT', plot_wt)  # wt = total biomass (Tn/ha)

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
            #"WSB",  # wsb = stem bark (Tn/ha)
            #"WSWB",  # wswb = stem wood and stem bark (Tn/ha)
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
            "hegyi",  # Hegyi competition index calculation

            # Quercus suber special variables
            #"dbh_oc",  # dbh over cork (cm) - Quercus suber
            #"h_debark",  # uncork height on the main stem (m) - Quercus suber
            #"nb",  # number of the main boughs stripped - Quercus suber
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
        
Existencias.vars()

