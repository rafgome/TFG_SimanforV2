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

from data.plot import Plot
from data.tree import Tree
from util import Tools
from abc import ABCMeta
from abc import abstractmethod
from data.variables import CUTS_LIST

import logging


class CutDownType(metaclass=ABCMeta):

    @staticmethod
    def get_avaliable_types():
        return CUTS_LIST

    def get_type_code(self, type: str):
        type_upper = type.upper()
        for i in range(len(CUTS_LIST)):
            if type_upper == CUTS_LIST[i][0]:
                return i

    def __init__(self, type: str = None):
        self.__type = self.get_type_code(type)

    @property
    def type(self):
        return self.__type

    def get_type(self):
        """
        That function returns the name of the cut criteria.
        There is an error when the cut type is VOLUME, that is why I created this if/else construction.
        """
        if self.__type == None:
            return CUTS_LIST[1][1]
        else:
            return CUTS_LIST[self.__type][1]

    def get_code_type(self):
        return CUTS_LIST[self.__type][0]

    @abstractmethod
    def cut_discriminator(self, trees: list, value: float):
        return

    @abstractmethod
    def accumulator(self, tree: Tree):
        return

    @abstractmethod
    def compute_expan(self, tree: Tree, accumulator: float, cut_discriminator: float):
        return
