#!/usr/bin/env python
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from simulation.inventory import Inventory
from scenario import OperationType
from scenario import Operation
from data.variables import CUTS_DICT

import i18n


class Step:
    """
    That class is the one used to print the scenario information at the output.
    """

    def __init__(self,
                 id: int,
                 inventory: Inventory,
                 op: OperationType,
                 description: str,
                 age: int,
                 min_age: int,
                 max_age: int,
                 operation: Operation,
                 cut_name: str):

        self.__id = id
        self.__operation = op
        self.__description = description
        self.__inventory = inventory
        self.__age = age
        self.__min_age = min_age
        self.__max_age = max_age
        # TODO: creo que aquí habría que eliminar el time del escenario y poner el correspondiente a cada modelo para evitar problemas de los usuarios
        self.__cut_time = operation.get_variable('time') if operation.has('time') else 0
        self.__cut_type = cut_name
        self.__severity = operation.get_variable('volumen') if operation.has('volumen') else None
        #self.__severity = operation.get_variable('intensity') if operation.has('intensity') else None
        self.__cut_criteria = CUTS_DICT[operation.get_variable('cut_down')] if operation.has('cut_down') else ''
        self.__preserve = operation.get_variable('preserve_trees') if operation.has('preserve_trees') else ''
        self.__species = operation.get_variable('species') if operation.has('species') else ''
        self.__volume_target = operation.get_variable('volume_target') if operation.has('volume_target') else ''
        self.__generate_output = True
        self.__full_operation = operation

    @property
    def id(self):
        return self.__id

    @property
    def action(self):
        return self.__action

    @property
    def age(self):
        return self.__age

    @property
    def cut_time(self):
        return self.__cut_time

    @property
    def inventory(self):
        return self.__inventory

    @property
    def description(self):
        return self.__description

    @property
    def preserve_trees(self):
        return self.__preserve_trees

    @property
    def species(self):
        return self.__species

    @property
    def volume_target(self):
        return self.__volume_target

    def is_printable(self):
        return self.__generate_output

    def generate_sheet(self):
        return self.__inventory.xslt()

    def generate_json_file(self, file_path):
        return self.__inventory.json()

    def plots_to_xslt(self, workbook):
        return

    def get_plot_ids(self):
        return self.inventory.get_plot_ids()

    def to_json(self, plot_id, names, row):
        """
        That function is not used
        """

        content = dict()

        values = dict()

        # trees_sheet is not programmed

        values[i18n.t('simanfor.general.' + names[0])] = self.__id - 1
        values[i18n.t('simanfor.general.' + names[1])] = self.__age
        values[i18n.t('simanfor.general.' + names[2])] = self.__min_age
        values[i18n.t('simanfor.general.' + names[3])] = self.__max_age
        values[i18n.t('simanfor.general.' + names[4])] = i18n.t('simanfor.general.' + self.__operation.get_code_name())
        values[i18n.t('simanfor.general.' + names[5])] = self.__cut_time
        values[i18n.t('simanfor.general.' + names[6])] = self.__cut_type
        values[i18n.t('simanfor.general.' + names[7])] = self.__severity
        values[i18n.t('simanfor.general.' + names[9])] = self.__cut_criteria
        values[i18n.t('simanfor.general.' + names[8])] = self.__preserve
        values[i18n.t('simanfor.general.' + names[10])] = self.__species
        values[i18n.t('simanfor.general.' + names[11])] = self.__volume_target

        content['info'] = values
        content['inventory'] = self.inventory.to_json(plot_id, None)

        return content

    def to_xslt(self, labels: dict, workbook, plot_id: int, scenario_file_name:str, row: int, next_step, next_operation,
                summary_row: int, decimals: int = 2):
        """
        Function to print the scenario information at the plot sheet.
        """
        
        ws_plot = workbook[labels['simanfor.general.plot_sheet']]

        global plots_count
        global node

        if plots_count != plot_id:  # when simulate different plots, is needed to recognise when a different one will be printed and restart the count
            node = 0
            plots_count = plot_id

        if node == 0:
            trees_sheet = labels['simanfor.general.initial_inventory']
            node += 1
        else:
            trees_sheet = (labels['simanfor.general.node_sheet'] + ' ' + str(node) + ' - ' + labels['simanfor.general.trees_sheet'])
            node += 1

        if self.__min_age == '' or self.__min_age == None:
            self.__min_age = '-'
        if self.__max_age == '' or self.__max_age == None:
            self.__max_age = '-'
        if self.__cut_type == '' or self.__cut_type == None:
            self.__cut_type = '-'
        if self.__severity == '' or self.__severity == None:
            self.__severity = '-'
        if self.__cut_criteria == '' or self.__cut_criteria == None:
            self.__cut_criteria = '-'
        if self.__preserve == '' or self.__preserve == None:
            self.__preserve = '-'
        if self.__species == '' or self.__species == None:
            self.__species = '-'
        if self.__volume_target == '' or self.__volume_target == None:
            self.__volume_target = '-'

        #ws_plot.cell(row=self.__id+1, column=1).value = self.__id - 1  3 we don't want to show that variable at the output
        ws_plot.cell(row=self.__id+1, column=1).value = scenario_file_name  # silenciate that line and reorder the following columns to eliminate the scenario file name of the output
        ws_plot.cell(row=self.__id+1, column=2).value = trees_sheet
        ws_plot.cell(row=self.__id+1, column=3).value = self.__age  # scenario age
        ws_plot.cell(row=self.__id+1, column=4).value = self.__min_age  # minimum scenario application age
        ws_plot.cell(row=self.__id+1, column=5).value = self.__max_age  # maximum scenario application age
        ws_plot.cell(row=self.__id+1, column=6).value = labels['simanfor.general.' + self.__operation.get_code_name()]  # name of the operation
        ws_plot.cell(row=self.__id+1, column=7).value = self.__cut_time  # time of the cut (should be 0)
        ws_plot.cell(row=self.__id+1, column=8).value = self.__cut_type  # type of the cut (by above, by below, systematic)
        ws_plot.cell(row=self.__id+1, column=9).value = self.__cut_criteria  # cut criteria
        ws_plot.cell(row=self.__id+1, column=10).value = self.__severity  # cut severity
        ws_plot.cell(row=self.__id+1, column=11).value = self.__preserve  # trees to preserve
        ws_plot.cell(row=self.__id+1, column=12).value = self.__species  # species to harvest
        ws_plot.cell(row=self.__id+1, column=13).value = self.__volume_target  # volume target when thinning by species


        if self.__cut_criteria == '-':
            ws_plot.cell(row=self.__id+1, column=9).value = self.__cut_criteria      
        else:
            ws_plot.cell(row=self.__id+1, column=9).value = labels['simanfor.general.' + self.__cut_criteria] 

        next_inventory = None if next_step is None else next_step.__inventory

        summary_row = self.__inventory.to_xslt(labels, workbook, plot_id, self.__id, next_inventory, 
                                               next_operation, self.__full_operation, summary_row, decimals)
        return summary_row

plots_count = node = 0