#!/usr/bin/env python
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


from abc import ABCMeta
from abc import abstractmethod
from data import Tree
from data import Plot
from data.general import Area, Model, Warnings
from util import Tools
from scipy import integrate
from models.trees import *
from data.general import Area
from data.variables import AREA_VARS, PLOT_VARS, TREE_VARS

import logging
import math
import numpy as np
import pandas as pd
import collections
import itertools


class TreeBiomass(metaclass=ABCMeta):

    def __init__(self, configuration=None):
        super().__init__(name="TreeBiomass", version=1)

    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def set_w_carbon_trees(tree):
        """
        Function to calculate biomass and carbon variables for each tree.
        It assigns the values to the tree object for the corresponding features available, returning '' if not available.
        :param tree: Tree object
        Source:
            Doc.: Castaño-Santamaría, J., Bravo, F. Variation in carbon concentration and basic density along stems of sessile oak (Quercus petraea (Matt.) Liebl.) and Pyrenean oak (Quercus pyrenaica Willd.) in the Cantabrian Range (NW Spain). Annals of Forest Science 69, 663–672 (2012). https://doi.org/10.1007/s13595-012-0183-6
            Ref.: Castaño-Santamaría and Bravo, 2012
            Doc.: Diéguez-Aranda U, Rojo A, Castedo-Dorado F, et al (2009). Herramientas selvícolas para la gestión forestal sostenible en Galicia. Forestry, 82, 1-16
            Ref.: Diéguez-Aranda et al. 2009
            Doc.: Herrero de Aza, C., Turrión, M.B., Pando, V. et al. Carbon in heartwood, sapwood and bark along the stem profile in three Mediterranean Pinus species. Annals of Forest Science 68, 1067 (2011). https://doi.org/10.1007/s13595-011-0122-y
            Ref.: Herrero de Aza et al., 2011
            Doc.: Ruiz-Peinado R, del Rio M, Montero G (2011). New models for estimating the carbon sink capacity of Spanish softwood species. Forest Systems, 20(1), 176-188
            Ref.: Ruiz-Peinado et al, 2011
            Doc.: Ruiz-Peinado R, Montero G, Del Rio M (2012). Biomass models to estimate carbon stocks for hardwood tree species. Forest systems, 21(1), 42-52
            Ref.: Ruiz-Peinado et al, 2012
            Doc.: C. Telmo, J. Lousada, N. Moreira (2010). Proximate analysis, backwards stepwise regression between gross calorific value, ultimate and chemical analysis of wood. Bioresource Technology, 101(11):3808-3815. https://doi.org/10.1016/j.biortech.2010.01.021.
            Ref.: Telmo et al., 2010
        """

        try:

            # TODO: to explore/include:
            # https://www.fs.usda.gov/research/nrs/news/highlights/how-much-carbon-tree-biomass#publications
            # https://github.com/mdoraisami/glowcad/tree/main


            # define variables
            wsw = wsb = wswb = w_cork = wthickb = wstb = wb2_7 = wb2_t = wthinb = wb05 = 0
            wb05_7 = wb0_2 = wdb = wl = wtbl = wbl0_7 = ws = wb = wr = wt = 0
            carbon_heartwood = carbon_sapwood = carbon_bark = c_value = 0

            # elif tree.specie == 17:  # Cedrus atlantica

                # carbon = 50.3*wt
                # Telmo et al., 2010

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
                # Ruiz-Peinado et al, 2011

                # Galicia
                # wswb = 0.02321*(tree.dbh**2.708)
                # wthickb = 3.7e-7*(tree.dbh**4.804)
                # wb2_7 = 0.02036*(tree.dbh**2.141)
                # wb0_2 = 0.1432*(tree.dbh**1.510)
                # wl = 0.1081*(tree.dbh**1.510)
                # wr = 0.01089*(tree.dbh**2.628)
                # Diéguez-Aranda et al. 2009

                c_value = 0.459
                # Herrero et al., 2011

            elif tree.specie == 22:  # Pinus uncinata

                wsw = 0.0203 * (tree.dbh ** 2) * tree.height
                wb2_t = 0.0379 * (tree.dbh ** 2)
                wtbl = 2.740 * tree.dbh - 2.641 * tree.height
                wr = 0.193 * (tree.dbh ** 2)
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
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 25:  # Pinus nigra

                wsw = 0.0403 * (tree.dbh ** 1.838) * (tree.height ** 0.945)  # Stem wood (kg)
                if tree.dbh <= 32.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.228 * ((tree.dbh - 32.5) ** 2)) * Z  # wthickb = branches > 7 cm biomass (kg)
                wb2_7 = 0.0521 * (tree.dbh ** 2)  # wb2_7 = branches (2-7 cm) biomass (kg)
                wtbl = 0.0720 * (tree.dbh ** 2)  # Thin branches + Leaves (<2 cm) biomass (kg)
                wr = 0.0189 * (tree.dbh ** 2.445)  # Roots biomass (kg)
                # Ruiz-Peinado et al, 2011

                c_value = 0.464
                # Herrero et al., 2011

            elif tree.specie == 26:  # Pinus pinaster

                # España
                wsw = 0.0278 * (tree.dbh ** 2.115) * (tree.height ** 0.618)
                wb2_t = 0.000381 * (tree.dbh ** 3.141)
                wtbl = 0.0129 * (tree.dbh ** 2.320)
                wr = 0.00444 * (tree.dbh ** 2.804)
                # Ruiz-Peinado et al, 2011

                # Galicia
                # wstb = 0.3882 + 0.01149*(tree.dbh**2)*tree.height
                # wsb = 0.0079*(tree.dbh**2.098)*(tree.height**0.466)
                # wb2_7 = 3.202 - 0.01484*(tree.dbh**2) - 0.4228*tree.height + 0.00279*(tree.dbh**2)*tree.height
                # wthinb = 0.09781*(tree.dbh**2.288)*(tree.height**(-0.9648))
                # wb05 = 0.00188*(tree.dbh**2.154)
                # wl = 0.005*(tree.dbh**2.383)
                # Diéguez-Aranda et al. 2009

                c_value = 0.468
                # Herrero et al., 2011

                # c_value = 0.484
                # Telmo et al., 2010

            elif tree.specie == 27:  # Pinus canariensis

                wsw = 0.0249 * ((tree.dbh ** 2) * tree.height) ** 0.975
                if tree.dbh <= 32.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.634 * ((tree.dbh - 32.5) ** 2)) * Z
                wb2_7 = 0.00162 * (tree.dbh ** 2) * tree.height
                wtbl = 0.0844 * (tree.dbh ** 2) - 0.0731 * (tree.height ** 2)
                wr = 0.155 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 28:  # Pinus radiata

                # España
                wstb = 0.01230 * (tree.dbh ** 1.604) * (tree.height ** 1.413)
                wsb = 0.003600 * (tree.dbh ** 2.656)
                wb2_7 = 1.938 + 0.001065 * (tree.dbh ** 2) * tree.height
                wthinb = 0.03630 * (tree.dbh ** 2.609) * (tree.height ** (-0.9417))
                wb05 = 0.007800 * (tree.dbh ** 1.961)
                wl = 0.04230 * (tree.dbh ** 1.714)
                wr = 0.06174 * (tree.dbh ** 2.144)

                # Galicia
                # wstb = 0.01230*(tree.dbh**1.604)*(tree.height**1.413)
                # wsb = 0.003600*(tree.dbh**2.656)
                # wb2_7 = 1.938 + 0.001065*(tree.dbh**2)*tree.height
                # wthinb = 0.03630*(tree.dbh**2.609)*(tree.height**(-0.9417))
                # wb05 = 0.007800*(tree.dbh**1.961)
                # wl = 0.04230*(tree.dbh**1.714)
                # wr = 0.06174*(tree.dbh**2.144)
                # Diéguez-Aranda et al. 2009

            elif tree.specie == 31:  # Abies alba

                wsw = 0.0189 * (tree.dbh ** 2) * tree.height
                wb2_t = 0.0584 * (tree.dbh ** 2)
                wtbl = 0.0371 * (tree.dbh ** 2) + 0.968 * tree.height
                wr = 0.101 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 32:  # Abies pinsapo

                wsw = 0.00960 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 32.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = ((1.637 * ((tree.dbh - 32.5) ** 2) - 0.0719 * (tree.dbh - 32.5) ** 2) * tree.height) * Z
                w2_7 = 0.00344 * (tree.dbh ** 2) * tree.height
                wtbl = 0.131 * tree.dbh * tree.height
                # Ruiz-Peinado et al, 2011

            # elif tree.specie == 34:  # Pseudotsuga menziesii

                # c_value = 0.476
                # Telmo et al., 2010

            elif tree.specie == 38:  # Juniperus thurifera

                wsw = 0.32 * (tree.dbh ** 2) * tree.height + 0.217 * tree.dbh * tree.height
                if tree.dbh <= 22.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.107 * ((tree.dbh - 22.5) ** 2)) * Z
                wb2_7 = 0.00792 * (tree.dbh ** 2) * tree.height
                wtbl = 0.273 * tree.dbh * tree.height
                wr = 0.0767 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2011

            elif tree.specie == 41:  # Quercus robur

                # Galicia
                # wsw = -5.714 + 0.01823*(tree.dbh**2)*tree.height
                # wsb = -1.5 + 0.03154*(tree.dbh**2) + 0.00111*(tree.dbh**2)*tree.height
                # wthickb = 3.427e-9*((tree.dbh**2)*tree.height)**2.310
                # wb2_7 = 4.268 + 0.003410*(tree.dbh**2)*tree.height
                # wthinb = 0.03851*(tree.dbh**1.784)
                # wb05 = 1.379 + 0.00024*(tree.dbh**2)*tree.height
                # wl = 0.01985*((tree.dbh**2)*tree.height)**0.7375
                # wr = 0.01160*((tree.dbh**2)*tree.height)**0.9625
                # Diéguez-Aranda et al. 2009

                # España
                wsw = -5.714 + 0.01823 * (tree.dbh ** 2) * tree.height
                wsb = -1.500 + 0.03154 * (tree.dbh ** 2) + 0.001110 * (tree.dbh ** 2) * tree.height
                wthickb = 3.427e-9 * (((tree.dbh ** 2) * tree.height) ** 2.310)
                wb2_7 = 4.268 + 0.003410 * (tree.dbh ** 2) * tree.height
                wthinb = 0.03851 * (tree.dbh ** 1.784) + 1.379
                wb05 = 0.00024 * (tree.dbh ** 2) * tree.height
                wl = 0.01985 * (((tree.dbh ** 2) * tree.height) ** 0.7375)
                wr = 0.01160 * ((tree.dbh ** 2) * tree.height) ** 0.9625

                c_value = 0.472
                # Telmo et al., 2010

            elif tree.specie == 42:  # Quercus petraea

                wstb = 0.001333 * (tree.dbh ** 2) * tree.height
                wb2_7 = 0.006531 * (tree.dbh ** 2) * tree.height - 0.07298 * tree.dbh * tree.height
                wthinb = 0.023772 * (tree.dbh ** 2) * tree.height
                # Ruiz-Peinado et al, 2012

                carbon_heartwood = wt * (0.2732 * 0.4601)  # heartwood
                carbon_sapwood = wt * (0.5427 * 0.4549)  # sapwood
                carbon_bark = wt * (0.1841 * 0.4686)  # bark
                # carbon = wt*(0.1841*0.4686 + 0.5427*0.4549 + 0.2732*0.4601)  # bark, sapwood and heartwood proportions
                # Castaño-Santamaría and Bravo, 2012

            elif tree.specie == 43:  # Quercus pyrenaica

                wstb = 0.0261 * (tree.dbh ** 2) * tree.height
                wb2_7 = - 0.0260 * (tree.dbh ** 2) + 0.536 * tree.height + 0.00538 * (tree.dbh ** 2) * tree.height
                wthinb = 0.898 * tree.dbh - 0.445 * tree.height
                wr = 0.143 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

                carbon_heartwood = wt * (0.2732 * 0.4582)  # heartwood
                carbon_sapwood = wt * (0.5427 * 0.4558)  # sapwood
                carbon_bark = wt * (0.1841 * 0.4578)  # bark
                # carbon = wt*(0.1841*0.4578 + 0.5427*0.4558 + 0.2732*0.4582)  # bark, sapwood and heartwood proportions
                # Castaño-Santamaría and Bravo, 2012

            elif tree.specie == 44:  # Quercus faginea

                wsw = 0.154 * (tree.dbh ** 2)
                wthickb = 0.0861 * (tree.dbh ** 2)
                wb2_7 = 0.127 * (tree.dbh ** 2) - 0.00598 * (tree.dbh ** 2) * tree.height
                wtbl = 0.0726 * (tree.dbh ** 2) - 0.00275 * (tree.dbh ** 2) * tree.height
                wr = 0.169 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 45:  # Quercus ilex

                wsw = 0.143 * (tree.dbh ** 2)
                if tree.dbh <= 12.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.0684 * ((tree.dbh - 12.5) ** 2) * tree.height) * Z
                wb2_7 = 0.0898 * (tree.dbh ** 2)
                wtbl = 0.0824 * (tree.dbh ** 2)
                wr = 0.254 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 46:  # Quercus suber

                wsw = 0.00525 * (tree.dbh ** 2) * tree.height + 0.278 * tree.dbh * tree.height
                wthickb = 0.0135 * (tree.dbh ** 2) * tree.height
                wb2_7 = 0.127 * tree.dbh * tree.height
                wtbl = 0.0463 * tree.dbh * tree.height
                wr = 0.0829 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

                # TODO: check before use
                # if 'h_debark' in TREE_VARS and 'dbh_oc' in TREE_VARS and 'nb' in TREE_VARS:
                #
                #     if isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float) and isinstance(tree.nb, float):
                #
                #         pbhoc = (tree.dbh_oc * math.pi) / 100  # perimeter at breast height outside cork (m)
                #         pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
                #         shs = tree.h_debark  # stripped height in the stem (m)
                #         nb = tree.nb + 1  # number of stripped main bough + 1
                #
                #         if tree.cork_cycle == 0:  # To use inmediately before the stripping process
                #             if nb == 1 and shs != 0:
                #                 tree.add_value('w_cork', math.exp(2.3665 + 2.2722 * math.log(pbhoc) + 0.4473 * math.log(shs)))
                #             elif nb != 1 and shs != 0:
                #                 tree.add_value('w_cork', math.exp(
                #                     2.1578 + 1.5817 * math.log(pbhoc) + 0.5062 * math.log(nb) + 0.6680 * math.log(shs)))
                #             else:
                #                 tree.add_value('w_cork', 0)
                #
                #         elif tree.cork_cycle == 1:  # To use after the stripping process or in a intermediate age of the cork cycle production
                #             if nb == 1 and shs != 0:
                #                 tree.add_value('w_cork', math.exp(2.7506 + 1.9174 * math.log(pbhic) + 0.4682 * math.log(shs)))
                #             elif nb != 1 and shs != 0:
                #                 tree.add_value('w_cork', math.exp(2.2137 + 0.9588 * math.log(shs) + 0.6546 * math.log(nb)))
                #             else:
                #                 tree.add_value('w_cork', 0)
                #         else:
                #             tree.add_value('w_cork', 0)
                #
                #     elif isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float) and not isinstance(tree.nb, float):
                #
                #         pbhoc = (tree.dbh_oc * math.pi) / 100  # perimeter at breast height outside cork (m)
                #         pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
                #         shs = tree.h_debark  # stripped height in the stem (m)
                #         nb = 1  # number of stripped main bough + 1
                #
                #         if tree.cork_cycle == 0 and shs != 0:  # To use inmediately before the stripping process
                #             tree.add_value('w_cork', math.exp(2.3665 + 2.2722 * math.log(pbhoc) + 0.4473 * math.log(shs)))
                #         elif tree.cork_cycle == 1 and shs != 0:  # To use after the stripping process or in a intermediate age of the cork cycle production
                #             tree.add_value('w_cork', math.exp(2.7506 + 1.9174 * math.log(pbhic) + 0.4682 * math.log(shs)))
                #         else:
                #             tree.add_value('w_cork', 0)
                #
                #     else:
                #
                #         tree.add_value('w_cork', 0)

            elif tree.specie == 47:  # Quercus canariensis

                wsw = 0.0126 * (tree.dbh ** 2) * tree.height
                wthickb = 0.103 * (tree.dbh ** 2)
                wbl0_7 = 0.167 * tree.dbh * tree.height
                wr = 0.135 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 54:  # Alnus glutinosa

                wsw = 0.0191 * (tree.dbh ** 2) * tree.height
                wb2_t = 0.0512 * (tree.dbh ** 2)
                wtbl = 0.0567 * tree.dbh * tree.height
                wr = 0.214 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 55:  # Fraxinus angustifolia

                wsw = 0.0296 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 12.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.231 * ((tree.dbh - 12.5) ** 2)) * Z
                wb2_7 = 0.0925 * (tree.dbh ** 2)
                wthinb = 2.005 * tree.dbh
                wr = 0.359 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

                c_value = 0.477
                # Telmo et al., 2010

            elif tree.specie == 61:  # Eucalyptus globulus

                # Galicia
                wstb = 0.01308 * (tree.dbh ** 1.870) * (tree.height ** 1.172)
                wsb = 0.01010 * (tree.dbh ** 2.484)
                wb05_7 = 0.003685 * (tree.dbh ** 2.654)
                wb05 = 0.01258 * (tree.dbh ** 1.705)
                wl = 0.02949 * (tree.dbh ** 1.917)
                # Diéguez-Aranda et al. 2009

                # España
                # wstb = 0.0221*(tree.dbh**2)*tree.height
                # wb2_7 = 0.154*(tree.dbh**1.668)
                # wtbl = 0.180*(((tree.dbh**2)*tree.height)**0.587)
                # Ruiz-Peinado et al, 2012

                c_value = 0.462
                # Telmo et al., 2010

            elif tree.specie == 64:  # Eucalyptus nittens

                # Sin ecuaciones de copa
                wstb = 0.0094 * (tree.dbh ** 2.033) * (tree.height ** 1.056)
                wsb = 0.01342 * (tree.dbh ** 2.361)
                wb2_7 = 0.000059 * (tree.dbh ** 3.760)
                wthinb = 0.01280 * (tree.dbh ** 1.858)
                wb05 = 0.000922 * (tree.dbh ** 2.632)
                wl = 0.0053 * (tree.dbh ** 2.393)
                wdb = 0.1451 * (tree.dbh ** 1.403)
                # Diéguez-Aranda et al. 2009

                # Con ecuaciones de copa
                # wstb = 0.1495*(tree.dbh**2.052)*(tree.height**0.8946)
                # wsb = 0.03190*(tree.dbh**2.108)
                # wb2_7 = 0.000822*(tree.dbh**2.644)*(tree.lcw**0.7627)
                # wthinb = 0.03005*(tree.dbh**1.590)
                # wb05 = 0.006230*(tree.dbh**1.949)*(tree.lcw**0.2189)
                # wl = 0.0168*(tree.dbh**1.516)*((tree.height - tree.hcb)**0.7747)
                # wdb = 0.007933*(tree.dbh**1.279)*(tree.hbc**1.254)
                # Diéguez-Aranda et al. 2009

            elif tree.specie == 66:  # Olea europaea

                wsw = 0.0114 * (tree.dbh ** 2) * tree.height
                wthickb = 0.0108 * (tree.dbh ** 2) * tree.height
                wb2_7 = 1.672 * tree.dbh
                wtbl = 0.0354 * (tree.dbh ** 2) + 1.187 * tree.height
                wr = 0.147 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 67:  # Ceratonia siliqua

                wsw = 0.142 * (tree.dbh ** 1.974)
                wthickb = 0.104 * (tree.dbh ** 2)
                wb2_7 = 0.0538 * (tree.dbh ** 2)
                wtbl = 0.151 * (tree.dbh ** 2) - 0.00740 * (tree.dbh ** 2) * tree.height
                wr = 0.335 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

            elif tree.specie == 71:  # Fagus sylvatica

                wsw = 0.0676 * (tree.dbh ** 2) + 0.0182 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 22.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.830 * ((tree.dbh - 22.5) ** 2) - 0.0248 * ((tree.dbh - 22.5) ** 2) * tree.height) * Z
                wb2_7 = 0.0792 * (tree.dbh ** 2)
                wthinb = 0.0930 * (tree.dbh ** 2) - 0.00226 * (tree.dbh ** 2) * tree.height
                wr = 0.106 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

                c_value = 0.467
                # Telmo et al., 2010

            elif tree.specie == 72:  # Castanea sativa

                wsw = 0.0142 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 12.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.223 * ((tree.dbh - 12.5) ** 2)) * Z
                wb2_7 = 0.230 * tree.dbh * tree.height
                wthinb = 0.221 * tree.dbh * tree.height
                wr = 0.0211 * (tree.dbh ** 2.804)
                # Ruiz-Peinado et al, 2012

                c_value = 0.471
                # Telmo et al., 2010

            # elif tree.specie == 95:  # Prunus avium

                # c_value = 0.486
                # Telmo et al., 2010

            elif tree.specie == 258:  # Populus x canadensis/euroamericana

                wsw = 0.0130 * (tree.dbh ** 2) * tree.height
                if tree.dbh <= 22.5:
                    Z = 0
                else:
                    Z = 1
                wthickb = (0.538 * ((tree.dbh - 22.5) ** 2) - 0.0130 * ((tree.dbh - 22.5) ** 2) * tree.height) * Z
                wb2_7 = 0.385 * (tree.dbh ** 2)
                wtbl = 0.0774 * (tree.dbh ** 2) - 0.00198 * (tree.dbh ** 2) * tree.height
                wr = 0.122 * (tree.dbh ** 2)
                # Ruiz-Peinado et al, 2012

                c_value = 0.478
                # Telmo et al., 2010

            elif tree.specie == 273:  # Betula alba

                wsw = 0.1485 * (tree.dbh ** 2.223)
                wsb = 0.03010 * (tree.dbh ** 2.186)
                wthickb = 1.515 * math.exp(0.09040 * tree.dbh)
                wb2_7 = 0.1374 * (tree.dbh ** 1.760)
                wthinb = 0.05 * (tree.dbh ** 1.618)
                wb05 = 0.03720 * (tree.dbh ** 1.581)
                wl = 0.03460 * (tree.dbh ** 1.645)
                wr = 1.042 * (tree.dbh ** 1.254)
                # Diéguez-Aranda et al. 2009

            # elif tree.specie == 475:  # Salix babylonica

                # c_value = 0.472
                # Telmo et al., 2010

            # elif tree.specie == 576:  # Acer pseudoplatanus

                # c_value = 0.468
                # Telmo et al., 2010

            # elif tree.specie == ---:  # Chlorophora excelsa

                # c_value = 0.507
                # Telmo et al., 2010

            # elif tree.specie == ---:  # Entandrophragma cylindricum

                # c_value = 0.478
                # Telmo et al., 2010

            # elif tree.specie == ---:  # Gossweilerodendron balsamiferum

                # c_value = 0.504
                # Telmo et al., 2010

            # elif tree.specie == ---:  # Bowdichia nitida

                # c_value = 0.523
                # Telmo et al., 2010

            # elif tree.specie == ---:  # Hymenaea courbaril

                # c_value = 0.483
                # Telmo et al., 2010


            # biomass and carbon by compartments
            ws = wsw + wsb + wswb + w_cork + wstb
            wb = wthickb + wb2_7 + wb2_t + wthinb + wb05 + wb05_7 + wb0_2 + wdb + wl + wtbl + wbl0_7
            wt = ws + wb + wr

            carbon_stem = ws * c_value
            carbon_branches = wb * c_value
            carbon_roots = wr * c_value
            carbon = carbon_stem + carbon_branches + carbon_roots

            # cases when carbon is calculated by types of wood instead of a c_value
            if carbon_bark != 0 and carbon_heartwood != 0 and carbon_sapwood != 0:
                carbon = carbon_bark + carbon_heartwood + carbon_sapwood


            # define features and values as tuples
            features_and_values = [
                ('wsw', wsw),
                ('wsb', wsb),
                ('wswb', wswb),
                ('w_cork', w_cork),
                ('wthickb', wthickb),
                ('wstb', wstb),
                ('wb2_7', wb2_7),
                ('wb2_t', wb2_t),
                ('wthinb', wthinb),
                ('wb05', wb05),
                ('wb05_7', wb05_7),
                ('wb0_2', wb0_2),
                ('wdb', wdb),
                ('wl', wl),
                ('wtbl', wtbl),
                ('wbl0_7', wbl0_7),
                ('ws', ws),
                ('wb', wb),
                ('wr', wr),
                ('wt', wt),
                ('carbon_heartwood', carbon_heartwood),
                ('carbon_sapwood', carbon_sapwood),
                ('carbon_bark', carbon_bark),
                ('carbon_stem', carbon_stem),
                ('carbon_branches', carbon_branches),
                ('carbon_roots', carbon_roots),
                ('carbon', carbon)
            ]

            # iterate over the list of tuples and add values to the 'tree' object
            for feature, value in features_and_values:
                if value == 0:
                    value = ''  # '' is more understandably than 0 when no equation is available
                if feature in TREE_VARS:  # if the feature is in the list of variables, add it to the tree object
                    tree.add_value(feature, value)

        except Exception:
            self.catch_model_exception()


    def set_w_carbon_plot(plot: Plot, list_of_trees):
        """
        Function to calculate biomass and carbon variables for each plot based on trees information.
        It assigns the values to the tree object for the corresponding features available, returning '' if not available.
        :param plot: Plot object
        :param list_of_trees: list of Tree objects
        """

        try:  # errors inside that construction will be announced

            # initialize variables
            plot_wsw = plot_wsb = plot_wswb = plot_w_cork = plot_wthickb = plot_wstb = plot_wb2_7 = plot_wb2_t = \
                plot_wthinb = plot_wb05 = plot_wb05_7 = plot_wb0_2 = plot_wdb = plot_wl = plot_wtbl = plot_wbl0_7 = \
                plot_ws = plot_wb = plot_wr = plot_wt = plot_carbon_heartwood = plot_carbon_sapwood = plot_carbon_bark = \
                plot_carbon_stem = plot_carbon_branches = plot_carbon_roots = plot_carbon = 0

            # define attributes and plot attributes
            attributes = ['wsw', 'wsb', 'wswb', 'w_cork', 'wthickb', 'wstb', 'wb2_7', 'wb2_t', 'wthinb', 'wb05',
                          'wb05_7', 'wb0_2', 'wdb', 'wl', 'wtbl', 'wbl0_7', 'ws', 'wb', 'wr', 'wt',
                          'carbon_heartwood', 'carbon_sapwood', 'carbon_bark', 'carbon_stem', 'carbon_branches',
                          'carbon_roots', 'carbon']

            plot_attributes = [plot_wsw, plot_wsb, plot_wswb, plot_w_cork, plot_wthickb, plot_wstb, plot_wb2_7,
                               plot_wb2_t, plot_wthinb, plot_wb05, plot_wb05_7, plot_wb0_2, plot_wdb, plot_wl,
                               plot_wtbl, plot_wbl0_7, plot_ws, plot_wb, plot_wr, plot_wt,
                               plot_carbon_heartwood, plot_carbon_sapwood, plot_carbon_bark, plot_carbon_stem,
                               plot_carbon_branches, plot_carbon_roots, plot_carbon]

            # for each tree, we are going to add the individual values to the plot value
            for tree in list_of_trees:

                # iterate over the list of attributes and plot attributes
                for attr, plot_attr, n in zip(attributes, plot_attributes, range(len(plot_attributes))):
                    if attr in TREE_VARS:  # if the attribute is in the list of variables, add it to the plot object
                        value = getattr(tree, attr, '')
                        if value != '':  # if the value is not empty, add it to the plot attribute
                            plot_attr += value * tree.expan / 1000
                            plot_attributes[n] = plot_attr  # update the plot attribute
                        else:
                            plot_attributes[n] = plot_attr  # previous value is maintained


            # define features and values as tuples
            features_and_values = [
                ('WSW', plot_attributes[0]),
                ('WSB', plot_attributes[1]),
                ('WSWB', plot_attributes[2]),
                ('W_CORK', plot_attributes[3]),
                ('WTHICKB', plot_attributes[4]),
                ('WSTB', plot_attributes[5]),
                ('WB2_7', plot_attributes[6]),
                ('WB2_T', plot_attributes[7]),
                ('WTHINB', plot_attributes[8]),
                ('WB05', plot_attributes[9]),
                ('WB05_7', plot_attributes[10]),
                ('WB0_2', plot_attributes[11]),
                ('WDB', plot_attributes[12]),
                ('WL', plot_attributes[13]),
                ('WTBL', plot_attributes[14]),
                ('WBL0_7', plot_attributes[15]),
                ('WS', plot_attributes[16]),
                ('WB', plot_attributes[17]),
                ('WR', plot_attributes[18]),
                ('WT', plot_attributes[19]),
                ('CARBON_HEARTWOOD', plot_attributes[20]),
                ('CARBON_SAPWOOD', plot_attributes[21]),
                ('CARBON_BARK', plot_attributes[22]),
                ('CARBON_STEM', plot_attributes[23]),
                ('CARBON_BRANCHES', plot_attributes[24]),
                ('CARBON_ROOTS', plot_attributes[25]),
                ('CARBON', plot_attributes[26])
            ]

            # iterate over the list of tuples and add values to the 'plot' object
            for feature, plot_attr in features_and_values:
                if plot_attr == 0:
                    plot_attr = ''  # '' is more understandably than 0 when no equation is available
                if feature in PLOT_VARS:  # if the feature is in the list of variables, add it to the plot object
                    plot.add_value(feature, plot_attr)

        except Exception:
            self.catch_model_exception()


    def set_w_carbon_plot_sp(plot: Plot, list_of_trees):
        """
        Function to calculate biomass and carbon variables for each plot based on trees information and split by species.
        It assigns the values to the tree object for the corresponding features available, returning '' if not available.
        :param plot: Plot object
        :param list_of_trees: list of Tree objects
        """

        try:  # errors inside that construction will be announced

            # initialize variables
            plot_ws_sp1 = plot_wb_sp1 = plot_wr_sp1 = plot_wt_sp1 = \
                plot_carbon_stem_sp1 = plot_carbon_branches_sp1 = plot_carbon_roots_sp1 = plot_carbon_sp1 = 0
            plot_ws_sp2 = plot_wb_sp2 = plot_wr_sp2 = plot_wt_sp2 = \
                plot_carbon_stem_sp2 = plot_carbon_branches_sp2 = plot_carbon_roots_sp2 = plot_carbon_sp2 = 0
            plot_ws_sp3 = plot_wb_sp3 = plot_wr_sp3 = plot_wt_sp3 = \
                plot_carbon_stem_sp3 = plot_carbon_branches_sp3 = plot_carbon_roots_sp3 = plot_carbon_sp3 = 0

            # define attributes and plot attributes
            tree_attributes = ['ws', 'wb', 'wr', 'wt', 'carbon_stem', 'carbon_branches', 'carbon_roots', 'carbon']

            attributes_sp1 = ['WS_SP1', 'WB_SP1', 'WR_SP1', 'WT_SP1',
                          'CARBON_STEM_SP1', 'CARBON_BRANCHES_SP1', 'CARBON_ROOTS_SP1', 'CARBON_SP1']
            attributes_sp2 = ['WS_SP2', 'WB_SP2', 'WR_SP2', 'WT_SP2',
                            'CARBON_STEM_SP2', 'CARBON_BRANCHES_SP2', 'CARBON_ROOTS_SP2', 'CARBON_SP2']
            attributes_sp3 = ['WS_SP3', 'WB_SP3', 'WR_SP3', 'WT_SP3',
                            'CARBON_STEM_SP3', 'CARBON_BRANCHES_SP3', 'CARBON_ROOTS_SP3', 'CARBON_SP3']

            # define plot attributes
            plot_attributes_sp1 = [plot_ws_sp1, plot_wb_sp1, plot_wr_sp1, plot_wt_sp1,
                                   plot_carbon_stem_sp1, plot_carbon_branches_sp1, plot_carbon_roots_sp1, plot_carbon_sp1]
            plot_attributes_sp2 = [plot_ws_sp2, plot_wb_sp2, plot_wr_sp2, plot_wt_sp2,
                                   plot_carbon_stem_sp2, plot_carbon_branches_sp2, plot_carbon_roots_sp2, plot_carbon_sp2]
            plot_attributes_sp3 = [plot_ws_sp3, plot_wb_sp3, plot_wr_sp3, plot_wt_sp3,
                                   plot_carbon_stem_sp3, plot_carbon_branches_sp3, plot_carbon_roots_sp3, plot_carbon_sp3]


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
            self.catch_model_exception()
