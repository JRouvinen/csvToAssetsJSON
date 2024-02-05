############################# Description ################################
# This script is created for FINLION FMN project.                        #
# This script is to converts csv files into JIRA Asset CSV format files #
#                                                                        #
# Author: Rouvinen Juha-Matti, Insta Advance                             #
# Date: 10/04/2023                                                       #
# Updated: 29/01/2024                                                    #
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
import os
import argparse
import main.mapping
from main import util_tools, process_file_b, process_folder_b, process_folder_c, file_handler
from datetime import datetime

# common variables
opened_files = []
__app_name__ = "CSV to JIRA Asset CSV Converter"
__version__ = "1.3"
# change log
change_log = [
    '1.0: Initial version',
    '1.1: Updated server and component parsing',
    '1.2: Updated project connector creation',
    '1.3: Updated import key creation and name parsing',
]

# print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cturq = '\033m[34m'
cend = '\033[0m'
chead = '\033[42m'


# create json from csv
def create_asset_csv(file, file_name, csv_files, name_check,
                     ver):  # args: ['file' / 'dir'], [path], [mapping], [csv files], [env name], [version]

    file_folder = file
    path = file_name[0]
    directory = os.getcwd()
    directory = directory.replace('\\', '/')
    file = str(path)
    path = directory + '/' + file
    files_in_folder = os.listdir(path)
    csv_file = csv_files
    env_name = name_check
    ver = ver
    # Get header data from csv_mapping file
    mapping = main.mapping.get_csv_mapping()
    now = datetime.now()
    file_process_id = str(datetime.timestamp(now)) + '_' + env_name
    file_process_id = file_process_id.split('.')[0]
    processed_files = []
    for fil_name in files_in_folder:
        if fil_name.endswith('.csv'):
            skipping = False
            header_type = None
            csv_file = fil_name
            csv_file = file_handler.file_handling('open', file_name[0] + '/' + fil_name, False)
            csv_file_lines = csv_file.read()
            csv_file_lines = csv_file_lines.splitlines()
            file_name_check_srv = fil_name.find('srv')
            file_name_check_software = fil_name.find('software')
            file_name_check_license = fil_name.find('license')

            if file_name_check_srv != -1:
                header_type = 'srv'
            elif file_name_check_software != -1:
                header_type = 'software'
            elif file_name_check_license != -1:
                header_type = 'license'
            else:
                print(f'{cyellow}[WARNING] No suitable file name (srv, software, license) found --> skipping file {cend}')
                skipping = True
                continue
            if skipping is False:
                try:
                    file_header = mapping[header_type]
                except KeyError:
                    header_type = header_type.capitalize()
                    file_header = mapping[header_type]
                # Write csv file
                csv_file_path = "path/to/csv_file.csv"
                # Create file header
                file_header = file_header.replace('[', '').replace(']', '')
                file_header = file_header.split(',')
                file_header_str = ';'.join(file_header).strip(' ')

                # check if output folder exists and create it if not
                directory = os.getcwd()
                directory = directory.replace('\\', '/')
                output_dir = directory + '/output/'
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                # check if current date folder exists in output folder and create it if not
                date = str(util_tools.get_date_time('date'))
                date_dir = output_dir + date
                if not os.path.exists(date_dir):
                    os.mkdir(date_dir)
                #new_file_name = fil_name.split('.')[0] + '_jira_assets' + '.csv'
                new_file_name = fil_name.replace('.csv', '') + '_jira_assets' + '.csv'
                #newfile_already_exists = True
                # Define server and component names
                new_file_name_list = new_file_name.split('_')
                server_name = new_file_name_list[2]
                component_name = new_file_name_list[3]
                # Create import keys
                #import_key_header = file_process_id + '_' + server_name
                number = 0
                path = date_dir + '/' + new_file_name
                newfile_already_exists = os.path.isfile(path)
                while newfile_already_exists is True:
                    newfile_already_exists = os.path.isfile(path)
                    if newfile_already_exists is True:
                        number += 1
                    #new_file_name = fil_name.split('.')[0] + '_jira_assets' + '_' + str(number) + '.csv'
                    new_file_name = fil_name.replace('.csv', '') + '_jira_assets' + '_' + str(number) + '.csv'
                    path = date_dir + '/' + new_file_name
                if number == 0:
                    #new_file_name = fil_name.split('.')[0] + '_jira_assets' + '.csv'
                    new_file_name = fil_name.replace('.csv', '') + '_jira_assets' + '.csv'
                new_file = open(date_dir + '/' + new_file_name, 'w')
                print(f'{(cgreen)}[->] Writing file: {date_dir}/{new_file_name}{(cend)}')
                new_file.write(str(file_header_str) + '\n')
                line_index = 0
                if len(processed_files) == 0:
                    import_key_header = file_process_id + '_' + server_name
                    line_to_write_list = [import_key_header + '_' + "Project_connector"]
                    line_to_write_list.append("Jira")
                    line_to_write_list.append("Assets")
                    line_to_write_list.append("Project_connector")
                    line_to_write_list.append(__version__)
                    line_to_write = ';'.join(line_to_write_list)
                    new_file.write(str(line_to_write) + '\n')
                for x in csv_file_lines:
                    if x != '':
                        line_index += 1
                        line_parts = x.split(';')
                        line_to_write_list = []
                        import_key_header = file_process_id + '_' + str(line_index) + '_' + server_name
                        line_to_write_list.append(import_key_header)
                        line_to_write_list.append(component_name)
                        line_to_write_list = line_to_write_list + line_parts
                        if len(file_header) - len(line_to_write_list) > 0:
                            for i in range(0, len(file_header) - (len(line_to_write_list))):
                                line_to_write_list.append('')
                        line_to_write = ';'.join(line_to_write_list)
                        new_file.write(str(line_to_write) + '\n')
                new_file.close()
                processed_files.append(fil_name)

            else:
                pass

    # print(f'{cgreen}----------------------------------------------------{cend}')
    # print(f'{cgreen}[#] {result}!{cend}')


# print version and change info
def print_version_change(info):
    if info == 'info':
        print(__app_name__ + ' - Version ' + __version__)
    if info == 'change':
        print(__app_name__ + ' - Version ' + __version__)
        print('Change log:')
        for x in change_log:
            print(x)
    exit()


# argument parser
def arg_parser():
    parser = argparse.ArgumentParser(description='Parameters to run program')
    parser.add_argument('-d', '--directory', help='Defines directory to process', nargs='+')
    parser.add_argument('-v', '--version', help='Prints version and change log [info/change]', nargs='+')
    args = vars(parser.parse_args())
    folder_cmd = args['directory']
    version_cmd = args['version']
    if version_cmd is None:
        return 'dir', folder_cmd
    else:
        if version_cmd[0] == 'info' or version_cmd[0] == 'change':
            print_version_change(version_cmd[0])


if __name__ == '__main__':
    os.system('color')
    to_process = arg_parser()
    print(f'{cgreen}######## {__app_name__} - {__version__} ########{cend}')
    file_name = to_process[1]
    file = to_process[0]
    csv_files = None
    mapping_files_missing = False
    user_input = None
    ver = __version__
    print(f'{cyellow}[<-] Checking file (csv_mapping.ini) path...{cend}')
    check = util_tools.check_file_or_folder_exists('csv_mapping.ini', 'file')
    if check is True:
        print(f'{cgreen}[->] File found...{cend}')
    if check is False:
        print(f'{cred}[!] Mapping file not found!{cend}')
        mapping_files_missing = True
    print(f'{cyellow}[<-] Checking file/folder path...{cend}')
    csv_files = util_tools.check_file_or_folder_exists(file_name[0], file)
    if csv_files == 0:
        print(f'{cred}[!] No files *.csv found from folder!{cend}')
        exit()
    else:
        print(f'{cgreen}[->] {csv_files} file(s) found from folder.{cend}')
        name_check = util_tools.file_names(file_name[0])
        if name_check[0]:
            print(f"{cyellow} [#] All filenames in folder don't match! {cend}")
            #name_check[1] = ""
        else:
            print(f'{cgreen}[->] {csv_files} filenames in folder match to *.csv {cend}')
    create_asset_csv(file, file_name, csv_files, name_check[1],
                     ver)  # args: ['file' / 'dir'], [path], [mapping], [csv files], [env name]
