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
        super().__init__(name="Systematics cut down", version=1, type=configuration['cut_down'])

    def initialize(self, plot: Plot):
        return

    def apply_model(self, plot: Plot, time: int, value: float, preserve_trees, species, volume_target, cut_criteria):
        """
        Function that imports the scenario variables to apply the "cut down systematic" havest model
        That function must be run only when you are working with tree models.
        """
        
        # activate harvest messages
        CutDownSupport.running_message(harvest_type='systematic thinning',
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

        trees_harvest = list()  # list of trees to harvest
        trees_not_harvest = list()  # list of trees to not harvest
        accumulator = 0  # accumulator variable
        full_accumulator = 0  # accumulator variable


        # split trees into harvest and not harvest trees
        for tree in trees:  # for each tree of the plot, split list into harvest and not harvest trees

            full_accumulator += self.type.accumulator(tree)  # get and sum the value for each tree to the cut criteria file

            if species == '' or (species != '' and int(tree.specie) == int(species)):  # if the tree is the species selected at the scenario...
                trees_harvest.append(tree)
            else:
                trees_not_harvest.append(tree)


        # manage trees to not harvest
        for tree in trees_not_harvest:  # for each tree of the plot that will be not harvested...

            # Note: that trees are processed before to avoid mistakes on the accumulator value
            accumulator += self.type.accumulator(tree)  # get and sum the value for each tree to the cut criteria file

            # preserve trees
            new_tree = Tree()
            new_tree.clone(tree)
            new_plot.add_tree(new_tree)


        # calculate cut_discriminator depending on the harvest intensity is applied over plot or species values
        if volume_target in ['species', 'especie']:  # if the volume target is referred to the species in the plot
            # get the % of expan to cut by species, according to the accumulator value
            value = value

        else:  # if the volume target is referred to the plot
            value = value * full_accumulator / 100
            value = (value / (full_accumulator - accumulator)) * 100

        # if the value is higher than 100%, as no more trees are available harvest intensity is reduced
        if value > 100:
            value = 100


        # manage trees to harvest
        for tree in trees_harvest:  # for each tree of the plot...

            new_tree = Tree()
            new_tree.clone(tree)  # tree is cloned

            new_tree.add_value('expan', tree.expan * ((100 - value) / 100))  # alive tree expan is reduced, all the trees at the same proportion
            new_tree.add_value('status', None)
            new_plot.add_tree(new_tree)

            cut_tree = Tree()
            cut_tree.clone(tree)
            cut_tree.add_value('status', 'C')
            cut_tree.add_value('expan', tree.expan - new_tree.expan)  # a clone with 'C' status is created to print it at the output, with the expan cut

            if cut_tree.expan > 0:  # cut trees will appear at the output only if the cut expan exists
                new_plot.add_tree(cut_tree)

        return new_plot
