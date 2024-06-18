#!/usr/bin/env python
#
# Copyright (c) $today.year Spiros Michalakopoulos (Sngular). All Rights Reserved.
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

OUTPUT_FILE_BASE = 'Output_Plot_'
OUTPUT_EXTENSION = ['xlsx', 'json']

AREA_VARS = [  # list of variables that give information about the study area (imported from inventory)
    'PLOT_TYPE',
    'PLOT_AREA',
    'PROVINCE',
    'STUDY_AREA',
    'MUNICIPALITY',
    'FOREST',
    'PROV_REGION',
    'MAIN_SPECIE',
    'SPECIE_IFN_ID', 
    'SLOPE',  # Slope  # (%)
    'ASPECT',  # Aspect  # (rad)
    'CONTINENTALITY',  # Continentality  # (linear distance to the Mediterranean sea, Km)
    'LONGITUDE',
    'LATITUDE',
    'ALTITUDE',
    'AA_RAINFALL',
    'MA_TEMPERATURE',
    'SEPTEMBER_RAIN',
    'SEPTEMBER_TEMP',
    'NOVEMBER_RAIN',
    'NOVEMBER_TEMP',
    'MARTONNE',
    'MARTONNE_2020',
    'MARTONNE_2040',
    'MARTONNE_2060',
    'MARTONNE_2080',

    # Cistus ladanifer special variables
    'TR',  # Treatment_type  # dummy variable (equal to 1 if the scrubland was developed on burned area and equal to 0 if the scrubland was developed on cleared area)
    'RAIN_AS',  # Rainfall_AS  # sum of the total precipitation of August and September (mm)
    'TMIN_SO',  # Tmin_SO  # is the sum of the minimum absolute temperature of September and October (ºC)
    'TMIN_ON',  # Tmin_ON  # is the sum of the minimum absolute temperature of October and November (ºC)
    'TMIN_OND',  # Tmin_OND  # is the sum of the minimum absolute temperature of October, November and December (ºC)
    'TMMIN_OCT',  # Tmmin_O  # mean minimum temperature of October (ºC)
    'TSUM_MEAN_SO',  # Tsum_mean_SO  # is the sum of the mean temperatures of September and October (ºC)
    'TSUM_MMIN_SO',  # Tsum_mmin_SO # is the sum of the mean minimum temperatures of September and October (ºC)
    'TSUM_MMIN_ON',  # Tsum_mmin_ON  # is the sum of the mean minimum temperatures of October and November (ºC)
    'TSUM_MMIN_SOND'  # Tsum_mmin_SOND  # is the sum of the mean minimum temperatures of September, October, November and December (ºC)
   
]


CUTS_LIST = [  # list of the cut types available on the simulator
    ('PERCENTOFTREES', 'PercentOfTrees'), 
    ('VOLUME', 'Volume'), 
    ('AREA', 'Area')
]

CUTS_DICT = {  # dictionary of the cut types available on the simulator
    'PERCENTOFTREES': 'Percent of trees',
    'VOLUME': 'Volumen',
    'AREA': 'Area'
}

MODEL_VARS = [  # list of model variables (created on each model)
    'MODEL_NAME',
    'SPECIE_IFN_ID',  # IFN (Spanish National Forestal Inventory) ID of the main specie    
    "APLICATION_AREA",
    "VALID_PROV_REG",
    "EXEC_TIME",
    "MODEL_TYPE",
    "MODEL_CARD_ES",
    "MODEL_CARD_EN"
]

PLOT_VARS = [  # list of plot variables on the simulator

    # IDs
    'INVENTORY_ID',
    'PLOT_ID',

    # Plot general information - temporal variables ---> AREA_VARS
    'PLOT_TYPE',
    'PLOT_AREA',
    'PROVINCE',
    'STUDY_AREA',
    'MUNICIPALITY',
    'FOREST',
    'PROV_REGION',
    'MAIN_SPECIE',
    'SPECIE_IFN_ID',  # IFN (Spanish National Forestal Inventory) ID of the main specie
    'ID_SP1',  # IFN (Spanish National Forestal Inventory) ID specie 1 - mixed models
    'ID_SP2',  # IFN (Spanish National Forestal Inventory) ID specie 2 - mixed models
    'SLOPE',  # Slope  # (%)
    'ASPECT',  # Aspect  # (rad)
    'CONTINENTALITY',  # Continentality  # (linear distance to the Mediterranean sea, Km)
    'LONGITUDE',
    'LATITUDE',
    'ALTITUDE',
    'AA_RAINFALL',
    'MA_TEMPERATURE',
    'SEPTEMBER_RAIN',
    'SEPTEMBER_TEMP',
    'NOVEMBER_RAIN',
    'NOVEMBER_TEMP',    
    'MARTONNE',
    'MARTONNE_2020',
    'MARTONNE_2040',
    'MARTONNE_2060',
    'MARTONNE_2080',

    # Cistus ladanifer special variables    
    'TR',  # Treatment_type  # dummy variable (equal to 1 if the scrubland was developed on burned area and equal to 0 if the scrubland was developed on cleared area)
    'RAIN_AS',  # Rainfall_AS  # sum of the total precipitation of August and September (mm)
    'TMIN_SO',  # Tmin_SO  # is the sum of the minimum absolute temperature of September and October (ºC)
    'TMIN_ON',  # Tmin_ON  # is the sum of the minimum absolute temperature of October and November (ºC)
    'TMIN_OND',  # Tmin_OND  # is the sum of the minimum absolute temperature of October, November and December (ºC)
    'TMMIN_OCT',  # Tmmin_O  # mean minimum temperature of October (ºC)
    'TSUM_MEAN_SO',  # Tsum_mean_SO  # is the sum of the mean temperatures of September and October (ºC)
    'TSUM_MMIN_SO',  # Tsum_mmin_SO # is the sum of the mean minimum temperatures of September and October (ºC)
    'TSUM_MMIN_ON',  # Tsum_mmin_ON  # is the sum of the mean minimum temperatures of October and November (ºC)
    'TSUM_MMIN_SOND',  # Tsum_mmin_SOND  # is the sum of the mean minimum temperatures of September, October, November and December (ºC)


    # Basic plot variables measured
    "EXPAN",  # Expan  # expansion factor
    'YEAR',  # year of the inventory
    "AGE",  # plot age (years)
    "SP1_PROPORTION",  # proportion of specie 1 on a mix plot - mixed models
    "SP2_PROPORTION",  # proportion of specie 2 on a mix plot - mixed models
    'SP1_N_PROPORTION',
    'SP2_N_PROPORTION',
    'SP3_N_PROPORTION',
    "DENSITY",  # plot density (nº trees/ha)
    "DENSITY_SP1",  # density of specie 1 on a mix plot - mixed models
    "DENSITY_SP2",  # density of specie 2 on a mix plot - mixed models
    "DENSITY_SP3",
    "DENSITY_CUT_VOLUME",  # stand density harvested volume (%)
    "DEAD_DENSITY",  # Nº of dead trees after an execution (nº trees/ha)
    "ING_DENSITY",  # Nº of ingrowth trees after an execution (nº trees/ha)

    # Basic plot variables calculated - basal area
    "BASAL_AREA",  # Basal area (m2/ha)
    "BASAL_AREA_SP1",  # basal area of specie 1 on a mix plot - mixed models
    "BASAL_AREA_SP2",  # basal area of specie 2 on a mix plot - mixed models
    "BASAL_AREA_SP3",
    "BA_MAX",  # Maximal Basal Area (cm2)
    "BA_MAX_SP1",  # Maximal Basal Area (cm2) of specie 1 on a mix plot - mixed models
    "BA_MAX_SP2",  # Maximal Basal Area (cm2) of specie 2 on a mix plot - mixed models        
    "BA_MAX_SP3",
    "BA_MIN",  # Minimal Basal Area (cm2)
    "BA_MIN_SP1",  # Minimal Basal Area (cm2) of specie 1 on a mix plot - mixed models
    "BA_MIN_SP2",  # Minimal Basal Area (cm2) of specie 2 on a mix plot - mixed models
    "BA_MIN_SP3",
    "MEAN_BA",  # Mean Basal Area (cm2)
    "MEAN_BA_SP1",  # Mean Basal Area (cm2) of specie 1 on a mix plot - mixed models
    "MEAN_BA_SP2",  # Mean Basal Area (cm2) of specie 2 on a mix plot - mixed models
    "MEAN_BA_SP3",
    "BA_CUT_VOLUME",  # Basal area harvested volume (%)
    "DEAD_BA",  # Basal area of dead trees after an execution (m2/ha)
    "ING_BA",  # Basal area of ingrowth trees after an execution (m2/ha)

    # Basic plot variables calculated - diameter
    "DBH_MAX",  # Maximal Diameter (cm)
    "DBH_MAX_SP1",  # Maximal Diameter (cm) of specie 1 on a mix plot - mixed models
    "DBH_MAX_SP2",  # Maximal Diameter (cm) of specie 2 on a mix plot - mixed models
    "DBH_MAX_SP3",
    "DBH_MIN",  # Minimal Diameter (cm)
    "DBH_MIN_SP1",  # Minimal Diameter (cm) of specie 1 on a mix plot - mixed models
    "DBH_MIN_SP2",  # Minimal Diameter (cm) of specie 2 on a mix plot - mixed models
    "DBH_MIN_SP3",
    "MEAN_DBH",  # Mean Diameter (cm)
    "MEAN_DBH_SP1",  # Mean Diameter (cm) of specie 1 on a mix plot - mixed models
    "MEAN_DBH_SP2",  # Mean Diameter (cm) of specie 2 on a mix plot - mixed models
    "MEAN_DBH_SP3",
    "QM_DBH",  # Quadratic mean dbh (cm)
    "QM_DBH_SP1",  # quadratic mean dbh of specie 1 - mixed models
    "QM_DBH_SP2",  # quadratic mean dbh of specie 2 - mixed models
    "QM_DBH_SP3",
    "DOMINANT_DBH",  # Dominant Diameter (cm)
    "DOMINANT_DBH_SP1",  # dominant diameter os specie 1 (cm) on mixed models
    "DOMINANT_DBH_SP2",  # dominant diameter os specie 2 (cm) on mixed models
    'DOMINANT_DBH_SP3',
    "DOMINANT_SECTION",  # Dominant section (cm)
    "DOMINANT_SECTION_SP1",  # Dominant section (cm) of specie 1 on a mix plot - mixed models
    "DOMINANT_SECTION_SP2",  # Dominant section (cm) of specie 2 on a mix plot - mixed models
    'DOMINANT_SECTION_SP3',

    # Basic plot variables calculated - height
    "H_MAX",  # Maximal Height (m)
    "H_MAX_SP1",  # Maximal Height (m) of specie 1 on a mix plot - mixed models
    "H_MAX_SP2",  # Maximal Height (m) of specie 2 on a mix plot - mixed models
    "H_MAX_SP3",
    "H_MIN",  # Minimal Height (m)
    "H_MIN_SP1",  # Minimal Height (m) of specie 1 on a mix plot - mixed models
    "H_MIN_SP2",  # Minimal Height (m) of specie 2 on a mix plot - mixed models
    "H_MIN_SP3",
    "MEAN_H",  # Mean height (m)
    "MEAN_H_SP1",  # Mean height (m) of specie 1 on a mix plot - mixed models
    "MEAN_H_SP2",  # Mean height (m) of specie 2 on a mix plot - mixed models
    "MEAN_H_SP3",
    "DOMINANT_H",  # Dominant height (m)
    "DOMINANT_H_SP1",  # dominant height of specie 1 - mixed models
    "DOMINANT_H_SP2",  # dominant height of specie 2 - mixed models
    'DOMINANT_H_SP3',

    # Basic plot variables calculated - crown
    "CROWN_MEAN_D",  # Mean crown diameter (m)
    "CROWN_MEAN_D_SP1",  # Mean crown diameter (m) for specie 1
    "CROWN_MEAN_D_SP2",  # Mean crown diameter (m) for specie 2    
    "CROWN_DOM_D",  # Dominant crown diameter (m)
    "CROWN_DOM_D_SP1",  # Dominant crown diameter (m) for specie 1
    "CROWN_DOM_D_SP2",  # Dominant crown diameter (m) for specie 2    
    "CANOPY_COVER",  # Canopy cover (%)
    "CANOPY_COVER_SP1",  # Canopy cover (%) for specie 1
    "CANOPY_COVER_SP2",  # Canopy cover (%) for specie 2      
    "CANOPY_VOL",  # Canopy volume (m3)   
    "CANOPY_VOL_SP1",  # Canopy volume (m3) for specie 1
    "CANOPY_VOL_SP2",  # Canopy volume (m3) for specie 2

    # Basic plot variables calculated - plot
    "SLENDERNESS_MEAN",  # slenderness calculated by using mean values of height and dbh (cm/cm)
    "SLENDERNESS_DOM",  # slenderness calculated by using top height and dbh values (cm/cm)  
    "REINEKE",  # Reineke Index or Stand Density Index - SDI
    "REINEKE_SP1",  # reineke index for specie 1 on mixed models
    "REINEKE_SP2",  # reineke index for specie 2 on mixed models
    "REINEKE_MAX",  # maximal reineke index
    "REINEKE_MAX_SP1",  # maximal reineke index for specie 1 on mixed models
    "REINEKE_MAX_SP2",  # maximal reineke index for specie 2 on mixed models
    "HART",  # Hart-Becking Index (S) calculated to simple rows 
    "HART_STAGGERED",  # Hart-Becking Index (S) calculated to staggered rows 
    "SI",  # Site index (m)

     # Plot variables calculated - volume and biomass
    "VOL",  # Volume (m3/ha)
    "BOLE_VOL",  # Volume under bark (m3/ha)
    "BARK_VOL",  # Bark Volume (m3/ha) 
    "VOL_CUT_VOLUME",  # Volume harvested percentage (%)
    "DEAD_VOL",  # Volume of dead trees after an execution (m3/ha)
    "ING_VOL",  # Volume of ingrowth trees after an execution (m3/ha)

    # Plot variables calculated - volume for mixed models
    "VOL_SP1",  # Volume (m3/ha)
    "BOLE_VOL_SP1",  # Volume under bark (m3/ha)
    "BARK_VOL_SP1",  # Bark Volume (m3/ha) 
    "VOL_SP2",  # Volume (m3/ha)
    "BOLE_VOL_SP2",  # Volume under bark (m3/ha)
    "BARK_VOL_SP2",  # Bark Volume (m3/ha)
    'VOL_SP3',
    'BOLE_VOL_SP3',
    'BARK_VOL_SP3',

    # Plot variables calculated - wood uses
    "UNWINDING",  # Unwinding = the useful wood volume unwinding destiny (m3/ha)
    "VENEER",  # Veneer = the useful wood volume veneer destiny (m3/ha)
    "SAW_BIG",  # Saw big =) the useful wood volume big saw destiny (m3/ha)
    "SAW_SMALL",  # Saw small = the useful wood volume small saw destiny (m3/ha)
    "SAW_CANTER",  # Saw canter = the useful wood volume canter saw destiny (m3/ha)
    "POST",  # Post = the useful wood volume post destiny (m3/ha)
    "STAKE",  # Stake = the useful wood volume stake destiny (m3/ha)
    "CHIPS",  # Chips = the useful wood volume chips destiny (m3/ha)
    'SAW_BIG_LIFEREBOLLO',
    'SAW_SMALL_LIFEREBOLLO',
    'STAVES_INTONA',
    'BOTTOM_STAVES_INTONA',
    'WOOD_PANELS_GAMIZ',
    'MIX_GARCIA_VARONA',

    'UNWINDING_SP1',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
    'VENEER_SP1',  # veneer = the useful wood volume veneer destiny (m3/ha)
    'SAW_BIG_SP1',  # saw_big = the useful wood volume big saw destiny (m3/ha)
    'SAW_SMALL_SP1',  # saw_small = the useful wood volume small saw destiny (m3/ha)
    'SAW_CANTER_SP1',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
    'POST_SP1',  # post = the useful wood volume post destiny (m3/ha)
    'STAKE_SP1',  # stake = the useful wood volume stake destiny (m3/ha)
    'CHIPS_SP1',  # chips = the useful wood volume chips destiny (m3/ha)
    
    'UNWINDING_SP2',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
    'VENEER_SP2',  # veneer = the useful wood volume veneer destiny (m3/ha)
    'SAW_BIG_SP2',  # saw_big = the useful wood volume big saw destiny (m3/ha)
    'SAW_SMALL_SP2',  # saw_small = the useful wood volume small saw destiny (m3/ha)
    'SAW_CANTER_SP2',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
    'POST_SP2',  # post = the useful wood volume post destiny (m3/ha)
    'STAKE_SP2',  # stake = the useful wood volume stake destiny (m3/ha)
    'CHIPS_SP2',  # chips = the useful wood volume chips destiny (m3/ha)

    'UNWINDING_SP3',
    'VENEER_SP3',
    'SAW_BIG_SP3',
    'SAW_SMALL_SP3',
    'SAW_CANTER_SP3',
    'POST_SP3',
    'STAKE_SP3',
    'CHIPS_SP3',

    # Plot variables calculated - biomass
    "WSW",  # wsw = stem wood (t/ha)
    "WSB",  # wsb = stem bark (t/ha)
    "WSWB",  # wswb = stem wood and stem bark (t/ha)
    "WTHICKB",  # wthickb = Thick branches > 7 cm (t/ha)
    "WSTB",  # wstb = wsw + wthickb, stem + branches > 7 cm (t/ha)
    "WB2_7",  # wb2_7 = branches (2-7 cm) (t/ha)
    "WB2_T",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (t/ha)
    "WTHINB",  # wthinb = Thin branches (2-0.5 cm) (t/ha)
    "WB05",  # wb05 = thinniest branches (<0.5 cm) (t/ha)
    "WB05_7",  # wb05_7 = branches between 0.5-7 cm (t/ha)
    "WB0_2",  # wb0_2 = branches < 2 cm (t/ha)
    "WDB",  # wdb = dead branches biomass (t/ha)
    "WL",  # wl = leaves (t/ha)
    "WTBL",  # wtbl = wthinb + wl; branches < 2 cm and leaves (t/ha)
    "WBL0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (t/ha)
    'WS',
    'WB',
    "WR",  # wr = roots (t/ha)
    "WT",  # wt = total biomass (t/ha)
    "WT_CUT_VOLUME",  # WT of the cut trees after a cut process (%)
    "DEAD_WT",  # WT of the dead trees after an execution (t/ha)
    "ING_WT",  # WT of the ingrowth trees after an execution (t/ha)

    # Plot variables calculated - biomass for mixed models
    "WSW_SP1",  # wsw = stem wood (t/ha)
    "WSB_SP1",  # wsb = stem bark (t/ha)
    "WSWB_SP1",  # wswb = stem wood and stem bark (t/ha)
    "WTHICKB_SP1",  # wthickb = Thick branches > 7 cm (t/ha)
    "WSTB_SP1",  # wstb = wsw + wthickb, stem + branches > 7 cm (t/ha)
    "WB2_7_SP1",  # wb2_7 = branches (2-7 cm) (t/ha)
    "WB2_T_SP1",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (t/ha)
    "WTHINB_SP1",  # wthinb = Thin branches (2-0.5 cm) (t/ha)
    "WB05_SP1",  # wb05 = thinniest branches (<0.5 cm) (t/ha)
    "WB05_7_SP1",  # wb05_7 = branches between 0.5-7 cm (t/ha)
    "WB0_2_SP1",  # wb0_2 = branches < 2 cm (t/ha)
    "WDB_SP1",  # wdb = dead branches biomass (t/ha)
    "WL_SP1",  # wl = leaves (t/ha)
    "WTBL_SP1",  # wtbl = wthinb + wl; branches < 2 cm and leaves (t/ha)
    "WBL0_7_SP1",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (t/ha)
    'WS_SP1',
    'WB_SP1',
    "WR_SP1",  # wr = roots (t/ha)
    "WT_SP1",  # wt = total biomass (t/ha)

    "WSW_SP2",  # wsw = stem wood (t/ha)
    "WSB_SP2",  # wsb = stem bark (t/ha)
    "WSWB_SP2",  # wswb = stem wood and stem bark (t/ha)
    "WTHICKB_SP2",  # wthickb = Thick branches > 7 cm (t/ha)
    "WSTB_SP2",  # wstb = wsw + wthickb, stem + branches > 7 cm (t/ha)
    "WB2_7_SP2",  # wb2_7 = branches (2-7 cm) (t/ha)
    "WB2_T_SP2",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (t/ha)
    "WTHINB_SP2",  # wthinb = Thin branches (2-0.5 cm) (t/ha)
    "WB05_SP2",  # wb05 = thinniest branches (<0.5 cm) (t/ha)
    "WB05_7_SP2",  # wb05_7 = branches between 0.5-7 cm (t/ha)
    "WB0_2_SP2",  # wb0_2 = branches < 2 cm (t/ha)
    "WDB_SP2",  # wdb = dead branches biomass (t/ha)
    "WL_SP2",  # wl = leaves (t/ha)
    "WTBL_SP2",  # wtbl = wthinb + wl; branches < 2 cm and leaves (t/ha)
    "WBL0_7_SP2",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (t/ha)
    'WS_SP2',
    'WB_SP2',
    "WR_SP2",  # wr = roots (t/ha)
    "WT_SP2",  # wt = total biomass (t/ha)

    'WS_SP3',
    'WB_SP3',
    'WR_SP3',
    'WT_SP3',

    # Plot variables calculated - carbon
    'CARBON_HEARTWOOD',
    'CARBON_SAPWOOD',
    'CARBON_BARK',
    'CARBON_STEM',
    'CARBON_BRANCHES',
    'CARBON_ROOTS',
    'CARBON',
    'CARBON_STEM_SP1',
    'CARBON_BRANCHES_SP1',
    'CARBON_ROOTS_SP1',
    'CARBON_SP1',
    'CARBON_STEM_SP2',
    'CARBON_BRANCHES_SP2',
    'CARBON_ROOTS_SP2',
    'CARBON_SP2',
    'CARBON_STEM_SP3',
    'CARBON_BRANCHES_SP3',
    'CARBON_ROOTS_SP3',
    'CARBON_SP3',

    # Species Diversity Indexes
    "SHANNON",  # Shannon-Weaver Diversity Index
    "SIMPSON",  # Simpson Diversity Index
    "MARGALEF",  # Margalef Specific Diversity Index
    "PIELOU",  # Pielou Diversity Index
    'DEADWOOD_INDEX_CESEFOR_G',
    'DEADWOOD_INDEX_CESEFOR_V',

    # Quercus suber special variables
    "W_CORK",  # fresh cork biomass (t/ha)
    "TOTAL_W_DEBARK",  # w cork accumulator to all the scenario (t)
    "TOTAL_V_DEBARK",  # v cork accumulator to all the scenario (m3)

    # Pinus pinea special variables
    "ALL_CONES",  # total of cones of the plot (anual mean)
    "SOUND_CONES",  # total sound (healthy) cones of the plot (anual mean)
    "SOUND_SEEDS",  # total sound (healthy) seeds of the plot (anual mean)
    "W_SOUND_CONES",  # weight of sound (healthy) cones (t/ha) (anual mean)
    "W_ALL_CONES",  # weight of all (healthy and not) cones (t/ha) (anual mean)

    # Mushrooms special variables
    "EDIBLE_MUSH",  # annual mushroom production of edible species (mean annual value) (kg/ha)
    "MARKETED_MUSH",  # annual mushroom production of marketed species (mean annual value) (kg/ha)
    "MARKETED_LACTARIUS",  # production of marketed Lactarius (mean annual value) (kg/ha)
    "MUSHROOM_PRODUCTIVITY",  # total fresh-weight mushroom productivity (kg fw/ha)

    # Cistus ladanifer special variables
    'TIME_AT',  # Time_AT  # time after treatment (years)
    'B_EDULIS',  # B_edulis  # annual yield of B. edulis sporocarps (kg/ha*year)
    'MYCOD',  # MycoD  # Shannon diversity index of mycorrhizal taxa
    'MYCOP',  # MycoP  # Annual mushroom yield from all mycorrhizal species (kg/ha*year)
    'SAPROD',  # SaproD  # Shannon diversity index of saprotrophic fungi
    'SAPROP',  # SaproP  # annual mushroom yield of saprotrophic species (kg/ha*year)

    # Auxiliar variables for future models - 11/08/2023
    'PLOT_VAR1',
    'PLOT_VAR2',
    'PLOT_VAR3',
    'PLOT_VAR4',
    'PLOT_VAR5',
    'PLOT_VAR6',
    'PLOT_VAR7',
    'PLOT_VAR8',
    'PLOT_VAR9',
    'PLOT_VAR10',
    'PLOT_VAR11',
    'PLOT_VAR12',
    'PLOT_VAR13',
    'PLOT_VAR14',
    'PLOT_VAR15',
    'PLOT_VAR16',
    'PLOT_VAR17',
    'PLOT_VAR18',
    'PLOT_VAR19',
    'PLOT_VAR20',
    'PLOT_VAR21',
    'PLOT_VAR22',
    'PLOT_VAR23',
    'PLOT_VAR24',
    'PLOT_VAR25',
    'PLOT_VAR26',
    'PLOT_VAR27',
    'PLOT_VAR28',
    'PLOT_VAR29',
    'PLOT_VAR30',
    'PLOT_VAR31',
    'PLOT_VAR32',
    'PLOT_VAR33',
    'PLOT_VAR34',
    'PLOT_VAR35',
    'PLOT_VAR36',
    'PLOT_VAR37',
    'PLOT_VAR38',
    'PLOT_VAR39',
    'PLOT_VAR40',
    'PLOT_VAR41',
    'PLOT_VAR42',
    'PLOT_VAR43',
    'PLOT_VAR44',
    'PLOT_VAR45',
    'PLOT_VAR46',
    'PLOT_VAR47',
    'PLOT_VAR48',
    'ZPCUM9',
    'ZPCUM8',
    'ZPCUM7',
    'ZPCUM6',
    'ZPCUM5',
    'ZPCUM4',
    'ZPCUM3',
    'ZPCUM2',
    'ZPCUM1',
    'ZQ95',
    'ZQ90',
    'ZQ85',
    'ZQ80',
    'ZQ75',
    'ZQ70',
    'ZQ65',
    'ZQ60',
    'ZQ55',
    'ZQ50',
    'ZQ45',
    'ZQ40',
    'ZQ35',
    'ZQ30',
    'ZQ25',
    'ZQ20',
    'ZQ15',
    'ZQ10',
    'ZQ5',
    'PZABOVE2',
    'PZABOVEZMEAN',
    'ZENTROPY',
    'ZKURT',
    'ZSKEW',
    'ZSD',
    'ZMEAN',
    'ZMAX',

    # The last variables of this list will be not printed; it's neccesary to include that variables on the following list:
    # PLOT_VARS_NOT_PRINT, and to leave them  at the end of that list
    "REF_SI_AGE",  # SI reference age (years)
    "REINEKE_VALUE", # r contstant value of SDI  to the specie of the model (-1.605 as default)
    'HEGYI_RADIUS'  # radius value to calculate the Hegyi competition index (m)
# MODEL_SPECIE_ID  # that variable is needed to use on the simulator, but not needed to be shown at the output
]

PLOT_VARS_NOT_PRINT = [  # that variables will be printed only at the description sheet
    'REINEKE_VALUE', 
    'REF_SI_AGE',
    'HEGYI_RADIUS'  # radius value to calculate the Hegyi competition index (m)
]

SCENARIO_VARS = [  # summary of proceses that can be done on the simulator
    'file_name',  # delete it to not show the scenario file name at the output
    'scenario_id',
    'trees_sheet',
    'scenario_age',
    'scenario_min_age',
    'scenario_max_age',
    'scenario_action',
    'action_time',
    'cut_type',
    'cut_criteria',
    'cut_severity',
    'preserve_trees',
    "species",
    "volume_target"
]

WARNING_VARS = [  # list of variables that activate warning messages if something is going wrong
    # to activate them, they must receive 1 as value
    'SPECIE_ERROR',  # That variable will show you a warning message if you try to use a model of one specie with an inventory of another
    'SPECIE_ERROR_TREES',  # That variable will show you a warning message if you try to use an inventory (on tree models) where the main specie is not represented by trees
    'EXEC_ERROR',  # That variable will contain a message about errors on the execution
    'EXEC_ERROR_SUMMARY',  # That variable will contain a message a little bit different to show on summary sheet about errors on the execution
    'CUT_ERROR',  # That variable will contain a message to notify in the plot sheet that the time for cuts must be 0
    'CUT_ERROR_SUMMARY'  # That variable will contain a message a little bit different to show on summary sheet about error on the cuts
]

TREE_VARS = [  # list of tree variables on the simulator

    # IDs
    "INVENTORY_ID",
    "PLOT_ID",
    "TREE_ID",

    # Special TREE_IDs to work with the IFN data
    "TREE_ID_IFN3_2",
    "TREE_ID_IFN3",
    "TREE_ID_IFN2",
    "TREE_ID_compare", 

    # Remarkable variables and basic variables measured
    "specie",
    "tree_age",
    "bearing",  # bearing from the tree to the central point of the plot ('rumbo')
    "distance",  # distance from the tree to the central point of the plot
    "expan",  # expansion factor
    "dbh_1",  # dbh measurement 1 (cm)
    "dbh_2",  # dbh measurement 2 (cm)
    "dbh",  # diameter at breast height (cm)
    "dbh_i",  # increment in diameter at breast height (cm)
    "height",  # total tree height (m)
    "height_i",  # increment in total tree height (m)
    "stump_h",   # stump height (m))
    "bark_1",  # bark thickness, measurement 1 (mm)
    "bark_2",  # bark thickness, measurement 2 (mm)
    "bark",  # mean bark thickness (mm)

   # Basic variables calculated
    "basal_area",  # basal area (cm2)
    "basal_area_i",  # increment in basal area (cm2)
    "basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
    "basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
    "bal",  # cumulative basal area (m2/ha)
    "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
    "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
    "ba_ha",  # basal area per ha (m2/ha) 
    "normal_circumference",  # circumference at breast height (cm)
    "slenderness",  # slenderness (cm/cm)

    # Basic variables on hegyi subplot
    "bal_intrasp_hegyi",  # intraspecific bal (m2/ha) inside hegyi subplot of each tree
    "bal_intersp_hegyi",  # interspecific bal (m2/ha) inside hegyi subplot of each tree
    "bal_ratio_intrasp_hegyi",  # intraspecific bal ratio (0 to 1) inside hegyi subplot of each tree
    "bal_ratio_intersp_hegyi",  # interspecific bal ratio (0 to 1) inside hegyi subplot of each tree
    "bal_total_hegyi",  # total bal (m2/ha) inside hegyi subplot of each tree
    "g_intrasp_hegyi",  # intraspecific basal area (m2/ha) inside hegyi subplot of each tree
    "g_intersp_hegyi",  # interspecific basal area (m2/ha) inside hegyi subplot of each tree
    "g_ratio_intrasp_hegyi",  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
    "g_ratio_intersp_hegyi",  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
    "g_total_hegyi",  # total basal area (m2/ha) inside hegyi subplot of each tree
    "n_intrasp_hegyi",  # intraspecific density (trees/ha) inside hegyi subplot of each tree
    "n_intersp_hegyi",  # interspecific density (trees/ha) inside hegyi subplot of each tree
    "n_ratio_intrasp_hegyi",  # intraspecific density ratio (0 to 1) inside hegyi subplot of each tree
    "n_ratio_intersp_hegyi",  # interspecific density ratio (0 to 1) inside hegyi subplot of each tree
    "n_total_hegyi",  # total density (trees/ha) inside hegyi subplot of each tree

    # Crown variables
    "cr",  # crown ratio (%)
    "lcw",  #  largest crown width (m)
    "hcb",  # height of the crown base (m)
    "hlcw",  # height of the largest crown width (m)
    "cpa",  # crown projection area (m2)
    "crown_vol",  # crown volume (m3)

    # Volume variables
    "vol",  # volume over bark (dm3)
    "bole_vol",  # volume under bark (dm3)
    "bark_vol",  # bark volume (dm3)
    "firewood_vol",  # firewood volume (dm3)
    "vol_ha",  # volume over bark per hectare (m3/ha)

    # Wood uses variables
    "unwinding",  # unwinding = the useful wood volume unwinding destiny (dm3)
    "veneer",  # veneer = the useful wood volume veneer destiny (dm3)
    "saw_big",  # saw_big = the useful wood volume big saw destiny (dm3)
    "saw_small",  # saw_small = the useful wood volume small saw destiny (dm3)
    "saw_canter",  # saw_canter = the useful wood volume canter saw destiny (dm3)
    "post",  # post = the useful wood volume post destiny (dm3)
    "stake",  # stake = the useful wood volume stake destiny (dm3)
    "chips",  # chips = the useful wood volume chips destiny (dm3)
    'saw_big_liferebollo',
    'saw_small_liferebollo',
    'staves_intona',
    'bottom_staves_intona',
    'wood_panels_gamiz',
    'mix_garcia_varona',

    # Biomass variables
    "wsw",  # wsw = stem wood (kg)
    "wsb",  # wsb = stem bark (kg)
    "wswb",  # wswb = stem wood and stem bark (kg)
    "w_cork",  # fresh cork biomass (kg)
    "wthickb",  # wthickb = Thick branches > 7 cm (kg)
    "wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
    "wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
    "wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
    "wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
    "wb05",  # wb05 = thinniest branches (<0.5 cm) (kg)
    "wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
    "wb0_2",  # wb0_2 = branches < 2 cm (kg)
    "wdb",  # wdb = dead branches biomass (kg)
    "wl",  # wl = leaves (kg)
    "wtbl",  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
    "wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
    'ws',
    'wb',
    "wr",  # wr = roots (kg)
    "wt",  # wt = total biomass (kg)
    'carbon_heartwood',
    'carbon_sapwood',
    'carbon_bark',
    'carbon_stem',
    'carbon_branches',
    'carbon_roots',
    'carbon',

    # Competition information
    "hegyi",  # Hegyi competition index calculation

    # Quercus suber special variables
    "dbh_oc",  # dbh over cork (cm) - Quercus suber
    "h_debark",  # uncork height on the main stem (m) - Quercus suber
    "nb",  # number of the main boughs stripped - Quercus suber
    "cork_cycle",  # moment to obtain cork data; 0 to the moment just immediately before the stripping process
    "count_debark",  # number of debarking treatments applied 
    "total_w_debark",  # w cork accumulator to all the scenario (kg)
    "total_v_debark",  # v cork accumulator to all the scenario (dm3)

    # Pinus pinea special variables
    "all_cones",  # number of all the cones of the tree (anual mean)
    "sound_cones",  # number of healthy cones in a tree (anual mean)
    "sound_seeds",  # total sound seeds of the tree (anual mean)
    "w_sound_cones",  # weight of sound (healthy) cones (kg) (anual mean)
    "w_all_cones",  # weight of all (healthy and not) cones (kg) (anual mean)

    # Vorest model variables
    'w_voronoi',  # weights used to construct the Voronoi diagrams 
    'neighbours_mean_dbh',  # mean dbh of the neighbour trees     
    'ogs',  # occupied growing space of tree i in year t, computed as the area of the weighted Voronoi region of the tree i restricted by the range of its zone of influence (radius) at time t
    'ags',  # area in its surroundings not occupied by neighboring trees and therefore available to that tree to search for light
    'pgs',  # potential growing space of tree i in year t estimated as the crown projection area of an open grown tree of the same dbh
    'rel_area',  # ratio of the occupied growing space (OGS) of a tree and its potential growing space (PGS) and it is used as a surrogate for the growing capacity of a tree

    # Auxiliar variables for future models - 10/08/2023
    'tree_var1',
    'tree_var2',
    'tree_var3',
    'tree_var4',
    'tree_var5',
    'tree_var6',
    'tree_var7',
    'tree_var8',
    'tree_var9',
    'tree_var10',
    'tree_var11',
    'tree_var12',
    'tree_var13',
    'tree_var14',
    'tree_var15',
    'tree_var16',
    'tree_var17',
    'tree_var18',
    'tree_var19',
    'tree_var20',
    'tree_var21',
    'tree_var22',
    'tree_var23',
    'tree_var24',
    'tree_var25',
    'tree_var26',
    'tree_var27',
    'tree_var28',
    'tree_var29',
    'tree_var30',
    'tree_var31',
    'tree_var32',
    'tree_var33',
    'tree_var34',
    'tree_var35',
    'tree_var36',
    'tree_var37',
    'tree_var38',
    'tree_var39',
    'tree_var40',
    'tree_var41',
    'tree_var42',
    'tree_var43',
    'tree_var44',
    'tree_var45',
    'tree_var46',
    'tree_var47',
    'tree_var48',

    # Tree general information
    "number_of_trees",
    "quality",
    "shape",
    "special_param",
    "remarks",
    "age_130",
    "social_class",
    "coord_x",
    "coord_y",
    "coord_z"
]

TREE_VARS_ORIGINAL = [  # list of tree variables on the simulator

    # IDs
    "INVENTORY_ID",
    "PLOT_ID",
    "TREE_ID",

    # Special TREE_IDs to work with the IFN data
    "TREE_ID_IFN3_2",
    "TREE_ID_IFN3",
    "TREE_ID_IFN2",
    "TREE_ID_compare", 

    # Remarkable variables and basic variables measured
    "specie",
    "tree_age",
    "bearing",  # bearing from the tree to the central point of the plot ('rumbo')
    "distance",  # distance from the tree to the central point of the plot    
    "expan",  # expansion factor
    "dbh_1",  # dbh measurement 1 (cm)
    "dbh_2",  # dbh measurement 2 (cm)
    "dbh",  # diameter at breast height (cm)
    "dbh_i",  # increment in diameter at breast height (cm)
    "height",  # total tree height (m)
    "height_i",  # increment in total tree height (m)
    "stump_h",   # stump height (m))
    "bark_1",  # bark thickness, measurement 1 (mm)
    "bark_2",  # bark thickness, measurement 2 (mm)
    "bark",  # mean bark thickness (mm)

   # Basic variables calculated
    "basal_area",  # basal area (cm2)
    "basal_area_i",  # increment in basal area (cm2)
    "basal_area_intrasp",  # intraspecific basal area (m2/ha) for mixed models
    "basal_area_intersp",  # interspecific basal area (m2/ha) for mixed models
    "bal",  # cumulative basal area (m2/ha)
    "bal_intrasp",  # intraspecific bal (m2/ha) for mixed models
    "bal_intersp",  # intraspecific bal (m2/ha) for mixed models
    "ba_ha",  # basal area per ha (m2/ha) 
    "normal_circumference",  # circumference at breast height (cm)
    "slenderness",  # slenderness (cm/cm)
    
    # Basic variables on hegyi subplot
    "bal_intrasp_hegyi",  # intraspecific bal (m2/ha) inside hegyi subplot of each tree
    "bal_intersp_hegyi",  # interspecific bal (m2/ha) inside hegyi subplot of each tree
    "bal_ratio_intrasp_hegyi",  # intraspecific bal ratio (0 to 1) inside hegyi subplot of each tree
    "bal_ratio_intersp_hegyi",  # interspecific bal ratio (0 to 1) inside hegyi subplot of each tree
    "bal_total_hegyi",  # total bal (m2/ha) inside hegyi subplot of each tree
    "g_intrasp_hegyi",  # intraspecific basal area (m2/ha) inside hegyi subplot of each tree
    "g_intersp_hegyi",  # interspecific basal area (m2/ha) inside hegyi subplot of each tree
    "g_ratio_intrasp_hegyi",  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
    "g_ratio_intersp_hegyi",  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
    "g_total_hegyi",  # total basal area (m2/ha) inside hegyi subplot of each tree
    "n_intrasp_hegyi",  # intraspecific density (trees/ha) inside hegyi subplot of each tree
    "n_intersp_hegyi",  # interspecific density (trees/ha) inside hegyi subplot of each tree
    "n_ratio_intrasp_hegyi",  # intraspecific density ratio (0 to 1) inside hegyi subplot of each tree
    "n_ratio_intersp_hegyi",  # interspecific density ratio (0 to 1) inside hegyi subplot of each tree
    "n_total_hegyi",  # total density (trees/ha) inside hegyi subplot of each tree

    # Crown variables
    "cr",  # crown ratio (%)
    "lcw",  #  largest crown width (m)
    "hcb",  # height of the crown base (m)
    "hlcw",  # height of the largest crown width (m)
    "cpa",  # crown projection area (m2)
    "crown_vol",  # crown volume (m3)

    # Volume variables
    "vol",  # volume over bark (dm3)
    "bole_vol",  # volume under bark (dm3)
    "bark_vol",  # bark volume (dm3)
    "firewood_vol",  # firewood volume (dm3)
    "vol_ha",  # volume over bark per hectare (m3/ha)

    # Wood uses variables
    "unwinding",  # unwinding = the useful wood volume unwinding destiny (dm3)
    "veneer",  # veneer = the useful wood volume veneer destiny (dm3)
    "saw_big",  # saw_big = the useful wood volume big saw destiny (dm3)
    "saw_small",  # saw_small = the useful wood volume small saw destiny (dm3)
    "saw_canter",  # saw_canter = the useful wood volume canter saw destiny (dm3)
    "post",  # post = the useful wood volume post destiny (dm3)
    "stake",  # stake = the useful wood volume stake destiny (dm3)
    "chips",  # chips = the useful wood volume chips destiny (dm3)
    'saw_big_liferebollo',
    'saw_small_liferebollo',
    'staves_intona',
    'bottom_staves_intona',
    'wood_panels_gamiz',
    'mix_garcia_varona',

    # Biomass variables
    "wsw",  # wsw = stem wood (kg)
    "wsb",  # wsb = stem bark (kg)
    "wswb",  # wswb = stem wood and stem bark (kg)
    "w_cork",  # fresh cork biomass (kg)
    "wthickb",  # wthickb = Thick branches > 7 cm (kg)
    "wstb",  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
    "wb2_7",  # wb2_7 = branches (2-7 cm) (kg)
    "wb2_t",  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
    "wthinb",  # wthinb = Thin branches (2-0.5 cm) (kg)
    "wb05",  # wb05 = thinniest branches (<0.5 cm) (kg)
    "wb05_7",  # wb05_7 = branches between 0.5-7 cm (kg)
    "wb0_2",  # wb0_2 = branches < 2 cm (kg)
    "wdb",  # wdb = dead branches biomass (kg)
    "wl",  # wl = leaves (kg)
    "wtbl",  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
    "wbl0_7",  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
    'ws',
    'wb',
    "wr",  # wr = roots (kg)
    "wt",  # wt = total biomass (kg)
    'carbon_heartwood',
    'carbon_sapwood',
    'carbon_bark',
    'carbon_stem',
    'carbon_branches',
    'carbon_roots',
    'carbon',

    # Competition information
    "hegyi",  # Hegyi competition index calculation

    # Quercus suber special variables
    "dbh_oc",  # dbh over cork (cm) - Quercus suber
    "h_debark",  # uncork height on the main stem (m) - Quercus suber
    "nb",  # number of the main boughs stripped - Quercus suber
    "cork_cycle",  # moment to obtain cork data; 0 to the moment just immediately before the stripping process
    "count_debark",  # number of debarking treatments applied 
    "total_w_debark",  # w cork accumulator to all the scenario (kg)
    "total_v_debark",  # v cork accumulator to all the scenario (dm3)

    # Pinus pinea special variables
    "all_cones",  # number of all the cones of the tree (anual mean)
    "sound_cones",  # number of healthy cones in a tree (anual mean)
    "sound_seeds",  # total sound seeds of the tree (anual mean)
    "w_sound_cones",  # weight of sound (healthy) cones (kg) (anual mean)
    "w_all_cones",  # weight of all (healthy and not) cones (kg) (anual mean)

    # Vorest model variables
    'w_voronoi',  # weights used to construct the Voronoi diagrams 
    'neighbours_mean_dbh',  # mean dbh of the neighbour trees     
    'ogs',  # occupied growing space of tree i in year t, computed as the area of the weighted Voronoi region of the tree i restricted by the range of its zone of influence (radius) at time t
    'ags',  # area in its surroundings not occupied by neighboring trees and therefore available to that tree to search for light
    'pgs',  # potential growing space of tree i in year t estimated as the crown projection area of an open grown tree of the same dbh
    'rel_area',  # ratio of the occupied growing space (OGS) of a tree and its potential growing space (PGS) and it is used as a surrogate for the growing capacity of a tree

    # Auxiliar variables for future models - 11/08/2023
    'tree_var1',
    'tree_var2',
    'tree_var3',
    'tree_var4',
    'tree_var5',
    'tree_var6',
    'tree_var7',
    'tree_var8',
    'tree_var9',
    'tree_var10',
    'tree_var11',
    'tree_var12',
    'tree_var13',
    'tree_var14',
    'tree_var15',
    'tree_var16',
    'tree_var17',
    'tree_var18',
    'tree_var19',
    'tree_var20',
    'tree_var21',
    'tree_var22',
    'tree_var23',
    'tree_var24',
    'tree_var25',
    'tree_var26',
    'tree_var27',
    'tree_var28',
    'tree_var29',
    'tree_var30',
    'tree_var31',
    'tree_var32',
    'tree_var33',
    'tree_var34',
    'tree_var35',
    'tree_var36',
    'tree_var37',
    'tree_var38',
    'tree_var39',
    'tree_var40',
    'tree_var41',
    'tree_var42',
    'tree_var43',
    'tree_var44',
    'tree_var45',
    'tree_var46',
    'tree_var47',
    'tree_var48',

    # Tree general information
    "number_of_trees",
    "quality",
    "shape",
    "special_param",
    "remarks",
    "age_130",
    "social_class",
    "coord_x",
    "coord_y",
    "coord_z"    
]


class Variables():

    def remove_var_plot(variables: list):
        """
        Function neccesary to remove the non desired variables from the plot variables list.
        It will be used from each model, and the variables to delete depends on the purpose of the model.
        """
        for var in variables:
            PLOT_VARS.remove(var)

    def remove_var_tree(variables: list):
        """
        Function neccesary to remove the non desired variables from the tree variables list.
        It will be used from each model, and the variables to delete depends on the purpose of the model.
        """

        for var in variables:
            TREE_VARS.remove(var)