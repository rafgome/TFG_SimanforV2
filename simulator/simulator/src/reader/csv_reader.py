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

import csv 
import logging
import os
import pandas as pd

from .reader import Reader
from util import Tools

class CSVReader(Reader):

    def __init__(self, input_files: list):

        # set default values to variables needed
        self.__documents = dict()
        self.__cursor = 0
        self.__sheet = None
        self.__headers = None  
        
        for filetype, filename in input_files.items():  # from the input files...
            
            if not os.path.exists(filename):  # if there is no input -> abort simulation
                Tools.print_log_line('filename ' + filename + " does not exists.", logging.ERROR)
                exit(-1)

            with open(filename, mode = 'r') as file:  # if there is a file to read...              

                self.__documents[filetype] = pd.read_csv(file)
                self.__documents[filetype] = self.__documents[filetype].to_dict(orient='list')
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

        global sheet_name  # variable created to make easy the assignment of data to each variable name
        sheet_name = sheet

        if has_header:  # if the inventory has header...
            self.__cursor = 0
            self.__headers = list()
            header = list(self.__sheet.keys())
            for item in header:  # it will receive the names of the variables
                self.__headers.append(item)


    def __iter__(self):
        return self


    def __next__(self):
        

        if self.__sheet is None:  # if no information is imported
            Tools.print_log_line("No sheet have been chosen.", logging.ERROR)
            raise StopIteration

        self.__cursor = self.__cursor + 1  # iterator

        values = list(self.__sheet.values())  # variable that contains all the values of the inventory

        if (len(values[0]) + 1) <= self.__cursor:  # iterator needed to stablish when the initial inventory has no more data
            raise StopIteration

        else:
            result = {}
            data = list(self.__sheet.values())  # import the values of the inventory (plot or tree)
            global old_sheet_name  # create a global variable to restart the variable "counter"


            if 'counter' not in globals():  # only in the first iteration...
                global counter  # we create a global variable to control the assignment of data to each variable
                counter = 0
                
                old_sheet_name = sheet_name  # and set the name of that variable to the same as the present sheet

            else:  # to all the iterations after the first one...

                if sheet_name != old_sheet_name:  # if the name of the sheet changes (plot -> tree)...
                    # we restablish the control variable names
                    counter = 0 
                    old_sheet_name = sheet_name

                else:  # for the same sheet...
                    counter += 1  # we move forward one more row


            if self.__headers is None:  # if the document hasn't headers...
#                for i in range(len(values[0])):  
                for j in range(len(data)):  # for each variable...
                    result[self.__headers[j]] = data[j][counter]  # we add the value to the plot/tree of the selected row

            else:  # if the document has headers...
 #               for i in range(len(values[0])):
                for j in range(len(data)):  # for each variable...
                    result[self.__headers[j]] = data[j][counter]  # we add the value to the plot/tree of the selected row

            return result  # and return the result (only 1 plot/tree per iteration)


    def read(self):
        return self.__next__()