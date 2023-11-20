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

from main import file_handler

#mapping parser
def get_mapping(type, folder):
    def create_dict(map_file):
        unit = ""
        component = ""
        mapping_dict = {}
        for line in map_file:
            if line.startswith('[') is True:
                component = ""
                component = line.strip()
                component = component.replace('[', '')
                component = component.replace(']', '')

            elif line.startswith('Unit') is True:
                unit_start = line.find('=')
                unit = line[unit_start + 2:]
                unit = unit.strip()

            if unit != '':
                mapping_dict[unit] = component
                unit = ""
        return mapping_dict
    if type == 'vm':
        vm_file = file_handler.file_handling('open', folder, True)
        vm_mapping = vm_file.readlines()
        vm_mapping_dict = {}
        vm_mapping_name = vm_mapping[0].split(';')
        vm_mapping_name = vm_mapping_name[1]
        vm_mapping_indx = vm_mapping_name.index('.')
        vm_mapping_name = vm_mapping_name[vm_mapping_indx + 1:]
        vm_mapping_indx = vm_mapping_name.index('.')
        vm_mapping_name = vm_mapping_name[vm_mapping_indx + 1:]
        vm_mapping_name = vm_mapping_name.replace('\n', '')
        for x in vm_mapping:
            values = x.split(';')
            vm_data = values[1]
            vm_data_inx = vm_data.index('.')
            vm_data1 = vm_data[:vm_data_inx]
            vm_data1_1 = vm_data[vm_data_inx + 1:]
            vm_data_inx = vm_data1_1.index('.')
            vm_data2 = vm_data1_1[:vm_data_inx]
            unit_data = values[0]
            vm_mapping_dict[unit_data] = vm_data1 + '-' + vm_data2
        return vm_mapping_dict, vm_mapping_name
    elif type == 'test':
        # create test mapping
        test_mapping = file_handler.file_handling('open', '../mapping/test_mapping.ini', False)
        test_mapping = test_mapping.read()
        test_mapping = test_mapping.splitlines()
        if test_mapping[0].startswith('#') is True:
            test_mapping = test_mapping[4:]
        test_mapping_dic = create_dict(test_mapping)
        # create license mapping
        test_lic_mapping = file_handler.file_handling('open', '../mapping/test_license_mapping.ini', False)
        test_lic_mapping = test_lic_mapping.read()
        test_lic_mapping = test_lic_mapping.splitlines()
        if test_lic_mapping[0].startswith('#') is True:
            test_lic_mapping = test_lic_mapping[4:]
        test_lic_mapping_dic = create_dict(test_lic_mapping)
        return test_mapping_dic, test_mapping_dic, test_lic_mapping_dic
    elif type == 'name':
        vm_file = file_handler.file_handling('open', folder, True)
        vm_name = vm_file.readline()
        vm_name = vm_name.split('.')
        vm_name = vm_name[2:]
        vm_name_srt = '.'.join(vm_name)
        vm_name_srt = vm_name_srt.replace('\n', '')
        return vm_name_srt
    else:
        #create sw mapping
        sw_mapping = file_handler.file_handling('open', '/mapping/sw_mapping.ini', False)
        sw_mapping = sw_mapping.read()
        sw_mapping = sw_mapping.splitlines()
        if sw_mapping[0].startswith('#') is True:
            sw_mapping = sw_mapping[4:]
        sw_mapping_dic = create_dict(sw_mapping)
        #create hw mapping
        hw_mapping = file_handler.file_handling('open', '/mapping/hw_mapping.ini', False)
        hw_mapping = hw_mapping.read()
        hw_mapping = hw_mapping.splitlines()
        if hw_mapping[0].startswith('#') is True:
            hw_mapping = hw_mapping[4:]
        hw_mapping_dic = create_dict(hw_mapping)
        # create license mapping
        lic_mapping = file_handler.file_handling('open', '/mapping/license_mapping.ini', False)
        lic_mapping = lic_mapping.read()
        lic_mapping = lic_mapping.splitlines()
        if lic_mapping[0].startswith('#') is True:
            lic_mapping = lic_mapping[4:]
        lic_mapping_dic = create_dict(lic_mapping)
        return sw_mapping_dic, hw_mapping_dic, lic_mapping_dic