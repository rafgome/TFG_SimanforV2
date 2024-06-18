#/usr/bin/env python3
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License", Version 2.0 (the "License")
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

# Poda por lo bajo

from models.harvest_model import HarvestModel
from data.plot import Plot
from data.tree import Tree
from data.general import Warnings
from data.search import OrderCriteria
from data.search import SearchCriteria
from data.search import EQUAL
from data.search import ASC
from data.search import DESC
from util import Tools
from models.trees.equations_tree_models import TreeEquations

import logging
import i18n

class CutDownSupport(HarvestModel):

    def running_message(harvest_type, value, harvest_criteria, preserve_trees, plot_id):
        """
        Print a message on the terminal to know which type of harvest if going to be applied.
        It is called from the harvest models.
        Args.:
            - harvest_type: harvest type selected by the user on the scenario
            - value: amount of trees to cut provided by the user on the scenario (%)
            - harvest_criteria: criteria to apply the harvest intensity provided by the user on the scenario
            - preserve_trees: amount of bigger trees to preserve provided by the user on the scenario (%, 15% by default)
            - plot_id: plot unique identification code
        """

        print('#--------------------------------------------------------------------------------------------------#')
        if harvest_type != 'systematic thinning with future trees' and harvest_type != 'high thinning with future trees':
            print(' Running: ', harvest_type, ', harvesting ', value, '% of the ', harvest_criteria, '. Plot: ', plot_id, sep='')
        else:
            print(' Running: ', harvest_type, ', harvesting ', value, '% of the ', harvest_criteria, ' and presenving the ',
            preserve_trees, '% of bigger trees. Plot: ', plot_id, sep='')
        print('#--------------------------------------------------------------------------------------------------#')

    def check_time(time):
        """
        Print a message on the terminal to know then the time established on the scenario is wrong.
        It activates a warning on the output.
        It is called from the harvest models.
        Args.:
            - time: time value provided by the user on the scenario (years)
        """

        if time != 0 and time != None:

            print('BE CAREFUL! When planning a harvest the scenario time must be 0 instead of ', time,
                  '!', sep='')
            print('Please, set the harvest time value to 0 on the scenario and run your simulation again.')
            # that variable must be activated just in case if the time of the cut is different to 0
            Warnings.cut_error = 1  # that variable value must be 1 to notify the error at the output


    def plot_data_selection(plot, order):
        """
        Selects the correct plot information to develop the thinning process.
        When trees are "invented" on the ingrowth function, then the argument "full=True" must be activated when
        accessing to the plot information. In other cases, that argument is leaved by default (False).
        It results the correct plot data and a list of the trees inside the plot.
        It is called from the harvest models.
        Args.:
            - plot: is the plot information received by the harvest model
            - order: is the order selected for the trees, important for develop the harvest types in the correct way
        """

        # clone plot data
        new_plot = Plot()
        new_plot.clone(plot)  # temporally it is cloned not taking into account ingrowth trees

        # establish an order (from lower to bigger dbh)
        order_criteria = OrderCriteria(order)
        order_criteria.add_criteria('dbh')

        # establish a criteria
        search_criteria = SearchCriteria()
        search_criteria.add_criteria('status', None, EQUAL)  # Cuts only are done over alive trees

        # get list of trees (temporally)
        trees = Tree.get_sord_and_order_tree_list(plot.trees, search_criteria=search_criteria,
                                                  order_criteria=order_criteria)  # import tree information

        # ingrowth flag: it will be activated if ingrowth function had included new trees on the plot
        ingrowth_flag = False

        # for each tree...
        for tree in trees:
            # check if the tree was created by the ingrowth function of the simulator
            if isinstance(tree.tree_id, int) and tree.tree_id >= 1000000:
                # if any tree was created by the ingrowth function, then the flag is activated
                ingrowth_flag = True
                break

        # if the flag was activated, full=True parameter is needed to pick the correct plot dataset
        if ingrowth_flag:
            new_plot.clone(plot, full=True)  # full = True also includes trees created by ingrowth
        else:
            new_plot.clone(plot)

        # the correct plot information and the tree list is the result of the function
        return new_plot, trees

