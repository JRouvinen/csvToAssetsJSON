
#imports
from main import util_tools, file_handler, progress_bar, mapping
import os
import json

#print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cturq = '\033m[34m'
cend = '\033[0m'
chead = '\033[42m'


def process_folder(*args):
    folder = args[1]
    number_of_csv_files = int(args[3])
    directory = os.getcwd()
    directory = directory.replace('\\', '/')
    folder_dir = directory + folder
    processed_csv_files = 0
    name = str(util_tools.get_date_time('date'))
    #updated on version 0.42
    asset_json_dict = {name: []}
    mapping_type = args[2]
    csv_files = args[3]
    file_name_short = None
    # get mapping
    mapping_list = mapping.get_mapping(None, None)
    sw_mapping = mapping_list[0]
    sw_mapping_values = sw_mapping.values()
    hw_mapping = mapping_list[1]
    hw_mapping_values = hw_mapping.values()
    #check if vm_inventory.csv file exists
    vm_inventory_exist = util_tools.check_file_or_folder_exists(folder+'/'+'vm_inventory.csv', 'file')
    #if true get json name and hw mapping from there else use hw mapping
    if vm_inventory_exist == 1:
        vm_mapping = mapping.get_mapping('vm', folder)
        vm_mapping_values = vm_mapping[0].values()
        #commented out on version 0.41 -> naming caused errors in JIRA Assets
        #name = vm_mapping[1]
        vm_mapping = vm_mapping[0]
        asset_json_dict = None
        asset_json_dict = {name: []}
    #get license mapping
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
            #changed on ver 0.41
            asset_json_dict[name].append(sw_mapping_dict)
            #asset_json_dict[name] = (sw_mapping_dict)


    if vm_inventory_exist == 1:
        for x in vm_mapping_values:
            value_in_list = values_in_list.count(x)
            if value_in_list == 0:
                hw_mapping_dict = {x: []}
                values_in_list.append(x)
                # changed on ver 0.41
                asset_json_dict[name].append(hw_mapping_dict)
                #asset_json_dict[name] = (hw_mapping_dict)


    for x in hw_mapping_values:
        value_in_list = values_in_list.count(x)
        if value_in_list == 0:
            hw_mapping_dict = {x: []}
            values_in_list.append(x)
            # changed on ver 0.41
            asset_json_dict[name].append(hw_mapping_dict)
            #asset_json_dict[name] = (hw_mapping_dict)

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
            if filename == 'vm_inventory.csv':
                if processed_csv_files > 0:
                    print()
                curr_csv_file += 1
                print(f'{cgreen}[#] File {curr_csv_file}/{number_of_csv_files} - Mapping "{filename}" found -> using mapping from that file {cend}')
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
                    print(f'{cgreen}[#] File {curr_csv_file}/{number_of_csv_files} - Appending data from "{filename}" to JSON {cend}')
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
                            if component_license != 0:  # processing of license data
                                try:
                                    upper_element = lic_main_value
                                except KeyError:
                                    upper_element = None
                                # START ------ commented out in version 0.321 ------

                                if upper_element != None:
                                    unit_dict = {'name': component, 'exp_date': ver, 'expiration status': ''}
                                    lic_dict = {lic_main_value: unit_dict}
                                    index_num = values_in_list.index(upper_element)
                                    # sub_indx = lic_values_in_list.index(component)
                                    # asset_json_dict[file_name_short][index_num][upper_element][sub_indx][
                                    # component] = unit_dict
                                    asset_json_dict[file_name_short].append(lic_dict)
                                # ------ commented out in version 0.321 ------ END

                            else:  # processing of other sw and/or hw data
                                unit_dict = {'name': unit, 'version': ver}
                                # check if component is already created
                                component_on_list = component_list.count(component)
                                if component_on_list == 0:
                                    component_dict = None
                                    component_list.append(component)
                                    component_dict = {component: []}
                                # add unit data to component
                                #changed on ver 0.41
                                component_dict[component].append(unit_dict)
                                # check if element is on list
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
                                    dash_indx = component.rfind('-')
                                    edited_component = component[:dash_indx]
                                    edited_component = 'mgmt-'+edited_component
                                    try:
                                        upper_element = vm_mapping[edited_component]
                                    except KeyError:
                                        upper_element = None
                                if old_upper_element is None:
                                    old_upper_element = upper_element
                                if upper_element != old_upper_element or lines_processed == 1:
                                    index_num = values_in_list.index(upper_element)
                                    asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)
                                    old_upper_element = upper_element
                                    component_dict = {component: []}
                                elif mapping_type == 'None':
                                    if component_dict != '':
                                        asset_json_dict[file_name_short][upper_element].append(component_dict)

                        lines_processed += 1
                        if lines_processed == lines:
                            license_wrt = False
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
                                        asset_json_dict[file_name_short].append(lic_dict)
                                        license_wrt = True
                                    except KeyError:
                                        upper_element = None
                                if license_wrt is False:
                                    index_num = values_in_list.index(upper_element)
                                    asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)

                        percents = 100
                        prog_bar = progress_bar.print_progress_bar(lines, lines_processed)  # total lines, current line
                        print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}' + '\r', end='')

                    # close file
                    file_handler.file_handling('close', csv_file, True)
            processed_csv_files += 1
            if processed_csv_files == csv_files:
                asset_json_dict[file_name_short].append({'name': 'Project_connector', 'Created': str(util_tools.get_date_time('date'))})
                asset_json_dict_to_write = str(asset_json_dict)
                asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
                #new_json_to_write = json.dumps(asset_json_dict_to_write)
                print('')
                # write file
                file_handler.file_handling('write', file_name_short, asset_json_dict_to_write, True)
                return 'Done'
