############################# Description ################################
# This script is created for FINLION FMN project.                        #
# This script is part of csvTocsv.py.                                   #
#                                                                        #
# Author: Rouvinen Juha-Matti, Insta Advance                             #
# Date: 12/12/2023                                                       #
# Updated: 12/12/2023                                                    #
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
import random

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
    if mapping_type == 'test':
        # get mapping
        mapping_list = mapping.get_mapping('test', None)  # type, folder
    else:
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
    file_process_id = str(random.Random().randint(1, 1000000))

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

    print(f'{cgreen}[#] Creating JSON from CSV{cend}')
    csv_file_list = csv_file.splitlines()
    lines = len(csv_file_list)
    # loop through lines
    # loop through lines
    for line in csv_file_list:
        if line != '':
            percents = round(lines_processed / lines * 100, 2)
            percents = str(percents)
            prog_bar = progress_bar.print_progress_bar(lines, lines_processed)  # total lines, current line
            print(f'{cgreen}[-] Progress: |{prog_bar}| {percents}% Complete{cend}' + '\r', end='')

            unit = ''
            ver = ''
            count_semicolon = line.count(';')
            if count_semicolon == 0:
                concate = ','
            else:
                concate = ';'
            # get component data
            old_component = component
            component_loc = line.find(concate)
            component = line[:component_loc]
            component = util_tools.clean_srt(component)
            # determine if component is license or sw/hw
            component_license = lic_values_in_list.count(component)

            # get unit data
            unit_loc = line.rfind(concate)
            unit = line[component_loc + 1:unit_loc]
            unit = util_tools.clean_srt(unit)
            # get version data
            ver = line[unit_loc + 1:]
            ver = util_tools.clean_srt(ver)
            # unit_dict = {'component': "", 'name': "", 'version': "", 'expiration date': "", 'expiration status': '','responsible manager': '', 'json created': ''}
            unit_key = file_process_id + "_" + str(lines_processed)
            unit_dict = {'import key': "", 'component': "", 'name': "", 'version': "", 'expiration date': "",
                         'expiration status': '', 'responsible manager': '', 'json created': ''}

            if component_license != 0 and mapping_type != 'empty':  # processing of license data
                try:
                    upper_element = lic_main_value
                except KeyError:
                    upper_element = None
                # START ------ commented out in version 0.321 ------

                if upper_element != None:
                    unit_dict['component'] = 'Lisenssi-' + upper_element
                    unit_dict['version'] = ver
                    unit_dict['name'] = component
                    unit_dict['expiration date'] = ver
                    asset_json_dict[file_name_short].append(unit_dict)
                # ------ commented out in version 0.321 ------ END

            else:  # processing of other sw and/or hw data

                # find upper element
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
                    print(f'{(cyellow)}[INPUT] Unit {unit} does not exist in mapping file, do you want to:{(cend)}')
                    user_input = input(
                        f'{(cyellow)}[INPUT] 1 - Manually add component for {unit}\n, 2 - Skip this unit {(cend)}')
                    if user_input == '1':
                        upper_element = input(
                            f'{(cyellow)}[INPUT] Mapping component for {unit}: {(cend)}')
                        # add all data to dict
                        # unit_dict['component'] = upper_element + "-" + component
                        # unit_dict['name'] = unit
                        # tests for better handling vB0.12
                        unit_dict['component'] = unit
                        unit_dict['name'] = upper_element + "-" + component
                        unit_dict['version'] = ver
                        # unit_dict['expiration date'] = ''
                        # unit_dict['expiration status'] = ''
                        # append to dict
                        asset_json_dict[file_name_short].append(unit_dict)
                    else:
                        pass
                if upper_element is not None:
                    # unit_dict['component'] = upper_element + "-" + component
                    # unit_dict['name'] = unit
                    # tests for better handling vB0.12
                    unit_dict['name'] = unit
                    unit_dict['component'] = upper_element
                    unit_dict['import key'] = unit_key
                    unit_dict['version'] = ver
                    # unit_dict['expiration date'] = ''
                    # unit_dict['expiration status'] = ''
                    # append to dict
                    asset_json_dict[file_name_short].append(unit_dict)

            lines_processed += 1

    lines_processed += 1
    percents = 100
    prog_bar = progress_bar.print_progress_bar(lines,
                                               lines_processed)  # total lines, current line
    print(f'{cgreen}[-] Progress: |{prog_bar}| {percents}% Complete{cend}' + '\r',
          end='')
    # close file
    file_handler.file_handling('close', csv_file, True)
    asset_json_dict[file_name_short].append(
        {'name': 'Project_connector', 'Created': str(util_tools.get_date_time('date')),
         'import key': file_process_id + "_" + str(util_tools.get_date_time('date'))})
    asset_json_dict_to_write = str(asset_json_dict)
    asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
    print('')
    # write file
    file_handler.file_handling('write', file_name_short, asset_json_dict_to_write, True)
    return 'Done'
