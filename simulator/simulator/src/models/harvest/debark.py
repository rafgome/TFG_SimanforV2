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
from models.harvest.cut_down_support import CutDownSupport

import logging
import i18n

class Debark(HarvestModel):

    def __init__(self, configuration=None):
        super().__init__(name="Debark", version=1, type=configuration['cut_down'])

    def initialize(self, plot: Plot):
        return

    def apply_model(self, plot: Plot, time: int, dbh_min: float, preserve_trees, species, volume_target, cut_criteria):
        """
        Function that imports the scenario variables to apply the "cut down by smallest" havest model
        That function must be run only when you are working with tree models.
        """

        # activate harvest messages
        CutDownSupport.running_message(harvest_type='debark thinning',
                                       value=value,
                                       harvest_criteria=self.type.get_type(),
                                       preserve_trees=preserve_trees,
                                       plot_id=plot.plot_id)

        CutDownSupport.check_time(time)


        # declare global variables
        global w_debark
        global v_debark

        # get plot and trees data selecting according to ingrowth function results
        new_plot, trees = CutDownSupport.plot_data_selection(plot, order=ASC)

        # I would like to set growth variables as 0 when applying harvests, but for some reason it doesn't work well
        # Even when I set growth variables again after harvests, the values continue as 0 until the last node
        # I decided to skip this step
        #TreeEquations.null_growth(trees)  # stablish growth on harvest process as 0

        for tree in trees:  # for each tree of the plot...

            new_tree = Tree()
            new_tree.clone(tree)  # tree is cloned

            if new_tree.dbh > dbh_min:  # if tree diameter is higher than the minimum stablished

                if new_tree.count_debark == 0:
                    new_tree.add_value('h_debark', 2)
                    new_tree.add_value('nb', 0)
                elif new_tree.count_debark == 1:
                    new_tree.add_value('h_debark', 2.5)
                    new_tree.add_value('nb', 2)
                else:
                    new_tree.add_value('h_debark', 3)
                    new_tree.add_value('nb', 4)

                new_tree.sum_value('count_debark', 1)

                new_tree.sum_value('total_w_debark', new_tree.w_cork)
                w_debark += new_tree.w_cork*new_tree.expan/1000
                
                new_tree.sum_value('total_v_debark', new_tree.bark_vol)
                v_debark += new_tree.bark_vol*new_tree.expan/1000

                new_tree.add_value('w_cork', 0)
                new_tree.add_value('bark_vol', 0)

                new_tree.add_value('dbh_oc', new_tree.dbh)
                new_tree.add_value('bark', 0.01)

            new_tree.add_value('status', None)
            new_plot.add_tree(new_tree)

        Plot.debark_plot(new_plot, w_debark, v_debark)  # upload plot cork variables      

        return new_plot

w_debark = v_debark = 0