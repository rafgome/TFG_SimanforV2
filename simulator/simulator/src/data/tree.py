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

from util import Tools
from .search.order_criteria import DESC
from data.variables import TREE_VARS
from data.variables import TREE_VARS_ORIGINAL
from data.inventory_translations.es import ES_TREE
from data.inventory_translations.gl import GL_TREE
from data.inventory_translations.en import EN_TREE

import logging
import json


IDS_VALUES = ['INVENTORY_ID',  # IDs variables list
              'PLOT_ID',
              'TREE_ID']

STR_VALUES = ['status']  # status value of the trees (M-> die, C-> harvested, I-> ingrowth)

JSON_STR_VALUES = ['PLOT_ID', 'TREE_ID', 'specie']  # json variables list


class Tree:

    # variable to count new trees added by the ingrowth function
    global new_ingrowth_tree
    new_ingrowth_tree = 1000000

    def __init__(self, data=None):

        self.__values = dict()

        if data is None:
            Tools.print_log_line("No data info when tree is generated", logging.WARNING)

            for var_name in TREE_VARS:
                self.__values[var_name] = 0
        else:
            for var_name in TREE_VARS:
                if var_name not in data.keys():
                    #Tools.print_log_line(var_name + ' is not in data document', logging.WARNING)
                    self.__values[var_name] = ''
                    self.translate_name(data, var_name)                     
                else:
                    self.__values[var_name] = data[var_name]

            if 'tree' in data: # json input
                self.map_json_to_xl(data)

        self.__values['status'] = None

        # Copy of the code needed to print the node 0 as the original initial inventory

        self.__values_original = dict()

        if data is None:
            Tools.print_log_line("No data info when tree is generated", logging.WARNING)

            for var_name in TREE_VARS_ORIGINAL:
                self.__values_original[var_name] = 0
        else:
            for var_name in TREE_VARS_ORIGINAL:
                if var_name not in data.keys():
                    Tools.print_log_line(var_name + ' is not in data document', logging.WARNING)
                    self.__values_original[var_name] = 0
                else:
                    self.__values_original[var_name] = data[var_name]

            if 'tree' in data: # json input
                self.map_json_to_xl(data)

        self.__values_original['status'] = None


    def translate_name(self, data, variable):
        """
        Function created to translate the names of initial inventory to the variables names of SIMANFOR.
        It is activated from __init__ function, and it uses the lists of variables from inventory_translations.
        """

        lang_list = (ES_TREE, EN_TREE, GL_TREE)  # list of available languages

        for lang in lang_list:  # for each language...
            for variable_lang in lang: # for each variable on the language...
                if variable == variable_lang:  # if the variable is on the language

                    try:  # condition needed to skip non used languages

                        self.__values[variable] = data[lang[variable_lang]]  # their value is added to the SIMANFOR variable

                    except KeyError:

                        None


    def map_json_to_xl(self, data):       
        """
        That function converts the name of the json input file variables to the simulator variables names.
        """

        self.__values['TREE_ID'] = data['tree']
        self.__values['specie'] = data['species']
        self.__values['coord_x'] = data['treelat']
        self.__values['coord_y'] = data['treelong']
        self.__values['height'] = float(data['height'])
        self.__values['dbh_1'] = float(data['dbh1'])
        self.__values['dbh_2'] = float(data['dbh2'])
        self.__values['PLOT_ID'] = data['plot']
        self.__values['dbh'] = float(data['dbh'])
        self.__values['expan'] = float(data['expan'])
        
    # def get_value(self, var):
    #     try:
    #         if self.__values[var] is None:
    #             return self.__values[var]
    #         elif var in STR_VALUES:
    #             return str(self.__values[var])
    #         if var in IDS_VALUES:
    #             return int(self.__values[var])
    #         else:
    #             return self.__values[var]
    #     except Exception as e:
    #         Tools.print_log_line(str(e) + ' when it tried to access variable ' + var, logging.ERROR)

    def get_value(self, var, json = False):
        """
        Function neccesary to obtain a variable value
        """

        try:
            if self.__values[var] is None:
                return self.__values[var]
            elif var in STR_VALUES or json == True:
                return str(self.__values[var])
            if var in IDS_VALUES:
                return self.__values[var]
                #return int(self.__values[var])
            else:
                return self.__values[var]
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to access variable ' + var, logging.ERROR)

    def get_value_original(self, var, json = False):
        """
        Function neccesary to obtain a variable value (only to node 0).
        """

        try:
            if self.__values_original[var] is None:
                return self.__values_original[var]
            elif var in STR_VALUES or json == True:
                return str(self.__values_original[var])
            if var in IDS_VALUES:
                return self.__values_original[var]
                #return int(self.__values_original[var])
            else:
                return self.__values_original[var]
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to access variable ' + var, logging.ERROR)


    def add_value(self, var, value):
        """
        Function neccesary to add a value to a tree variable by sustitution from the past value.
        """

        try:
            if value is None:
                self.__values[var] = value
            elif var in STR_VALUES:
                self.__values[var] = str(value)
            elif var in IDS_VALUES:
                self.__values[var] = value
                #self.__values[var] = int(value)
            else:
                self.__values[var] = float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + value, logging.ERROR)

    def set_value(self, var, value):
        """
        Function neccesary to add a value to a plot variable by sustitution from the past value. Is the same as add_value.
        """

        try:
            if var in STR_VALUES:
                self.__values[var] = str(value)
            elif var in IDS_VALUES:
                self.__values[var] = value
                #self.__values[var] = int(value)
            else:
                self.__values[var] = float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + str(value), logging.ERROR)

    def sum_value(self, var, value):
        """
        Function neccesary to sum a value to a plot variable.
        """

        try:
            if var in IDS_VALUES:
                self.__values[var] = value  # as it can be a str value, we cannot sum/sub it
                #self.__values[var] += int(value)
            else:
                self.__values[var] += float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + str(value), logging.ERROR)

    def sub_value(self, var, value):
        """
        Function neccesary to subtrack a value to a plot variable.
        """

        try:
            if var in IDS_VALUES:
                self.__values[var] = value  # as it can be a str value, we cannot sum/sub it
                #self.__values[var] -= int(value)
            else:
                self.__values[var] -= float(value)
        except Exception as e:
            Tools.print_log_line(str(e) + ' when it tried to update variable ' + var + ' with value ' + str(value), logging.ERROR)

    @property
    def plot_id(self):
        #return int(self.__values['TREE_ID'])
        return self.__values['PLOT_ID']

    @property
    def tree_id(self):
        #return int(self.__values['TREE_ID'])
        return self.__values['TREE_ID']

    @property
    def id(self):
        #if isinstance(self.__values['PLOT_ID'], int):
            #return int(self.__values['TREE_ID'])
        #else:
        return self.__values['TREE_ID']

    def get_array(self):
        tmp = list()
        for key, value in self.__values.iteritems():
            tmp.append(value)
        return tmp

    @staticmethod
    def variables_names():
        return TREE_VARS + STR_VALUES

    @staticmethod
    def variables_names_original():
        return TREE_VARS_ORIGINAL + STR_VALUES

       ###--- From this point, tree variables are created in order to work with them by using the models ---###

###############################################################################################################
#####################################  Special TREE_IDs to work with the IFN data  ############################
###############################################################################################################

    @property
    def tree_id_ifn3_2(self):
        return self.__values['TREE_ID_IFN3_2']

    @property
    def tree_id_ifn3(self):
        return self.__values['TREE_ID_IFN3']

    @property
    def tree_id_ifn2(self):
        return self.__values['TREE_ID_IFN2']

    @property
    def tree_id_compare(self):
        return self.__values['TREE_ID_compare']                        

###############################################################################################################
##############################################  Tree general information  #####################################
###############################################################################################################
  
    @property
    def number_of_trees(self):
        return self.__values['number_of_trees']

    @property
    def specie(self):
        return self.__values['specie']

    @property
    def bearing(self):
        return self.__values['bearing']

    @property
    def distance(self):
        return self.__values['distance']        

    @property
    def quality(self):
        return self.__values['quality']

    @property
    def shape(self):
        return self.__values['shape']

    @property
    def special_param(self):
        return self.__values['special_param']

    @property
    def remarks(self):
        return self.__values['remarks']

    @property
    def age_130(self):
        return self.__values['age_130']

    @property
    def social_class(self):
        return self.__values['social_class']

    @property
    def tree_age(self):
        return self.__values['tree_age']

    @property
    def coord_x(self):
        return self.__values['coord_x']

    @property
    def coord_y(self):
        return self.__values['coord_y']

    @property
    def coord_z(self):
        return self.__values['coord_z']

###############################################################################################################
#########################################  Basic variables measured  ##########################################
###############################################################################################################

    @property
    def dbh_1(self):
        return self.__values['dbh_1']

    @property
    def dbh_2(self):
        return self.__values['dbh_2']

    @property
    def dbh(self):
        return self.__values['dbh']

    @property
    def dbh_i(self):
        return self.__values['dbh_i']

    @property
    def stump_h(self):
        return self.__values['stump_h']

    @property
    def height(self):
        return self.__values['height']

    @property
    def height_i(self):
        return self.__values['height_i']

    @property
    def bark_1(self):
        return self.__values['bark_1']

    @property
    def bark_2(self):
        return self.__values['bark_2']

    @property
    def bark(self):
        return self.__values['bark']

    @property
    def expan(self):
        return self.__values['expan']

###############################################################################################################
#########################################  Basic variables calculated  ########################################
###############################################################################################################

    @property
    def normal_circumference(self):
        return self.__values['normal_circumference']

    @property
    def slenderness(self):
        return self.__values['slenderness']

    @property
    def basal_area(self):
        return self.__values['basal_area']

    @property
    def basal_area_i(self):
        return self.__values['basal_area_i']

    @property
    def basal_area_intrasp(self):
        return self.__values['basal_area_intrasp']

    @property
    def basal_area_intersp(self):
        return self.__values['basal_area_intersp']

    @property
    def bal(self):
        return self.__values['bal']

    @property
    def bal_intrasp(self):
        return self.__values['bal_intrasp']

    @property
    def bal_intersp(self):
        return self.__values['bal_intersp']

    @property
    def ba_ha(self):
        return self.__values['ba_ha']

###############################################################################################################
#####################################  Basic variables on Hegyi subplot  ######################################
###############################################################################################################

    @property
    def bal_intrasp_hegyi(self):
        return self.__values['bal_intrasp_hegyi']

    @property
    def bal_intersp_hegyi(self):
        return self.__values['bal_intersp_hegyi']

    @property
    def bal_ratio_intrasp_hegyi(self):
        return self.__values['bal_ratio_intrasp_hegyi']

    @property
    def bal_ratio_intersp_hegyi(self):
        return self.__values['bal_ratio_intersp_hegyi']

    @property
    def bal_total_hegyi(self):
        return self.__values['bal_total_hegyi']

    @property
    def g_intrasp_hegyi(self):
        return self.__values['g_intrasp_hegyi']

    @property
    def g_intersp_hegyi(self):
        return self.__values['g_intersp_hegyi']

    @property
    def g_ratio_intrasp_hegyi(self):
        return self.__values['g_ratio_intrasp_hegyi']

    @property
    def g_ratio_intersp_hegyi(self):
        return self.__values['g_ratio_intersp_hegyi']

    @property
    def g_total_hegyi(self):
        return self.__values['g_total_hegyi']

    @property
    def n_intrasp_hegyi(self):
        return self.__values['n_intrasp_hegyi']

    @property
    def n_intersp_hegyi(self):
        return self.__values['n_intersp_hegyi']

    @property
    def n_ratio_intrasp_hegyi(self):
        return self.__values['n_ratio_intrasp_hegyi']

    @property
    def n_ratio_intersp_hegyi(self):
        return self.__values['n_ratio_intersp_hegyi']

    @property
    def n_total_hegyi(self):
        return self.__values['n_total_hegyi']
        
###############################################################################################################
##############################################  Crown variables  ##############################################
###############################################################################################################

    @property
    def cr(self):
        return self.__values['cr']

    @property
    def lcw(self):
        return self.__values['lcw']

    @property
    def hcb(self):
        return self.__values['hcb']

    @property
    def hlcw(self):
        return self.__values['hlcw']

    @property
    def cpa(self):
        return self.__values['cpa']

    @property
    def crown_vol(self):
        return self.__values['crown_vol']

###############################################################################################################
##############################################  Volume variables ##############################################
###############################################################################################################

    @property
    def vol(self):
        return self.__values['vol']

    @property
    def bole_vol(self):
        return self.__values['bole_vol']

    @property
    def bark_vol(self):
        return self.__values['bark_vol']

    @property
    def firewood_vol(self):
        return self.__values['firewood_vol']

    @property
    def vol_ha(self):
        return self.__values['vol_ha']

###############################################################################################################
##############################################  Biomass variables #############################################
###############################################################################################################

    @property
    def wsw(self):
        return self.__values['wsw']

    @property
    def wsb(self):
        return self.__values['wsb']

    @property
    def wswb(self):
        return self.__values['wswb']

    @property
    def w_cork(self):
        return self.__values['w_cork']

    @property
    def wthickb(self):
        return self.__values['wthickb']

    @property
    def wstb(self):
        return self.__values['wstb']

    @property
    def wb2_7(self):
        return self.__values['wb2_7']

    @property
    def wb2_t(self):
        return self.__values['wb2_t']

    @property
    def wthinb(self):
        return self.__values['wthinb']

    @property
    def wb05(self):
        return self.__values['wb05']

    @property
    def wb05_7(self):
        return self.__values['wb05_7']

    @property
    def wb0_2(self):
        return self.__values['wb0_2']

    @property
    def wdb(self):
        return self.__values['wdb']

    @property
    def wl(self):
        return self.__values['wl']

    @property
    def wtbl(self):
        return self.__values['wtbl']

    @property
    def wbl0_7(self):
        return self.__values['wbl0_7']

    @property
    def wr(self):
        return self.__values['wr']

    @property
    def wt(self):
        return self.__values['wt']

###############################################################################################################
############################################  Wood uses variables #############################################
###############################################################################################################

    @property
    def unwinding(self):
        return self.__values['unwinding']

    @property
    def veneer(self):
        return self.__values['veneer']

    @property
    def saw_big(self):
        return self.__values['saw_big']

    @property
    def saw_small(self):
        return self.__values['saw_small']

    @property
    def saw_canter(self):
        return self.__values['saw_canter']

    @property
    def post(self):
        return self.__values['post']

    @property
    def stake(self):
        return self.__values['stake']

    @property
    def chips(self):
        return self.__values['chips']

###############################################################################################################
########################################## Competition information ############################################
###############################################################################################################

    @property
    def hegyi(self):
        return self.__values['hegyi']

###############################################################################################################
######################################  Quercus suber special variables #######################################
###############################################################################################################

    @property
    def dbh_oc(self):
        return self.__values['dbh_oc']

    @property
    def h_debark(self):
        return self.__values['h_debark']

    @property
    def nb(self):
        return self.__values['nb']

    @property
    def cork_cycle(self):
        return self.__values['cork_cycle']

    @property
    def count_debark(self):
        return self.__values['count_debark']

    @property
    def total_w_debark(self):
        return self.__values['total_w_debark']

    @property
    def total_v_debark(self):
        return self.__values['total_v_debark']

###############################################################################################################
#######################################  Pinus pinea special variables ########################################
###############################################################################################################

    @property
    def all_cones(self):
        return self.__values['all_cones']

    @property
    def sound_cones(self):
        return self.__values['sound_cones']

    @property
    def sound_seeds(self):
        return self.__values['sound_seeds']

    @property
    def w_sound_cones(self):
        return self.__values['w_sound_cones']

    @property
    def w_all_cones(self):
        return self.__values['w_all_cones']

###############################################################################################################
#########################################  Vorest special variables ###########################################
###############################################################################################################

    @property
    def w_voronoi(self):
        return self.__values['w_voronoi']

    @property
    def neighbours_mean_dbh(self):
        return self.__values['neighbours_mean_dbh']

    @property
    def ogs(self):
        return self.__values['ogs']

    @property
    def ags(self):
        return self.__values['ags']

    @property
    def pgs(self):
        return self.__values['pgs']

    @property
    def rel_area(self):
        return self.__values['rel_area']

###############################################################################################################
############################## Auxiliar variables for future models - 11/08/2023 ##############################
###############################################################################################################

    @property
    def tree_var1(self):
        return self.__values['tree_var1']

    @property
    def tree_var2(self):
        return self.__values['tree_var2']

    @property
    def tree_var3(self):
        return self.__values['tree_var3']

    @property
    def tree_var4(self):
        return self.__values['tree_var4']

    @property
    def tree_var5(self):
        return self.__values['tree_var5']

    @property
    def tree_var6(self):
        return self.__values['tree_var6']

    @property
    def tree_var7(self):
        return self.__values['tree_var7']

    @property
    def tree_var8(self):
        return self.__values['tree_var8']

    @property
    def tree_var9(self):
        return self.__values['tree_var9']

    @property
    def tree_var10(self):
        return self.__values['tree_var10']

    @property
    def tree_var11(self):
        return self.__values['tree_var11']

    @property
    def tree_var12(self):
        return self.__values['tree_var12']

    @property
    def tree_var13(self):
        return self.__values['tree_var13']

    @property
    def tree_var14(self):
        return self.__values['tree_var14']

    @property
    def tree_var15(self):
        return self.__values['tree_var15']

    @property
    def tree_var16(self):
        return self.__values['tree_var16']

    @property
    def tree_var17(self):
        return self.__values['tree_var17']

    @property
    def tree_var18(self):
        return self.__values['tree_var18']

    @property
    def tree_var19(self):
        return self.__values['tree_var19']

    @property
    def tree_var20(self):
        return self.__values['tree_var20']

    @property
    def tree_var21(self):
        return self.__values['tree_var21']

    @property
    def tree_var22(self):
        return self.__values['tree_var22']

    @property
    def tree_var23(self):
        return self.__values['tree_var23']

    @property
    def tree_var24(self):
        return self.__values['tree_var24']

    @property
    def tree_var25(self):
        return self.__values['tree_var25']

    @property
    def tree_var26(self):
        return self.__values['tree_var26']

    @property
    def tree_var27(self):
        return self.__values['tree_var27']

    @property
    def tree_var28(self):
        return self.__values['tree_var28']

    @property
    def tree_var29(self):
        return self.__values['tree_var29']

    @property
    def tree_var30(self):
        return self.__values['tree_var30']

    @property
    def tree_var31(self):
        return self.__values['tree_var31']

    @property
    def tree_var32(self):
        return self.__values['tree_var32']

    @property
    def tree_var33(self):
        return self.__values['tree_var33']

    @property
    def tree_var34(self):
        return self.__values['tree_var34']

    @property
    def tree_var35(self):
        return self.__values['tree_var35']

    @property
    def tree_var36(self):
        return self.__values['tree_var36']

    @property
    def tree_var37(self):
        return self.__values['tree_var37']

    @property
    def tree_var38(self):
        return self.__values['tree_var38']

    @property
    def tree_var39(self):
        return self.__values['tree_var39']

    @property
    def tree_var40(self):
        return self.__values['tree_var40']

    @property
    def tree_var41(self):
        return self.__values['tree_var41']

    @property
    def tree_var42(self):
        return self.__values['tree_var42']

    @property
    def tree_var43(self):
        return self.__values['tree_var43']

    @property
    def tree_var44(self):
        return self.__values['tree_var44']

    @property
    def tree_var45(self):
        return self.__values['tree_var45']

    @property
    def tree_var46(self):
        return self.__values['tree_var46']

    @property
    def tree_var47(self):
        return self.__values['tree_var47']

    @property
    def tree_var48(self):
        return self.__values['tree_var48']

    @property
    def carbon_stem(self):
        return self.__values['carbon_stem']

    @property
    def carbon_branches(self):
        return self.__values['carbon_branches']

    @property
    def carbon_roots(self):
        return self.__values['carbon_roots']

    @property
    def wb(self):
        return self.__values['wb']

    @property
    def ws(self):
        return self.__values['ws']

    @property
    def carbon_heartwood(self):
        return self.__values['carbon_heartwood']

    @property
    def carbon_sapwood(self):
        return self.__values['carbon_sapwood']

    @property
    def carbon_bark(self):
        return self.__values['carbon_bark']

    @property
    def saw_big_liferebollo(self):
        return self.__values['saw_big_liferebollo']

    @property
    def saw_small_liferebollo(self):
        return self.__values['saw_small_liferebollo']

    @property
    def staves_intona(self):
        return self.__values['staves_intona']

    @property
    def bottom_staves_intona(self):
        return self.__values['bottom_staves_intona']

    @property
    def wood_panels_gamiz(self):
        return self.__values['wood_panels_gamiz']

    @property
    def mix_garcia_varona(self):
        return self.__values['mix_garcia_varona']

    @property
    def carbon(self):
        return self.__values['carbon']

###############################################################################################################
################################################### STATUS ####################################################
###############################################################################################################

    @property
    def status(self):
        return self.__values['status']





    def set_status(self, value):
        self.__values['status'] = value

    def clone(self, tree):
        """
        Function used to clone the tree information.
        It is used on basic_engine file.
        """
        
        for var_name in TREE_VARS:
            self.__values[var_name] = tree.get_value(var_name)

    def create_new_from_clone(self, tree, n_code):
        """
        Function used to create a new tree from a clone of a real tree information.
        It is used on basic_engine file.
        Args.:
            - self: list of trees (alive/ingrowth)
            - tree: tree information to clone
            - n_code: flag to know if a new tree should have a new code or not (each new tree is created twice, with status = 'I' and '')
        """

        for var_name in TREE_VARS:

            # I just give to the tree a new label, the rest of variables are calculated on basic_engine
            if var_name == 'TREE_ID':

                # global variable to don't repeat new codes
                global new_ingrowth_tree
                if n_code == 'new':
                    new_ingrowth_tree += 1

                self.__values[var_name] = new_ingrowth_tree

            else:
                self.__values[var_name] = tree.get_value(var_name)


    def json(self, tree):
        return json.dumps(self.__values)

    @staticmethod
    def sum_tree_list(trees: list, variable: str):
        """
        Function needed to calculate the amount of N of the plot.
        PercentOfTrees file uses that function in order to cut the exactly proportion of trees that the user stablish.
        """

        sum = 0

        for tree in trees:
            sum += tree.get_value(variable)

        return sum

    @staticmethod
    def get_sord_and_order_tree_list(input, search_criteria=None, order_criteria=None):
        """
        Function neccesary to set an order of the trees in a plot.
        It is used in multiple files, models included.
        """

        def sort_key(element: Tree):
            if element.get_value(order_criteria.get_first()) is None:
                return 0.0
            return element.get_value(order_criteria.get_first())

        if isinstance(input, dict):
            data = input.values()
        elif isinstance(input, list) or isinstance(input, {}.values().__class__):
            data = input
        else:
            Tools.print_log_line('Input list must be list and dict', logging.WARNING)
            return None

        tmp = list()

        if search_criteria is not None:
            for tree in data:
                valid = 0
                for criteria in search_criteria.criterion:
                    if criteria.is_valid(tree.get_value(criteria.variable)):
                        valid += 1

                if valid == len(search_criteria.criterion):
                    tmp.append(tree)
        else:
            for tree in data:
                tmp.append(tree)

        if order_criteria is not None:
            tmp = sorted(tmp, key=sort_key, reverse=False if order_criteria.type == DESC else True)

        return tmp

    def calculate_tree_from_plot(self, plot):
        """
        Function designed to obtain the mean of tree values from the plot information.
        Actually it is not working, is a simple translation from the last Simanfor
        """

        self.__values['expan'] = plot.density
        self.__values['height'] = plot.dominant_h
        self.__values['basal_area'] = plot.basal_area * 10000 / self.__values['expan']
        # self.__values['dbh'] = 2 * math.sqrt(self.__values['basal_area'] / math.pi)
        self.__values['slenderness'] = self.__values['height'] * 100 / self.__values['dbh']
        self.__values['tree_age'] = plot.age
        self.__values['vol'] = plot.vol / self.__values['expan']
        self.__values['bole_vol'] = plot.bole_vol / self.__values['expan']
        self.__values['lcw'] = plot.crown_dom_d

    def print_value(self, variable, decimals: int = 2):
        """
        Function neccesary to print the tree values on the output (except node 0).
        """
        
        if variable not in STR_VALUES:
            if isinstance(self.__values[variable], str):
                if len(self.__values[variable]) > 0 and variable not in JSON_STR_VALUES:
                    return self.__values[variable]
            elif variable not in JSON_STR_VALUES:
                if self.__values[variable] == None:
                    self.__values[variable] = 0
                return round(float(self.__values[variable]), decimals)
        return self.__values[variable]

    def print_value_original(self, variable, decimals: int = 2):
        """
        Function neccesary to print the tree values on the output (only node 0).
        """
        
        if variable not in STR_VALUES:
            if isinstance(self.__values_original[variable], str):
                if len(self.__values_original[variable]) > 0 and variable not in JSON_STR_VALUES:
                    return self.__values_original[variable]
            elif variable not in JSON_STR_VALUES:
                if self.__values_original[variable] == None:
                    self.__values_original[variable] = 0
                return round(float(self.__values_original[variable]), decimals)
        return self.__values_original[variable]

    def to_json(self):
        """
        Function used to print tree information at json output file.
        """
        
        content = dict()

        for key, value in self.__values.items():
            content[key] = value

        return content

    def to_xslt(self, sheet, row, decimals: int = 2):
        """
        Function used to print tree information at xlsx output file.
        """
        
        column = 0

        for key in self.__values.keys():
            column += 1
            sheet.cell(row=row, column=column).value = self.print_value(key, decimals)

    def to_xslt_original(self, sheet, row, decimals: int = 2):
        """
        Function used to print tree information at xlsx output file.
        That function runs only at node 0.
        """
        
        column = 0

        for key in self.__values_original.keys():
            column += 1
            sheet.cell(row=row, column=column).value = self.print_value_original(key, decimals)

