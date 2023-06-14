############################# Description ################################
# This script is created for FINLION FMN project.                        #
# This script is part of csvToJSON.py.                                   #
#                                                                        #
# Author: Rouvinen Juha-Matti, Insta Advance                             #
# Date: 10/04/2023                                                       #
# Updated: 24/05/2023                                                    #
############################# License ####################################
#       Copyright [2023] [Insta Advance, Juha-Matti Rouvinen]            #
#                                                                        #
#   Licensed under the Apache License, Version 2.0 (the "License");      #
#   you may not use this file except in compliance with the License.     #
#   You may obtain a copy of the License at                              #
#                                                                        #
#       http://www.apache.org/licenses/LICENSE-2.0                       #
##########################################################################

# imports
from main import file_handler, util_tools, mapping, progress_bar

# print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cturq = '\033m[34m'
cend = '\033[0m'
chead = '\033[42m'


def process_file(*args):  # args: ['file' / 'dir'], [path], [mapping], [csv files]
    # file path to process
    file = args[1]
    mapping_type = args[2]
    # get mapping
    mapping_list = mapping.get_mapping(None, None) #type, folder
    sw_mapping = mapping_list[0]
    sw_mapping_values = sw_mapping.values()
    hw_mapping = mapping_list[1]
    hw_mapping_values = hw_mapping.values()
    lic_mapping = mapping_list[2]
    lic_main_values = lic_mapping.values()
    lic_main_value = None
    lic_mapping_values = lic_mapping.keys()
    lic_mapping_dict = None

    # open file
    csv_file = file_handler.file_handling('open', file, True)
    csv_file = csv_file.read()
    # get file name
    file_name_short = file[:-4]
    count_dashes = file_name_short.count('/')
    if count_dashes != 0:
        last_dash = file_name_short.rfind('/')
        file_name_short = file_name_short[last_dash + 1:]

    file_name_short = util_tools.clean_srt(file_name_short)
    file_name_short = file_name_short.replace('.', '')
    asset_json_dict = {file_name_short: []}

    # create sw and hw value lists into asset json
    lic_values_in_list = []
    values_in_list = []
    for x in sw_mapping_values:
        value_in_list = values_in_list.count(x)
        if value_in_list == 0:
            sw_mapping_dict = {x: []}
            values_in_list.append(x)
            asset_json_dict[file_name_short].append(sw_mapping_dict)

    for x in hw_mapping_values:
        value_in_list = values_in_list.count(x)
        if value_in_list == 0:
            hw_mapping_dict = {x: []}
            values_in_list.append(x)
            asset_json_dict[file_name_short].append(hw_mapping_dict)
    for x in lic_main_values:
        if lic_main_value is None:
            lic_main_value = x
            values_in_list.append(x)
            lic_main_value_dict = {lic_main_value: []}

    for x in lic_mapping_values:
        value_in_list = lic_values_in_list.count(x)
        if value_in_list == 0:
            lic_values_in_list.append(x)

    component = None
    component_list = []
    component_dict = None
    lines_processed = 0
    old_upper_element = None
    upper_element = None

    print(f'{(cgreen)}[#] Creating JSON from CSV{(cend)}')
    csv_file_list = csv_file.splitlines()
    lines = len(csv_file_list)
    # loop through lines
    for line in csv_file_list:
        if lines_processed == 0:
            pass
        else:
            percents = round(lines_processed / lines * 100, 2)
            percents = str(percents)
            prog_bar = progress_bar.print_progress_bar(lines, lines_processed)  # total lines, current line
            print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}' + '\r', end='')

            unit = ''
            ver = ''
            count_semicolon = line.count(';')
            if count_semicolon == 0:
                concat = ','
            else:
                concat = ';'
            # get all data pieces -----
            # get component data
            old_component = component
            component_loc = line.find(concat)
            component = line[:component_loc]
            component = util_tools.clean_srt(component)
            # determine if component is license or sw/hw
            component_license = lic_values_in_list.count(component)

            # get unit data
            unit_loc = line.rfind(concat)
            unit = line[component_loc + 1:unit_loc]
            unit = util_tools.clean_srt(unit)
            # get version data
            ver = line[unit_loc + 1:]
            ver = util_tools.clean_srt(ver)
            if component_license != 0:  # processing of license data
                try:
                    upper_element = lic_main_value
                except KeyError:
                    upper_element = None

                if upper_element != None:
                    unit_dict = {'name': component, 'exp_date': ver, 'expiration status': ''}
                    lic_dict = {lic_main_value: unit_dict}
                    index_num = values_in_list.index(upper_element)
                    asset_json_dict[file_name_short].append(lic_dict)

            else:  # processing of other sw and or hw data
                unit_dict = {'name': unit, 'version': ver}
                # check if component is already created
                component_on_list = component_list.count(component)
                if component_on_list == 0:
                    component_dict = None
                    component_list.append(component)
                    component_dict = {component: []}
                # add unit data to component
                component_dict[component] = unit_dict
                # check if element is on list
                try:
                    upper_element = sw_mapping[component]
                except KeyError:
                    upper_element = None
                if upper_element is None:
                    try:
                        upper_element = hw_mapping[component]
                    except KeyError:
                        upper_element = None
                elif upper_element is None:
                    try:
                        upper_element = lic_main_value
                    except KeyError:
                        upper_element = None
                if old_upper_element == None:
                    old_upper_element = upper_element
                if upper_element != old_upper_element or lines_processed == 1:
                    index_num = values_in_list.index(upper_element)
                    asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)
                    old_upper_element = upper_element
                    component_dict = {component: ''}
                elif mapping_type == 'None':
                    if component_dict != '':
                        asset_json_dict[file_name_short][upper_element].append(component_dict)

        lines_processed += 1
        if lines_processed == lines:
            if component_dict != '' and component_dict is not None:
                try:
                    upper_element = sw_mapping[component]
                except KeyError:
                    upper_element = None
                if upper_element is None:
                    try:
                        upper_element = hw_mapping[component]
                    except KeyError:
                        upper_element = None
                if upper_element is None:
                    try:
                        upper_element = lic_main_value
                    except KeyError:
                        upper_element = None
                index_num = values_in_list.index(upper_element)
                asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)

        percents = 100
        prog_bar = progress_bar.print_progress_bar(lines, lines_processed)  # total lines, current line
        print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}' + '\r', end='')

    # close file
    file_handler.file_handling('close', csv_file, True)
    asset_json_dict_to_write = str(asset_json_dict)
    asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
    print('')
    # write file
    file_handler.file_handling('write', file_name_short, asset_json_dict_to_write, True)
    return 'Done'
