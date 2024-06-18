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
from util import Tools
from scipy import integrate
from models.trees import *
from data.general import Area
from data.variables import TREE_VARS

import logging
import math
import numpy as np


class TreeModel(metaclass=ABCMeta):

    def __init__(self, name: str, version: int):
        self.__tree = None
        self.__name = name
        self.__version = version

        Tools.print_log_line("Loading model " + str(self.name) + "(" + str(self.version) + ")", logging.INFO)

    def catch_model_exception(self):  # that function catch errors and show the line where they are
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Oops! You made a mistake: ', exc_type, ' check inside ', fname, ' model, line', exc_tb.tb_lineno)

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def tree(self):
        return self.__tree

    def set_tree(self, tree: Tree):
        Tools.print_log_line("Loading tree (" + tree.id + ") into model" + self.tree + "(" + self.version + ")", logging.INFO)
        self.__tree = tree

    @abstractmethod
    def initialize(self, plot: Plot):
        return

    @abstractmethod
    def survival(self, years:int, plot: Plot, tree: Tree):
        return

    @abstractmethod
    def growth(self, years:int, plot: Plot, old_tree: Tree, new_tree: Tree):
        return

    @abstractmethod
    def ingrowth(self, years: int, plot: Plot):
        return

    @abstractmethod
    def ingrowth_distribution(self, years: int, plot: Plot, area: float):
        return

    @abstractmethod
    def update_model(self, years: int, plot: Plot, trees: list):
        return

    @staticmethod
    def simps(a, b, epsilon, tree, f):
        """
        This function was programmed to use simps integral without import libraries.
        """

        h = 0
        s = 0
        s1 = 0
        s2 = 0
        s3 = 0
        x = 0

        s2 = 1
        h = b - a
        s = f(tree, a) + f(tree, b)

        while True:

            s3 = s2
            h = h / 2
            s1 = 0
            x = a + h
            while x < b:
                s1 = s1 + 2 * f(tree, x)
                x = x + 2 * h
            s = s + s1
            s2 = (s + s1) * h / 3
            x = abs(s3 - s2) / 15

            if x > epsilon:
                break

        return s2


    def merch_calculation(tree: Tree, class_conditions, model):
        """
        Function needed to calculate the merchantable volumen of the different wood uses.
        That function must be activated by using merchantable function on the model, and it will need his taper_over_bark function to calculate it
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
                    usage[class_conditions[counter][0]] = True  # if stump + log <= 1 (total relative height), then the use is accepted
                else:
                    usage[class_conditions[counter][0]] = False  # if not, the use is rejected

            count = -1
            global merch_list  # share that list to give access in other functions
            merch_list = []  # that list will obtain the results of calculate the different log volumes
            
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
                    dr = model().taper_over_bark(tree, hro)  # diameter of tree at the stump height
                    while dr > class_conditions[count][3] and (hro + 0.05/ht <= 1):  # if the diameter > dmax, and hr <= 1...
                        hro += 0.05 / ht  # we go over the log looking for the part with diameter <= dmax for that usage
                        dr = model().taper_over_bark(tree, hro)  # we calculate the diameter on the next point, to verify the conditions
                    while dr >= class_conditions[count][2] and (hro + class_conditions[count][1] <= 1):  # satisfying dmax, if diameter > dmin and hro is between integration limits (0-1)...
                        hro += class_conditions[count][1]  # from the start point on the tree, we add the length of a log with the usage specifications
                        dr = model().taper_over_bark(tree, hro)  # we again calculate the diameter at this point; the second while condition has sense in here, to not get over 1 integration limit
                        if dr >= class_conditions[count][2] and hro <= 1:  # as taper equation reduce the diameter, it is not needed to check it
                        # if the log diameter > dmin, and hro doesn't overpass 1 (integration limit)
                            hr = np.arange((hro - class_conditions[count][1]), hro, 0.001)  # integration conditions for taper equation
                            d = model().taper_over_bark(tree, hr)  # we get the taper equation with the previous conditions
                            f = (d / 20) ** 2  # to calculate the volume (dm3), we change the units of the result and calculate the radius^2 (instead of diameter)
                            vol += math.pi * ht * 10 * (integrate.simps(f, hr))  # volume calculation, using the previous information
                    if i == True:  # once the tree finish all the while conditions, it comes here, because it continues verifying that condition
                        merch_list.append(vol)  # once we have the total volume for each usage, we add the value to that list
                else:  # if the tree is not useful for one usage, it comes here
                    merch_list.append(0)  # as it is not useful, we add 0 value to that usage

        except Exception:
            TreeModel.catch_model_exception()

        return usage, merch_list


    def merch_calculation_mix(tree: Tree, plot: Plot, class_conditions, model):
        """
        Function needed to calculate the merchantable volumen of the different wood uses, adapted to tree mixed models.
        That function must be activated by using merchantable function on the model, and it will need his taper_over_bark function to calculate it
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
                    usage[class_conditions[counter][0]] = True  # if stump + log <= 1 (total relative height), then the use is accepted
                else:
                    usage[class_conditions[counter][0]] = False  # if not, the use is rejected

            count = -1
            global merch_list  # share that list to give access in other functions
            merch_list = []  # that list will obtain the results of calculate the different log volumes

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
                    dr = model().taper_over_bark(tree, plot, hro)  # diameter of tree at the stump height
                    while dr > class_conditions[count][3] and (hro + 0.05/ht <= 1):  # if the diameter > dmax, and hr <= 1...
                        hro += 0.05 / ht  # we go over the log looking for the part with diameter <= dmax for that usage
                        dr = model().taper_over_bark(tree, plot, hro)  # we calculate the diameter on the next point, to verify the conditions
                    while dr >= class_conditions[count][2] and (hro + class_conditions[count][1] <= 1):  # satisfying dmax, if diameter > dmin and hro is between integration limits (0-1)...
                        hro += class_conditions[count][1]  # from the start point on the tree, we add the length of a log with the usage specifications
                        dr = model().taper_over_bark(tree, plot, hro)  # we again calculate the diameter at this point; the second while condition has sense in here, to not get over 1 integration limit
                        if dr >= class_conditions[count][2] and hro <= 1:  # as taper equation reduce the diameter, it is not needed to check it
                        # if the log diameter > dmin, and hro doesn't overpass 1 (integration limit)
                            hr = np.arange((hro - class_conditions[count][1]), hro, 0.001)  # integration conditions for taper equation
                            d = model().taper_over_bark(tree, plot, hr)  # we get the taper equation with the previous conditions
                            f = (d / 20) ** 2  # to calculate the volume (dm3), we change the units of the result and calculate the radius^2 (instead of diameter)
                            vol += math.pi * ht * 10 * (integrate.simps(f, hr))  # volume calculation, using the previous information
                    if i == True:  # once the tree finish all the while conditions, it comes here, because it continues verifying that condition
                        merch_list.append(vol)  # once we have the total volume for each usage, we add the value to that list
                else:  # if the tree is not useful for one usage, it comes here
                    merch_list.append(0)  # as it is not useful, we add 0 value to that usage

        except Exception:
            TreeModel.catch_model_exception()

        return usage, merch_list


    def merch_calculation_master(self, tree, plot, class_conditions, model):
        """
        Function needed to calculate the merchantable volumen of the different wood uses.
        That function must be activated by using merchantable function on the model, and it will need his taper_over_bark function to calculate it
        """

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
                usage[class_conditions[counter][0]] = True  # if stump + log <= 1 (total relative height), then the use is accepted
            else:
                usage[class_conditions[counter][0]] = False  # if not, the use is rejected

        count = -1
        global merch_list  # share that list to give access in other functions
        merch_list = []  # that list will obtain the results of calculate the different log volumes

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
                dr = model.taper_over_bark(self, tree, plot, hro)  # diameter of tree at the stump height
                while dr > class_conditions[count][3] and (hro + 0.05/ht <= 1):  # if the diameter > dmax, and hr <= 1...
                    hro += 0.05 / ht  # we go over the log looking for the part with diameter <= dmax for that usage
                    dr = model.taper_over_bark(self, tree, plot, hro)  # we calculate the diameter on the next point, to verify the conditions
                while dr >= class_conditions[count][2] and (hro + class_conditions[count][1] <= 1):  # satisfying dmax, if diameter > dmin and hro is between integration limits (0-1)...
                    hro += class_conditions[count][1]  # from the start point on the tree, we add the length of a log with the usage specifications
                    dr = model.taper_over_bark(self, tree, plot, hro)  # we again calculate the diameter at this point; the second while condition has sense in here, to not get over 1 integration limit
                    if dr >= class_conditions[count][2] and hro <= 1:  # as taper equation reduce the diameter, it is not needed to check it
                    # if the log diameter > dmin, and hro doesn't overpass 1 (integration limit)
                        hr = np.arange((hro - class_conditions[count][1]), hro, 0.001)  # integration conditions for taper equation
                        d = model.taper_over_bark(self, tree, plot, hr)  # we get the taper equation with the previous conditions
                        f = (d / 20) ** 2  # to calculate the volume (dm3), we change the units of the result and calculate the radius^2 (instead of diameter)
                        vol += math.pi * ht * 10 * (integrate.simps(f, hr))  # volume calculation, using the previous information
                if i == True:  # once the tree finish all the while conditions, it comes here, because it continues verifying that condition
                    merch_list.append(vol)  # once we have the total volume for each usage, we add the value to that list
            else:  # if the tree is not useful for one usage, it comes here
                merch_list.append(0)  # as it is not useful, we add 0 value to that usage

        return usage, merch_list


    def merch_calculation_all_species(tree: Tree, class_conditions, model):
        """
        Function needed to calculate the merchantable volumen of the different wood uses.
        That function must be activated by using merchantable function on the all species model, and it will need his taper_over_bark function to calculate it
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
                    usage[class_conditions[counter][0]] = True  # if stump + log <= 1 (total relative height), then the use is accepted
                else:
                    usage[class_conditions[counter][0]] = False  # if not, the use is rejected

            count = -1
            global merch_list  # share that list to give access in other functions
            merch_list = []  # that list will obtain the results of calculate the different log volumes
            
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
                    dr = model().taper_over_bark_Fang(tree, hro)  # diameter of tree at the stump height
                    while dr > class_conditions[count][3] and (hro + 0.05/ht <= 1):  # if the diameter > dmax, and hr <= 1...
                        hro += 0.05 / ht  # we go over the log looking for the part with diameter <= dmax for that usage
                        dr = model().taper_over_bark_Fang(tree, hro)  # we calculate the diameter on the next point, to verify the conditions
                    while dr >= class_conditions[count][2] and (hro + class_conditions[count][1] <= 1):  # satisfying dmax, if diameter > dmin and hro is between integration limits (0-1)...
                        hro += class_conditions[count][1]  # from the start point on the tree, we add the length of a log with the usage specifications
                        dr = model().taper_over_bark_Fang(tree, hro)  # we again calculate the diameter at this point; the second while condition has sense in here, to not get over 1 integration limit
                        if dr >= class_conditions[count][2] and hro <= 1:  # as taper equation reduce the diameter, it is not needed to check it
                        # if the log diameter > dmin, and hro doesn't overpass 1 (integration limit)
                            hr = np.arange((hro - class_conditions[count][1]), hro, 0.001)  # integration conditions for taper equation
                            d = model().taper_over_bark_Fang(tree, hr)  # we get the taper equation with the previous conditions
                            f = (d / 20) ** 2  # to calculate the volume (dm3), we change the units of the result and calculate the radius^2 (instead of diameter)
                            vol += math.pi * ht * 10 * (integrate.simps(f, hr))  # volume calculation, using the previous information
                    if i == True:  # once the tree finish all the while conditions, it comes here, because it continues verifying that condition
                        merch_list.append(vol)  # once we have the total volume for each usage, we add the value to that list
                else:  # if the tree is not useful for one usage, it comes here
                    merch_list.append(0)  # as it is not useful, we add 0 value to that usage

        except Exception:
            TreeModel.catch_model_exception()

        return usage, merch_list


    def choose_martonne(plot_id, year, list_years):
        """
        Function created to select the Martonne Index corresponding to the year of the plot.
        Initially, it was created to be applied at mixed tree models.
        """
        # TODO: borrar esta función y desviarla a equations_tree_models
        if year <= list_years[0]: # under 2020 (default)
            M = Area.martonne[plot_id]
        elif year <= list_years[1]: # 2021-2040
            M = Area.martonne_2020[plot_id]
        elif year <= list_years[2]: # 2041-2060
            M = Area.martonne_2040[plot_id]
        elif year <= list_years[3]: # 2061-2080
            M = Area.martonne_2060[plot_id]
        elif year <= list_years[4]: # 2081-2100
            M = Area.martonne_2080[plot_id]
        else:
            M = Area.martonne[plot_id]  # value by default

        return M


    def voronoi(p,resolucion=100):
       
        n = len(p)
        areaRegiones = [0 for i in range(n)]  # contiene las areas de las regiones medidas en numero de pixeles
       
        W = np.array([[int(-1) for j in range(resolucion)] for i in range(resolucion)])
        for i in range(resolucion):
            for j in range(resolucion):
               
                q = -1
                d = np.inf  # infinity
                for k in range(len(p)):
                    daux = math.sqrt((float(i)/resolucion-p[k][0][0])**2+(float(j)/resolucion-p[k][0][1])**2)/p[k][1]
                    if daux < d and daux < p[k][1]:
                        d = daux
                        q = k
                        W[j][i] = k
               
                areaRegiones[q] += 1
                                 
        return W,areaRegiones


    def neighbours(W,p):
        n = len(p)
        m = len(W)
        V = np.array([[0 for i in range(n)] for j in range(n)])
        for i in range(m-1):
            for j in range(m-1):
                if W[i,j] != -1 :
                   
                    if W[i,j] != W[i,j+1] and W[i,j+1] != -1:  
                        V[W[i,j],W[i,j+1]] = 1
                        V[W[i,j+1],W[i,j]] = 1
                    if W[i,j] != W[i+1,j] and W[i+1,j] != -1:
                        V[W[i,j],W[i+1,j]] = 1
                        V[W[i+1,j],W[i,j]] = 1
                    if W[i,j] != W[i+1,j+1] and W[i+1,j+1] != -1:
                        V[W[i,j],W[i+1,j+1]] = 1
                        V[W[i+1,j+1],W[i,j]] = 1
        return V                    


# la funcion calculaRadios calcula el radio de cada punto en función de su peso y lo añade a los paramatros del punto

    def calculateRadius(p): 
        for i in p:
            i.append(math.exp(0.092+0.538*math.log(i[1])))
        return p   


    def mean_dbh(plot_trees):
        """ Function created to calculate plot mean dbh, if it is needed on initialize process"""

        plot_expan = plot_dbh = 0

        for tree in plot_trees:

            plot_expan += tree.expan
            plot_dbh += tree.dbh*tree.expan
        
        if plot_expan != 0:
            return plot_dbh/plot_expan
        else:
            return 0


    def hegyi(plot, tree_i, plot_trees, radius_limit = 0):
        """ 
        Hegyi index calculation. Another variables related with bal, basal area and density inside the Hegyi subplot are caltulated.
        That function is activated from the initialize and the update_model functions of the models which need it.
        Source: 
            Doc.: Hegyi F (1974). A simulation model for managing jack-pine stands simulation. RoyalColl. For, Res. Notes, 30, 74-90    
        """

        try:

            if radius_limit == 0 or radius_limit == '':  # create the radius_limit value as default
                radius_limit = tree_i.height*0.25

            TreeModel.check_plot_coordinates(plot)  # check if the plot position information is available
            TreeModel.calculate_coordinates_all_trees(plot, plot_trees)  # calculate tree coordinates if it is needed


            if "coord_x" in TREE_VARS and "coord_y" in TREE_VARS and tree_i.coord_x != '' and tree_i.coord_y != '':  # if position variable exists...

                # lists needed
                neighbours_i = list()
                individual_hegyi = list()

                bal = bal_intrasp = bal_intersp = g_intrasp = g_intersp = N_intrasp = N_intersp = 0  # variables needed to other calculations


                for tree_j in plot_trees:  # tree that we want to know if is a neighbour or not from tree_i

                    if tree_i.tree_id != tree_j.tree_id:  # do not include a tree as neighbour of himself

                        x_diff = tree_i.coord_x - tree_j.coord_x  # distance on x axis
                        y_diff = tree_i.coord_y - tree_j.coord_y  # distance on y axis
                        dist_ij = math.sqrt((x_diff**2) + (y_diff**2))  # distance between i and j tree (hypotenuse)

                        if dist_ij <= radius_limit:  # if the tree is inside the limit radius...

                            neighbours_i.append(tree_j)  # the tree is added to a list

                            hegyi_ij = tree_i.dbh/(tree_j.dbh*(dist_ij + 1))  # hegyi index calculation
                            individual_hegyi.append(hegyi_ij)  # add hegyi index value to a list

                        
                            #------------------------ BAL, N and G -----------------------------#

                            if int(tree_i.specie) == int(tree_j.specie):  # intraspecific condition                            

                                bal_intrasp += tree_j.basal_area*tree_j.expan/10000  # accumulator to calculate that plot variable
                                N_intrasp += tree_j.expan  # accumulator to calculate density per specie (trees/ha)
                                g_intrasp += tree_j.basal_area*tree_j.expan/10000  # accumulator to calculate that plot variable (m2/ha)
                           
                            else:  # interspecific condition                            

                                bal_intersp += tree_j.basal_area*tree_j.expan/10000  # accumulator to calculate that plot variable
                                N_intersp += tree_j.expan  # accumulator to calculate density per specie (trees/ha)
                                g_intersp += tree_j.basal_area*tree_j.expan/10000  # accumulator to calculate that plot variable (m2/ha)
                        
                    else:  # for the tree_i, data is needed to be included on the next variables
                 
                        N_intrasp += tree_j.expan  # accumulator to calculate density per specie (trees/ha)
                        g_intrasp += tree_j.basal_area*tree_j.expan/10000  # accumulator to calculate that plot variable (m2/ha)



                hegyi_index = sum(individual_hegyi)  # sum the individual hegyi index to get the final hegyi value
                tree_i.add_value('hegyi', hegyi_index)  # add the value to the tree

                tree_i.add_value("bal_intrasp_hegyi", bal_intrasp)  # intraspecific bal (m2/ha) inside hegyi subplot of each tree
                tree_i.add_value("bal_intersp_hegyi", bal_intersp)  # interspecific bal (m2/ha) inside hegyi subplot of each tree
                if bal_intrasp > 0:
                    tree_i.add_value("bal_ratio_intrasp_hegyi", bal_intrasp/(bal_intrasp + bal_intersp))  # intraspecific bal ratio (0 to 1) inside hegyi subplot of each tree
                else:
                    tree_i.add_value("bal_ratio_intrasp_hegyi", 0)  # intraspecific bal ratio (0 to 1) inside hegyi subplot of each tree                   
                if bal_intersp > 0:
                    tree_i.add_value("bal_ratio_intersp_hegyi", bal_intersp/(bal_intrasp + bal_intersp))  # interspecific bal ratio (0 to 1) inside hegyi subplot of each tree
                else:
                    tree_i.add_value("bal_ratio_intersp_hegyi", 0)  # interspecific bal ratio (0 to 1) inside hegyi subplot of each tree
                tree_i.add_value("bal_total_hegyi", bal_intrasp + bal_intersp)  # total bal (m2/ha) inside hegyi subplot of each tree
                tree_i.add_value("g_intrasp_hegyi", g_intrasp)  # intraspecific basal area (m2/ha) inside hegyi subplot of each tree
                tree_i.add_value("g_intersp_hegyi", g_intersp)  # interspecific basal area (m2/ha) inside hegyi subplot of each tree
                if g_intrasp > 0:                
                    tree_i.add_value("g_ratio_intrasp_hegyi", g_intrasp/(g_intrasp + g_intersp))  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
                else:
                    tree_i.add_value("g_ratio_intrasp_hegyi", 0)
                if g_intersp > 0:
                    tree_i.add_value("g_ratio_intersp_hegyi", g_intersp/(g_intrasp + g_intersp))  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
                else:
                    tree_i.add_value("g_ratio_intersp_hegyi", 0)
                tree_i.add_value("g_total_hegyi", g_intrasp + g_intersp)  # total basal area (m2/ha) inside hegyi subplot of each tree
                tree_i.add_value("n_intrasp_hegyi", N_intrasp)  # intraspecific density (trees/ha) inside hegyi subplot of each tree
                tree_i.add_value("n_intersp_hegyi", N_intersp)  # interspecific density (trees/ha) inside hegyi subplot of each tree
                if N_intrasp > 0:
                    tree_i.add_value("n_ratio_intrasp_hegyi", N_intrasp/(N_intrasp + N_intersp))  # intraspecific density ratio (0 to 1) inside hegyi subplot of each tree
                else:
                    tree_i.add_value("n_ratio_intrasp_hegyi", 0)
                if N_intersp > 0:
                    tree_i.add_value("n_ratio_intersp_hegyi", N_intersp/(N_intrasp + N_intersp))  # interspecific density ratio (0 to 1) inside hegyi subplot of each tree
                else:
                    tree_i.add_value("n_ratio_intersp_hegyi", 0)
                tree_i.add_value("n_total_hegyi", N_intrasp + N_intersp)  # total density (trees/ha) inside hegyi subplot of each tree

            else:

                print("Hegyi index was not possible to calculate due to the lack of position tree information.")

        except Exception:
            TreeModel.catch_model_exception()


    def calculate_coordinates(plot, tree_i):
        """
        Function that calculates the coordinates of one single tree by using the bearing and distance
        of the tree to the coordinates of the plot center.
        Longitude and latitude are transformed into Area variables instead of Plot variables. To call them, 
        you must use: Area.longitude[plot.plot_id] - Area.latitude[plot.plot_id]             
        """

        try:

            bearing_rad = TreeModel.grad2rad(tree_i.bearing)

            tree_i.add_value('coord_x', tree_i.distance*math.cos(bearing_rad) + Area.longitude[plot.plot_id])
            tree_i.add_value('coord_y', tree_i.distance*math.sin(bearing_rad) + Area.latitude[plot.plot_id])

        except Exception:
            TreeModel.catch_model_exception()


    def calculate_coordinates_all_trees(plot, plot_trees):
        """
        Function that calculates the coordinates of all the trees of the plots by using the bearing and distance
        of the trees to the coordinates of the plot center.
        Longitude and latitude are transformed into Area variables instead of Plot variables. To call them, 
        you must use: Area.longitude[plot.plot_id] - Area.latitude[plot.plot_id]        
        """

        try:

            for tree in plot_trees:
                
                if tree.coord_x == '' and tree.coord_y == '':                 
    
                    bearing_rad = TreeModel.grad2rad(tree.bearing)

                    tree.add_value('coord_x', tree.distance*math.cos(bearing_rad) + Area.longitude[plot.plot_id])
                    tree.add_value('coord_y', tree.distance*math.sin(bearing_rad) + Area.latitude[plot.plot_id])

        except Exception:
            TreeModel.catch_model_exception()


    def deg2rad(angle):
        """Convert degrees (grados sexagesimales) to radians"""
        return angle*math.pi/180


    def rad2deg(angle):
        """Convert radians to degrees (grados sexagesimales)"""
        return angle*180/math.pi


    def grad2rad(angle):
        """Convert gradians (grados centesimales) to radians"""
        return angle*(2*math.pi)/400 


    def rad2grad(angle):
        """Convert radians to gradians (grados centesimales)"""
        return angle*400/(2*math.pi) 


    def check_plot_coordinates(plot):
        """
        Function needed to check if the plot position information is available.
        Longitude and latitude are transformed into Area variables instead of Plot variables. To call them, 
        you must use: Area.longitude[plot.plot_id] - Area.latitude[plot.plot_id]
        """

        if Area.longitude[plot.plot_id] == '':
            Area.longitude[plot.plot_id] = 0  # set 0 as a number reference
            print("Plot longitude doesn't exist; set as 0 to calculate trees position on the plot.")

        if Area.latitude[plot.plot_id] == '':
            Area.latitude[plot.plot_id] = 0  # set 0 as a number reference
            print("Plot latitude doesn't exist; set as 0 to calculate trees position on the plot.")            


    def Fang_taper(tree: Tree, hr: float, values):

        # TODO: borrar esta función y desviarla a equations_tree_volume

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
    

        else:  # if it is not an equation available...

            dob = 0

        return dob