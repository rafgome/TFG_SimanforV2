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

from dask.distributed import Client
from dask.distributed import progress

from engine import Engine
from util.tools import Tools
from simulation.inventory import Inventory
from engine.engine import DEFAULT_CONFIG

from models import TreeModel
from models import HarvestModel
from models import LoadModel
from models import StandModel
from data import Plot
from data import Tree
from data import SearchCriteria
from data import OrderCriteria
from scenario import Operation

from data import GREATEREQUAL
from data import LESS
from data import EQUAL

import logging
import math

from dask import delayed


DEFAULT_CONFIG = {
    "processes": False,
    "threads_per_worker": 1,
    "num_workers": 2,
    "memory_limit": "1GB"
}


class DaskEngine(Engine):

    def __init__(self, configuration):

        if configuration is None:
            configuration = DEFAULT_CONFIG

        # self.__processes = configuration['processes']
        # self.__threads_per_worker = configuration['threads_per_worker']
        # self.__num_workers = configuration['num_workers']
        # self.__memory_limit = configuration['memory_limit']
        # self.__client = Client(processes=self.__threads_per_worker,
        #                        threads_per_worker=self.__threads_per_worker,
        #                        n_workers=self.__num_workers,
        #                        memory_limit=self.__memory_limit)

        # self.__client = Client(n_workers=4, processes=False, threads_per_worker = 1)
        self.__client = Client(n_workers=4)

        self.__processes = None
        self.__threads_per_worker = None
        self.__num_workers = None
        self.__memory_limit = None


        # Tools.print_log_line(self.__client, logging.INFO)

        # print(self.__client)

        print('ENTRO AQUI')

    @property
    def processes(self):
        return self.__processes

    @property
    def threads_per_worker(self):
        return self.__threads_per_worker

    @property
    def num_workers(self):
        return self.____num_workers

    @property
    def memory_limit(self):
        return self.__memory_limit

    def get_info(self):
        return self.__client


    def apply_harvest_model(self, inventory: Inventory, model: HarvestModel, operation: Operation):

        result_inventory: inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        if 'AGE' in PLOT_VARS:
            plot_age = plot.age
        else:
            plot_age = 0

        for plot in inventory.plots:

            if min <= plot_age <= max:

                try:
                    new_plot = model.apply_model(plot, operation.get_variable('time'), operation.get_variable('volumen'))
                    new_plot.recalculate()
                    new_plot.cut_vars()
                    result_inventory.add_plot(new_plot)
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

            else:
                Tools.print_log_line('Plot ' + str(plot.id) + ' was not added', logging.INFO)

        return result_inventory

    def apply_harvest_stand_model(self, inventory: Inventory, model: HarvestModel, operation: Operation):

        result_inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        if 'AGE' in PLOT_VARS:
            plot_age = plot.age
        else:
            plot_age = 0

        for plot in inventory.plots:

            if min <= plot_age <= max:

                new_plot = Plot()
                new_plot.clone(plot)

                try:
                    model.apply_tree_model(plot, new_plot, operation.get_variable('time'))
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

            result_inventory.add_plot(new_plot)

        return result_inventory

    def apply_initialize_tree_model(self, inventory: Inventory, model: TreeModel, operation: Operation):

        result_inventory = Inventory()

        for plot in inventory.plots:

            new_plot = Plot()
            new_plot.clone(plot, True)

            try:
                model.initialize(new_plot)
            except Exception as e:
                Tools.print_log_line(str(e), logging.ERROR)

            #TODO: CHANGED THIS
            new_plot.recalculate()

            result_inventory.add_plot(new_plot)

        return result_inventory

    def apply_initialize_stand_model(self, inventory: Inventory, model: TreeModel, operation: Operation):

        result_inventory = Inventory()

        for plot in inventory.plots:

            new_plot = Plot()
            new_plot.clone(plot, True)

            try:
                model.initialize(new_plot)
            except Exception as e:
                Tools.print_log_line(str(e), logging.ERROR)

            # new_plot.recalculate()

            result_inventory.add_plot(new_plot)

        return result_inventory
    
    
    def recalculate_process(self, plot: Plot, model: TreeModel, time, trees: list, result_inventory: Inventory):

        plot = delayed(model.update_model)(time, plot, trees)
        plot = delayed(plot.recalculate)()
        
        return plot
    
    
    def apply_tree_model(self, inventory: Inventory, model: TreeModel, operation: Operation):

        result_inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        recalc_list = []
        # model_process_list = []

        if 'AGE' in PLOT_VARS:
            plot_age = plot.age
        else:
            plot_age = 0

        for plot in inventory.plots:

            cut_pies_mayores = list()
            dead_pies_mayores = list()
            result_pies_mayores = list()
            add_pies_mayores = list()  # aquí recojo árboles de masa añadida, con status = I

            if min <= plot_age <= max:

                new_plot = Plot()
                new_plot.clone(plot)

                search_criteria = SearchCriteria()
                search_criteria.add_criteria('status', None, EQUAL)

                source_trees = Tree.get_sord_and_order_tree_list(plot.trees, search_criteria=search_criteria)

                dead_tree = dead_n = dead_ba = dead_vol = dead_wt = 0

                for tree in source_trees:

                    survival_ratio: float = 0.0

                    try:
                        survival_ratio = model.survival(operation.get_variable('time'), new_plot, tree)
                    except Exception as e:
                        Tools.print_log_line(str(e), logging.ERROR)

                    if survival_ratio > 0:

                        new_tree = Tree()
                        new_tree.clone(tree)
                        new_tree.add_value('expan', survival_ratio * new_tree.expan)

                        new_tree_dead = Tree()
                        new_tree_dead.clone(tree)
                        new_tree_dead.add_value('status', 'M')
                        new_tree_dead.add_value('expan', (1 - survival_ratio) * new_tree_dead.expan)

                        # temporal variables to calculate plot information about dead trees
                        dead_tree = (1 - survival_ratio) * new_tree_dead.expan
                        dead_n += (1 - survival_ratio) * new_tree_dead.expan
                        if new_tree_dead.basal_area == '':
                            new_tree_dead.add_value('basal_area', 0)
                        dead_ba += dead_tree*new_tree_dead.basal_area
                        if new_tree_dead.vol == '':
                            new_tree_dead.add_value('vol', 0)
                        dead_vol += dead_tree*new_tree_dead.vol
                        if new_tree_dead.wt == '':
                            new_tree_dead.add_value('wt', 0)
                        dead_wt += dead_tree*new_tree_dead.wt

                        try:
                            model.growth(operation.get_variable('time'), new_plot, tree, new_tree)
                        except Exception as e:
                            Tools.print_log_line(str(e), logging.ERROR)

                        #ActualizaDatosPieMayor(new_tree);

                        #source_trees.update_tree(tree)

                        result_pies_mayores.append(new_tree)
                        dead_pies_mayores.append(new_tree_dead)

                new_plot.add_value('DEAD_DENSITY', dead_n)
                new_plot.add_value('DEAD_BA', dead_ba/10000)
                new_plot.add_value('DEAD_VOL', dead_vol/1000)
                new_plot.add_value('DEAD_WT', dead_wt/1000)

                                # Aquí comienza el código correspondiente a la masa añadida (ingrowth) en las ejecuciones
                # Su funcionamiento, en principio, será similar a la función de supervivencia
                # Se añadirá el EXPAN que se considere a cada árbol directamente en las ejecuciones, y mostraremos en el output un "clon" de cada árbol con el valor del 
                # EXPAN añadido, y con el status = I (Ingrowth) para poder identificarlo (como con árboles muertos)



                new_area_basimetrica: float = 0
                distribution: float = 0  # creo esta variable, que estaba sin crear

                try:
                    new_area_basimetrica = model.ingrowth(operation.get_variable('time'), new_plot);
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                if new_area_basimetrica > 0:  # si no se añade masa, se omite este paso

                    try:
                        distribution = model.ingrowth_distribution(operation.get_variable('time'), new_plot, new_area_basimetrica)

                    except Exception as e:
                        Tools.print_log_line(str(e), logging.ERROR)

                    # Distribución homogénea

                    order_criteria = OrderCriteria()
                    order_criteria.add_criteria('dbh')  # cambio add_variable por add_criteria

                    tree_to_add: Tree = Tree.get_sord_and_order_tree_list(result_pies_mayores, order_criteria=order_criteria)

                    sum_g = 0  # esta variable recoge el sumatorio de secciones normales de la parcela, para usar el valor en los cálculos posteriores
                    for tree in tree_to_add:
                        sum_g += tree.basal_area  # * tree.expan  -->  no se multiplica por tree.expan 

                    ing_tree = ing_n = ing_ba = ing_vol = ing_wt = 0

                    if distribution == None:  # si no existe una función de distribución

                        # n_trees = len(tree_to_add)  # calculamos el nº de árboles de la parcela  -->  ahora ya no hace falta, pero lo dejo de momento

                        for tree in tree_to_add:  # para los árboles que quiero añadir (todos los de la parcela serán modificados, en principio)
                            # voy a añadir una parte proporcional a cada uno; duplico la lista de árboles para que en el output se añada la masa y además se pueda
                            # mostrar que expan se ha añadido a cada árbol, tal cual se hace con los árboles muertos

                            new_d_tree = Tree()  # estos árboles serán los que se muestran sin status y pasan a la siguiente ejecución
                            new_d_tree.clone(tree)
                            new_d_tree.add_value('expan', (new_area_basimetrica*10000) / sum_g + new_d_tree.expan)  ### hay que revisar este cálculo

                            new_tree_add = Tree()  # estos árboles serán los que se muestran con status = I
                            new_tree_add.clone(tree)
                            new_tree_add.add_value('status', 'I')  # habría que conseguir que estos árboles aparecieran pintados en el output
                            new_tree_add.add_value('expan', (new_area_basimetrica*10000) / sum_g)  ### hay que revisar este cálculo

                            # temporal variables to calculate plot information about dead trees
                            ing_tree = (new_area_basimetrica*10000) / sum_g
                            ing_n += (new_area_basimetrica*10000) / sum_g
                            if new_d_tree.basal_area == '':
                                new_d_tree.add_value('basal_area', 0)
                            ing_ba += ing_tree*new_d_tree.basal_area
                            if new_d_tree.vol == '':
                                new_d_tree.add_value('vol', 0)                            
                            ing_vol += ing_tree*new_d_tree.vol
                            if new_d_tree.wt == '':
                                new_d_tree.add_value('wt', 0)                            
                            ing_wt += ing_tree*new_d_tree.wt

                            result_pies_mayores.append(new_d_tree)  # añado los árboles con EXPAN modificado a la lista
                            add_pies_mayores.append(new_tree_add)  # añado los árboles con status = I a una nueva lista

                # result_pies_mayores.extend(cut_pies_mayores)
                # result_pies_mayores.extend(dead_pies_mayores)


                    # para los modelos en los que sí hay unas condiciones establecidas en ingrowth_distribution, entonces se aplica lo siguiente

                    else:  # si existe una función de distribución definida por el usuario

                        # var = 0  # acumulador del nº de árboles de cada CD  -->  ya no es necesario, lo silencio de momento
                        sum_g = 0  # acumulador del sumatorio de secciones normales para cada CD
                        count = 0  # contador para entrar en la posición de la lista que deseamos

                        for tree in tree_to_add:  # con este bucle añado el nº de árboles que hay para cada CD puesta por el usuario                     
                            
                            for k in distribution:  # para cada CD puesta por el usuario

                                if tree.dbh >= distribution[count][0] and tree.dbh < distribution[count][1]:  # si se cumplen los límites de diámetro

                                    # var += 1  # añadimos 1 al nº de árboles que cumplen la condición 
                                    sum_g += tree.basal_area  # * tree.expan  -->  no se multiplica por tree.expan                             
                                    break  # pasamos al siguiente árbol

                                else:  # si se deja de cumplir la condición de diámetro (los árboles están ordenados por dbh, de menor a mayor)

                                    # distribution[count].append(var)  # añadimos el nº de árboles a la lista
                                    distribution[count].append(sum_g)  # añadimos la suma de secciones normales por CD a la lista
                                    count += 1  # avanzamos una posición en la lista
                                    # var = 0  # comenzamos la cuenta desde 0
                                    sum_g = 0  # comenzamos la cuenta desde 0

                        # distribution[count].append(var)  # esto es necesario para añadir el valor a la última CD
                        distribution[count].append(sum_g)  # esto es necesario para añadir el valor a la última CD

                        for tree in tree_to_add:
                        # aquí se repartirá el valor del área basimétrica en las distintas clases diamétricas (propuestas en el modelo), de manera equitativa para cada árbol

                            for k in distribution:  # para cada CD

                                if tree.dbh >= k[0] and tree.dbh < k[1]:  # si se cumplen los límites de diámetro (ordenados de menor a mayor)

                                    new_d_tree = Tree()  # estos árboles serán los que se muestran sin status y pasan a la siguiente ejecución
                                    new_d_tree.clone(tree)
                                    new_d_tree.add_value('expan', (k[2]*10000) / k[3] + new_d_tree.expan)  # añadimos la parte proporcional del expan a cada árbol
                                    # OJO! Si hubiera que meter de nuevo el nº de pies en cada CD, entonces las posiciones de las listas variarían!
                                    new_tree_add = Tree()  # estos árboles serán los que se muestran con status = I
                                    new_tree_add.clone(tree)
                                    new_tree_add.add_value('status', 'I')  # habría que conseguir que estos árboles aparecieran pintados en el output
                                    new_tree_add.add_value('expan', (k[2]*10000) / k[3])  # añadimos la parte proporcional del expan a cada árbol

                                    # temporal variables to calculate plot information about dead trees
                                    ing_tree = (k[2]*10000) / k[3]
                                    ing_n += (k[2]*10000) / k[3]
                                    if new_d_tree.basal_area == '':
                                        new_d_tree.add_value('basal_area', 0)                                    
                                    ing_ba += ing_tree*new_d_tree.basal_area
                                    if new_d_tree.vol == '':
                                        new_d_tree.add_value('vol', 0)                                       
                                    ing_vol += ing_tree*new_d_tree.vol
                                    if new_d_tree.wt == '':
                                        new_d_tree.add_value('wt', 0)                                       
                                    ing_wt += ing_tree*new_d_tree.wt

                                    result_pies_mayores.append(new_d_tree)  # añado los árboles con EXPAN modificado a la lista
                                    add_pies_mayores.append(new_tree_add)  # añado los árboles con status = I a una nueva lista
                                    
                                    break  # salto al árbol siguiente
                                                
                    new_plot.add_value('ING_DENSITY', ing_n)
                    new_plot.add_value('ING_BA', ing_ba/10000)
                    new_plot.add_value('ING_VOL', ing_vol/1000)
                    new_plot.add_value('ING_WT', ing_wt/1000)   

                result_pies_mayores.extend(cut_pies_mayores)  # se añaden los pies cortados
                result_pies_mayores.extend(dead_pies_mayores)  # se añaden los pies muertos
                result_pies_mayores.extend(add_pies_mayores)  # añado árboles con status = I
                
                new_plot.add_trees(result_pies_mayores)
                # new_plot.recalculate()  --> Spiros

                # recalc_list.append(self.recalculate_process(new_plot, model, 
                #        operation.get_variable('time'), result_pies_mayores, result_inventory))

                try:
                    model.update_model(operation.get_variable('time'), new_plot, result_pies_mayores)
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                new_plot.recalculate()

                result_inventory.add_plot(new_plot)

            else:
                Tools.print_log_line('Plot ' + str(plot.id) + ' was not added', logging.INFO)

        # pdb.set_trace()
        # result_inventory = (delayed(result_inventory.add_plots)(recalc_list)).compute(scheduler="single-threaded")
        # result_inventory = (delayed(result_inventory.add_plots)(recalc_list)).compute(scheduler="threads")
        # result_inventory = (delayed(result_inventory.add_plots)(recalc_list)).compute(scheduler="processes")
        ### result_inventory = (delayed(result_inventory.add_plots)(recalc_list)).compute(scheduler="distributed") # default, same as empty ""

        return result_inventory
    

    def apply_tree_stand_model(self, inventory: Inventory, model: StandModel, operation: Operation):

        result_inventory = Inventory()

        min = operation.get_variable('min_age') if operation.has('min_age') else 0
        max = operation.get_variable('max_age') if operation.has('max_age') else 1000000

        if 'AGE' in PLOT_VARS:
            plot_age = plot.age
        else:
            plot_age = 0

        for plot in inventory.plots:

            if min <= plot_age <= max:

                new_plot = Plot()
                new_plot.clone(plot)

                try:
                    model.apply_tree_model(plot, new_plot, operation.get_variable('time'))
                except Exception as e:
                    Tools.print_log_line(str(e), logging.ERROR)

                result_inventory.add_plot(new_plot)

        return result_inventory

    def apply_load_model(self, file_path: str, model: LoadModel, operation: Operation):
        return model.apply_model(file_path, operation.get_variable('init'))

    def close(self):
        self.__client.close()
        # exit(-1)
        return
