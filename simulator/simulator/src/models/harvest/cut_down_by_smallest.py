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

class CutDownBySmallest(HarvestModel):

    def __init__(self, configuration=None):
        super().__init__(name="Cut Down by Smallest", version=1, type=configuration['cut_down'])

    def initialize(self, plot: Plot):
        return

    def apply_model(self, plot: Plot, time: int, value: float, preserve_trees, species, volume_target, cut_criteria):
        """
        Function that imports the scenario variables to apply the "cut down by smallest" havest model
        That function must be run only when you are working with tree models.
        """

        # activate harvest messages
        CutDownSupport.running_message(harvest_type='low thinning',
                                       value=value,
                                       harvest_criteria=self.type.get_type(),
                                       preserve_trees=preserve_trees,
                                       plot_id=plot.plot_id)

        CutDownSupport.check_time(time)

        # set needed variables
        accumulator = 0
        cut_all_the_rest = False  # flag variable

        # get plot and trees data selecting according to ingrowth function results
        new_plot, trees = CutDownSupport.plot_data_selection(plot, order=ASC)

        # uses cut discriminator programmed at the cut criteria file
        cut_discriminator = self.type.cut_discriminator(trees, value)
        # is important to remark that cut_discriminator is NOT the % of expan to cut, it's the opposite, the % of expan that will continue alive

        # I would like to set growth variables as 0 when applying harvests, but for some reason it doesn't work well
        # Even when I set growth variables again after harvests, the values continue as 0 until the last node
        # I decided to skip this step
        #TreeEquations.null_growth(trees)  # stablish growth on harvest process as 0

        for tree in trees:  # for each tree of the plot...

            accumulator += self.type.accumulator(tree)  # get and sum the value for each tree to the cut criteria file

            if not cut_all_the_rest:  # while flag variable is not activated...

                new_tree = Tree()
                new_tree.clone(tree)  # we clone the tree

                if accumulator >= cut_discriminator:  # once the sum pf trees is higher or equal to the discriminator

                    cut_all_the_rest = True  # flag is activated
                    new_expan = self.type.compute_expan(tree, accumulator, cut_discriminator)  # we calculate the amount of expan of the last tree that must continue alive

                    if new_expan <= 0:  # if the last tree has no expan alive, all the tree change to dead
                        new_tree.add_value('expan', new_expan)
                        new_tree.add_value('status', 'C')
                    else:  # if not...
                        cut_tree = Tree()
                        cut_tree.clone(tree)  # we clone again the tree
                        cut_tree.add_value('status', 'C')  # set 'C' status to the part of the expan that will be cut
                        cut_tree.add_value('expan', new_expan)  # and assign the expan

                        if cut_tree.expan > 0:
                            new_plot.add_tree(cut_tree)  # and the cut tree is added to the list

                        new_tree.sub_value('expan', new_expan)  # the part of cut expan is take away from the initial expan
                        new_tree.add_value('status', None)

                new_plot.add_tree(new_tree)  # and we add it to the list of trees

            else:  # once the flag is activated, all the trees and expan must be cut
                new_tree = Tree()
                new_tree.clone(tree)
                new_tree.add_value('status', 'C')
                new_plot.add_tree(new_tree)

        return new_plot
