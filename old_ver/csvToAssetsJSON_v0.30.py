#--------Description--------
# This script is created for FINLION FMN project.
# Aim of this script is to convert csv files into JIRA Asset JSON format files
# Author: Rouvinen Juha-Matti, Insta Advance
# Date: 10/04/2023
#---------------------------
# List of To Do -
# TODO: Test different argument variations
# TODO: Refactor code into more manageable imports
# DONE: Bug - File creation name loop doesn't work
# DONE: Bug - Color formatting doesn't work properly in wind cmd / powershell
# TODO: Simplify the JSON structure
#
#---------------------------
#imports
import os
import argparse
from datetime import datetime

#common variables
opened_files = []
__app_name__ = "CSV to JIRA Asset JSON"
__version__ = "0.31"
#change log
change_log = [

'0.22 -> first working version #10/04/2023',
'0.23 -> argparser implementation and added print colors #12/04/2023',
'0.24 -> configparser support #12/04/2023',
'0.25 -> mapping support and better arg parsing #13/04/2023',
'0.26 -> Improved mapping support and fixed mapping parsing #42/04/2023',
'0.27 -> Support for sw / hw arguments and own mapping files for both #14/04/2023',
'0.28 -> fixes on bugs, support for folder processing and better progressbar #17/04/2023',
'0.29 -> updated arg parser (version command) and better mapping processing #18/04/2023',
'0.30 -> updated output file/folder processing, updates on file writing and fixes on arg parsing #19/04/2023',
'0.31 ->  Bug fixes: Color formatting doesnt work properly in wind cmd / powershell,file creation loop fixed  #21/04/2023',

]

#print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cend = '\033[0m'
chead = '\033[42m'

# check if file is there
def check_file_or_folder_exists(file,type):
    is_file = False
    is_folder = False
    if type == 'file':
        print(f'{(cyellow)}[<-] Checking file ({file}) path...{(cend)}')
        is_file = os.path.isfile(file)
        print(f'{(cgreen)}[->] File found: {is_file}{(cend)}')
        if is_file is False:
            print(f'{(cred)}[!] File not found! -> stopping program!!!{(cend)}')
            exit()
    else:
        print(f'{(cyellow)}[<-] Checking file ({file}) path...{(cend)}')
        if file.endswith('.csv'):
            is_file = os.path.isfile(file)
        else:
            csv_file = file+'.csv'
            is_file = os.path.isfile(csv_file)
        if is_file is True:
            check_file_type(file)
        #print(f'{(cgreen)}[->] File found: {is_file}{(cend)}')
        if is_file is False:
            print(f'{(cyellow)}[->] File not found: {is_file}{(cend)}')
            print(f'{(cyellow)}[<-] Checking folder ({file}) path{(cend)}')
            directory = os.getcwd()
            directory = directory.replace('\\', '/')
            folder_dir = directory + file
            is_folder = os.path.exists(folder_dir)
        if is_folder is False and is_file is False:
            print(f'{(cred)}[!] File/Folder not found! -> stopping program{(cend)}')
            exit()
        elif is_folder is True:
            print(f'{(cgreen)}[->] Folder found: {is_folder}{(cend)}')
            print(f'{(cyellow)}[<-] Checking files inside the folder{(cend)}')
            csv_files = 0
            for fname in os.listdir(folder_dir):
                if fname.endswith('.csv'):
                    csv_files += 1
            else:
                pass
            if csv_files == 0:
                print(f'{(cred)}[!] No CSV files found inside the folder{(cend)}')
                exit()
            else:
                print(f'{(cgreen)}[->] {csv_files} files found in the folder{(cend)}')
                print(f'{(cgreen)}----------------------------------------------------{(cend)}')

            return csv_files

# Returns time/date
def get_date_time(type):
    now = datetime.now()  # current date and time
    time = now.strftime("%H:%M:%S")
    date = now.date()
    if type == 'time':
        return time
    elif type == 'date':
        return date

#print progressbar
def print_progress_bar(*args): #total lines, current line
    total_lines = int(args[0])
    current_line = int(args[1])
    fill = '█'
    printEnd = "\r"
    length = 50
    percent = float(current_line/total_lines*100)
    filledLength = int(length * current_line // total_lines)
    bar = fill * filledLength + '-' * (length - filledLength)
    return bar

#create json from csv
def create_asset_json(*args): # args: ['file' / 'dir'], [path], [mapping], [csv files]
    file_folder = args[0]
    mapping_type = args[2]
    if mapping_type == 'sw':
        sw_mapping = get_mapping('sw')
        sw_mapping = sw_mapping[0]
        sw_mapping_values = sw_mapping.values()
    elif mapping_type == 'hw':
        hw_mapping = get_mapping('hw')
        hw_mapping = hw_mapping[1]
        hw_mapping_values = hw_mapping.values()
    else:
        mapping = get_mapping()
        sw_mapping = mapping[0]
        sw_mapping_values = sw_mapping.values()
        hw_mapping = mapping[1]
        hw_mapping_values = hw_mapping.values()

    #print(sw_mapping)
    #print(hw_mapping)
    # process single file
    if file_folder == 'file':
        file = args[1]
        #open file
        csv_file = file_handling('open', file, True)
        csv_file = csv_file.read()
        #get file name
        file_name_short = file[:-4]
        file_name_short = clean_srt(file_name_short)
        file_name_short = file_name_short.replace('.','')
        asset_json_dict = {file_name_short: []}

        #create sw and hw value lists into asset json

        values_in_list = []
        for x in sw_mapping_values:
            value_in_list = values_in_list.count(x)
            if value_in_list == 0:
                sw_mapping_dict = {x:[]}
                values_in_list.append(x)
                asset_json_dict[file_name_short].append(sw_mapping_dict)

        for x in hw_mapping_values:
            value_in_list = values_in_list.count(x)
            if value_in_list == 0:
                hw_mapping_dict = {x: []}
                values_in_list.append(x)
                asset_json_dict[file_name_short].append(hw_mapping_dict)

        component = None
        component_list = []
        component_dict = None
        lines_processed = 0
        old_upper_element = None

        print(f'{(cgreen)}[#] Creating JSON from CSV{(cend)}')
        csv_file_list = csv_file.splitlines()
        lines = len(csv_file_list)
        #print(f'{(cblue)}[#] Reading lines in file: {lines} lines found{(cend)}')
        #loop through lines
        for line in csv_file_list:
            if lines_processed == 0:
                pass
            else:
                percents = round(lines_processed/lines*100,2)
                percents = str(percents)
                prog_bar = print_progress_bar(lines, lines_processed) #total lines, current line
                print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}'+'\r', end='')

                unit = ''
                ver = ''
                count_semicolon = line.count(';')
                if count_semicolon == 0:
                    concate = ','
                else:
                    concate = ';'
                #get all data -----
                #get component data
                old_component = component
                component_loc = line.find(concate)
                component = line[:component_loc]
                component = clean_srt(component)
                #get unit data
                unit_loc = line.rfind(concate)
                unit = line[component_loc+1:unit_loc]
                unit = clean_srt(unit)
                #get version data
                ver = line[unit_loc+1:]
                ver = clean_srt(ver)
                unit_dict = {'name':unit,'version':ver}
                #check if component is already created
                component_on_list = component_list.count(component)
                if component_on_list == 0:
                    component_dict = None
                    component_list.append(component)
                    component_dict = {component: []} 
                #add unit data to component
                component_dict[component].append(unit_dict)  
                #check if element is on list
                try:
                    upper_element = sw_mapping[component]
                except KeyError:
                    upper_element = None
                if upper_element is None:
                    try:
                        upper_element = hw_mapping[component]
                    except KeyError:
                        upper_element = None

                if old_upper_element == None:
                    old_upper_element = upper_element
                if upper_element != old_upper_element or lines_processed == 1:
                    index_num = values_in_list.index(upper_element)
                    asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)
                    old_upper_element = upper_element
                    component_dict = {component: []}
                elif mapping_type == 'None':
                    if component_dict != '':
                        asset_json_dict[file_name_short][0][upper_element].append(component_dict)


            lines_processed += 1
            if lines_processed == lines:
                if component_dict != '':
                    try:
                        upper_element = sw_mapping[component]
                    except KeyError:
                        upper_element = None
                    if upper_element is None:
                        try:
                            upper_element = hw_mapping[component]
                        except KeyError:
                            upper_element = None
                    index_num = values_in_list.index(upper_element)
                    asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)

            percents = 100
            prog_bar = print_progress_bar(lines, lines_processed)  # total lines, current line
            print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}' + '\r', end='')

        #print(asset_json_dict)

        #close file
        file_handling('close', csv_file, True)
        asset_json_dict_to_write = str(asset_json_dict)
        asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
        print('')
        #write file
        file_handling('write', file_name_short, asset_json_dict_to_write, True)
    
    #process folder
    else:
        folder = args[1]
        number_of_csv_files = int(args[3])
        directory = os.getcwd()
        directory = directory.replace('\\', '/')
        folder_dir = directory + folder
        processed_csv_files = 0
        name = str(get_date_time('date'))
        asset_json_dict = {name: []}
        values_in_list = []

        for x in sw_mapping_values:
            value_in_list = values_in_list.count(x)
            if value_in_list == 0:
                sw_mapping_dict = {x: []}
                values_in_list.append(x)
                asset_json_dict[name].append(sw_mapping_dict)

        for x in hw_mapping_values:
            value_in_list = values_in_list.count(x)
            if value_in_list == 0:
                hw_mapping_dict = {x: []}
                values_in_list.append(x)
                asset_json_dict[name].append(hw_mapping_dict)

        for filename in os.listdir(folder_dir):
            f = os.path.join(folder_dir, filename)
            if os.path.isfile(f):
                if filename.endswith('.csv'):
                    overall_percents = round(processed_csv_files / number_of_csv_files * 100, 2)
                    overall_percents = str(overall_percents)
                    file_to_read = folder+'/'+filename
                    # open file
                    csv_file = file_handling('open', file_to_read, True)
                    csv_file = csv_file.read()
                    # get file name
                    #file_name_short = filename[:-4]
                    #file_name_short = clean_srt(file_name_short)
                    #file_name_short = file_name_short.replace('.', '')
                    file_name_short = name
                    # create sw and hw value lists into asset json


                    component = None
                    component_list = []
                    component_dict = None
                    lines_processed = 0
                    old_upper_element = None

                    curr_csv_file = processed_csv_files+1
                    if curr_csv_file > number_of_csv_files:
                        curr_csv_file = number_of_csv_files
                    print(f'{(cgreen)}[#] Creating JSON {curr_csv_file}/{number_of_csv_files} from CSV {(cend)}')
                    csv_file_list = csv_file.splitlines()
                    lines = len(csv_file_list)
                    # loop through lines
                    for line in csv_file_list:
                        if lines_processed == 0:
                            pass
                        else:
                            percents = round(lines_processed / lines * 100, 2)
                            percents = str(percents)
                            prog_bar = print_progress_bar(lines, lines_processed)  # total lines, current line
                            print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}' + '\r', end='')

                            unit = ''
                            ver = ''
                            count_semicolon = line.count(';')
                            if count_semicolon == 0:
                                concate = ','
                            else:
                                concate = ';'
                            # get all data -----
                            # get component data
                            old_component = component
                            component_loc = line.find(concate)
                            component = line[:component_loc]
                            component = clean_srt(component)
                            # get unit data
                            unit_loc = line.rfind(concate)
                            unit = line[component_loc + 1:unit_loc]
                            unit = clean_srt(unit)
                            # get version data
                            ver = line[unit_loc + 1:]
                            ver = clean_srt(ver)
                            unit_dict = {'name': unit, 'version': ver}
                            # check if component is already created
                            component_on_list = component_list.count(component)
                            if component_on_list == 0:
                                component_dict = None
                                component_list.append(component)
                                component_dict = {component: []}
                                # add unit data to component
                            component_dict[component].append(unit_dict)
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

                            if old_upper_element == None:
                                old_upper_element = upper_element
                            if upper_element != old_upper_element or lines_processed == 1:
                                index_num = values_in_list.index(upper_element)
                                asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)
                                old_upper_element = upper_element
                                component_dict = {component: []}
                            elif mapping_type == 'None':
                                if component_dict != '':
                                    asset_json_dict[file_name_short][0][upper_element].append(component_dict)

                        lines_processed += 1
                        if lines_processed == lines:
                            if component_dict != '':
                                try:
                                    upper_element = sw_mapping[component]
                                except KeyError:
                                    upper_element = None
                                if upper_element is None:
                                    try:
                                        upper_element = hw_mapping[component]
                                    except KeyError:
                                        upper_element = None
                                index_num = values_in_list.index(upper_element)
                                asset_json_dict[file_name_short][index_num][upper_element].append(component_dict)

                        percents = 100
                        prog_bar = print_progress_bar(lines, lines_processed)  # total lines, current line
                        print(f'{(cgreen)}[-] Progress: |{prog_bar}| {percents}% Complete{(cend)}' + '\r', end='')

                    # print(asset_json_dict)

                    # close file
                    file_handling('close', csv_file, True)
                processed_csv_files += 1
                if processed_csv_files == csv_files:
                    asset_json_dict_to_write = str(asset_json_dict)
                    asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
                    print('')
                    # write file
                    file_handling('write', file_name_short, asset_json_dict_to_write, True)

    print(f'{(cgreen)}----------------------------------------------------{(cend)}')
    print(f'{(cgreen)}[#] Done!{(cend)}')
    
#file handling
def file_handling(*args): #open, filename, printout | write, filename,text | close, filename
    operation = args[0]
    file = args[1]
    to_print = args[2]
    #open file
    if operation == 'open':
        directory = os.getcwd()
        directory = directory.replace('\\', '/')
        file = str(file)
        file = directory+'/'+file
        if to_print is True:
            print(f'{(cyellow)}[<-] Reading file: {file}{(cend)}')
        f = open(file, 'r')
        opened_files.append(f)
        return f
    #write file
    if operation == 'write':
        #check if output folder exists and create it if not
        directory = os.getcwd()
        directory = directory.replace('\\','/')
        output_dir = directory+'/output/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        #check if current date folder exists in output folder and create it if not
        date = str(get_date_time('date'))
        date_dir = output_dir+date
        if not os.path.exists(date_dir):
            os.mkdir(date_dir)
        new_file_name = file + '.json'
        newfile_already_exists = True
        number = 0
        path = date_dir+'/'+new_file_name
        while newfile_already_exists is True:
            newfile_already_exists = os.path.isfile(path)
            number += 1
            new_file_name = file+'_'+str(number)+'.json'
            path = date_dir + '/' + new_file_name
        #check_file_or_folder_exists(new_file_name, 'file')
        if number == 0:
            new_file_name = file + '.json'
        new_file = open(date_dir+'/'+new_file_name, 'w')
        print(f'{(cyellow)}[->] Writing file: {date_dir}/{new_file_name}{(cend)}')
        new_file.write(str(to_print))
        new_file.close()
    #close file
    if operation == 'close':
        file_to_close = opened_files[0]
        file_to_close.close()

#string cleaning
def clean_srt(string):
    cleaned_str = string.strip()
    cleaned_str = cleaned_str.replace('"', '')
    cleaned_str = cleaned_str.replace('\n', '')
    cleaned_str = cleaned_str.replace('\\', '')

    return cleaned_str

#file type check
def check_file_type(file):
    end = file[-4:]
    if end != '.csv':
        file = file+'.csv'
    return file

def print_version_change(info):
    if info == 'info':
        print(__app_name__+' - Version '+__version__)
    if info == 'change':
        print(__app_name__+' - Version '+__version__)
        print('Change log:')
        for x in change_log:
            print(x)
    exit()

#argument parser
def arg_parser():
    parser = argparse.ArgumentParser(description='Parameters to run program')
    parser.add_argument('-f','--file',help='Defines single file to process', nargs='+')
    parser.add_argument('-d','--directory',help='Defines directory to process', nargs='+')
    parser.add_argument('-m','--mapping',help='Defines what mapping should be used [sw/hw]', nargs='+')
    parser.add_argument('-v','--version',help='Prints version and change log [info/change]', nargs='+')
    args = vars(parser.parse_args())

    file_cmd = args['file']

    dir_cmd = args['directory']
    folder_cmd = args['directory']
    mapping_cmd = args['mapping']
    version_cmd = args['version']
    if version_cmd is None:
        if file_cmd != None:
            path = args['file']
            target_file = path[0]
            mapping = mapping_cmd
            return 'file', target_file, mapping
        else:
            path = args['directory']
            target_dir = path[0]
            mapping = mapping_cmd
            return 'dir', target_dir, mapping
    else:
        if version_cmd[0] == 'info' or version_cmd[0] == 'change':
            print_version_change(version_cmd[0])

#mapping parser
def get_mapping():
    def create_dict(map_file):
        unit = ""
        component = ""
        mapping_dict = {}
        for line in map_file:
            # print(component)
            # print(unit)
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
    #create sw mapping
    sw_mapping = file_handling('open', 'sw_mapping.ini', False)
    sw_mapping = sw_mapping.read()
    sw_mapping = sw_mapping.splitlines()
    sw_mapping_dic = create_dict(sw_mapping)
    #create hw mapping
    hw_mapping = file_handling('open', 'hw_mapping.ini', False)
    hw_mapping = hw_mapping.read()
    hw_mapping = hw_mapping.splitlines()
    hw_mapping_dic = create_dict(hw_mapping)

    return sw_mapping_dic, hw_mapping_dic

if __name__ == '__main__':
    os.system('color')
    #csv_to_process = 'sample_version_inf_modded_v5.csv'
    to_process = arg_parser()
    #print(to_process)
    print(f'{cgreen}######## {__app_name__} - {__version__} ########{cend}')
    file_name = to_process[1]
    file = to_process[0]
    mapping = None
    csv_files = None
    if to_process[2] is None:
        mapping = mapping
        check_file_or_folder_exists('sw_mapping.ini', 'file')
        check_file_or_folder_exists('hw_mapping.ini', 'file')
        csv_files = check_file_or_folder_exists(file_name, '')
        #csv_files = check_file_or_folder_exists(file, 'folder')
        #file_name = check_file_type(file_name)
    if mapping == 'sw':
        check_file_or_folder_exists('sw_mapping.ini', 'file')
        if file == 'file':
            file_name = check_file_type(file_name)
            check_file_or_folder_exists(file_name, 'file')
        elif to_process[0] == 'dir':
            csv_files = check_file_or_folder_exists(file_name, 'folder')
    elif mapping == 'hw':
        check_file_or_folder_exists('hw_mapping.ini', 'file')
        if file == 'file':
            check_file_or_folder_exists(file_name, 'file')
            file_name = check_file_type(to_process[1])
        elif file == 'dir':
            csv_files = check_file_or_folder_exists(file, 'folder')
    create_asset_json(file,file_name,mapping, csv_files) # args: ['file' / 'dir'], [path], [mapping], [csv files]


