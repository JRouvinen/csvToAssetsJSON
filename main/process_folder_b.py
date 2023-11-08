############################# Description ################################
# This script is created for FINLION FMN project.                        #
# This script is part of csvToJSON.py.                                   #
#                                                                        #
# Author: Rouvinen Juha-Matti, Insta Advance                             #
# Date: 10/04/2023                                                       #
# Updated: 29/06/2023                                                    #
############################# License ####################################
#       Copyright [2023] [Insta Advance, Juha-Matti Rouvinen]            #
#                                                                        #
#   Licensed under the Apache License, Version 2.0 (the "License");      #
#   you may not use this file except in compliance with the License.     #
#   You may obtain a copy of the License at                              #
#                                                                        #
#       http://www.apache.org/licenses/LICENSE-2.0                       #
##########################################################################
import fnmatch
import random

# imports
from main import util_tools, file_handler, progress_bar, mapping
import os
import json

# print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cturq = '\033m[34m'
cend = '\033[0m'
chead = '\033[42m'


def process_folder(*args):  # args: ['file' / 'dir'], [path], [mapping], [csv files], [env name], [version]
    folder = args[1]
    number_of_csv_files = int(args[3])
    directory = os.getcwd()
    directory = directory.replace('\\', '/')
    folder_dir = directory + folder
    processed_csv_files = 0
    name = str(util_tools.get_date_time('date'))
    # updated on version 0.42
    asset_json_dict = {name: []}
    mapping_type = args[2]
    csv_files = args[3]
    env_name = args[4]
    ver = args[5]
    file_name_short = None
    if mapping_type == 'test':
        # get mapping
        mapping_list = mapping.get_mapping('test', None)  # type, folder
    else:
        # get mapping
        mapping_list = mapping.get_mapping(None, None)  # type, folder
    sw_mapping = mapping_list[0]
    sw_mapping_values = sw_mapping.values()
    hw_mapping = mapping_list[1]
    hw_mapping_values = hw_mapping.values()
    # check if vm_inventory file exists
    pattern = 'vm_inventory*.csv'
    files_in_folder = os.listdir(folder_dir)
    vm_inventory_exist = 0
    vm_inv_file_name = None
    for fil_name in files_in_folder:
        if fnmatch.fnmatch(fil_name, pattern):
            vm_inventory_exist += 1
            vm_inv_file_name = fil_name
        if vm_inventory_exist > 1:
            print(f'{(cred)}[ERROR] Several vm_inventory files found --> stop execution {(cend)}' + '\r', end='')
            exit()
        # if true get json name and hw mapping from there else use hw mapping
    if vm_inventory_exist == 1:
        vm_mapping = mapping.get_mapping('vm', folder + '/' + vm_inv_file_name)
        vm_mapping_values = vm_mapping[0].values()
        # commented out on version 0.41 -> naming caused errors in JIRA Assets
        name = vm_mapping[1]
        vm_mapping = vm_mapping[0]
        asset_json_dict = None
        asset_json_dict = {name: []}
    # get license mapping
    lic_mapping = mapping_list[2]
    lic_main_values = lic_mapping.values()
    lic_main_value = None
    lic_mapping_values = lic_mapping.keys()

    # create sw and hw value lists into asset json
    lic_values_in_list = []
    values_in_list = []

    for x in sw_mapping_values:
        value_in_list = values_in_list.count(x)
        if value_in_list == 0:
            sw_mapping_dict = {x: []}
            values_in_list.append(x)
            # changed on ver 0.41
            # asset_json_dict[name].append(sw_mapping_dict)
            # asset_json_dict[name] = (sw_mapping_dict)

    if vm_inventory_exist == 1:
        for x in vm_mapping_values:
            value_in_list = values_in_list.count(x)
            value_in_hw_mapping = hw_mapping.get(x)
            if value_in_list == 0 and value_in_hw_mapping is None:
                hw_mapping_dict = {x: []}
                values_in_list.append(x)
                # changed on ver 0.41
                # asset_json_dict[name].append(hw_mapping_dict)
                # asset_json_dict[name] = (hw_mapping_dict)

    for x in hw_mapping_values:
        value_in_list = values_in_list.count(x)
        if value_in_list == 0:
            hw_mapping_dict = {x: []}
            values_in_list.append(x)
            # changed on ver 0.41
            # asset_json_dict[name].append(hw_mapping_dict)
            # asset_json_dict[name] = (hw_mapping_dict)

    for x in lic_main_values:
        if lic_main_value is None:
            lic_main_value = x
            values_in_list.append(x)
    # START ------ commented out in version 0.321 ------

    for x in lic_mapping_values:
        value_in_list = lic_values_in_list.count(x)
        if value_in_list == 0:
            # lic_mapping_dict = {x: []}
            lic_values_in_list.append(x)
            # lic_main_value_dict[lic_main_value].append(lic_mapping_dict)
    # asset_json_dict[name].append(lic_main_value_dict)

    # ------ commented out in version 0.321 ------ END
    # loop through all the files in the folder

    for filename in os.listdir(folder_dir):
        f = os.path.join(folder_dir, filename)
        if os.path.isfile(f):
            # changed on v0.431
            # check if vm_inventory file exists
            pattern = 'vm_inventory*.csv'
            files_in_folder = os.listdir(folder_dir)
            vm_inventory_exist = 0
            if fnmatch.fnmatch(filename, pattern) is True:
                vm_inventory_exist += 1

            if vm_inventory_exist > 0:
                if processed_csv_files > 0:
                    print()
                curr_csv_file += 1
                print(
                    f'{cgreen}[#] File {curr_csv_file}/{number_of_csv_files} - Mapping "{filename}" found -> using mapping from that file {cend}')
                vm_inventory_file = 0
                pass

            else:
                if filename.endswith('.csv'):
                    if processed_csv_files > 0:
                        print()
                    file_to_read = folder + '/' + filename
                    # open file
                    csv_file = file_handler.file_handling('open', file_to_read, True)
                    csv_file = csv_file.read()
                    # get file name
                    # file_name_short = filename[:-4]
                    # file_name_short = clean_srt(file_name_short)
                    # file_name_short = file_name_short.replace('.', '')
                    file_name_short = name
                    file_process_id = env_name + '_' + str(random.Random().randint(1, 1000000))
                    # create sw and hw value lists into asset json
                    component = None
                    component_list = []
                    component_dict = None
                    lines_processed = 0
                    old_upper_element = None
                    upper_element = None
                    curr_csv_file = processed_csv_files + 1
                    if curr_csv_file > number_of_csv_files:
                        curr_csv_file = number_of_csv_files
                    print(
                        f'{cgreen}[#] File {curr_csv_file}/{number_of_csv_files} - Appending data from "{filename}" to JSON {cend}')
                    csv_file_list = csv_file.splitlines()
                    lines = len(csv_file_list)
                    # loop through lines
                    for line in csv_file_list:
                        if line != '':
                            percents = round(lines_processed / lines * 100, 2)
                            percents = str(percents)
                            prog_bar = progress_bar.print_progress_bar(lines,
                                                                       lines_processed)  # total lines, current line
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

                            # Updated on version B0.13
                            # unit_key = file_process_id+"_"+str(lines_processed)
                            unit_key = env_name
                            unit_dict = {'import key': "", 'unit':"",'component': "", 'name': "", 'version': "",
                                         'expiration date': "", 'expiration status': '', 'responsible manager': '',
                                         'json created': ''}

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
                                        if vm_inventory_exist == 1:
                                            upper_element = vm_mapping[component]
                                    except KeyError:
                                        upper_element = None
                                if upper_element is None:
                                    try:
                                        upper_element = hw_mapping[component]
                                    except KeyError:
                                        upper_element = None
                                if upper_element is None:
                                    print(
                                        f'{cyellow}[INPUT] Unit {unit} on line {lines_processed} does not exist in mapping file, do you want to:{cend}')
                                    user_input = input(
                                        f'{cyellow}[INPUT] 1 - Manually add component for {unit}\n, 2 - Skip this unit {cend}')
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
                                    unit_dict['unit'] = upper_element
                                    # tests for better handling vB0.12
                                    unit_dict['name'] = component
                                    unit_dict['component'] = unit
                                    # Updated on version B0.13
                                    unit_dict['import key'] = unit_key + '_' + upper_element + '_' + unit+'_'+component
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
            processed_csv_files += 1
            if processed_csv_files == csv_files:
                asset_json_dict[file_name_short].append(
                    {'name': 'Project_connector', 'Created': str(util_tools.get_date_time('date')),
                     'import key': file_process_id + "_" + str(util_tools.get_date_time('date')),'version': ver})
                asset_json_dict_to_write = str(asset_json_dict)
                asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
                # new_json_to_write = json.dumps(asset_json_dict_to_write)
                print('')
                # write file
                file_handler.file_handling('write', file_name_short, asset_json_dict_to_write, True)
                return 'Done'
