EN_PLOT = {
    # IDs and model information
    'INVENTORY_ID': 'Inventory_ID',
    'PLOT_ID': 'Plot_ID',

    # Plot general information about the study area
    'PLOT_TYPE': 'Plot_type',
    'PLOT_AREA': 'Plot_area',
    'PROVINCE': 'Province',
    'STUDY_AREA': 'Study_Area',
    'MUNICIPALITY': 'Municipality',
    'FOREST': 'Forest',
    'PROV_REGION': 'Provenance_region',
    'MAIN_SPECIE': 'Species_composition',
    'SPECIE_IFN_ID': 'Main_specie_ID',  # IFN (Spanish National Forestal Inventory) ID of the main specie
    'SLOPE': 'Slope',  # (%)
    'ASPECT': 'Aspect',  # (rad)
    'CONTINENTALITY': 'Continentality',  # (linear distance to the Mediterranean sea, km)
    'LONGITUDE': 'Longitude',
    'LATITUDE': 'Latitude',
    'ALTITUDE': 'Altitude',
    'AA_RAINFALL': 'Average_Annual_Rainfall',  # (mm)
    'MA_TEMPERATURE': 'Mean_Annual_Temperature',  # (ºC)
    'SEPTEMBER_RAIN': 'September_Rainfall',  # (mm)
    'SEPTEMBER_TEMP': 'September_Mean_Temperature',  # (ºC)
    'NOVEMBER_RAIN': 'November_Rainfall',  # (mm)
    'NOVEMBER_TEMP': 'November_Mean_Temperature',  # (ºC)   
    'MARTONNE': 'Martonne_index',
    'MARTONNE_2020': 'Martonne_index_1',
    'MARTONNE_2040': 'Martonne_index_2',
    'MARTONNE_2060': 'Martonne_index_3',
    'MARTONNE_2080': 'Martonne_index_4',

    # Basic plot variables measured
    'EXPAN': 'Expan',  # expansion factor
    'AGE': 'T',  # (years)
    'YEAR': 'Year',
    'DENSITY': 'N',  # (nº trees/ha)
    'DENSITY_CUT_VOLUME': 'N_harvested_volume',  # stand density harvested volume (%)
    'DEAD_DENSITY': 'Dead_N',  # Nº of dead trees after an execution (nº trees/ha)
    'ING_DENSITY': 'Ingrowth_N',  # Nº of ingrowth trees after an execution (nº trees/ha)

    # Basic plot variables calculated - basal area
    'BASAL_AREA': 'G',  # (m2/ha)
    'BA_MAX': 'g_max',  # (cm2)
    'BA_MIN': 'g_min',  # (cm2)
    'MEAN_BA': 'g_mean',  # (cm2)
    'BA_CUT_VOLUME': 'G_harvested_volume',  # Basal area harvested volume (%)
    'DEAD_BA': 'Dead_G',  # Basal area of dead trees after an execution (m2/ha)
    'ING_BA': 'Ingrowth_G',  # Basal area of ingrowth trees after an execution (m2/ha)

    # Basic plot variables calculated - diameter   
    'DBH_MAX': 'dbh_max',  # (cm)
    'DBH_MIN': 'dbh_min',  # (cm)    
    'MEAN_DBH': 'dbh_mean',  # (cm)
    'QM_DBH': 'dg',  # (cm)
    'DOMINANT_DBH': 'Do',  # (cm)
    'DOMINANT_SECTION': 'Dominant_section',  # Dominant section of the plot (cm)

    # Basic plot variables calculated - height
    'H_MAX': 'h_max',  # (m)
    'H_MIN': 'h_min',  # (m)
    'MEAN_H': 'h_mean',  # (m)
    'DOMINANT_H': 'Ho',  # (m)

    # Basic plot variables calculated - crown
    'CROWN_MEAN_D': 'Mean_crown_d',  # (m)
    'CROWN_DOM_D': 'Do_crown',  # (m)
    'CANOPY_COVER': 'Canopy_cover',  # (%)
    'CANOPY_VOL': 'Canopy_vol',  # Canopy volume (m3)   

    # Basic plot variables calculated - plot
    'SLENDERNESS_MEAN': 'Slenderness',  # slenderness calculated by using mean values of height and dbh (cm/cm)
    'SLENDERNESS_DOM': 'Dominant_Slenderness',  # slenderness calculated by using top height and dbh values (cm/cm)
    'REINEKE': 'SDI',  # Stand Density Index - SDI
    'REINEKE_MAX': 'SDImax',  # Maximum Stand Density Index
    'REINEKE_VALUE': 'r_(SDI)',  # r contstant value of SDI  to the specie of the model (-1.605 as default)    
    'HART': 'HartBecking__Simple_rows',  # Hart-Becking Index - S
    'HART_STAGGERED': 'HartBecking__Staggered_rows',  # Hart-Becking Index - S
    'SI': 'SI',  # (m)
    'REF_SI_AGE': 'SI_ref_age',  # SI reference age (years)
    'HEGYI_RADIUS': 'Hegyi_radius',  # radius value to calculate the Hegyi competition index (m)

    # Plot variables calculated - volume
    'VOL': 'V',  # (m3/ha)
    'BOLE_VOL': 'Bole_V',  # (m3/ha)
    'BARK_VOL ': 'Bark_V',  # (m3/ha)
    'VOL_CUT_VOLUME': 'V_harvested',  # Volume harvested percentage (%)
    'DEAD_VOL': 'Dead_V',  # Volume of dead trees after an execution (m3/ha)
    'ING_VOL': 'Ingrowth_V',  # Volume of ingrowth trees after an execution (m3/ha)

    # Plot variables calculated - biomass
    'WSW': 'WSW',  # wsw = stem wood (Tn/ha)
    'WSB': 'WSB',  # wsb = stem bark (Tn/ha)
    'WSWB': 'WSWB',  # wswb = stem wood and stem bark (Tn/ha)
    'WTHICKB': 'WTHICKB',  # wthickb = Thick branches > 7 cm (Tn/ha)
    'WSTB': 'WSTB',  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
    'WB2_7': 'WB2_7',  # wb2_7 = branches (2-7 cm) (Tn/ha)
    'WB2_T': 'WB2_t',  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
    'WTHINB': 'WTHINB',  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
    'WB05': 'WB0.5',  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
    'WB05_7': 'WB05_7',  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
    'WB0_2': 'WB0_2',  # wb0_2 = branches < 2 cm (Tn/ha)
    'WDB': 'WDB',  # wdb = dead branches biomass (Tn/ha)
    'WL': 'WL',  # wl = leaves (Tn/ha)
    'WTBL': 'WTBL',  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
    'WBL0_7': 'WBL0_7',  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
    'WR': 'WR',  # wr = roots (Tn/ha)
    'WT': 'WT',  # wt = total biomass (Tn/ha)
    'DEAD_WT': 'Dead_WT',  # WT of the dead trees after an execution (Tn/ha)
    'ING_WT': 'Ingrowth_WT',  # WT of the ingrowth trees after an execution (Tn/ha)

    # Plot variables calculated - wood uses
    'UNWINDING': 'V_unwinding',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
    'VENEER': 'V_veneer',  # veneer = the useful wood volume veneer destiny (m3/ha)
    'SAW_BIG': 'V_saw_big',  # saw_big = the useful wood volume big saw destiny (m3/ha)
    'SAW_SMALL': 'V_saw_small',  # saw_small = the useful wood volume small saw destiny (m3/ha)
    'SAW_CANTER': 'V_saw_canter',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
    'POST': 'V_post',  # post = the useful wood volume post destiny (m3/ha)
    'STAKE': 'V_stake',  # stake = the useful wood volume stake destiny (m3/ha)
    'CHIPS': 'V_chips',  # chips = the useful wood volume chips destiny (m3/ha)

    # Species Diversity Indexes
    'SHANNON': 'Shannon',
    'SIMPSON': 'Simpson',
    'MARGALEF': 'Margalef',
    'PIELOU': 'Pielou',

    # Quercus suber special variables
    'W_CORK': 'W_Fresh_Cork',  # fresh cork biomass (Tn/ha)
    'TOTAL_W_DEBARK': 'W_debarked',  # Total cork biomass (Tn/ha) extraxted from debark treatments
    'TOTAL_V_DEBARK': 'V_debarked',  # Total cork volume (m3/ha) extracted from debark treatments

    # Pinus pinea special variables
    'ALL_CONES': 'Cones',  # total of cones of the plot (anual mean)
    'SOUND_CONES': 'Healthy_cones',  # total sound (healthy) cones of the plot (anual mean)
    'SOUND_SEEDS': 'Healthy_seeds',  # total sound (healthy) seeds of the plot (anual mean)
    'W_SOUND_CONES': 'W_healthy_cones',  # weight of sound (healthy) cones (Tn/ha) (anual mean)
    'W_ALL_CONES': 'W_cones',  # weight of all (healthy and not) cones (Tn/ha) (anual mean)

    # Mushrooms special variables
    'EDIBLE_MUSH': 'Edible_mushroom',  # annual mushroom production of edible species (mean value) (kg/ha)
    'MARKETED_MUSH': 'Marketed_mushroom',  # annual mushroom production of marketed species (mean value) (kg/ha)
    'MARKETED_LACTARIUS': 'Marketed_lactarius',  # production of marketed Lactarius (kg/ha*year)
    'MUSHROOM_PRODUCTIVITY': 'Mushrooms_production',


    # MIXED MODELS
    # General data
    'ID_SP1': 'ID_sp1',  # IFN (Spanish National Forestal Inventory) ID specie 1 - mixed models
    'SP1_PROPORTION': 'Proportion_sp1',  # proportion of specie 1 on a mix plot - mixed models
    'DENSITY_SP1': 'N_sp1',  # density of specie 1 on a mix plot - mixed models
    'BASAL_AREA_SP1': 'G_sp1',  # basal area os specie 1 on a mix plot - mixed models
    'BA_MAX_SP1': 'g_max_sp1',  # (cm2)
    'BA_MIN_SP1': 'g_min_sp1',  # (cm2)
    'MEAN_BA_SP1': 'g_media_sp1',  # (cm2) 
    'QM_DBH_SP1': 'dg_sp1',  # quadratic mean dbh of specie 1 - mixed models
    'DBH_MAX_SP1': 'dbh_max_sp1',  # (cm)
    'DBH_MIN_SP1': 'dbh_min_sp1',  # (cm)
    'MEAN_DBH_SP1': 'dbh_medio_sp1',  # (cm)
    'DOMINANT_DBH_SP1': 'Do_sp1',  # dominant diameter os specie 1 (cm) on mixed models
    'H_MAX_SP1': 'h_max_sp1',  # (m)
    'H_MIN_SP1': 'h_min_sp1',  # (m)
    'MEAN_H_SP1': 'h_media_sp1',  # (m)
    'DOMINANT_H_SP1': 'Ho_sp1',  # dominant height of specie 1 - mixed models
    'DOMINANT_SECTION_SP1': 'Dominant_section_sp1',  # (cm)
    'REINEKE_SP1': 'SDI_sp1',  # reineke index for specie 1 on mixed models
    'REINEKE_MAX_SP1': 'SDImax_sp1',  # maximal reineke index for specie 1 on mixed models

    'ID_SP2': 'ID_sp2',  # IFN (Spanish National Forestal Inventory) ID specie 2 - mixed models
    'SP2_PROPORTION': 'Proportion_sp2',  # proportion of specie 2 on a mix plot - mixed models
    'DENSITY_SP2': 'N_sp2',  # density of specie 2 on a mix plot - mixed models
    'BASAL_AREA_SP2': 'G_sp2',  # basal area os specie 2 on a mix plot - mixed models
    'BA_MAX_SP2': 'g_max_sp2',  # (cm2)
    'BA_MIN_SP2': 'g_min_sp2',  # (cm2)
    'MEAN_BA_SP2': 'g_media_sp2',  # (cm2)
    'QM_DBH_SP2': 'dg_sp2',  # quadratic mean dbh of specie 2 - mixed models
    'DBH_MAX_SP2': 'dbh_max_sp2',  # (cm)
    'DBH_MIN_SP2': 'dbh_min_sp2',  # (cm)
    'MEAN_DBH_SP2': 'dbh_medio_sp2',  # (cm) 
    'H_MAX_SP2': 'h_max_sp2',  # (m)
    'H_MIN_SP2': 'h_min_sp2',  # (m)
    'MEAN_H_SP2': 'h_media_sp2',  # (m)
    'DOMINANT_H_SP2': 'Ho_sp2',  # dominant height of specie 2 - mixed models
    'DOMINANT_DBH_SP2': 'Do_sp2',  # dominant diameter os specie 2 (cm) on mixed models
    'DOMINANT_SECTION_SP2': 'Dominant_section_sp2',  # (cm) 
    'REINEKE_SP2': 'SDI_sp2',  # reineke index for specie 2 on mixed models
    'REINEKE_MAX_SP2': 'SDImax_sp2',  # maximal reineke index for specie 2 on mixed models

    # Crown
    'CROWN_MEAN_D_SP1': 'Mean_crown_d_sp1',  # (m)
    'CROWN_DOM_D_SP1': 'Do_crown_sp1',  # (m)
    'CANOPY_COVER_SP1': 'Canopy_cover_sp1',  # (%)
    'CANOPY_VOL_SP1': 'Canopy_vol_sp1',  # Canopy volume (m3) for specie 1

    'CROWN_MEAN_D_SP2': 'Mean_crown_d_sp2',  # (m)
    'CROWN_DOM_D_SP2': 'Do_crown_sp2',  # (m)
    'CANOPY_COVER_SP2': 'Canopy_cover_sp2',  # (%)        
    'CANOPY_VOL_SP2': 'Canopy_vol_sp2',  # Canopy volume (m3) for specie 2

    # Biomass
    'WSW_SP1': 'WSW_sp1',  # wsw = stem wood (Tn/ha)
    'WSB_SP1': 'WSB_sp1',  # wsb = stem bark (Tn/ha)
    'WSWB_SP1': 'WSWB_sp1',  # wswb = stem wood and stem bark (Tn/ha)
    'WTHICKB_SP1': 'WTHICKB_sp1',  # wthickb = Thick branches > 7 cm (Tn/ha)
    'WSTB_SP1': 'WSTB_sp1',  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
    'WB2_7_SP1': 'WB2_7_sp1',  # wb2_7 = branches (2-7 cm) (Tn/ha)
    'WB2_T_SP1': 'WB_2_T_sp1',  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
    'WTHINB_SP1': 'WTHINB_sp1',  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
    'WB05_SP1': 'WB05_sp1',  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
    'WB05_7_SP1': 'WB05_7_sp1',  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
    'WB0_2_SP1': 'WB0_2_sp1',  # wb0_2 = branches < 2 cm (Tn/ha)
    'WDB_SP1': 'WDB_sp1',  # wdb = dead branches biomass (Tn/ha)
    'WL_SP1': 'WL_sp1',  # wl = leaves (Tn/ha)
    'WTBL_SP1': 'WTBL_sp1',  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
    'WBL0_7_SP1': 'WBL0_7_sp1',  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
    'WR_SP1': 'WR_sp1',  # wr = roots (Tn/ha)
    'WT_SP1': 'WT_sp1',  # wt = total biomass (Tn/ha)

    'WSW_SP2': 'WSW_sp2',  # wsw = stem wood (Tn/ha)
    'WSB_SP2': 'WSB_sp2',  # wsb = stem bark (Tn/ha)
    'WSWB_SP2': 'WSWB_sp2',  # wswb = stem wood and stem bark (Tn/ha)
    'WTHICKB_SP2': 'WTHICKB_sp2',  # wthickb = Thick branches > 7 cm (Tn/ha)
    'WSTB_SP2': 'WSTB_sp2',  # wstb = wsw + wthickb, stem + branches > 7 cm (Tn/ha)
    'WB2_7_SP2': 'WB2_7_sp2',  # wb2_7 = branches (2-7 cm) (Tn/ha)
    'WB2_T_SP2': 'WB_2_T_sp2',  # wb2_t = wb2_7 + wthickb; branches > 2 cm (Tn/ha)
    'WTHINB_SP2': 'WTHINB_sp2',  # wthinb = Thin branches (2-0.5 cm) (Tn/ha)
    'WB05_SP2': 'WB05_sp2',  # wb05 = thinniest branches (<0.5 cm) (Tn/ha)
    'WB05_7_SP2': 'WB05_7_sp2',  # wb05_7 = branches between 0.5-7 cm (Tn/ha)
    'WB0_2_SP2': 'WB0_2_sp2',  # wb0_2 = branches < 2 cm (Tn/ha)
    'WDB_SP2': 'WDB_sp2',  # wdb = dead branches biomass (Tn/ha)
    'WL_SP2': 'WL_sp2',  # wl = leaves (Tn/ha)
    'WTBL_SP2': 'WTBL_sp2',  # wtbl = wthinb + wl; branches < 2 cm and leaves (Tn/ha)
    'WBL0_7_SP2': 'WBL0_7_sp2',  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (Tn/ha)
    'WR_SP2': 'WR_sp2',  # wr = roots (Tn/ha)
    'WT_SP2': 'WT_sp2',  # wt = total biomass (Tn/ha)

    # Volume
    'VOL_SP1': 'V_sp1',  # (m3/ha)
    'BOLE_VOL_SP1': 'Bole_V_sp1',  # (m3/ha)
    'BARK_VOL_SP1': 'Bark_V_sp1',  # (m3/ha) 

    'VOL_SP2': 'V_sp2',  # (m3/ha)
    'BOLE_VOL_SP2': 'Bole_V_sp2',  # (m3/ha)
    'BARK_VOL_SP2': 'Bark_V_sp2',  # (m3/ha) 
    
    # Merchantable variables    
    'UNWINDING_SP1': 'V_unwinding_sp1',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
    'VENEER_SP1': 'V_veneer_sp1',  # veneer = the useful wood volume veneer destiny (m3/ha)
    'SAW_BIG_SP1': 'V_saw_big_sp1',  # saw_big = the useful wood volume big saw destiny (m3/ha)
    'SAW_SMALL_SP1': 'V_saw_small_sp1',  # saw_small = the useful wood volume small saw destiny (m3/ha)
    'SAW_CANTER_SP1': 'V_saw_canter_sp1',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
    'POST_SP1': 'V_post_sp1',  # post = the useful wood volume post destiny (m3/ha)
    'STAKE_SP1': 'V_stake_sp1',  # stake = the useful wood volume stake destiny (m3/ha)
    'CHIPS_SP1': 'V_chips_sp1',  # chips = the useful wood volume chips destiny (m3/ha)
    
    'UNWINDING_SP2': 'V_unwinding_sp2',  # unwinding = the useful wood volume unwinding destiny (m3/ha)
    'VENEER_SP2': 'V_veneer_sp2',  # veneer = the useful wood volume veneer destiny (m3/ha)
    'SAW_BIG_SP2': 'V_saw_big_sp2',  # saw_big = the useful wood volume big saw destiny (m3/ha)
    'SAW_SMALL_SP2': 'V_saw_small_sp2',  # saw_small = the useful wood volume small saw destiny (m3/ha)
    'SAW_CANTER_SP2': 'V_saw_canter_sp2',  # saw_canter = the useful wood volume canter saw destiny (m3/ha)
    'POST_SP2': 'V_post_sp2',  # post = the useful wood volume post destiny (m3/ha)
    'STAKE_SP2': 'V_stake_sp2',  # stake = the useful wood volume stake destiny (m3/ha)
    'CHIPS_SP2': 'V_chips_sp2',  # chips = the useful wood volume chips destiny (m3/ha)

    # Auxiliar variables for future models - 08/03/2023
    'PLOT_VAR1': 'PLOT_VAR1',
    'PLOT_VAR2': 'PLOT_VAR2',
    'PLOT_VAR3': 'PLOT_VAR3',
    'PLOT_VAR4': 'PLOT_VAR4',
    'PLOT_VAR5': 'PLOT_VAR5',
    'PLOT_VAR6': 'PLOT_VAR6',
    'PLOT_VAR7': 'PLOT_VAR7',
    'PLOT_VAR8': 'PLOT_VAR8',
    'PLOT_VAR9': 'PLOT_VAR9',
    'PLOT_VAR10': 'PLOT_VAR10',
    'PLOT_VAR11': 'PLOT_VAR11',
    'PLOT_VAR12': 'PLOT_VAR12',
    'PLOT_VAR13': 'PLOT_VAR13',
    'PLOT_VAR14': 'PLOT_VAR14',
    'PLOT_VAR15': 'PLOT_VAR15',
    'PLOT_VAR16': 'PLOT_VAR16',
    'PLOT_VAR17': 'PLOT_VAR17',
    'PLOT_VAR18': 'PLOT_VAR18',
    'PLOT_VAR19': 'PLOT_VAR19',
    'PLOT_VAR20': 'PLOT_VAR20',
    'PLOT_VAR21': 'PLOT_VAR21',
    'PLOT_VAR22': 'PLOT_VAR22',
    'PLOT_VAR23': 'PLOT_VAR23',
    'PLOT_VAR24': 'PLOT_VAR24',
    'PLOT_VAR25': 'PLOT_VAR25',
    'PLOT_VAR26': 'PLOT_VAR26',
    'PLOT_VAR27': 'PLOT_VAR27',
    'PLOT_VAR28': 'PLOT_VAR28',
    'PLOT_VAR29': 'PLOT_VAR29',
    'PLOT_VAR30': 'PLOT_VAR30',
    'PLOT_VAR31': 'PLOT_VAR31',
    'PLOT_VAR32': 'PLOT_VAR32',
    'PLOT_VAR33': 'PLOT_VAR33',
    'PLOT_VAR34': 'PLOT_VAR34',
    'PLOT_VAR35': 'PLOT_VAR35',
    'PLOT_VAR36': 'PLOT_VAR36',
    'PLOT_VAR37': 'PLOT_VAR37',
    'PLOT_VAR38': 'PLOT_VAR38',
    'PLOT_VAR39': 'PLOT_VAR39',
    'PLOT_VAR40': 'PLOT_VAR40',
    'PLOT_VAR41': 'PLOT_VAR41',
    'PLOT_VAR42': 'PLOT_VAR42',
    'PLOT_VAR43': 'PLOT_VAR43',
    'PLOT_VAR44': 'PLOT_VAR44',
    'PLOT_VAR45': 'PLOT_VAR45',
    'PLOT_VAR46': 'PLOT_VAR46',
    'PLOT_VAR47': 'PLOT_VAR47',
    'PLOT_VAR48': 'PLOT_VAR48',
    'UNWINDING_SP3': 'UNWINDING_SP3',
    'VENEER_SP3': 'VENEER_SP3',
    'SAW_BIG_SP3': 'SAW_BIG_SP3',
    'SAW_SMALL_SP3': 'SAW_SMALL_SP3',
    'SAW_CANTER_SP3': 'SAW_CANTER_SP3',
    'POST_SP3': 'POST_SP3',
    'STAKE_SP3': 'STAKE_SP3',
    'CHIPS_SP3': 'CHIPS_SP3',
    'VOL_SP3': 'VOL_SP3',
    'BOLE_VOL_SP3': 'BOLE_VOL_SP3',
    'BARK_VOL_SP3': 'BARK_VOL_SP3',
    'CARBON_STEM_SP1': 'CARBON_STEM_SP1',
    'CARBON_BRANCHES_SP1': 'CARBON_BRANCHES_SP1',
    'CARBON_ROOTS_SP1': 'CARBON_ROOTS_SP1',
    'CARBON_SP1': 'CARBON_SP1',
    'CARBON_STEM_SP2': 'CARBON_STEM_SP2',
    'CARBON_BRANCHES_SP2': 'CARBON_BRANCHES_SP2',
    'CARBON_ROOTS_SP2': 'CARBON_ROOTS_SP2',
    'CARBON_SP2': 'CARBON_SP2',
    'CARBON_STEM_SP3': 'CARBON_STEM_SP3',
    'CARBON_BRANCHES_SP3': 'CARBON_BRANCHES_SP3',
    'CARBON_ROOTS_SP3': 'CARBON_ROOTS_SP3',
    'CARBON_SP3': 'CARBON_SP3',
    'WS_SP3': 'WS_SP3',
    'WB_SP3': 'WB_SP3',
    'WR_SP3': 'WR_SP3',
    'WT_SP3': 'WT_SP3',
    'WS_SP2': 'WS_SP2',
    'WB_SP2': 'WB_SP2',
    'WS_SP1': 'WS_SP1',
    'WB_SP1': 'WB_SP1',
    'CARBON_STEM': 'CARBON_STEM',
    'CARBON_BRANCHES': 'CARBON_BRANCHES',
    'CARBON_ROOTS': 'CARBON_ROOTS',
    'WB': 'WB',
    'WS': 'WS',
    'ZPCUM9': 'ZPCUM9',
    'ZPCUM8': 'ZPCUM8',
    'ZPCUM7': 'ZPCUM7',
    'ZPCUM6': 'ZPCUM6',
    'ZPCUM5': 'ZPCUM5',
    'ZPCUM4': 'ZPCUM4',
    'ZPCUM3': 'ZPCUM3',
    'ZPCUM2': 'ZPCUM2',
    'ZPCUM1': 'ZPCUM1',
    'ZQ95': 'ZQ95',
    'ZQ90': 'ZQ90',
    'ZQ85': 'ZQ85',
    'ZQ80': 'ZQ80',
    'ZQ75': 'ZQ75',
    'ZQ70': 'ZQ70',
    'ZQ65': 'ZQ65',
    'ZQ60': 'ZQ60',
    'ZQ55': 'ZQ55',
    'ZQ50': 'ZQ50',
    'ZQ45': 'ZQ45',
    'ZQ40': 'ZQ40',
    'ZQ35': 'ZQ35',
    'ZQ30': 'ZQ30',
    'ZQ25': 'ZQ25',
    'ZQ20': 'ZQ20',
    'ZQ15': 'ZQ15',
    'ZQ10': 'ZQ10',
    'ZQ5': 'ZQ5',
    'PZABOVE2': 'PZABOVE2',
    'PZABOVEZMEAN': 'PZABOVEZMEAN',
    'ZENTROPY': 'ZENTROPY',
    'ZKURT': 'ZKURT',
    'ZSKEW': 'ZSKEW',
    'ZSD': 'ZSD',
    'ZMEAN': 'ZMEAN',
    'ZMAX': 'ZMAX',
    'SP3_N_PROPORTION': 'SP3_N_PROPORTION',
    'SP2_N_PROPORTION': 'SP2_N_PROPORTION',
    'SP1_N_PROPORTION': 'SP1_N_PROPORTION',
    'BASAL_AREA_SP3': 'BASAL_AREA_SP3',
    'QM_DBH_SP3': 'QM_DBH_SP3',
    'DENSITY_SP3': 'DENSITY_SP3',
    'MEAN_H_SP3': 'MEAN_H_SP3',
    'H_MIN_SP3': 'H_MIN_SP3',
    'H_MAX_SP3': 'H_MAX_SP3',
    'MEAN_DBH_SP3': 'MEAN_DBH_SP3',
    'DBH_MIN_SP3': 'DBH_MIN_SP3',
    'DBH_MAX_SP3': 'DBH_MAX_SP3',
    'MEAN_BA_SP3': 'MEAN_BA_SP3',
    'BA_MIN_SP3': 'BA_MIN_SP3',
    'BA_MAX_SP3': 'BA_MAX_SP3',
    'DOMINANT_SECTION_SP3': 'DOMINANT_SECTION_SP3',
    'DOMINANT_DBH_SP3': 'DOMINANT_DBH_SP3',
    'DOMINANT_H_SP3': 'DOMINANT_H_SP3',
    'CARBON_HEARTWOOD': 'CARBON_HEARTWOOD',
    'CARBON_SAPWOOD': 'CARBON_SAPWOOD',
    'CARBON_BARK': 'CARBON_BARK',
    'DEADWOOD_INDEX_CESEFOR_G': 'DEADWOOD_INDEX_CESEFOR_G',
    'DEADWOOD_INDEX_CESEFOR_V': 'DEADWOOD_INDEX_CESEFOR_V',
    'SAW_BIG_LIFEREBOLLO': 'SAW_BIG_LIFEREBOLLO',
    'SAW_SMALL_LIFEREBOLLO': 'SAW_SMALL_LIFEREBOLLO',
    'STAVES_INTONA': 'STAVES_INTONA',
    'BOTTOM_STAVES_INTONA': 'BOTTOM_STAVES_INTONA',
    'WOOD_PANELS_GAMIZ': 'WOOD_PANELS_GAMIZ',
    'MIX_GARCIA_VARONA': 'MIX_GARCIA_VARONA',
    'CARBON': 'CARBON',

}

EN_TREE = {
    # IDs
    'INVENTORY_ID': 'Inventory_ID',
    'PLOT_ID': 'Plot_ID',
    'TREE_ID': 'Tree_ID',

    # Special TREE_IDs to work with the IFN data
    'TREE_ID_IFN3_2': 'TREE_ID_IFN3_2',
    'TREE_ID_IFN3': 'TREE_ID_IFN3',
    'TREE_ID_IFN2': 'TREE_ID_IFN2',
    'TREE_ID_compare': 'TREE_ID_compare',

    # Tree general information
    'number_of_trees': 'number_of_trees',
    'specie': 'species',
    'bearing': 'bearing',  # bearing from the tree to the central point of the plot ('rumbo')
    'distance': 'distance',  # distance from the tree to the central point of the plot     
    'quality': 'quality',
    'shape': 'shape',
    'special_param': 'special_parameters',
    'remarks': 'remarks',
    'age_130': 'normal_age',  # (years)
    'social_class': 'social_class',
    'tree_age': 't',  # (years)
    'coord_x': 'coord_X',
    'coord_y': 'coord_Y',
    'coord_z': 'coord_Z',

    # Basic variables measured        
    'dbh_1': 'dbh_1',  # diameter measurement 1 (cm)
    'dbh_2': 'dbh_2',  # diameter measurement 2 (cm)
    'dbh': 'dbh',  # diameter at breast height (cm)
    'dbh_i': 'dbh_i',  # increment in diameter at breast height (cm)
    'stump_h': 'stump_h',  # (m)
    'height': 'h',  # total height (m)
    'height_i': 'height_i',  # increment in total tree height (m)
    'bark_1': 'bark_1',  # bark thickness measurement 1 (mm)
    'bark_2': 'bark_2',  # bark thickness measurement 2 (mm)
    'bark': 'bark',  # mean bark thickness (mm)
    'expan': 'expan',  # expansion factor

    # Basic variables calculated
    'normal_circumference': 'normal_circumference',  # circumference at breast height (cm)
    'slenderness': 'slenderness',  # (cm/cm)
    'basal_area': 'g',  # (cm2)
    'basal_area_i': 'basal_area_i',  # increment in basal area (cm2)
    'bal': 'bal',  # (m2/ha)
    'ba_ha': 'g_ha',  # (m2/ha)

    # Crown variables
    'cr': 'cr',  # (%)
    'lcw': 'lcw',  #  largest crown width (m)
    'hcb': 'hcb',  # height crown base (m)
    'hlcw': 'hlcw',  # height of largest crown width (m)
    'cpa': 'cpa',  # crown projection area (m2)
    'crown_vol': 'crown_vol',  # crown volume (m3)

    # Volume variables
    'vol': 'v',  # volume with bark (dm3)
    'bole_vol': 'bole_v',  # volume without bark (dm3)
    'bark_vol': 'bark_v',  # volume of bark (dm3)
    'firewood_vol': 'fuelwood_v',  # (dm3)
    'vol_ha': 'v_ha',  # volume with bark per hectare (m3/ha)

    # Biomass variables
    'wsw': 'wsw',  # wsw = stem wood (kg)
    'wsb': 'wsb',  # wsb = stem bark (kg)
    'wswb': 'wswb',  # wswb = stem wood and stem bark (kg)
    'w_cork': 'w_fresh_cork',  # fresh cork biomass (kg)
    'wthickb': 'wthickb',  # wthickb = Thick branches > 7 cm (kg)
    'wstb': 'wstb',  # wstb = wsw + wthickb, stem + branches > 7 cm (kg)
    'wb2_7': 'wb2_7',  # wb2_7 = branches (2-7 cm) (kg)
    'wb2_t': 'wb2_t',  # wb2_t = wb2_7 + wthickb; branches > 2 cm (kg)
    'wthinb': 'wthinb',  # wthinb = Thin branches (2-0.5 cm) (kg)
    'wb05': 'wb0.5',  # wb05 = thinniest branches (<0.5 cm) (kg)
    'wb05_7': 'wb05_7',  # wb05_7 = branches between 0.5-7 cm (kg)
    'wb0_2': 'wb0_2',  # wb0_2 = branches < 2 cm (kg)
    'wdb': 'wdb',  # wdb = dead branches biomass (kg)
    'wl': 'wl',  # wl = leaves (kg)
    'wtbl': 'wtbl',  # wtbl = wthinb + wl; branches < 2 cm and leaves (kg)
    'wbl0_7': 'wbl0_7',  # wbl0_7 = wb2_7 + wthinb + wl; branches < 7 cm and leaves (kg)
    'wr': 'wr',  # wr = roots (kg)
    'wt': 'wt',  # wt = total biomass (kg)

    # Wood uses variables    
    'unwinding': 'v_unwinding',  # unwinding = the useful wood volume unwinding destiny (dm3)
    'veneer': 'v_veneer',  #v eneer = the useful wood volume veneer destiny (dm3)
    'saw_big': 'v_saw_big',  # saw_big = the useful wood volume big saw destiny (dm3)
    'saw_small': 'v_saw_small',  # saw_small = the useful wood volume small saw destiny (dm3)
    'saw_canter': 'v_saw_canter',  # saw_canter = the useful wood volume canter saw destiny (dm3)
    'post': 'v_post',  # post = the useful wood volume post destiny (dm3)
    'stake': 'v_stake',  # stake = the useful wood volume stake destiny (dm3)
    'chips': 'v_chips',  # chips = the useful wood volume chips destiny (dm3)

    # Competition information
    'hegyi': 'hegyi_index',  # Hegyi competition index calculation

    # Quercus suber special variables
    'dbh_oc': 'dbh_over_cork',  # dbh over cork (cm) - Quercus suber
    'h_debark': 'uncork_h',  # uncork height on main stem (m) - Quercus suber
    'nb': 'uncork_boughs',  # number of main bough stripped - Quercus suber
    'cork_cycle': 'cork_cycle',  # moment to obtain cork data; 0 to the moment just immediately before the stripping process,
    'count_debark': 'n_debarks',  # Accountant of debark operations realised over each tree
    'total_w_debark': 'w_debarked',  # Cork biomass accumulator (kg) from the extracted cork of each tree with debark operations
    'total_v_debark': 'v_debarked',  # Cork volume accumulator (dm3) from the extracted cork of each tree with debark operations

# or 1 to the moment after the stripping process or at an intermediate age of the cork cycle production - Quercus suber
    # uncork_type': 'tipo de descorche  # s = only stem; pb = principal branches; sb = secondary branches - Quercus suber

    # Pinus pinea special variables
    'all_cones': 'cones',  # number of all the cones of the tree (anual mean)
    'sound_cones': 'healthy_cones',  # number of healthy cones in a tree  (anual mean)
    'sound_seeds': 'healthy_seeds',  # total sound seeds of the tree (anual mean)
    'w_sound_cones': 'w_healthy_cones',  # weight of sound (healthy) cones (kg) (anual mean)
    'w_all_cones': 'w_cones',  # weight of all (healthy and not) cones (kg) (anual mean)

    # mixed models
    'bal_intrasp': 'bal_intrasp',  # intraspecific bal (m2/ha) for mixed models
    'bal_intersp': 'bal_intersp',  # intraspecific bal (m2/ha) for mixed models
    'basal_area_intrasp': 'g_intrasp',  # intraspecific basal area (m2/ha) for mixed models
    'basal_area_intersp': 'g_intersp',  # interspecific basal area (m2/ha) for mixed models
    
    # Basic variables on hegyi subplot
    'bal_intrasp_hegyi': 'bal_intrasp_hegyi',  # intraspecific bal (m2/ha) inside hegyi subplot of each tree
    'bal_intersp_hegyi': 'bal_intersp_hegyi',  # interspecific bal (m2/ha) inside hegyi subplot of each tree
    'bal_ratio_intrasp_hegyi': 'bal_ratio_intrasp_hegyi',  # intraspecific bal ratio (0 to 1) inside hegyi subplot of each tree
    'bal_ratio_intersp_hegyi': 'bal_ratio_intersp_hegyi',  # interspecific bal ratio (0 to 1) inside hegyi subplot of each tree
    'bal_total_hegyi': 'bal_total_hegyi',  # total bal (m2/ha) inside hegyi subplot of each tree
    'g_intrasp_hegyi': 'g_intrasp_hegyi',  # intraspecific basal area (m2/ha) inside hegyi subplot of each tree
    'g_intersp_hegyi': 'g_intersp_hegyi',  # interspecific basal area (m2/ha) inside hegyi subplot of each tree
    'g_ratio_intrasp_hegyi': 'g_ratio_intrasp_hegyi',  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
    'g_ratio_intersp_hegyi': 'g_ratio_intersp_hegyi',  # intraspecific basal area ratio (0 to 1) inside hegyi subplot of each tree
    'g_total_hegyi': 'g_total_hegyi',  # total basal area (m2/ha) inside hegyi subplot of each tree
    'n_intrasp_hegyi': 'n_intrasp_hegyi',  # intraspecific density (trees/ha) inside hegyi subplot of each tree
    'n_intersp_hegyi': 'n_intersp_hegyi',  # interspecific density (trees/ha) inside hegyi subplot of each tree
    'n_ratio_intrasp_hegyi': 'n_ratio_intrasp_hegyi',  # intraspecific density ratio (0 to 1) inside hegyi subplot of each tree
    'n_ratio_intersp_hegyi': 'n_ratio_intersp_hegyi',  # interspecific density ratio (0 to 1) inside hegyi subplot of each tree
    'n_total_hegyi': 'n_total_hegyi',  # total density (trees/ha) inside hegyi subplot of each tree

    # Vorest model variables
    'w_voronoi': 'w_voronoi',  # weights used to construct the Voronoi diagrams
    'neighbours_mean_dbh': 'neighbours_mean_dbh',  # mean dbh of the neighbour trees
    'ogs': 'ogs',  # occupied growing space of tree i in year t, computed as the area of the weighted Voronoi region of the tree i restricted by the range of its zone of influence (radius) at time t
    'ags': 'ags',  # area in its surroundings not occupied by neighboring trees and therefore available to that tree to search for light
    'pgs': 'pgs',  # potential growing space of tree i in year t estimated as the crown projection area of an open grown tree of the same dbh
    'rel_area': 'rel_area',  # ratio of the occupied growing space (OGS) of a tree and its potential growing space (PGS) and it is used as a surrogate for the growing capacity of a tree

    # Auxiliar variables for future models - 08/03/2023
    'tree_var1': 'tree_var1',
    'tree_var2': 'tree_var2',
    'tree_var3': 'tree_var3',
    'tree_var4': 'tree_var4',
    'tree_var5': 'tree_var5',
    'tree_var6': 'tree_var6',
    'tree_var7': 'tree_var7',
    'tree_var8': 'tree_var8',
    'tree_var9': 'tree_var9',
    'tree_var10': 'tree_var10',
    'tree_var11': 'tree_var11',
    'tree_var12': 'tree_var12',
    'tree_var13': 'tree_var13',
    'tree_var14': 'tree_var14',
    'tree_var15': 'tree_var15',
    'tree_var16': 'tree_var16',
    'tree_var17': 'tree_var17',
    'tree_var18': 'tree_var18',
    'tree_var19': 'tree_var19',
    'tree_var20': 'tree_var20',
    'tree_var21': 'tree_var21',
    'tree_var22': 'tree_var22',
    'tree_var23': 'tree_var23',
    'tree_var24': 'tree_var24',
    'tree_var25': 'tree_var25',
    'tree_var26': 'tree_var26',
    'tree_var27': 'tree_var27',
    'tree_var28': 'tree_var28',
    'tree_var29': 'tree_var29',
    'tree_var30': 'tree_var30',
    'tree_var31': 'tree_var31',
    'tree_var32': 'tree_var32',
    'tree_var33': 'tree_var33',
    'tree_var34': 'tree_var34',
    'tree_var35': 'tree_var35',
    'tree_var36': 'tree_var36',
    'tree_var37': 'tree_var37',
    'tree_var38': 'tree_var38',
    'tree_var39': 'tree_var39',
    'tree_var40': 'tree_var40',
    'tree_var41': 'tree_var41',
    'tree_var42': 'tree_var42',
    'tree_var43': 'tree_var43',
    'tree_var44': 'tree_var44',
    'tree_var45': 'tree_var45',
    'tree_var46': 'tree_var46',
    'tree_var47': 'tree_var47',
    'tree_var48': 'tree_var48',
    'carbon_stem': 'carbon_stem',
    'carbon_branches': 'carbon_branches',
    'carbon_roots': 'carbon_roots',
    'wb': 'wb',
    'ws': 'ws',
    'carbon_heartwood': 'carbon_heartwood',
    'carbon_sapwood': 'carbon_sapwood',
    'carbon_bark': 'carbon_bark',
    'saw_big_liferebollo': 'saw_big_liferebollo',
    'saw_small_liferebollo': 'saw_small_liferebollo',
    'staves_intona': 'staves_intona',
    'bottom_staves_intona': 'bottom_staves_intona',
    'wood_panels_gamiz': 'wood_panels_gamiz',
    'mix_garcia_varona': 'mix_garcia_varona',
    'carbon': 'carbon',

    # Status
    'status': 'status',  # status of the tree, M-> die, C-> harvested, I-> ingrowth
}