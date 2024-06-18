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
from scipy import integrate
from util import Tools
from data.variables import TREE_VARS
from data.variables import PLOT_VARS

import math
import sys
import logging
import numpy as np
import os

class BasicTreeModel(TreeModel):

    def __init__(self, configuration=None):
        return 0.0

    def catch_model_exception(self):
        return 0.0

    def initialize(self, plot: Plot):
        return 0.0

    def survival(self, time: int, plot: Plot, tree: Tree):
        return 0.0

    def growth(self, time: int, plot: Plot, old_tree: Tree, new_tree: Tree):
        return 0.0

    def ingrowth(self, time: int, plot: Plot):
        return 0.0

    def ingrowth_distribution(self, time: int, plot: Plot, area: float):
        return 0.0

    def update_model(self, time: int, plot: Plot, trees: list):
        return 0.0

    def taper_over_bark(self, tree: Tree, hr: float):
        return 0.0

    def taper_under_bark(self, tree: Tree, hr: float):
        return 0.0

    def merchantable(self, tree: Tree):
        return 0.0

    def merchantable_plot(self, plot: Plot):
        return 0.0

    def crown(self, tree: Tree, plot: Plot, func):
        return 0.0

    def vol(self, tree: Tree, plot: Plot):
        return 0.0

    def biomass(self, tree: Tree):
        return 0.0

    def biomass_plot(self, plot: Plot):
        return 0.0

    def vars():
        return 0.0