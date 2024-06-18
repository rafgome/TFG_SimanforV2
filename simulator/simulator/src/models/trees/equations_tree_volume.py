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

import math
import sys
import logging
import numpy as np
import os


class TreeVolume(TreeModel):

    def __init__(self, configuration=None):
        super().__init__(name="TreeVolume", version=1)


    def catch_model_exception(self):  # that Function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)

    def ifn3_vol_eqs(self):
        """
        Function that returns the volume equations for each species

        #complete
        """

        # try:
        #
        #     # TODO: ajustar estructura y comprobar Dn, Ht, Dnm, CD, CDm
        # https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/temas/inventarios-nacionales/documentador_sig_tcm30-536622.pdf
        #
        #     VCC_1 = a + b * (tree.dbh ** 2) * tree.height
        #     VCC_11 = p * tree.dbh * (tree.height ** 2)
        #     VSC_7 = a + b * tree.vol + c * tree.vol ** 2
        #     VLE_10 = a + b * tree.vol + c * tree.vol ** 2
        #     VLE_12 = p * (tree.dbh ** q
        #     IAVC_8 = a + b * tree.vol + c * tree.vol ** 2
        #     IAVC_13 = a + b * (tree.dbh - plot.dbh_mean)
        #     IAVC_14 = p * (tree.dbh ** q)
        #     IAVC_15 = a + b * (CD - CDm)
        #     IAVC_16 = a + b * (tree.dbh ** 2)
        #     IAVC_17 = a + b * tree.dbh + c * (tree.dbh ** 2)
        #     IAVC_18 = p * math.exp(q * tree.dbh)
        #     IAVC_19 = a + b * tree.dbh + c * (tree.dbh ** 2) + d * (tree.dbh ** 3)
        #     IAVC_20 = a + b * tree.dbh + c * (tree.dbh ** 3)
        #     IAVC_21 = c * (tree.dbh ** 2) + d * (tree.dbh ** 3)
        #     IAVC_25 = p * tree.dbh * q * tree.height * r
        #
        # except Exception:
        #     TreeVolume.catch_model_exception()


    def set_tree_vol(tree):
        """
        Volume variables (tree).
        Function to calculate volume variables for each tree according to the species.
        It sets the volume over bark (m3), volume under bark (m3), bark volume (m3) and volume over bark per hectare (m3/ha).
        It uses Fang model for diameter over bark and diameter under bark, or other equations if Fang model is not available.
        Args:
            tree: Tree object
        Sources:
            Doc.: Badía M, Rodríguez F, Broto M (2001). Modelos del perfil del árbol. Aplicación al pino radiata (Pinus radiata D. Don). In Congresos Forestales
            Ref.: Badía et al, 2001
            Doc.: Calama R, Montero G (2006). Stand and tree-level variability on stem form and tree volume in Pinus pinea L.: a multilevel random components approach. Forest Systems, 15(1), 24-41
            Ref.: Calama and Montero, 2006
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp
            Ref.: Lizarralde 2008
            Doc.: López-Sánchez C A (2009). Estado selvícola y modelos de crecimiento y gestión de plantaciones de Pseudotsuga menziesii (Mirb.) Franco en España (Doctoral dissertation, Doctoral thesis. Universidad de Santiago de Compostela, Lugo.
            Ref.: López-Sánchez, 2009
            Doc.: Manrique-González, J., Bravo, F., del Peso, C., Herrero, C., Rodríguez, F., 2017. Ecuaciones de perfil para las especies de roble albar (Quercus petraea (Matt.) Liebl.) y rebollo (Quercus pyrenaica Willd) en la comarca de la “Castillería” en el Norte de la provincia de Palencia. 7º Congreso Forestal Español (póster).  http://7cfe.congresoforestal.es/sites/default/files/comunicaciones/776.pdf
            Ref.: Manrique-González et al., 2017
        """

        try:  # errors inside that construction will be announced

            # declare variables
            Fang_values_dob = Fang_values_dub = False  # Fang values for dob and dub
            hr = np.arange(0, 1, 0.001)  # that line establish the integrated conditions for volume calculation
            dob = dub = ''  # diameter over bark (cm) and diameter under bark (cm)

            if int(tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):  # Pinus sylvestris

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

                dub = (1 + 0.3485 * 2.7182818284 ** (-23.9191 * hr)) * 0.7966 * tree.dbh * pow((1 - hr), (
                        0.6094 - 0.7086 * (1 - hr)))
                # Lizarralde, 2008

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ppinea'):  # Pinus pinea

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

                beta1 = 1.0972
                beta2 = -2.8505
                H = tree.height * 10  # dm
                dubmm = tree.dbh * 10 * ((H - hr * H) / (H - 13)) + beta1 * (
                        ((H ** 1.5 - (hr * H) ** 1.5) * (hr * H - 13)) / H ** 1.5) + beta2 * (
                                ((H - (hr * H)) ** 4) * (hr * H - 13) / (H ** 4))
                dub = dubmm * 0.1  # mm to cm
                # Calama and Montero, 2006

            elif int(tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):  # Pinus halepensis

                a1 = 0.4893
                a2 = 1.9362
                a3 = 0.0559
                # rwb = radius with bark (cm)
                A = (a1 * tree.dbh) / (1 - 2.7182818284 ** (a3 * (1.3 - tree.height)))
                B = (tree.dbh / 2 - a1 * tree.dbh) * (1 - (1 / (1 - 2.7182818284 ** (a2 * (1.3 - tree.height)))))
                C = 2.7182818284 ** (-a2 * hr * tree.height) * (
                            ((tree.dbh / 2 - a1 * tree.dbh) * 2.7182818284 ** (1.3 * a2)) / (
                                1 - 2.7182818284 ** (a2 * (1.3 - tree.height))))
                D = 2.7182818284 ** (a3 * hr * tree.height) * ((a1 * tree.dbh * 2.7182818284 ** (-a3 * tree.height)) / (
                            1 - 2.7182818284 ** (a3 * (1.3 - tree.height))))
                rwb = A + B + C - D
                dob = rwb * 2
                # Saldaña, 2010

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pnigra'):  # Pinus nigra

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):  # Pinus pinaster

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

                dub = (1 + 2.4771 * 2.7182818284 ** (-5.0779 * hr)) * 0.2360 * tree.dbh * pow((1 - hr), (
                        0.4733 - 3.0371 * (1 - hr)))
                # Lizarralde, 2008

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pradiata'):  # Pinus radiata

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

                # a1 = 0.6665
                # a11 = 0.002472
                # a2 = -0.7668
                # a3 = 0.18857
                # a4 = 11.4727
                # a5 = 0.90117

                # h = tree.height*100  # height in cm
                # z = hr*tree.height*100  # relative height in cm

                # dub = a5*tree.dbh*((1 - z/h)**(a1 + a11*h/tree.dbh + a2*(1 - z/h))) * (1 + a3*(2.7182818284**(-a4*z/h)))
                # predictions are higher than vob
                # Badía et al, 2001

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pmenziesii'):  # Pseudotsuga menziesii

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

                Fang_values_dub = TreeVolume.get_Fang_values_dub(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Jthurifera'):  # Juniperus thurifera

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qrobur'):  # Quercus robur

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qpetraea'):  # Quercus petraea

                dob = (1 + 0.558513 * 2.7182818284 ** (-25.933370 * hr / tree.height)) * (0.942294 * tree.dbh * (
                            (1 - hr / tree.height) ** (1.312840 - 0.342491 * (tree.height / tree.dbh) - 1.239930 *
                                                       (1 - hr / tree.height))))
                # Manríquez-González et al., 2017

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):  # Quercus pyrenaica

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

                # dob = (1 + 0.558513 * 2.7182818284 ** (-25.933370 * hr / tree.height)) * (0.942294 * tree.dbh * (
                #             (1 - hr / tree.height) ** (1.312840 - 0.342491 * (tree.height / tree.dbh) - 1.239930 *
                #                                        (1 - hr / tree.height))))
                # Manríquez-González et al., 2017

            elif int(tree.specie) == TreeEquations.get_ifn_id('Eglobulus'):  # Eucalyptus globulus

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Enittens'):  # Eucalyptus nittens

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):  # Fagus sylvatica

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Csativa'):  # Castanea sativa

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('PPxcanadensis'):  # Populus x canadensis/euroamericana

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            elif int(tree.specie) == TreeEquations.get_ifn_id('Balba'):  # Betula alba

                Fang_values_dob = TreeVolume.get_Fang_values_dob(tree)

            else:  # no volume equation available

                Fang_values_dob = Fang_values_dub = False


            # calculate volume over bark
            if Fang_values_dob != False:  # Fang model for diameter over bark

                dob = TreeVolume.Fang_taper(tree, hr, Fang_values_dob)

            if type(dob) == np.ndarray:  # dob must be a list of values

                fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
                tree.add_value('vol', math.pi * tree.height *
                               10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
                tree.add_value('vol_ha', tree.vol * tree.expan / 10000)  # volume over bark (m3/ha)

            else:  # if it is int, then not equations are available

                tree.add_value('vol', '')
                tree.add_value('vol_ha', '')  # volume over bark (m3/ha)


            # calculate volume under bark
            if Fang_values_dub != False:  # Fang model for diameter under bark

                dub = TreeVolume.Fang_taper(tree, hr, Fang_values_dub)

            if type(dub) == np.ndarray:  # dub must exist as a list of values

                fwb = (dub / 20) ** 2  # radius^2 using dob (dm2)
                tree.add_value('bole_vol', math.pi * tree.height *
                               10 * integrate.simps(fwb, hr))  # volume under bark using simpson integration (dm3)

                if tree.vol != '':
                    tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)

            else:  # if it is int, then not equations are available

                tree.add_value('bole_vol', '')  # volume under bark using simpson integration (dm3)
                tree.add_value('bark_vol', '')  # bark volume (dm3)


        except Exception:
            TreeVolume.catch_model_exception()


    def set_plot_vol(plot, list_of_trees):
        """
        Volume variables (plot).
        Function to calculate plot volume variables by using tree information.
        It sets the plot volume over bark (m3/ha), plot volume under bark (m3/ha) and plot bark volume (m3/ha).
        Args:
            plot: Plot object
            list_of_trees: list of Tree objects
        """

        try:  # errors inside that construction will be announced

            # by default values
            plot.add_value('VOL', 0)  # plot volume over bark (m3/ha)
            plot.add_value('BOLE_VOL', 0)  # plot volume under bark (m3/ha)
            plot.add_value('BARK_VOL', 0)  # plot bark volume (m3/ha)

            # for each tree in plot
            for tree in list_of_trees:

                if tree.vol != '':

                    plot.sum_value('VOL', tree.vol * tree.expan / 1000)  # plot volume over bark (m3/ha)

                if tree.bole_vol != '':

                    plot.sum_value('BOLE_VOL', tree.bole_vol * tree.expan / 1000)  # plot volume under bark (m3/ha)
                    plot.sum_value('BARK_VOL', tree.bark_vol * tree.expan / 1000)  # plot bark volume (m3/ha)

            if plot.vol == 0:  # if there is no volume, then value is empty
                plot.add_value('VOL', '')  # plot volume over bark (m3/ha)

            if plot.bole_vol == 0:  # if there is no volume, then value is empty
                plot.add_value('BOLE_VOL', '')  # plot volume under bark (m3/ha)

            if plot.bark_vol == 0:  # if there is no volume, then value is empty
                plot.add_value('BARK_VOL', '')  # plot bark volume (m3/ha)

        except Exception:
            TreeVolume.catch_model_exception()


    def set_plot_vol_sp(plot, list_of_trees):
        """
        Function to calculate plot volume by species.
        It sets volume over bark, volume under bark and volume of bark for species 1, 2 and others (3).
        Args:
            plot: Plot object
            list_of_trees: list of Tree objects
        """

        try:  # errors inside that construction will be announced

            # define attributes and plot attributes
            tree_attributes = ['vol', 'bole_vol', 'bark_vol']

            attributes_sp1 = ['VOL_SP1', 'BOLE_VOL_SP1', 'BARK_VOL_SP1']
            attributes_sp2 = ['VOL_SP2', 'BOLE_VOL_SP2', 'BARK_VOL_SP2']
            attributes_sp3 = ['VOL_SP3', 'BOLE_VOL_SP3', 'BARK_VOL_SP3']

            # define plot attributes
            plot_attributes_sp1 = [0, 0, 0]
            plot_attributes_sp2 = [0, 0, 0]
            plot_attributes_sp3 = [0, 0, 0]


            # for each tree, we are going to add the individual values to the plot value
            for tree in list_of_trees:

                # distinguish between species
                if tree.specie == plot.id_sp1:
                    plot_attributes = plot_attributes_sp1
                elif tree.specie == plot.id_sp2:
                    plot_attributes = plot_attributes_sp2
                else:
                    plot_attributes = plot_attributes_sp3

                # iterate over the list of attributes and plot attributes
                for attr, plot_attr, n in zip(tree_attributes, plot_attributes, range(len(plot_attributes))):
                    if attr in TREE_VARS:  # if the attribute is in the list of variables, add it to the plot object
                        value = getattr(tree, attr, '')
                        if value != '':  # if the value is not empty, add it to the plot attribute
                            plot_attr += value * tree.expan / 1000
                            plot_attributes[n] = plot_attr  # update the plot attribute
                        else:
                            plot_attributes[n] = plot_attr  # previous value is maintained

                # rewrite plot attributes
                # distinguish between species
                if tree.specie == plot.id_sp1:
                    plot_attributes_sp1 = plot_attributes
                elif tree.specie == plot.id_sp2:
                    plot_attributes_sp2 = plot_attributes
                else:
                    plot_attributes_sp3 = plot_attributes


            # define features and values as tuples
            features_and_values_sp1 = list(zip(attributes_sp1, plot_attributes_sp1))
            features_and_values_sp2 = list(zip(attributes_sp2, plot_attributes_sp2))
            features_and_values_sp3 = list(zip(attributes_sp3, plot_attributes_sp3))
            features_and_values = features_and_values_sp1 + features_and_values_sp2 + features_and_values_sp3

            # iterate over the list of tuples and add values to the 'plot' object
            for feature, plot_attr in features_and_values:
                if plot_attr == 0:
                    plot_attr = ''  # '' is more understandably than 0 when no equation is available
                if feature in PLOT_VARS:  # if the feature is in the list of variables, add it to the plot object
                    plot.add_value(feature, plot_attr)

        except Exception:
            TreeVolume.catch_model_exception()


    def get_Fang_values_dob(tree):
        """
        Function that provides Fang values for diameter over bark.
        It is called from the function 'set_tree_vol'.
        Values are used by the function 'Fang_taper'.
        Args:
            tree: Tree object
        Sources:
            Doc.: Badía M, Rodríguez F, Broto M (2001). Modelos del perfil del árbol. Aplicación al pino radiata (Pinus radiata D. Don). In Congresos Forestales
            Ref.: Badía et al, 2001
            Doc.: Calama R, Montero G (2006). Stand and tree-level variability on stem form and tree volume in Pinus pinea L.: a multilevel random components approach. Forest Systems, 15(1), 24-41
            Ref.: Calama and Montero, 2006
            Doc.: Lizarralde I (2008). Dinámica de rodales y competencia en las masas de pino silvestre (Pinus sylvestris L.) y pino negral (Pinus pinaster Ait.) de los Sistemas Central e Ibérico Meridional. Tesis Doctoral. 230 pp
            Ref.: Lizarralde 2008
            Doc.: López-Sánchez C A (2009). Estado selvícola y modelos de crecimiento y gestión de plantaciones de Pseudotsuga menziesii (Mirb.) Franco en España (Doctoral dissertation, Doctoral thesis. Universidad de Santiago de Compostela, Lugo.
            Ref.: López-Sánchez, 2009
            Doc.: Manrique-González, J., Bravo, F., del Peso, C., Herrero, C., Rodríguez, F., 2017. Ecuaciones de perfil para las especies de roble albar (Quercus petraea (Matt.) Liebl.) y rebollo (Quercus pyrenaica Willd) en la comarca de la “Castillería” en el Norte de la provincia de Palencia. 7º Congreso Forestal Español (póster).  http://7cfe.congresoforestal.es/sites/default/files/comunicaciones/776.pdf
            Ref.: Manrique-González et al., 2017
        """

        try:  # errors inside that construction will be announced

            if int(tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):  # Pinus sylvestris

                Fang_values_dob = (0.000051, 1.845867, 1.045022, 0.000011, 0.000038, 0.000030, 0, 0)
                # Rodriguez & Torre, 2015

                # Fang_values_dob = (6.421e-5, 1.817, 1.001, 1.357e-5, 3.059e-5, 2.699e-5, 0.08199, 0.6237)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ppinea'):  # Pinus pinea

                Fang_values_dob = (0.000067, 1.698754, 1.210604, 0.000006, 0.000033, 0.000026, 0.021072, 0.475953)
                # Rodriguez & Torre, 2015

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pnigra'):  # Pinus nigra

                Fang_values_dob = (0.000049, 1.982808, 0.905147, 0.000014, 0.000036, 0.000029, 0.091275, 0.781990)
                # Rodriguez & Torre, 2015

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):  # Pinus pinaster

                Fang_values_dob = (0.000048, 1.929098, 0.976356, 0.000010, 0.000035, 0.000033, 0.064157, 0.681476)
                # Rodriguez & Torre, 2015

                # Fang_values_dob = (3.974e-5, 1.876, 1.079, 1.003e-5, 3.695e-5, 2.910e-5, 0.1013, 0.7233)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pradiata'):  # Pinus radiata

                Fang_values_dob = (0.000058, 1.829097, 1.007844, 0.000009, 0.000033, 0.000030, 0, 0)
                # CESEFOR

                # Fang_values_dob = (4.851e-5, 1.883, 1.004, 8.702e-6, 3.302e-5, 2.899e-5, 0.06526, 0.6560)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pmenziesii'):  # Pseudotsuga menziesii

                Fang_values_dob = (0.00008564, 1.775, 0.9510, 0.000009340, 0.00003169, 0.00002786, 0.07362, 0.5397)
                # López-Sánchez, 2009

                # Fang_values_dob = (8.560e-5, 1.771, 0.9510, 9.340e-6, 3.169e-5, 2.786e-5, 0.07362, 0.5397)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Jthurifera'):  # Juniperus thurifera

                Fang_values_dob = (0.000074, 1.86289, 0.901233, 0.000001, 0.000028, 0.000037, 0.008578, 0.711639)
                # Rodriguez & Torre, 2015

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qrobur'):  # Quercus robur

                Fang_values_dob = (4.618e-5, 1.771, 1.165, 5.159e-6, 3.157e-5, 2.553e-5, 0.04025, 0.5184)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):  # Quercus pyrenaica

                Fang_values_dob = (0.000051, 1.867810, 0.989625, 0.000007, 0.000030, 0.000032, 0.047757, 0.825279)
                # Rodriguez & Torre, 2015

            elif int(tree.specie) == TreeEquations.get_ifn_id('Eglobulus'):  # Eucalyptus globulus

                Fang_values_dob = (4.896e-5, 1.679, 1.186, 4.901e-6, 3.246e-5, 4.156e-5, 0.04503, 0.8364)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Enittens'):  # Eucalyptus nittens

                Fang_values_dob = (5.024e-5, 1.823, 1.046, 5.700e-6, 3.074e-5, 2.797e-5, 0.03111, 0.5643)
                # Diéguez-Aranda et al., 2009

            elif int(tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):  # Fagus sylvatica

                Fang_values_dob = (0.000120, 2.036193, 0.799343, 0.000015, 0.000033, 0.005194, 0.074439, 0.873445)
                # Rodriguez & Torre, 2015

            elif int(tree.specie) == TreeEquations.get_ifn_id('Csativa'):  # Castanea sativa

                Fang_values_dob = (0.00005542, 1.914, 0.936, 0.000009869, 0.00003362, 0.00002667, 0.07191, 0.5590)
                # Bravo et al., 2011

            elif int(tree.specie) == TreeEquations.get_ifn_id('PPxcanadensis'):  # Populus x canadensis/euroamericana

                Fang_values_dob = (0.000044, 1.872438, 1.023328, 0.000013, 0.000028, 0.000026, 0.032326, 0.645012)
                # Rodriguez & Torre, 2015

            elif int(tree.specie) == TreeEquations.get_ifn_id('Balba'):  # Betula alba

                Fang_values_dob = (5.991e-5, 1.925, 0.8637, 5.266e-6, 2.838e-5, 2.428e-5, 0.04425, 0.9984)
                # Diéguez-Aranda et al., 2009

            else:  # no volume equation available

                Fang_values_dob = False

        except Exception:
            TreeVolume.catch_model_exception()

        return Fang_values_dob


    def get_Fang_values_dub(tree):
        """
        Function that provides Fang values for diameter under bark.
        It is called from the function 'set_tree_vol'.
        Values are used by the function 'Fang_taper'.
        Args:
            tree: Tree object
        Sources:
            Doc.: López-Sánchez C A (2009). Estado selvícola y modelos de crecimiento y gestión de plantaciones de Pseudotsuga menziesii (Mirb.) Franco en España (Doctoral dissertation, Doctoral thesis. Universidad de Santiago de Compostela, Lugo.
            Ref.: López-Sánchez, 2009
        """

        try:  # errors inside that construction will be announced

            if int(tree.specie) == TreeEquations.get_ifn_id('Pmenziesii'):  # Pseudotsuga menziesii

                Fang_values_dub = (0.00005695, 1.741, 1.072, 0.000009823, 0.00003246, 0.00002745, 0.06750, 0.5149)
                # López-Sánchez, 2009

            else:  # no volume equation available

                Fang_values_dub = False

        except Exception:
            TreeVolume.catch_model_exception()

        return Fang_values_dub


    def Fang_taper(tree: Tree, hr: float, values):
        """
        Fang taper equation.
        It is called from the function 'set_tree_vol'.
        Args:
            tree: Tree object
            hr: relative height (0-1)
            values: Fang values for dob or dub
        """

        if type(values) != bool:  # if it is an equation available...

            ao = values[0]
            a1 = values[1]
            a2 = values[2]
            b1 = values[3]
            b2 = values[4]
            b3 = values[5]
            p1 = values[6]
            p2 = values[7]

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
                I1 = np.array(
                    I1)  # when the lists are full, we transform the list into an array to simplify the following calculations
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
            c1 = math.sqrt((ao * (dbh ** a1) * (h ** (a2 - (k / b1))) / (
                        b1 * (ro - r1) + b2 * (r1 - alpha1 * r2) + b3 * alpha1 * r2)))

            if isinstance(hr, float) == False:  # on the cases where hr is an array...
                dob = []
                counter = 0
                for x in hr:  # for each hr value, we calculate the values of dob
                    d = (c1 * (math.sqrt(
                        ht ** ((k - b1) / b1) * (1 - hr[counter]) ** ((k - beta[counter]) / beta[counter]) * alpha1 ** (
                                    I1[counter] + I2[counter]) * alpha2 ** (I2[counter]))))
                    dob.append(d)  # we add the value to a list
                    counter += 1
                dob = np.array(dob)  # and transform the list to an array
            else:  # on the case we have only 1 value to hr, we calculate dob directly
                dob = (c1 * (math.sqrt(
                    ht ** ((k - b1) / b1) * (1 - hr) ** ((k - beta) / beta) * alpha1 ** (I1 + I2) * alpha2 ** (I2))))


        else:  # if it is not an equation available...

            dob = 0

        return dob


    def set_tree_merch(tree):
        """
        Merchantable wood calculation (tree).
        A function needed to calculate the different commercial volumes of wood depending on the industrial destiny.
        It uses the function merch_calculation_all_species to calculate the commercial volume of wood.
        Args:
            tree: Tree object
        Data criteria to classify the wood by different uses were obtained from:
            Doc.: Fernández-Manso A, Sarmiento A (2004). El pino radiata (Pinus radiata). Manual de gestión forestal sostenible. Junta de Castilla y León.
            Ref.: Fernández-Manso et al, 2004
            Doc.: Rodríguez F (2009). Cuantificación de productos forestales en la planificación forestal: Análisis de casos con cubiFOR. In Congresos Forestales
            Ref.: Rodríguez, 2009
        """

        try:  # errors inside that construction will be announced

            ht = tree.height  # the total height as ht to simplify

            # Note:
            # class_conditions have different lists for each usage, following that structure: [wood_usage, hmin/ht, dmin, dmax]
            # [WOOD USE NAME, LOG RELATIVE LENGTH RESPECT TOTAL TREE HEIGHT, MINIMUM DIAMETER, MAXIMUM DIAMETER]

            if int(tree.specie) == TreeEquations.get_ifn_id('Falnus'):  # Frangula alnus
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Aaltissima'):  # Ailanthus altissima
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Msylvestris'):  # Malus sylvestris
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Caustralis'):  # Celtis australis
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Tbaccata'):  # Taxus baccata
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Crataegus'):  # Crataegus spp.
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pyrus'):  # Pyrus spp.
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Catlantica'), TreeEquations.get_ifn_id('Cdeodara'),
                                      TreeEquations.get_ifn_id('Clibani'), TreeEquations.get_ifn_id('Cedrus')):  # Cedrus spp. - Cedrus atlantica, C. deodara, C. libani, C. spp.
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Psylvestris'):  # Pinus sylvestris
                class_conditions = [['unwinding', 3 / ht, 40, 160], ['veneer', 3 / ht, 40, 160],
                                    ['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ppinea'):  # Pinus pinea
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Phalepensis'):  # Pinus halepensis
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pnigra'):  # Pinus nigra
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ppinaster'):  # Pinus pinaster
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pradiata'):  # Pinus radiata
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]
                #  Fernández-Manso et al, 2004

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pabies'):  # Picea abies
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pmenziesii'):  # Pseudotsuga menziesii
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Csempervirens'), TreeEquations.get_ifn_id('Carizonica'),
              TreeEquations.get_ifn_id('Clusitanica'), TreeEquations.get_ifn_id('Cmacrocarpa'), TreeEquations.get_ifn_id('Cupressus')):
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Jcommunis'):  # Juniperus communis
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Jthurifera'):  # Juniperus thurifera
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Jphoenica'):  # Juniperus phoenica
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['post', 6 / ht, 15, 28],
                                    ['stake', 1.8 / ht, 6, 16]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qrobur'):  # Quercus robur
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qpetraea'):  # Quercus petraea
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qpyrenaica'):  # Quercus pyrenaica
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qfaginea'):  # Quercus faginea
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qilex'):  # Quercus ilex
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Qsuber'):  # Quercus suber
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Palba'):  # Populus alba
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ptremula'):  # Populus tremula
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Aglutinosa'):  # Alnus glutinosa
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Fangustifolia'), TreeEquations.get_ifn_id('Fexcelsior'),
                                      TreeEquations.get_ifn_id('Fornus'), TreeEquations.get_ifn_id('Fraxinus')):  # Fraxinus spp. - F. angustifolia, F. excelsior, F. omus, F. spp.
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Uminor'), TreeEquations.get_ifn_id('Uglabra'),
                    TreeEquations.get_ifn_id('Upumila'), TreeEquations.get_ifn_id('Ulmus')):  # Ulmus spp. - U. minor, U. glabra, U. pumila, U. spp.
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Salix'), TreeEquations.get_ifn_id('Salba'),
              TreeEquations.get_ifn_id('Satrocinerea'), TreeEquations.get_ifn_id('Sbabylonica'), TreeEquations.get_ifn_id('Scantabrica'),
              TreeEquations.get_ifn_id('Scaprea'), TreeEquations.get_ifn_id('Selaeagnos'), TreeEquations.get_ifn_id('Sfragilis'),
              TreeEquations.get_ifn_id('Scanariensis'), TreeEquations.get_ifn_id('Spurpurea')):  # Salix spp. - S. spp., S. alba, S. atrocinerea, S. babylonica, S. cantabrica, S. caprea, S. eleagnos, S. fragilis, S. canariensis, S. purpurea
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Ecamaldulensis'):  # Eucalyptus camaldulensis
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Iaquifolium'):  # Ilex aquifolium
                class_conditions = [['saw_canter', 2.5 / ht, 15, 28]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Oeuropaea'):  # Olea europaea
                class_conditions = [['unwinding', 1.2 / ht, 20, 160], ['veneer', 1.2 / ht, 20, 160],
                                    ['saw_canter', 2.5 / ht, 12, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Aunedo'):  # Arbutus unedo
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Fsylvatica'):  # Fagus sylvatica
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Csativa'):  # Castanea sativa
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Betula'), TreeEquations.get_ifn_id('Balba'),
                                  TreeEquations.get_ifn_id('Bpendula')):  # Betula spp. - B. spp., B. alba, B. pendula
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Cavellana'):  # Corylus avellana
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Jregia'):  # Juglans regia
                class_conditions = [['unwinding', 1.2 / ht, 20, 160], ['veneer', 1.2 / ht, 20, 160],
                                    ['saw_canter', 2.5 / ht, 12, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Acampestre'), TreeEquations.get_ifn_id('Amonspessulanum'),
              TreeEquations.get_ifn_id('Anegundo'), TreeEquations.get_ifn_id('Aopalus'), TreeEquations.get_ifn_id('Apseudoplatanus'),
              TreeEquations.get_ifn_id('Aplatanoides'), TreeEquations.get_ifn_id('Acer')):  # Acer spp. - A. campestre, A. monspessulanum, A. negundo, A. opalus, A. pseudoplatanus, A. platanoides, A. spp.
                class_conditions = [['unwinding', 1.2 / ht, 20, 160], ['veneer', 1.2 / ht, 20, 160],
                                    ['saw_canter', 2.5 / ht, 12, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Sorbus'), TreeEquations.get_ifn_id('Saria'),
              TreeEquations.get_ifn_id('Saucuparia'), TreeEquations.get_ifn_id('Sdomestica'), TreeEquations.get_ifn_id('Storminalis'),
              TreeEquations.get_ifn_id('Slatifolia'), TreeEquations.get_ifn_id('Schamaemespilus')):  # Sorbus spp. - S. spp., S. aria, S. aucuparia, S. domestica, S. torminalis, S. latifolia, S. chamaemespilus
                class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200],
                                    ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) in (TreeEquations.get_ifn_id('Prunus'), TreeEquations.get_ifn_id('Pspinosa'),
              TreeEquations.get_ifn_id('Pavium'), TreeEquations.get_ifn_id('Plusitanica'),
              TreeEquations.get_ifn_id('Ppadus')):  # Prunus spp. - P. spp, P.spinosa, P. avium, P. lusitanica, P. padus
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Snigra'):  # Sambucus nigra
                class_conditions = [['chips', 1 / ht, 5, 1000000]]

            elif int(tree.specie) == TreeEquations.get_ifn_id('Pxcanadensis'):  # Populus x canadensis/euroamericana
                class_conditions = [['unwinding', 1.2 / ht, 20, 160], ['veneer', 1.2 / ht, 20, 160],
                                    ['saw_canter', 2.5 / ht, 12, 28], ['chips', 1 / ht, 5, 1000000]]

            else:  # no volume equation available, just chips by default
                class_conditions = [['chips', 1 / ht, 5, 1000000]]


            # usage and merch_list are a dictionary and a list returned from merch_calculation function
            # to that function, we must send the following information: tree, class_conditions, and the name of our class on this model you are using
            usage, merch_list = TreeVolume.merch_calculation_all_species(tree, class_conditions)

            if merch_list:  # check if the list is empty
                counter = -1
                for k, i in usage.items():
                    counter += 1
                    tree.add_value(k, merch_list[counter])  # add merch_list values to each usage

        except Exception:
            TreeVolume.catch_model_exception()

    def set_plot_merch(plot, list_of_trees):
        """
        Merchantable wood calculation at plot level.
        That function must be call after the set_tree_merch function to calculate the merchantable volume of each tree.
        It sums the values of all trees to obtain the total volume of the plot for each wood use.
        Args:
            plot: the plot object
            list_of_trees: list of trees in the plot
        """

        try:  # errors inside that construction will be announced

            # by default values
            merch_values_plot = [0, 0, 0, 0, 0, 0, 0, 0]
            merch_features_plot = ['UNWINDING', 'VENEER', 'SAW_BIG', 'SAW_SMALL', 'SAW_CANTER', 'POST', 'STAKE', 'CHIPS']
            merch_features_tree = ['unwinding', 'veneer', 'saw_big', 'saw_small', 'saw_canter', 'post', 'stake', 'chips']
            for feature in merch_features_plot:
                plot.add_value(feature, 0)


            # for each tree in plot
            for tree in list_of_trees:

                # iterate over the list of attributes and plot attributes
                for attr, plot_attr, n in zip(merch_features_tree, merch_values_plot, range(len(merch_values_plot))):
                    if attr in TREE_VARS:  # if the attribute is in the list of variables, add it to the plot object
                        value = getattr(tree, attr, '')
                        if value != '':  # if the value is not empty, add it to the plot attribute
                            plot_attr += value * tree.expan / 1000
                            merch_values_plot[n] = plot_attr  # update the plot attribute
                        else:
                            merch_values_plot[n] = plot_attr  # previous value is maintained


            # define features and values as tuples
            features_and_values = list(zip(merch_features_plot, merch_values_plot))

            # iterate over the list of tuples and add values to the 'plot' object
            for feature, plot_attr in features_and_values:
                if plot_attr == 0:
                    plot_attr = ''  # '' is more understandably than 0 when no equation is available
                if feature in PLOT_VARS:  # if the feature is in the list of variables, add it to the plot object
                    plot.add_value(feature, plot_attr)

        except Exception:
            TreeVolume.catch_model_exception()


    def set_plot_merch_sp(plot, list_of_trees):
        """
        Merchantable wood calculation at plot level by species.
        That function must be call after the set_tree_merch function to calculate the merchantable volume of each tree.
        It sums the values of all trees to obtain the total volume of the plot for each wood use and species.
        Args:
            plot: the plot object
            list_of_trees: list of trees in the plot
        """

        try:  # errors inside that construction will be announced

            # by default values
            merch_values_plot_sp1 = [0, 0, 0, 0, 0, 0, 0, 0]
            merch_values_plot_sp2 = [0, 0, 0, 0, 0, 0, 0, 0]
            merch_values_plot_sp3 = [0, 0, 0, 0, 0, 0, 0, 0]

            # define tree and plot attributes
            merch_features_tree = ['unwinding', 'veneer', 'saw_big', 'saw_small', 'saw_canter', 'post', 'stake', 'chips']

            merch_features_plot_sp1 = ['UNWINDING_SP1', 'VENEER_SP1', 'SAW_BIG_SP1', 'SAW_SMALL_SP1', 'SAW_CANTER_SP1',
                                       'POST_SP1', 'STAKE_SP1', 'CHIPS_SP1']
            merch_features_plot_sp2 = ['UNWINDING_SP2', 'VENEER_SP2', 'SAW_BIG_SP2', 'SAW_SMALL_SP2', 'SAW_CANTER_SP2',
                                       'POST_SP2', 'STAKE_SP2', 'CHIPS_SP2']
            merch_features_plot_sp3 = ['UNWINDING_SP3', 'VENEER_SP3', 'SAW_BIG_SP3', 'SAW_SMALL_SP3', 'SAW_CANTER_SP3',
                                       'POST_SP3', 'STAKE_SP3', 'CHIPS_SP3']


            # for each tree, we are going to add the individual values to the plot value
            for tree in list_of_trees:

                # distinguish the species of the tree
                if tree.specie == plot.id_sp1:
                    merch_values_plot = merch_values_plot_sp1
                elif tree.specie == plot.id_sp2:
                    merch_values_plot = merch_values_plot_sp2
                else:
                    merch_values_plot = merch_values_plot_sp3

                # iterate over the list of attributes and plot attributes
                for attr, plot_attr, n in zip(merch_features_tree, merch_values_plot, range(len(merch_values_plot))):
                    if attr in TREE_VARS:  # if the attribute is in the list of variables, add it to the plot object
                        value = getattr(tree, attr, '')
                        if value != '':  # if the value is not empty, add it to the plot attribute
                            plot_attr += value * tree.expan / 1000
                            merch_values_plot[n] = plot_attr  # update the plot attribute
                        else:
                            merch_values_plot[n] = plot_attr  # previous value is maintained

                # rewrite the values of the plot
                # distinguish the species of the tree
                if tree.specie == plot.id_sp1:
                    merch_values_plot_sp1 = merch_values_plot
                elif tree.specie == plot.id_sp2:
                    merch_values_plot_sp2 = merch_values_plot
                else:
                    merch_values_plot_sp3 = merch_values_plot


            # define features and values as tuples
            features_and_values_sp1 = list(zip(merch_features_plot_sp1, merch_values_plot_sp1))
            features_and_values_sp2 = list(zip(merch_features_plot_sp2, merch_values_plot_sp2))
            features_and_values_sp3 = list(zip(merch_features_plot_sp3, merch_values_plot_sp3))
            features_and_values = features_and_values_sp1 + features_and_values_sp2 + features_and_values_sp3

            # iterate over the list of tuples and add values to the 'plot' object
            for feature, plot_attr in features_and_values:
                if plot_attr == 0:
                    plot_attr = ''  # '' is more understandably than 0 when no equation is available
                if feature in PLOT_VARS:  # if the feature is in the list of variables, add it to the plot object
                    plot.add_value(feature, plot_attr)

        except Exception:
            TreeVolume.catch_model_exception()


    def merch_calculation_all_species(tree, class_conditions):
        """
        Function needed to calculate the merchantable volumen of the different wood uses.
        That function must be activated by using merchantable function on the all species model, and it will need
        the Fang_taper and Fang_values_dob functions to calculate the volume.
        Args:
            tree: the tree object
            class_conditions: list of lists with the following structure: [wood_usage, hmin/ht, dmin, dmax]
        """

        try:

            ht = tree.height  # the total height as ht to simplify

            global usage  # share that dictionary to give access in other functions
            usage = {}  # that dictionary will obtain the values of usage acceptability for each tree

            if 'stump_h' in TREE_VARS:
                if tree.stump_h != 0 and tree.stump_h != '':
                    hro = tree.stump_h / ht  # initial height = stump height
                else:
                    hro = 0.20 / ht  # initial height = stump height
            else:
                hro = 0.20 / ht  # initial height = stump height

            counter = -1
            for k in class_conditions:  # for each list (usage+conditions) on class_conditions...
                counter += 1
                if (class_conditions[counter][1] + hro) <= 1:
                    usage[class_conditions[counter][
                        0]] = True  # if stump + log <= 1 (total relative height), then the use is accepted
                else:
                    usage[class_conditions[counter][0]] = False  # if not, the use is rejected

            count = -1
            global merch_list  # share that list to give access in other functions
            merch_list = []  # that list will obtain the results of calculate the different log volumes

            Fang_values = TreeVolume.get_Fang_values_dob(tree)  # we get the values of Fang equation
            if Fang_values == False:  # if there is no equation available...
                return usage, merch_list  # we return the empty lists
            else:
                for k, i in usage.items():  # for each usage defined before...

                    if 'stump_h' in TREE_VARS:
                        if tree.stump_h != 0 and tree.stump_h != '':
                            hro = tree.stump_h / ht  # initial height = stump height
                        else:
                            hro = 0.20 / ht  # initial height = stump height
                    else:
                        hro = 0.20 / ht  # initial height = stump height

                    vol = 0
                    count += 1  # that variable allow us to go over the lists
                    if i == True:  # if the log satisfy the restrictions...
                        dr = TreeVolume.Fang_taper(tree, hro, Fang_values)  # diameter of tree at the stump height
                        while dr > class_conditions[count][3] and (
                                hro + 0.05 / ht <= 1):  # if the diameter > dmax, and hr <= 1...
                            hro += 0.05 / ht  # we go over the log looking for the part with diameter <= dmax for that usage
                            dr = TreeVolume.Fang_taper(tree, hro, Fang_values)  # we calculate the diameter on the next point, to verify the conditions
                        while dr >= class_conditions[count][2] and (hro + class_conditions[count][
                            1] <= 1):  # satisfying dmax, if diameter > dmin and hro is between integration limits (0-1)...
                            hro += class_conditions[count][
                                1]  # from the start point on the tree, we add the length of a log with the usage specifications
                            dr = TreeVolume.Fang_taper(tree, hro, Fang_values)  # we again calculate the diameter at this point; the second while condition has sense in here, to not get over 1 integration limit
                            if dr >= class_conditions[count][
                                2] and hro <= 1:  # as taper equation reduce the diameter, it is not needed to check it
                                # if the log diameter > dmin, and hro doesn't overpass 1 (integration limit)
                                hr = np.arange((hro - class_conditions[count][1]), hro,
                                               0.001)  # integration conditions for taper equation
                                d = TreeVolume.Fang_taper(tree, hr, Fang_values)  # we get the taper equation with the previous conditions
                                f = (d / 20) ** 2  # to calculate the volume (dm3), we change the units of the result and calculate the radius^2 (instead of diameter)
                                vol += math.pi * ht * 10 * (integrate.simps(f, hr))  # volume calculation, using the previous information
                        if i == True:  # once the tree finish all the while conditions, it comes here, because it continues verifying that condition
                            merch_list.append(vol)  # once we have the total volume for each usage, we add the value to that list
                    else:  # if the tree is not useful for one usage, it comes here
                        merch_list.append(0)  # as it is not useful, we add 0 value to that usage

        except Exception:
            TreeVolume.catch_model_exception()

        return usage, merch_list
