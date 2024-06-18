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


class CutDownSystematics(HarvestModel):

    def __init__(self, configuration=None):
        super().__init__(name="Systematics cut down with Future Trees", version=1, type=configuration['cut_down'])

    def initialize(self, plot: Plot):
        return

    def apply_model(self, plot: Plot, time: int, value: float, preserve_trees, species, volume_target, cut_criteria):
        """
        Function that imports the scenario variables to apply the "cut down systematic preserving future trees" havest model
        That function must be run only when you are working with tree models.
        """

        # activate harvest messages
        CutDownSupport.running_message(harvest_type='systematic thinning with future trees',
                                       value=value,
                                       harvest_criteria=self.type.get_type(),
                                       preserve_trees=preserve_trees,
                                       plot_id=plot.plot_id)

        CutDownSupport.check_time(time)

        # get plot and trees data selecting according to ingrowth function results
        new_plot, trees = CutDownSupport.plot_data_selection(plot, order=ASC)

        # I would like to set growth variables as 0 when applying harvests, but for some reason it doesn't work well
        # Even when I set growth variables again after harvests, the values continue as 0 until the last node
        # I decided to skip this step
        #TreeEquations.null_growth(trees)  # stablish growth on harvest process as 0

        # % to preserve and harvest
        preserve = preserve_trees / 100
        harvest = 1 - preserve

        # variable to control which trees should not be harvested
        accumulator = full_accumulator = 0

        # get the stand value of the criteria variable (N, G, V)
        for tree in trees:

            # get and sum the value for each tree to the cut criteria file
            full_accumulator += self.type.accumulator(tree)

        # set the finish point of the harvest
        cut_discriminator_finish = full_accumulator * harvest

        # updating value: get nº of trees to cut and recalculate %
        value = ((value * full_accumulator) / 100)
        value = (value / cut_discriminator_finish) * 100

        # harvest preserving trees with higher dbh
        for tree in trees:

            # create variables for accumulator without and with the tree, and the tree accumulator (N, G, V)
            accumulator_before_my_tree = accumulator
            accumulator += self.type.accumulator(tree)  # get and sum the value for each tree to the cut criteria file
            # my_tree_accumulator = accumulator - accumulator_before_my_tree

            # trees to harvest using the new harvest value
            if accumulator < cut_discriminator_finish:

                # divide the tree into alive and harvested part
                new_tree = Tree()
                new_tree.clone(tree)  # tree is cloned

                new_tree.add_value('expan', tree.expan * ((100 - value) / 100))  # alive tree expan is reduced, all the trees at the same proportion
                new_tree.add_value('status', None)

                cut_tree = Tree()
                cut_tree.clone(tree)
                cut_tree.add_value('status', 'C')
                cut_tree.add_value('expan', tree.expan - new_tree.expan)  # a clone with 'C' status is created to print it at the output, with the expan cut

                if cut_tree.expan > 0:  # cut trees will appear at the output only if the cut expan exists
                    new_plot.add_tree(cut_tree)

            # tree that must be divided into harvested and alive before to apply the harvest to just one part
            elif accumulator >= cut_discriminator_finish and accumulator_before_my_tree < cut_discriminator_finish:

                # divide the tree into alive and harvested part
                new_tree = Tree()
                new_tree.clone(tree)  # tree is cloned

                # we calculate the amount of expan of the last tree that must continue alive
                expan_to_harvest = self.type.compute_expan(tree, cut_discriminator_finish, accumulator_before_my_tree)

                if expan_to_harvest <= 0:  # if the last tree has no expan alive, all the tree change to dead

                    new_tree.add_value('expan', expan_to_harvest * (value / 100))
                    new_tree.add_value('status', 'C')

                else:  # if not...

                    cut_tree = Tree()
                    cut_tree.clone(tree)  # we clone again the tree
                    cut_tree.add_value('status', 'C')  # set 'C' status to the part of the expan that will be cut
                    cut_tree.add_value('expan', expan_to_harvest * (value / 100))  # and assign the expan

                    if cut_tree.expan > 0:
                        new_plot.add_tree(cut_tree)  # and the cut tree is added to the list

                    new_tree.sub_value('expan', expan_to_harvest * (value / 100))  # the part of cut expan is take away from the initial expan
                    new_tree.add_value('status', None)

            # trees to preserve without changes
            else:

                new_tree = Tree()
                new_tree.clone(tree)  # tree is cloned

            new_plot.add_tree(new_tree)

        return new_plot
