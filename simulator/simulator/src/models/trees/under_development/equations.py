#!/usr/bin/env python3
#
# Python structure developed by iuFOR and Sngular.
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

from models import TreeModel
from data import Distribution
from data import DESC
from data import Plot
from data import Tree
from data.general import Area, Model, Warnings
from scipy import integrate
from util import Tools
from data.variables import TREE_VARS, PLOT_VARS, AREA_VARS, MODEL_VARS, WARNING_VARS

import math
import sys
import logging
import numpy as np
import os

# Equations compilation model (Spain), version 01
# Written by iuFOR
# Sustainable Forest Management Research Institute UVa-INIA, iuFOR (dbhiversity of Valladolid-INIA)
# Higher Technical School of Agricultural Engineering, dbhiversity of Valladolid - Avd. Madrid s/n, 34004 Palencia (Spain)
# http://sostenible.palencia.uva.es/


class Equations(TreeModel):

    # Species and provenance regions organised in lists

    global Phalepensis_ar, Phalepensis_ar_cat, Pnigra_cat, Ppinaster_at_c, Ppinaster_at_i, Ppinaster_me_sim, Ppinea_and, Ppinea_cat, Ppinea_sc, Pradiata_gal, Psylvestris_sim
    global Fsylvatica, Qpetraea_pal, Qpyrenaica_cyl, Qrobur_gal, Qsuber_cat

    Fsylvatica = [10] #[]  # Fagus sylvatica
    Phalepensis_ar = [10] #[3, 4, 5, 6]  # Pinus halepensis - Aragón
    Phalepensis_ar_cat = [10] #[1, 2, 3, 4, 5, 6]  # Pinus halepensis - Aragón and Cataluña
    Pnigra_cat = [10] #[3, 4, 5]  # Pinus nigra - Cataluña
    Ppinaster_at_c = [10] #['1a']  # Pinus pinaster atlantica - Galicia coast
    Ppinaster_at_i = [10] #['1b']  # Pinus pinaster atlantica - Galicia inland
    Ppinaster_me_sim = [10] #[8, 9, 10, 11, 12, 13]  # Pinus pinaster mesogeensis - Sistema Ibérico Meridional
    Ppinea_and = [10] #[4, 5]  # Pinus pinea - West Andalucía
    Ppinea_cat = [10] #[6, 7]  # Pinus pinea - Cataluña
    Ppinea_sc = [10] #[1, 2]  # Pinus pinea - Sistema Central
    Pradiata_gal = [10] #[1, 2, 3, 4, 5]  # Pinus radiata - Galicia
    Psylvestris_sim = [10] #[8, 9, 12, 13, 14]  # Pinus sylvestris - Sistema Ibérico Meridional
    Qpetraea_pal = [10] #[4]  # Quercus petraea - North Palencia
    Qpyrenaica_cyl = [10] #[3, 4, 5, 6, 7, 8, 9, 11, 12]  # Quercus pyrenaica - Castilla y León
    Qrobur_gal = [10] #[1]  # Quercus robur - Galicia
    Qsuber_cat = [10] #[8, 9, 'Q']  # Quercus suber - Cataluña

    global P9010
    P9010 = 0  # define the variable that later we will use to calculate Pinus pinea height


    def __init__(self, configuration=None):
        super().__init__(name="Equations", version=1)


    def catch_model_exception(self):  # that Function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)


    def P9010_distribution(self, plot: Plot, tree: Tree):
        """
        That function is only needed on Pinus pinea model.
        It is needed to calculate the difference between the 90th and 10th percentiles from the diametric distribution (cm),
        which is a parameter useful on the h/d equation of Calama and Montero (2004).
        """

        try:
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


    def si(self, plot, tree):
        """
        Site Index calculation linked to Master Model.
        Function selection criteria depending to the specie and location, using inventory data.
        Sources are available on each single specie model.
        """

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    pass
            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    pass
                elif plot.prov_region in Ppinea_cat:
                    pass
                elif plot.prov_region in Ppinea_sc:
                    pass
            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    pass
                elif plot.prov_region in Phalepensis_ar_cat:
                    pass
            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    pass
            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    pass
                elif plot.prov_region in Ppinaster_at_i:
                    pass
                elif plot.prov_region in Ppinaster_me_sim:
                    pass
            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    pass
            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    pass
            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    pass
            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    pass
            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    pass
            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    pass

        except Exception:
            self.catch_model_exception()


    def height(self, plot, tree):
        """
        Height calculation linked to Master Model.
        Function selection criteria depending to the specie and location, using inventory data.
        Sources are available on each single specie model.
        """

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    ht = (13 + (27.0392 + 1.4853 * plot.dominant_h * 10 - 0.1437 * plot.qm_dbh * 10) * math.exp(-8.0048 / math.sqrt(tree.dbh * 10))) / 10
            
            elif tree.specie == 23:
                global P9010
                if plot.prov_region in Ppinea_and:
                    K = 1  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia

                elif plot.prov_region in Ppinea_cat:
                    K = 1  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia

                elif plot.prov_region in Ppinea_sc:
                    K = 0  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia

                if P9010 == 0:  # condition needed to only calculate that variable once
                    P9010 = Equations.P9010_distribution(self, plot, tree)  # that line is needed to activate the calculation of P9010, needed later

                ht = 1.3 + math.exp((1.7306 + 0.0882 * plot.dominant_h - 0.0062 * P9010 - 0.0936*K) + ((- 25.2776 + 1.6999 * math.log(plot.density) + 4.743*K) / (tree.dbh + 1)))

            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    a = 2.5511
                    b = pow(1.3, a)
                    ht = pow(b + (pow(plot.dominant_h, a) - b)*(1 - math.exp(-0.025687 * tree.dbh)) / (1 - math.exp(-0.025687 * plot.dominant_dbh)), 1/a)
                    
                elif plot.prov_region in Phalepensis_ar_cat:
                    a = 2.5511
                    b = pow(1.3, a)
                    ht = pow(b + (pow(plot.dominant_h, a) - b)*(1 - math.exp(-0.025687 * tree.dbh)) / (1 - math.exp(-0.025687 * plot.dominant_dbh)), 1/a)
                    
            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    beta6 = 0.4666
                    beta7 = -0.4356
                    beta8 = 0.0092
                    ht = 1.3 + (plot.dominant_h - 1.3)*((tree.dbh/plot.dominant_dbh)**(beta6 + beta7*(tree.dbh/plot.dominant_dbh) + beta8*plot.si))

            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    I = 1  # dummy variable which assumes a value of 0 for the interior ecoregion and 1 for the coastal ecoregion.
                    ht = (1.3**(1.894 + 1.469*I) + (plot.dominant_h**(1.894 + 1.469*I) - 1.3**(1.894 + 1.469*I)) * ((1 - math.exp(-(0.04611 - 0.04734*I)*tree.dbh)) / (1 - math.exp(-(0.04611 - 0.04734*I)*plot.dominant_dbh))))**(1/(1.894 + 1.469*I))

                elif plot.prov_region in Ppinaster_at_i:
                    I = 0  # dummy variable which assumes a value of 0 for the interior ecoregion and 1 for the coastal ecoregion.
                    ht = (1.3**(1.894 + 1.469*I) + (plot.dominant_h**(1.894 + 1.469*I) - 1.3**(1.894 + 1.469*I)) * ((1 - math.exp(-(0.04611 - 0.04734*I)*tree.dbh)) / (1 - math.exp(-(0.04611 - 0.04734*I)*plot.dominant_dbh))))**(1/(1.894 + 1.469*I))

                elif plot.prov_region in Ppinaster_me_sim:
                    ht = (13 + (32.3287 + 1.6688 * plot.dominant_h * 10 - 0.1279 * plot.qm_dbh * 10) * math.exp(-11.4522 / math.sqrt(tree.dbh * 10))) / 10

            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    a = 0.02961
                    b = 1.633
                    ht = (1.3**b + (plot.dominant_h**b - 1.3**b) * ((1 - math.exp(-a*tree.dbh)) / (1 - math.exp(-a*plot.dominant_dbh))))**(1/b)

            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    ht = (1.3**(1.067) + (plot.dominant_h**(1.067) - 1.3**(1.067)) * ((1 - math.exp(-0.06160*tree.dbh)) / (1 - math.exp(-0.06160*plot.dominant_dbh)))**(1/1.067))

            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    ht = 0

            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    ht = 1.3 + (3.099 - 0.00203 * plot.basal_area + 1.02491 * plot.dominant_h * math.exp(-8.5052 / tree.dbh))

            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    ht = 1.3 + (plot.dominant_h - 1.3)*((tree.dbh/plot.dominant_dbh)**0.4898)

            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    ht = 1.732*(tree.dbh**0.769)

        except Exception:
            self.catch_model_exception()

        return ht


    def crown(self, plot, tree):
        """
        Crown variables calculation linked to Master Model.
        Function selection criteria depending to the specie and location, using inventory data.
        Sources are available on each single specie model.
        """ 

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    tree.add_value('hlcw', tree.height / (1 + math.exp(float(-0.0012 * tree.height * 10 - 0.0102 * tree.bal - 0.0168 * plot.basal_area))))
                    tree.add_value('hcb', tree.hlcw / (1 + math.exp(float(1.2425 * (plot.basal_area/(tree.height*10)) + 0.0047 * plot.basal_area - 0.5725 * math.log(plot.basal_area) - 0.0082 * tree.bal))))
                    tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
                    tree.add_value('lcw', (1 / 10.0) * (0.2518 * tree.dbh * 10) * math.pow(tree.cr, (0.2386 + 0.0046 * (tree.height - tree.hcb) * 10)))  # maximum crown-width (m)

            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    pass
                elif plot.prov_region in Ppinea_cat:
                    pass
                elif plot.prov_region in Ppinea_sc:
                    pass
            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    tree.add_value('hcb', tree.height / (1 + math.exp(-0.82385 + 4.039408*plot.hart*0.01 - 0.01969*plot.si - 0.594323*tree.bal/plot.basal_area)))  # basal crown height (m) calculation
                    tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
                    tree.add_value('lcw', 0.672001 * pow(tree.dbh, 0.880032) * pow(tree.height, -0.60344) * math.exp(0.057872 * tree.height))  # maximum crown-width (m)

                elif plot.prov_region in Phalepensis_ar_cat:
                    tree.add_value('hcb', tree.height / (1 + math.exp(-0.82385 + 4.039408*plot.hart*0.01 - 0.01969*plot.si - 0.594323*tree.bal/plot.basal_area)))  # basal crown height (m) calculation
                    tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
                    tree.add_value('lcw', 0.672001 * pow(tree.dbh, 0.880032) * pow(tree.height, -0.60344) * math.exp(0.057872 * tree.height))  # maximum crown-width (m)

            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    pass
            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    
                    if tree.hcb != 0:

                        c0 = 1.297
                        c1 = 0
                        c2 = - 0.08765
                        c3 = 3.972
                        e0 = 0.5156
                        e1 = - 1.712
                        e2 = - 0.01789

                        HBLF = tree.hcb
                        HT = tree.height
                        d = tree.dbh
                        LCR = ((math.exp(-0.9438 + 0.8371*math.log(d))) / 2) * (((HT - HBLF) / HT)**(e0 + e1/d + e2*(HT - HBLF)))
                        HLCR = HBLF + (HT - HBLF) / (1 + math.exp(c0 + c1*HT + c2*(HT - HBLF) + c3/d))
                        
                        tree.add_value('lcw', LCR)  # maximum crown-width (m)
                        tree.add_value('hlcw', HLCR)  # height maximum crown-width (m)
                        tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)

                    else:
                        pass

                elif plot.prov_region in Ppinaster_at_i:

                    if tree.hcb != 0:

                        c0 = 1.297
                        c1 = 0
                        c2 = - 0.08765
                        c3 = 3.972
                        e0 = 0.5156
                        e1 = - 1.712
                        e2 = - 0.01789

                        HBLF = tree.hcb
                        HT = tree.height
                        d = tree.dbh
                        LCR = ((math.exp(-0.9438 + 0.8371*math.log(d))) / 2) * (((HT - HBLF) / HT)**(e0 + e1/d + e2*(HT - HBLF)))
                        HLCR = HBLF + (HT - HBLF) / (1 + math.exp(c0 + c1*HT + c2*(HT - HBLF) + c3/d))
                        
                        tree.add_value('lcw', LCR)  # maximum crown-width (m)
                        tree.add_value('hlcw', HLCR)  # height maximum crown-width (m)
                        tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)

                    else:
                        pass

                elif plot.prov_region in Ppinaster_me_sim:
                    tree.add_value('hlcw', tree.height / (1 + math.exp(float(-0.0041 * tree.height * 10 - 0.0093 * tree.bal - 0.0123 * plot.basal_area))))  # height of the larguest crown width (m) calculation
                    tree.add_value('hcb', tree.hlcw / (1 + math.exp(float(0.0078 * plot.basal_area - 0.5488 * math.log(plot.basal_area) - 0.0085 * tree.bal))))  # larguest crown width (m) calculation
                    tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
                    tree.add_value('lcw', (1 / 10.0) * (0.1826 * tree.dbh * 10) * math.pow(tree.cr, (0.1594 + 0.0014 * (tree.height - tree.hcb) * 10)))  # maximum crown-width (m)

            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    tree.add_value('hlcw', - 4.7570 - 0.08092*tree.dbh + 0.6408*tree.height + 0.1881*tree.tree_age + 0.1998*plot.si)
                    tree.add_value('hcb', - 3.265 - 0.1415*tree.dbh + 0.5117*tree.height + 0.1430*tree.tree_age + 0.1691*plot.dominant_h)
                    tree.add_value('cr', 1 - tree.hcb / tree.height)  # crown ratio (%)
                    tree.add_value('lcw', 0.06185*(tree.dbh**1.185)*math.exp(-0.009319*plot.basal_area -0.009502*plot.age))  # maximum crown-width (m)

            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    pass
            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    pass
            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    pass
            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    tree.add_value('lcw', (0.2416 + 0.0013*plot.qm_dbh)*tree.dbh - 0.0015*(tree.dbh**2))  # largest crown width (m)

            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    pass

        except Exception:
            self.catch_model_exception()


    def vol(self, plot, tree, dob, dub, hr):
        """
        Volume calculation linked to Master Model.
        Function selection criteria depending to the specie and location, using inventory data.
        Sources are available on each single specie model.
        """

        try:

            #-----------------------------------VOLUME_OVER_BARK-----------------------------------------#

            if not isinstance(dob, bool):
                fwb = (dob / 20) ** 2  # radius^2 using dob (dm2)
                tree.add_value('vol', math.pi * tree.height * 10 * integrate.simps(fwb, hr))  # volume over bark using simpson integration (dm3)
                tree.add_value('vol_ha', tree.vol * tree.expan / 1000)  # volume over bark per ha (m3/ha)

            #-----------------------------------VOLUME_UNDER_BARK-----------------------------------------#

            if not isinstance(dub, bool) and tree.specie != 46:            
                fub = (dub / 20) ** 2  # radius^2 using dub (dm2)
                tree.add_value('bole_vol', math.pi * tree.height * 10 * integrate.simps(fub, hr))  # volume under bark using simpson integration (dm3)

            #-----------------------------------VOLUME_BARK-----------------------------------------#

            if not isinstance(dob, bool) and not isinstance(dub, bool) and tree.specie != 46:
                tree.add_value('bark_vol', tree.vol - tree.bole_vol)  # bark volume (dm3)

            #-----------------------------------QUERCUS SUBER VOLUME-----------------------------------------#

            if tree.specie == 46:
                if plot.prov_region in Qsuber_cat:

                    tree.add_value('bole_vol', 0.000115*(tree.dbh**2.147335) * 1000)  # volume under bark (dm3)

                    if isinstance(tree.bark, float) and isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float):
                        tree.add_value('bark_vol', (tree.bark/100) * (tree.h_debark*10) * ((tree.dbh + tree.dbh_oc) / 20))  # cork fresh volume (dm3)
                        tree.add_value('vol', tree.bole_vol + tree.bark_vol)
                        tree.add_value('vol_ha', tree.vol * tree.expan / 1000)  # volume over bark per ha (m3/ha)

        except Exception:
            self.catch_model_exception()


    def merchantable(self, plot, tree):
        """
        Merchantable classes calculation linked to Master Model.
        Function selection criteria depending to the specie and location, using inventory data.
        Sources are available on each single specie model.
        """

        if tree.height != 0:  # only calculate that to the trees with height data
            ht = tree.height
        else:  # return an empty list to the trees without height data
            return []  
        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    class_conditions = [['unwinding', 3/ht, 40, 160], ['veneer', 3/ht, 40, 160], ['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]] 
            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]] 
                elif plot.prov_region in Ppinea_cat:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]] 
                elif plot.prov_region in Ppinea_sc:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]] 
            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]
                elif plot.prov_region in Phalepensis_ar_cat:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]]
            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['post', 6/ht, 15, 28], ['stake', 1.8/ht, 6, 16], ['chips', 1/ht, 5, 1000000]]
            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
                elif plot.prov_region in Ppinaster_at_i:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
                elif plot.prov_region in Ppinaster_me_sim:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]] 
            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]] 
            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    class_conditions = [['saw_big', 2.5/ht, 40, 200], ['saw_small', 2.5/ht, 25, 200], ['saw_canter', 2.5/ht, 15, 28], ['chips', 1/ht, 5, 1000000]]
            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    class_conditions = [['saw_big', 2.5 / ht, 40, 200], ['saw_small', 2.5 / ht, 25, 200], ['saw_canter', 2.5 / ht, 15, 28], ['chips', 1 / ht, 5, 1000000]] 

        except Exception:
            self.catch_model_exception()

        return class_conditions


    def biomass(self, plot, tree):
        """
        Biomass calculation linked to Master Model.
        Function selection criteria depending to the specie and location, using inventory data.
        Sources are available on each single specie model.
        """

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:

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
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:

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
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

                elif plot.prov_region in Ppinea_cat:

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
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

                elif plot.prov_region in Ppinea_sc:

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
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:

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

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

                elif plot.prov_region in Phalepensis_ar_cat:

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

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:

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

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:

                    wstb = 0.3882 + 0.01149*(tree.dbh**2)*tree.height
                    wsb = 0.007900*(tree.dbh**2.098)*(tree.height**0.4660)
                    wb2_7 = 3.202 - 0.01484*(tree.dbh**2) - 0.4228*tree.height + 0.00279*(tree.dbh**2)*tree.height
                    wthinb = 0.09781*(tree.dbh**2.288)*(tree.height**-0.9648) 
                    wb05 = 0.001880*(tree.dbh**2.154)
                    wl = 0.005*(tree.dbh**2.383)
                    wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl

                    tree.add_value('wsw', 0)  # wsw = stem wood (kg)
                    tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', 0)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', wl)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', 0)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

                elif plot.prov_region in Ppinaster_at_i:

                    wstb = 0.3882 + 0.01149*(tree.dbh**2)*tree.height
                    wsb = 0.007900*(tree.dbh**2.098)*(tree.height**0.4660)
                    wb2_7 = 3.202 - 0.01484*(tree.dbh**2) - 0.4228*tree.height + 0.00279*(tree.dbh**2)*tree.height
                    wthinb = 0.09781*(tree.dbh**2.288)*(tree.height**-0.9648) 
                    wb05 = 0.001880*(tree.dbh**2.154)
                    wl = 0.005*(tree.dbh**2.383)
                    wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl

                    tree.add_value('wsw', 0)  # wsw = stem wood (kg)
                    tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', 0)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', wl)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', 0)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

                elif plot.prov_region in Ppinaster_me_sim:

                    wsw = 0.0278 * (tree.dbh ** 2.115) * (tree.height ** 0.618)
                    wb2_t = 0.000381 * (tree.dbh ** 3.141)
                    wtbl = 0.0129 * (tree.dbh ** 2.320)
                    wr = 0.00444 * (tree.dbh ** 2.804)
                    wt = wsw + wb2_t + wtbl + wr

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', 0)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', 0)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', wb2_t)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:

                    wstb = 0.01230*(tree.dbh**1.604)*(tree.height**1.413)
                    wsb = 0.003600*(tree.dbh**2.656)
                    wb2_7 = 1.938 + 0.001065*(tree.dbh**2)*tree.height
                    wthinb = 0.03630*(tree.dbh**2.609)*(tree.height**(-0.9417)) 
                    wb05 = 0.007800*(tree.dbh**1.961)
                    wl = 0.04230*(tree.dbh**1.714)
                    wr = 0.06174*(tree.dbh**2.144)
                    wt = wstb + wsb + wb2_7 + wthinb + wb05 + wl + wr

                    tree.add_value('wsw', 0)  # wsw = stem wood (kg)
                    tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', 0)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', wl)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
       
                    wsw = -5.714 + 0.01823*(tree.dbh**2) * tree.height
                    wsb = -1.500 + 0.03154*(tree.dbh**2) + 0.001110 * (tree.dbh**2) * tree.height
                    wthickb = 3.427e-9*(((tree.dbh**2) * tree.height) ** 2.310)
                    wb2_7 = 4.268 + 0.003410*(tree.dbh**2) * tree.height
                    wthinb = 0.03851*(tree.dbh**1.784) + 1.379 
                    wb05 = 0.00024*(tree.dbh**2) * tree.height
                    wl = 0.01985*(((tree.dbh**2) * tree.height) ** 0.7375)
                    wr = 0.01160*((tree.dbh**2)*tree.height) ** 0.9625
                    wt = wsw + wsb + wb2_7 + wthickb + wthinb + wb05 + wl + wr

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', wsb)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', wb05)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', wl)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:

                    wstb = 0.001333*(tree.dbh**2)*tree.height
                    wb2_7 = 0.006531*(tree.dbh**2)*tree.height - 0.07298*tree.dbh*tree.height
                    wthinb = 0.023772*(tree.dbh**2)*tree.height
                    wt = wstb + wb2_7 + wthinb

                    tree.add_value('wsw', 0)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', 0)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', 0)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:

                    wstb = 0.0261 * (tree.dbh ** 2) * tree.height
                    wb2_7 = - 0.0260 * (tree.dbh ** 2) + 0.536 * tree.height + 0.00538 * (tree.dbh ** 2) * tree.height
                    wthinb = 0.898 * tree.dbh - 0.445 * tree.height
                    wr = 0.143 * (tree.dbh ** 2)
                    wt = wstb + wb2_7 + wthinb + wr

                    tree.add_value('wsw', 0)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', 0)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', wstb)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:

                    wsw = 0.00525*(tree.dbh**2)*tree.height + 0.278*tree.dbh*tree.height
                    wthickb = 0.0135*(tree.dbh**2)*tree.height
                    wb2_7 = 0.127*tree.dbh*tree.height
                    wtbl = 0.0463*tree.dbh*tree.height
                    wr = 0.0829*(tree.dbh**2)
                    wt = wsw + wb2_7 + wthickb + wtbl + wr

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    # tree.add_value('w_cork', w_cork)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', 0)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', wtbl)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)

                    if isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float) and isinstance(tree.nb, float):

                        pbhoc = (tree.dbh_oc*math.pi) / 100  # perimeter at breast height outside cork (m)
                        pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
                        shs = tree.h_debark  # stripped height in the stem (m)
                        nb = tree.nb + 1  # number of stripped main bough + 1

                        if tree.cork_cycle == 0:  # To use inmediately before the stripping process
                            if nb == 1:
                                tree.add_value('w_cork', math.exp(2.3665 + 2.2722*math.log(pbhoc) + 0.4473*math.log(shs)))
                            else:
                                tree.add_value('w_cork', math.exp(2.1578 + 1.5817*math.log(pbhoc) + 0.5062*math.log(nb) + 0.6680*math.log(shs)))
                        
                        elif tree.cork_cycle == 1:  # To use after the stripping process or in a intermediate age of the cork cycle production
                            if nb == 1:
                                tree.add_value('w_cork', math.exp(2.7506 + 1.9174*math.log(pbhic) + 0.4682*math.log(shs)))
                            else:
                                tree.add_value('w_cork', math.exp(2.2137 + 0.9588*math.log(shs) + 0.6546*math.log(nb)))

                    elif isinstance(tree.h_debark, float) and isinstance(tree.dbh_oc, float) and not isinstance(tree.nb, float):

                        pbhoc = (tree.dbh_oc*math.pi) / 100  # perimeter at breast height outside cork (m)
                        pbhic = tree.normal_circumference / 100  # perimeter at breast height inside cork (m)
                        shs = tree.h_debark  # stripped height in the stem (m)
                        nb = 1  # number of stripped main bough + 1

                        if tree.cork_cycle == 0:  # To use inmediately before the stripping process
                            tree.add_value('w_cork', math.exp(2.3665 + 2.2722*math.log(pbhoc) + 0.4473*math.log(shs)))
                        
                        elif tree.cork_cycle == 1:  # To use after the stripping process or in a intermediate age of the cork cycle production
                            tree.add_value('w_cork', math.exp(2.7506 + 1.9174*math.log(pbhic) + 0.4682*math.log(shs)))
                    else:
                        
                        tree.add_value('w_cork', 0)

            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:

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

                    tree.add_value('wsw', wsw)  # wsw = stem wood (kg)
                    tree.add_value('wsb', 0)  # wsb = stem bark (kg)
                    tree.add_value('w_cork', 0)   # fresh cork biomass (kg)
                    tree.add_value('wthickb', wthickb)  # wthickb = Thick branches > 7 cm (kg)
                    tree.add_value('wstb', 0)  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
                    tree.add_value('wb2_7', wb2_7)  # wb2_7 = branches (2-7 cm) (kg)
                    tree.add_value('wb2_t', 0)  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
                    tree.add_value('wthinb', wthinb)  # wthinb = Thin branches (2-0.5 cm) (kg)
                    tree.add_value('wb05', 0)  # wb05 = thinnest branches (< 0.5 cm) (kg)
                    tree.add_value('wl', 0)  # wl = leaves (kg)
                    tree.add_value('wtbl', 0)  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
                    tree.add_value('wbl0_7', 0)  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
                    tree.add_value('wr', wr)  # wr = roots (kg)
                    tree.add_value('wt', wt)  # wt = total biomass (kg)


        except Exception:
            self.catch_model_exception()


    def survival(self, time: int, plot: Plot, tree: Tree):
        """
        Survive function. The trees that are death appear on the output with "M" on the "State of the tree" column
        """

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    cvdbh = math.sqrt(pow(plot.qm_dbh, 2) - pow(plot.mean_dbh, 2)) / plot.mean_dbh
                    surv = (1 / (1 + math.exp(-6.8548 + (9.792 / tree.dbh) + 0.121 * tree.bal * cvdbh + 0.037 * plot.si)))

            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    surv = 1

                elif plot.prov_region in Ppinea_cat:
                    surv = 1

                elif plot.prov_region in Ppinea_sc:
                    surv = 1

            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    surv = 1 / (1 + math.exp(-6.5934 + 0.0305 * plot.basal_area + 5.6845 * tree.bal / plot.basal_area - 8.1523 * plot.hart))  # 10 years period change

                elif plot.prov_region in Phalepensis_ar_cat:
                    surv = 1 / (1 + math.exp(-6.5934 + 0.0305 * plot.basal_area + 5.6845 * tree.bal / plot.basal_area - 8.1523 * plot.hart))  # 10 years period change

            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    beta0 = -0.4070
                    beta1 = -0.0400
                    beta2 = 6.9900
                    surv = 1 / (1 + math.exp( - (beta0 + beta1*tree.bal + beta2*(tree.height / plot.dominant_h))))

                    if surv <= 0:
                        surv = 0

            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    surv = 1

                elif plot.prov_region in Ppinaster_at_i:
                    surv = 1
                    
                elif plot.prov_region in Ppinaster_me_sim:
                    surv = 1 - (1 / (1 + math.exp(2.0968 + (4.7358 * tree.dbh / plot.qm_dbh) - 0.0012 * plot.si * plot.basal_area)))
                    if surv <= 0:
                        surv = 0

            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    BALMOD = (1 - (1 - (tree.bal/plot.basal_area))) / plot.hart
                    surv = 1 / (1 + math.exp(-2.093 - 3.214*(tree.dbh/plot.qm_dbh) - 0.001096*(tree.dbh**2) + 0.03703*plot.basal_area - 0.07873*plot.dominant_h + 0.3036*BALMOD))
                    
            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    surv = 1
                    
            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    surv = 1
                    
            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    mortality = 1 / (1 + math.exp(1.3286 - 9.791 / tree.dbh + 3.5383 * tree.height / plot.dominant_h))
                    surv = 1 - mortality

            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    surv = 1
                    
            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    surv = 1
                    
        except Exception:
            self.catch_model_exception()

        return surv


    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        """
        Function that rdbh the diameter and height growing equations
        """

        global P9010  # the explanation of that variable is on P9010_distribution function
        P9010 = 0  # leave the variable value as 0 to calculate it again on that execution

        try:

            new_tree.sum_value('tree_age', time)

            if old_tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:

                    if plot.si == 0:
                        dbhg5: float = 0
                    else:
                        dbhg5: float = math.exp(-0.37110 + 0.2525 * math.log(old_tree.dbh * 10) + 0.7090 * math.log((old_tree.cr + 0.2) / 1.2) + 0.9087 * math.log(plot.si) - 0.1545 * math.sqrt(plot.basal_area) - 0.0004 * (old_tree.bal * old_tree.bal / math.log(old_tree.dbh * 10)))
                    new_tree.sum_value("dbh", dbhg5 / 10)


                    if dbhg5 == 0:
                        htg5: float = 0
                    else:
                        htg5: float = math.exp(3.1222 - 0.4939 * math.log(dbhg5 * 10) + 1.3763 * math.log(plot.si) - 0.0061 * old_tree.bal + 0.1876 * math.log(old_tree.cr))
                    new_tree.sum_value("height", htg5 / 100)

            elif old_tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    cat = 0  # cat = 1 if the analysis is for Catalonia; 0 for Spain in general
                    K = 1  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia

                elif plot.prov_region in Ppinea_cat:
                    cat = 1  # cat = 1 if the analysis is for Catalonia; 0 for Spain in general
                    K = 1  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia

                elif plot.prov_region in Ppinea_sc:
                    cat = 0  # cat = 1 if the analysis is for Catalonia; 0 for Spain in general
                    K = 0  # 0 for Central Spain in general; 1 for Catalonia and West Andalusia

                if plot.si == 0:
                    dbhg5 = 0
                else:
                    dbhg5 = math.exp(2.2451 - 0.2615 * math.log(old_tree.dbh) - 0.0369 * plot.dominant_h - 0.1368 * math.log(plot.density) + 0.0448 * plot.si + 0.1984 * (old_tree.dbh / plot.qm_dbh) - 0.5542 * cat + 0.0277 * cat * plot.si) - 1
                new_tree.sum_value("dbh", dbhg5)

                # height calculation is a little bit special, so it will be calculated in another function

            elif old_tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    
                    if plot.si == 0:
                        dbhg10 = 0
                    else:
                        dbhg10 = 0.906633 * math.exp(0.09701 * old_tree.dbh - 0.00111 * (old_tree.dbh ** 2) - 0.05201 * plot.basal_area + 0.050652 * plot.si - 0.09366 * old_tree.bal / plot.basal_area)
                        # dbhg5 = dbhg10*0.5  # that equation calculates diameter grow for 10 years, activate taht line if we want the calculation for 5 years
                    # new_tree.sum_value("dbh", dbhg5)
                    new_tree.sum_value("dbh", dbhg10)


                    if dbhg10 == 0:
                        ht = old_tree.height
                    else:
                        a = 2.5511
                        b = pow(1.3, a)
                        ht = pow(b + (pow(plot.dominant_h, a) - b) * (1 - math.exp(-0.025687 * new_tree.dbh)) / (1 - math.exp(-0.025687 * plot.dominant_dbh)), 1/a)
                    new_tree.add_value("height", ht)  # that equation calculates height using the new diameter; is not a growing equation

                elif plot.prov_region in Phalepensis_ar_cat:
                    
                    if plot.si == 0:
                        dbhg10 = 0
                    else:
                        dbhg10 = 0.906633 * math.exp(0.09701 * old_tree.dbh - 0.00111 * (old_tree.dbh ** 2) - 0.05201 * plot.basal_area + 0.050652 * plot.si - 0.09366 * old_tree.bal / plot.basal_area)
                        # dbhg5 = dbhg10*0.5  # that equation calculates diameter grow for 10 years, activate taht line if we want the calculation for 5 years
                    # new_tree.sum_value("dbh", dbhg5)
                    new_tree.sum_value("dbh", dbhg10)


                    if dbhg10 == 0:
                        ht = old_tree.height
                    else:
                        a = 2.5511
                        b = pow(1.3, a)
                        ht = pow(b + (pow(plot.dominant_h, a) - b) * (1 - math.exp(-0.025687 * new_tree.dbh)) / (1 - math.exp(-0.025687 * plot.dominant_dbh)), 1/a)
                    new_tree.add_value("height", ht)  # that equation calculates height using the new diameter; is not a growing equation

            elif old_tree.specie == 25:
                if plot.prov_region in Pnigra_cat:

                    beta0 = 4.8413
                    beta1 = -8.6610
                    beta2 = -0.0054
                    beta3 = -1.0160
                    beta4 = 0.0545
                    beta5 = -0.0035
                    dbhg5: float = beta0 + beta1/old_tree.dbh + beta2*old_tree.bal + beta3*math.log(plot.basal_area) + beta4*plot.si + beta5*plot.age
                    new_tree.sum_value("dbh", dbhg5)
                    

                    beta6 = 0.4666
                    beta7 = -0.4356
                    beta8 = 0.0092
                    htg5: float = 1.3 + (plot.dominant_h - 1.3)*((dbhg5/plot.dominant_dbh)**(beta6 + beta7*(dbhg5/plot.dominant_dbh) + beta8*plot.si))
                    new_tree.sum_value("height", htg5)

            elif old_tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    pass
                elif plot.prov_region in Ppinaster_at_i:
                    pass
                elif plot.prov_region in Ppinaster_me_sim:
                    
                    if plot.si == 0:
                        dbhg5 = 0  # math.exp(0.2030 * math.log(old_tree.dbh * 10) + 0.4414 * math.log((old_tree.cr + 0.2) / 1.2) + 0.8379 * math.log(1) - 0.1295 * math.sqrt(plot.basal_area) - 0.0007 * math.pow(old_tree.ba_ha,2) / math.log(old_tree.dbh * 10))
                    else:
                        dbhg5 = math.exp(
                            0.2030 * math.log(old_tree.dbh * 10) + 0.4414 * math.log((old_tree.cr + 0.2) / 1.2) + 0.8379 * math.log(
                                plot.si) - 0.1295 * math.sqrt(plot.basal_area) - 0.0007 * math.pow(old_tree.bal,2) / math.log(
                                old_tree.dbh * 10))

                    new_tree.sum_value("dbh", dbhg5 / 10)


                    if dbhg5 == 0:
                        htg5 = 0
                    else:
                        htg5: float = math.exp(
                            0.21603 + 0.40329 * math.log(dbhg5 / 2) - 1.12721 * math.log(old_tree.dbh * 10) + 1.18099 * math.log(
                                old_tree.height * 100) + 3.01622 * old_tree.cr)

                    new_tree.sum_value("height", htg5 / 100)

            elif old_tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    
                    BALMOD = (1 - (1 - (old_tree.bal/plot.basal_area))) / plot.hart
                    BAR = (old_tree.basal_area*0.01)/plot.basal_area  # is a basal area ratio (g/G, where g is the basal area of the tree (m2))

                    ig = 0.3674 * (old_tree.dbh**2.651) * (plot.basal_area**(-0.7540)) * math.exp(-0.05207*old_tree.tree_age - 0.05291*BALMOD -102*BAR)

                    dbhg1 = ((ig/math.pi) ** 0.5) * 2
                    new_tree.sum_value("dbh", dbhg1)  # annual diameter increment (cm)


                    RBA_D = ((old_tree.basal_area*0.01)/plot.basal_area) ** (old_tree.dbh/plot.qm_dbh)  # a ratio basal area-diameter ([g/G]d/Dg)

                    if plot.si == 0:
                        htg1: float = 0
                    else:
                        htg1 = 0.05287 * (old_tree.height**(-0.5733)) * (old_tree.dbh**0.5437) * (plot.si**1.084) * math.exp(-0.03242*old_tree.tree_age - 50.87*RBA_D)

                    new_tree.sum_value("height", htg1)  # annual height increment (m)


            elif old_tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    pass
            elif old_tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    pass
            elif old_tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    
                    if plot.si == 0:
                        dbhg10 = 0
                    else:
                        STR = 0  # su valor debe ser 1 cuando la masa esta en el estrato 1
                        dbhg10 = math.exp(0.8351 + 0.1273 * math.log(old_tree.dbh) - 0.00006 * (
                                    old_tree.dbh ** 2) - 0.01216 * old_tree.bal - 0.00016 * plot.density - 0.03386 * plot.dominant_h + 0.04917 * plot.si - 0.1991 * STR) - 1
                    new_tree.sum_value("dbh", dbhg10)  # growing equation developed to 10 years period


                    if dbhg10 == 0:
                        htg10 = old_tree.height
                    else:
                        htg10: float = 1.3 + (3.099 - 0.00203*plot.basal_area + 1.02491*plot.dominant_h * math.exp(-8.5052/new_tree.dbh))
                    new_tree.add_value("height", htg10) # ecuación de relación h/d, NO para el crecimiento

            elif old_tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    
                    if plot.si == 0:
                        idu = 0
                    else:
                        idu = 0.18 + 7.89/plot.density - 1.02/plot.si + 2.45/old_tree.dbh
                    new_tree.sum_value('dbh', idu)  # annual diameter increment under cork (cm)


                    h2 = 1.3 + (plot.dominant_h - 1.3)*((new_tree.dbh/plot.dominant_dbh)**0.4898)
                    new_tree.add_value('height', h2)  # height/diameter equation result (m)


                    t = old_tree.tree_age + 1  # years
                    Xo1 = 0.5*(math.log(old_tree.bark) - 0.57*math.log(1 - math.exp(-0.04*old_tree.tree_age)))
                    # Xo2 = math.sqrt((math.log(old_tree.bark) - 0.57*math.log(1 - math.exp(-0.04*old_tree.tree_age))**2 - 4*1.86*math.log(1 - math.exp(-0.04*old_tree.tree_age))))
                    Xo = Xo1 # +- Xo2

                    cork_2 = old_tree.bark*(((1 - math.exp(-0.04*t)) / (1 - math.exp(-0.04*old_tree.tree_age)))**((0.57+1.86)/Xo))
                    new_tree.sum_value('bark', cork_2)

            elif old_tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    pass

        #new_tree.add_value('basal_area', math.pi*(new_tree.dbh/2)**2)  # update basal area (cm2) 

        #self.vol(new_tree, plot)  # update volume variables (dm3)

        except Exception:
            self.catch_model_exception()


    def ingrowth(self, time: int, plot: Plot):
        """
        Ingrowth stand function.
        That function calculates the probability that trees are added to the plot, and if that probability is higher than a limit value, then basal area
        incorporated is calculated. The next function will order how to divide that basal area into the different diametric classes.
        """

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    pass
            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    pass
                elif plot.prov_region in Ppinea_cat:
                    pass
                elif plot.prov_region in Ppinea_sc:
                    pass
            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    pass
                elif plot.prov_region in Phalepensis_ar_cat:
                    pass
            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    pass
            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    pass
                elif plot.prov_region in Ppinaster_at_i:
                    pass
                elif plot.prov_region in Ppinaster_me_sim:
                    pass
            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    pass
            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    pass
            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    pass
            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    pass
            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    pass
            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    pass

        except Exception:
            self.catch_model_exception()


    def ingrowth_distribution(self, time: int, plot: Plot, area: float):
        """
        Tree diametric classes distribution
        That function must return a list with different sublists for each diametric class, where the conditions to ingrowth function are written
        That function has the aim to divide the ingrowth (added basal area of ingrowth) in different proportions depending on the orders given
        On the cases that a model hasn´t a good known distribution, just return None to share that ingrowth between all the trees of the plot
        """

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    pass
            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    pass
                elif plot.prov_region in Ppinea_cat:
                    pass
                elif plot.prov_region in Ppinea_sc:
                    pass
            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    pass
                elif plot.prov_region in Phalepensis_ar_cat:
                    pass
            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    pass
            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    pass
                elif plot.prov_region in Ppinaster_at_i:
                    pass
                elif plot.prov_region in Ppinaster_me_sim:
                    pass
            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    pass
            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    pass
            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    pass
            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    pass
            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    pass
            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    pass

        except Exception:
            self.catch_model_exception()


    def taper_over_bark(self, tree, plot, hr):
        """
        Function that returns the taper equation to calculate the diameter (cm, over bark) at different height
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually
        """

        try:

            taper_model = 0

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:
                    
                    ao = 0.000051
                    a1 = 1.845867
                    a2 = 1.045022
                    b1 = 0.000011
                    b2 = 0.000038
                    b3 = 0.000030
                    p1 = 0.093625
                    p2 = 0.763750
                    taper_model = 'Fang' 
                          
            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:

                    ao = 0.000067
                    a1 = 1.698754
                    a2 = 1.210604
                    b1 = 0.000006
                    b2 = 0.000033
                    b3 = 0.000026
                    p1 = 0.021072
                    p2 = 0.475953
                    taper_model = 'Fang' 

                elif plot.prov_region in Ppinea_cat:

                    ao = 0.000067
                    a1 = 1.698754
                    a2 = 1.210604
                    b1 = 0.000006
                    b2 = 0.000033
                    b3 = 0.000026
                    p1 = 0.021072
                    p2 = 0.475953
                    taper_model = 'Fang' 

                elif plot.prov_region in Ppinea_sc:

                    ao = 0.000067
                    a1 = 1.698754
                    a2 = 1.210604
                    b1 = 0.000006
                    b2 = 0.000033
                    b3 = 0.000026
                    p1 = 0.021072
                    p2 = 0.475953
                    taper_model = 'Fang' 

            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    
                    E = 100 * tree.height / tree.dbh
                    dob = (1 + 1.121163 * 2.7182818284**(-10.23293 * hr)) * 0.696362 * tree.dbh * pow(1 - hr, 1.266261 - (0.003553 * E) - 1.865418 * (1 - hr))

                elif plot.prov_region in Phalepensis_ar_cat:

                    E = 100 * tree.height / tree.dbh
                    dob = (1 + 1.121163 * 2.7182818284**(-10.23293 * hr)) * 0.696362 * tree.dbh * pow(1 - hr, 1.266261 - (0.003553 * E) - 1.865418 * (1 - hr))

            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:

                    ao = 0.000049
                    a1 = 1.982808
                    a2 = 0.905147
                    b1 = 0.000014
                    b2 = 0.000036
                    b3 = 0.000029
                    p1 = 0.091275
                    p2 = 0.781990
                    taper_model = 'Fang' 

            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:

                    ao = 3.974e-5
                    a1 = 1.876
                    a2 = 1.079
                    b1 = 1.003e-5
                    b2 = 3.695e-5
                    b3 = 2.910e-5
                    p1 = 0.1013
                    p2 = 0.7233
                    taper_model = 'Fang' 

                elif plot.prov_region in Ppinaster_at_i:

                    ao = 3.974e-5
                    a1 = 1.876
                    a2 = 1.079
                    b1 = 1.003e-5
                    b2 = 3.695e-5
                    b3 = 2.910e-5
                    p1 = 0.1013
                    p2 = 0.7233
                    taper_model = 'Fang' 

                elif plot.prov_region in Ppinaster_me_sim:

                    ao = 0.000048
                    a1 = 1.929098
                    a2 = 0.976356
                    b1 = 0.000010
                    b2 = 0.000035
                    b3 = 0.000033
                    p1 = 0.064157
                    p2 = 0.681476
                    taper_model = 'Fang'

            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:

                    ao = 4.851e-5
                    a1 = 1.883
                    a2 = 1.004
                    b1 = 8.702e-6
                    b2 = 3.302e-5
                    b3 = 2.899e-5
                    p1 = 0.06526
                    p2 = 0.6560
                    taper_model = 'Fang'

            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:

                    ao = 4.618e-5
                    a1 = 1.771
                    a2 = 1.165
                    b1 = 5.159e-6
                    b2 = 3.157e-5
                    b3 = 2.553e-5
                    p1 = 0.04025
                    p2 = 0.5184
                    taper_model = 'Fang'

            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                   
                    dbh = tree.dbh
                    ht = 1
                    dob = (1 + 0.558513*2.7182818284**(-25.933370*hr/ht))*(0.942294*dbh*((1 - hr/ht)**(1.312840 - 0.342491*(ht/dbh) - 1.239930*(1 - hr/ht))))

            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:

                    ao = 0.000051
                    a1 = 1.867810
                    a2 = 0.989625
                    b1 = 0.000007
                    b2 = 0.000030
                    b3 = 0.000032
                    p1 = 0.047757
                    p2 = 0.825279
                    taper_model = 'Fang'

            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    dob = False

            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:

                    ao = 0.000120
                    a1 = 2.036193
                    a2 = 0.799343
                    b1 = 0.000015
                    b2 = 0.000033
                    b3 = 0.005194
                    p1 = 0.074439
                    p2 = 0.873445
                    taper_model = 'Fang'



            if taper_model == 'Fang':

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


    def taper_under_bark(self, tree, plot, hr):
        """
        Function that returns the taper equation to calculate the diameter (cm, without bark) at different height
        ¡IMPORTANT! It is not used math.exp because of calculation error, we use the number "e" instead, wrote by manually
        """

        taper_model = 0

        try:

            if tree.specie == 21:
                if plot.prov_region in Psylvestris_sim:

                    dub = (1 + 0.3485 * 2.7182818284 ** (-23.9191 * hr)) * 0.7966 * tree.dbh * pow((1 - hr), (0.6094 - 0.7086 * (1 - hr)))

            elif tree.specie == 23:
                if plot.prov_region in Ppinea_and:
                    
                    beta1 = 1.0972
                    beta2 = -2.8505
                    H = tree.height*10  # dm
                    dubmm = tree.dbh * 10 * ((H - hr*H) / (H - 13)) + beta1 * (
                                ((H ** 1.5 - (hr*H) ** 1.5) * (hr*H - 13)) / H ** 1.5) + beta2 * (
                                       ((H - (hr*H)) ** 4) * (hr*H - 13) / (H ** 4))
                    dub = dubmm*0.1  # mm to cm

                elif plot.prov_region in Ppinea_cat:
                    
                    beta1 = 1.0972
                    beta2 = -2.8505
                    H = tree.height*10  # dm
                    dubmm = tree.dbh * 10 * ((H - hr*H) / (H - 13)) + beta1 * (
                                ((H ** 1.5 - (hr*H) ** 1.5) * (hr*H - 13)) / H ** 1.5) + beta2 * (
                                       ((H - (hr*H)) ** 4) * (hr*H - 13) / (H ** 4))
                    dub = dubmm*0.1  # mm to cm

                elif plot.prov_region in Ppinea_sc:
                    
                    beta1 = 1.0972
                    beta2 = -2.8505
                    H = tree.height*10  # dm
                    dubmm = tree.dbh * 10 * ((H - hr*H) / (H - 13)) + beta1 * (
                                ((H ** 1.5 - (hr*H) ** 1.5) * (hr*H - 13)) / H ** 1.5) + beta2 * (
                                       ((H - (hr*H)) ** 4) * (hr*H - 13) / (H ** 4))
                    dub = dubmm*0.1  # mm to cm

            elif tree.specie == 24:
                if plot.prov_region in Phalepensis_ar:
                    dub = False

                elif plot.prov_region in Phalepensis_ar_cat:
                    dub = False

            elif tree.specie == 25:
                if plot.prov_region in Pnigra_cat:
                    dub = False

            elif tree.specie == 26:
                if plot.prov_region in Ppinaster_at_c:
                    dub = False

                elif plot.prov_region in Ppinaster_at_i:
                    dub = False

                elif plot.prov_region in Ppinaster_me_sim:
                    dub = (1 + 2.4771 * 2.7182818284 ** (-5.0779 * hr)) * 0.2360 * tree.dbh * pow((1 - hr), (0.4733 - 3.0371 * (1 - hr)))

            elif tree.specie == 28:
                if plot.prov_region in Pradiata_gal:
                    dub = False

            elif tree.specie == 41:
                if plot.prov_region in Qrobur_gal:
                    dub = False

            elif tree.specie == 42:
                if plot.prov_region in Qpetraea_pal:
                    dub = False

            elif tree.specie == 43:
                if plot.prov_region in Qpyrenaica_cyl:
                    dub = False

            elif tree.specie == 46:
                if plot.prov_region in Qsuber_cat:
                    dub = False

            elif tree.specie == 71:
                if plot.prov_region in Fsylvatica:
                    dub = False

        except Exception:
            self.catch_model_exception()

        return dub  # diameter under bark (cm)

