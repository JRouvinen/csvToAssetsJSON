############################# Description ################################
# This script is created for FINLION FMN project.                        #
# This script is part of csvToJSON.py.                                   #
#                                                                        #
# Author: Rouvinen Juha-Matti, Insta Advance                             #
# Date: 17/11/2023                                                       #
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
import fnmatch
import random
from datetime import datetime

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
    asset_json_dict = None
    mapping_type = args[2]
    csv_files = args[3]
    env_name = args[4]
    now = datetime.now()
    file_process_id = str(datetime.timestamp(now))+'_' +env_name
    file_process_id = file_process_id.split('.')[0]
    ver = args[5]
    file_name_short = None
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
    if vm_inventory_exist == 1:
        server_name = mapping.get_mapping('name', folder + '/' + vm_inv_file_name)
        vm_mapping = mapping.get_mapping('vm', folder + '/' + vm_inv_file_name)
        vm_mapping_values = list(vm_mapping[0].values())
        vm_mapping_keys = list(vm_mapping[0].keys())
        asset_json_dict = {server_name: []}
        if len(vm_mapping_values) != 0:
            added_values = []
            added_keys = []
            for i in vm_mapping_values:
                if i not in added_values:
                    asset_json_dict[server_name].append({i: []})
                    added_values.append(i)
            index = 0
            for i in vm_mapping_keys:
                if i not in added_keys:
                    dict_index = added_values.index(vm_mapping_values[index])
                    asset_json_dict[server_name][dict_index][added_values[dict_index]].append({i: []})
                    added_keys.append(i)
                index += 1

    for fil_name in files_in_folder:
        not_vm_inventory = fil_name.find('vm_inventory')
        if fil_name.endswith('.csv') and not_vm_inventory == -1:
            if processed_csv_files > 0:
                print()
            file_to_read = folder + '/' + fil_name
            # open file
            csv_file = file_handler.file_handling('open', file_to_read, True)
            csv_file = csv_file.read()
            if vm_inventory_exist == 0:
                server_name = fil_name.split('_')[2]
            unit_name_list = fil_name.split('_')
            unit_name_list_len = len(unit_name_list)
            if unit_name_list_len > 4:
                unit_name_first = fil_name.split('_')[unit_name_list_len-2]
                unit_name_last = unit_name_list[unit_name_list_len-1].split('.')[0]
                unit_name = unit_name_first + '_' + unit_name_last
            else:
                unit_name = unit_name_list[unit_name_list_len-1].split('.')[0]

            if asset_json_dict is None:
                asset_json_dict = {server_name: []}
            # create sw and hw value lists into asset json
            component = None
            if len(added_keys) == 0:
                component_list = []
            else:
                component_list = added_keys
            component_dict = None
            lines_processed = 0
            old_upper_element = None
            upper_element = None
            curr_csv_file = processed_csv_files + 1
            if curr_csv_file > number_of_csv_files:
                curr_csv_file = number_of_csv_files
            print(
                f'{cgreen}[#] File {curr_csv_file}/{number_of_csv_files} - Appending data from "{fil_name}" to JSON {cend}')
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
                    # append asset json dict
                    #if component not in component_list:
                    #    component_list.append(component)
                    #    component_dict = {component: []}
                    #    asset_json_dict[server_name].append(component_dict)
                    # get unit data
                    unit_loc = line.rfind(concate)
                    unit = line[component_loc + 1:]
                    unit = util_tools.clean_srt(unit)
                    unit = unit.split(';')[0]
                    # get version data
                    ver = line[unit_loc + 1:]
                    ver = util_tools.clean_srt(ver)
                    # unit_dict = {'component': "", 'name': "", 'version': "", 'expiration date': "", 'expiration status': '','responsible manager': '', 'json created': ''}

                    # Updated on version B0.13
                    # unit_key = file_process_id+"_"+str(lines_processed)
                    unit_key = env_name
                    unit_dict = {'import key': "", 'unit': "", 'component': "", 'version': "",
                                 'expiration date': "", 'expiration status': '', 'responsible manager': '',
                                 }
                    unit_dict['import key'] = file_process_id + '_' + unit_name + '_' + component+'_'+unit
                    unit_dict['unit'] = unit
                    unit_dict['component'] = component
                    unit_dict['version'] = ver
                    #find correct asset_json_dict index for component
                    unit_dict_added = False
                    for i in range(0, len(asset_json_dict[server_name])):
                        value = list(asset_json_dict[server_name][i].keys())[0]
                        indx = 0
                        for y in asset_json_dict[server_name][i][value]:
                            key_y = list(y.keys())[0]
                            if component == key_y:
                                asset_json_dict[server_name][i][value][indx][key_y].append(unit_dict)
                                unit_dict_added = True
                            else:
                                component_switch = component.split('-')
                                if len(component_switch) > 1:
                                    component_switch = component_switch[1]+'-'+component_switch[0]
                                else:
                                    component_switch = component_switch[0]
                                if component_switch == key_y:
                                    unit_dict['component'] = component_switch
                                    asset_json_dict[server_name][i][value][indx][key_y].append(unit_dict)
                                    unit_dict_added = True
                            indx += 1
                    if not unit_dict_added:
                        print(f'{cyellow}[!] {component} not found in premade template, trying to figure correct placement {cend}' + '\r', end='')
                        #check if correct unit exists
                        for i in range(0, len(asset_json_dict[server_name])):
                            value = list(asset_json_dict[server_name][i].keys())[0]
                            if value == unit_name:
                                print(f'{cyellow}[!] Creating new partition into {value} for {component}  {cend}' + '\r',
                                    end='')
                                new_dict = {component:[]}
                                asset_json_dict[server_name][i].append(new_dict)
                                asset_json_dict[server_name][i][component].append(unit_dict)
                                unit_dict_added = True
                        if not unit_dict_added:
                        # piece together new unit for the server from file name
                            new_server_name = fil_name.split('_')[2:]
                            if new_server_name[0] == env_name and not unit_dict_added:
                                new_server_name = new_server_name[1:]
                                new_server_name = new_server_name[1] + '_' + new_server_name[0]
                                new_server_name = new_server_name.replace('.csv', '')
                            else:
                                new_server_name = '_'.join(new_server_name)
                        #check if similar server name exists
                            for i in range(0, len(asset_json_dict[server_name])):
                                value = list(asset_json_dict[server_name][i].keys())[0]
                                if value == new_server_name:
                                    print(f'{cyellow}[!] Creating new partition into {value} for {component}  {cend}' + '\r',
                                        end='')
                                    # add new component to asset_json_dict
                                    new_dict = {component: []}
                                    lenght = len(asset_json_dict[server_name])
                                    asset_json_dict[server_name][lenght-1][value].append(new_dict)
                                    lenght_2 = len(asset_json_dict[server_name][lenght - 1][value])
                                    asset_json_dict[server_name][lenght-1][value][lenght_2 - 1][component].append(unit_dict)
                                    unit_dict_added = True

                            if not unit_dict_added:
                                # add new unit to asset_json_dict
                                    asset_json_dict[server_name].append({new_server_name: []})
                                # add new component to asset_json_dict
                                    new_dict = {component: []}
                                    lenght = len(asset_json_dict[server_name])
                                    asset_json_dict[server_name][lenght-1][new_server_name].append(new_dict)
                                    asset_json_dict[server_name][lenght-1][new_server_name][0][component].append(unit_dict)
                                    unit_dict_added = True
                                # add new unit_dict to asset_json_dict
                        if not unit_dict_added:
                            print(f'{cyellow}[!] Could not find correct placement for {component}, skipping... {cend}' + '\r', end='')

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
        asset_json_dict[server_name].append(
            {'name': 'Project_connector', 'Created': str(util_tools.get_date_time('date')),
             'import key': file_process_id + "_" + str(util_tools.get_date_time('date')), 'version': ver})
        asset_json_dict_to_write = str(asset_json_dict)
        asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
        new_json_to_write = json.dumps(asset_json_dict_to_write)
        print('')
        # write file
        file_handler.file_handling('write', server_name, asset_json_dict_to_write, True)
        return 'Done'