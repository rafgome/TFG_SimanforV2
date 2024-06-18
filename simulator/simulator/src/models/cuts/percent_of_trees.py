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

from .cut_down import CutDownType
from data.tree import Tree
from util import Tools

import logging


class PercentOfTrees(CutDownType):

    def __init__(self):
        super().__init__(type='PercentOfTrees')
        Tools.print_log_line('Creating percents of trees cut technique', logging.INFO)

    def cut_discriminator(self, trees, value):
        """
        Function needed to calculate the amount of N to cut by using the user values.
        """

        if value < 0 or value > 100:
            Tools.print_log_line('Value must debe ser un valor entre 0 y 100', logging.ERROR)
        else:
            return Tree.sum_tree_list(trees, 'expan')*((100 - value)/100.0)  # that function send the limit, in terms of N, to realise the cut
        return 0

    def accumulator(self, tree: Tree):
        """
        Function used by cut types files, that return the value of each tree to the cut criteria.
        """

        return tree.expan

    def compute_expan(self, tree: Tree, accumulator: float, cut_discriminator: float):
        """
        Function that calculate, for the last tree alive, the amount of expan that will continue alive and the part that will be cut.
        """

        return accumulator - cut_discriminator

