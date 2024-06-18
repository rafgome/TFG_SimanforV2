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

# from models.tree_model import StandModel
from models import StandModel
from data import Tree
from data import Parcel
from util import Tools

import math


class BasicTreeModel(StandModel):

    def __init__(self, configuration=None):
        super().__init__(name="Stand Basic Model", version=21)

    def calculate_initial_inventory(self, parcel: Parcel):
        return 0.0

    def initialize(self, parcel: Parcel):

        par_a: float = 0.8534446
        par_b: float = -0.27
        par_c: float = 0.439

        parcel.add_value('SI', par_a * parcel.h_dominante / math.pow(1 - math.exp(par_b * parcel.edad / 10), 1/par_c))
        IC: float = parcel.si / 10

        parcel.add_value('VAR_1', IC)

        par_b0: float = 1.42706
        par_b1: float = 0.388317
        par_b2: float = -30.691629
        par_b3: float = 1.034549

        parcel.add_value('VCC', math.e)

        parcel.VCC = math.exp(par_b0 + par_b1 * IC + par_b2 / parcel.edad + par_b3 * math.log(parcel.a_basimetrica))

    def growth(self, plot: Parcel, new_plot: Parcel, years: int):
        new_plot: Parcel = Parcel()
        new_plot.close(plot)

        new_plot.add_value('SI', plot.si)
        new_plot.sum_value('EDAD', years)
        new_plot.add_value('VAR_1', plot.get_value('VAR_1'))

        new_ic: float = plot.si / 10

        par_a17: float = 1.9962
        par_b17: float = 0.2642
        par_c17: float = 0.46
        h0_17: float = 10 * par_a17 * math.pow(1 - math.exp(- 1 * par_b17 * plot.edad / 10), 1 / par_c17)

        par_a29: float = 3.1827
        par_b29: float = 0.3431
        par_c29: float = 0.3536
        h0_29: float = 10 * par_a29 * math.pow(1 - math.exp(- 1 * par_b29 * plot.edad / 10), 1 / par_c29)

        new_plot.add_value('VAR_2', h0_17)
        new_plot.add_value('VAR_3', h0_29)
        new_plot.add_value('H_DOMINANTE', h0_17 + (h0_29 - h0_17) * (new_ic - 1.7) / 1.2)

        par_a0: float = 5.103222
        par_b0: float = 1.42706
        par_b1: float = 0.388317
        par_b2: float = -30.691629
        par_b3: float = 1.034549

        new_plot.add_value('A_BASIMETRICA', math.pow(plot.a_basimetrica, plot.edad / new_plot.edad) * math.exp(
            par_a0 * (1 - plot.edad / new_plot.edad)))

        par_a0: float = -2.34935
        par_a1: float = 0.000000099
        par_a2: float = 4.87390

        new_plot.add_value('N_PIESHA', math.pow(math.pow(plot.n_piesha, par_a0) + par_a1 * (
                    math.pow(new_plot.edad / 100, par_a2) - math.pow(plot.edad / 100, par_a2)), 1 / par_a0))
        new_plot.add_value('VCC', math.exp(
            par_b0 + par_b1 * new_ic + par_b2 / new_plot.edad + par_b3 * math.log(plot.a_basimetrica)))
        new_plot.add_value('VAR_10', math.exp(par_b0 + par_b1 * new_ic + par_b2 / new_plot.edad + par_b3 * (
                    math.Log(plot.a_basimetrica) * plot.edad / new_plot.edad + par_a0 * (
                        1 - plot.edad / new_plot.edad))))

        par_a0: float = -1.155649
        par_a1: float = 0.976772

        new_plot.add_value('H_MEDIA', par_a0 + par_a1 * new_plot.h_dominante)

        new_sec_normal: float = new_plot.a_basimetrica * 10000 / new_plot.n_piesha
        new_plot.add_value('D_CUADRATICO', 2 * math.sqrt(new_sec_normal / math.pi))

        new_plot.add_value('VAR_8', new_plot.n_piesha * math.pow(25 / new_plot.d_cuadratico, -1.75))
        new_plot.add_value('I_REINEKE', new_plot.get_value('VAR_8'))

    def harvest(self, plot: Parcel, new_plot: Parcel):

        return
