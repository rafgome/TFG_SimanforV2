#!/usr/bin/env python
#
# Copyright (c) $today.year Moises Martinez (Sngular). All Rights Reserved.
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

import json
import logging
import os

from .reader import Reader
from util import Tools


class JSONReader(Reader):


    def __init__(self, input_files: list):


        self.__documents = dict()
        self.__cursor = 0
        self.__sheet = None
        self.__headers = None
        
        for filetype, filename in input_files.items():
            
            if not os.path.exists(filename):
                Tools.print_log_line('filename ' + filename + " does not exists.", logging.ERROR)
                exit(-1)
            
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:

                self.__documents[filetype] = json.loads(f.read())
                Tools.print_log_line('Inventory file ' + filename + ' loaded', logging.INFO)


    @property
    def document(self):
        return self.__document


    def choose_sheet(self, sheet, has_header=False):
        """
        Function that obtain the documents and import the data to the simulator.
        """

        self.__sheet = self.__documents[sheet]
        self.__cursor = -1
        
        if has_header:  # if the inventory has header...
            self.__cursor = 0
            self.__headers = list()
            header = self.__sheet['head']['vars']

            for item in header:  # it will receive the names of the variables
                self.__headers.append(item)


    def __iter__(self):
        return self


    def __next__(self):


        if self.__sheet is None:  # if no information is imported
            Tools.print_log_line("No sheet have been chosen.", logging.ERROR)
            raise StopIteration

        if len(self.__sheet['results']['bindings']) <= self.__cursor:  # iterator needed to stablish when the initial inventory has no more data
            raise StopIteration

        else:
            result = {}
            data = self.__sheet['results']['bindings'][self.__cursor]  # import the values of the inventory (plot or tree)

            if self.__headers is None:  # if the document hasn't headers...
                for i in range(len(data)):  # for each variable...
                    result[i] = data[self.__headers[i]]['value']  # we add the value to the plot/tree of the selected row
            else:  # if the document has headers...
                for i in range(len(data)):  # for each variable...
                    result[self.__headers[i]] = data[self.__headers[i]]['value']  # we add the value to the plot/tree of the selected row

            self.__cursor = self.__cursor + 1

            return result  # and return the result (only 1 plot/tree per iteration)

        raise StopIteration


    def read(self):
        return self.__next__()
