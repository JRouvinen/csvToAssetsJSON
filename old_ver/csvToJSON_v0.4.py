# --------Description--------
# This script is created for FINLION FMN project.
# Aim of this script is to convert csv files into JIRA Asset JSON format files
# Author: Rouvinen Juha-Matti, Insta Advance
# Date: 10/04/2023
# Updated: 25/04/2023
# ---------------------------
# Notes
#
#
#
#
#
#
# ---------------------------
# imports
import os
import argparse

import main.mapping
from main import util_tools, process_file, process_folder

# common variables
opened_files = []
__app_name__ = "CSV to JIRA Asset JSON"
__version__ = "0.4"
# change log
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
    '0.31 ->  Bug fixes: Color formatting doesnt work properly in wind cmd / '
    'powershell,file creation loop fixed  #21/04/2023',
    '0.32 ->  Bug fixes: File writer wont append name correctly '
    '| Simplify JSON structure | Mapping file for lisences | move mapping files into mapping folder #25/04/2023',
    '0.321->  Refactored License JSON structure -> all licenses are under Licenses and not sub-components #25/04/2023',
    '0.4->  -- needs to be added -- #27/04/2023',

]

# print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cturq = '\033m[34m'
cend = '\033[0m'
chead = '\033[42m'
# print markers
markers_dict = {
    0: '[#]',
    1: '!',
    2: '[<-]',
    3: '[->]',
    4: '[!]',
    5: '[----------------------------------------------------]',
}


# create json from csv

def create_asset_json(*args):  # args: ['file' / 'dir'], [path], [mapping], [csv files]

    file_folder = args[0]
    path = args[1]
    mapping = args[2]
    csv_file = args[3]
    # process single file
    if file_folder == 'file':
        result = main.process_file.process_file(file_folder, path, mapping, csv_file)

    # process folder
    else:
        result = process_folder.process_folder(file_folder, path, mapping, csv_file)
    print(f'{cgreen}----------------------------------------------------{cend}')

    print(f'{cgreen}[#] {result}!{cend}')


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
    parser.add_argument('-f', '--file', help='Defines single file to process', nargs='+')
    parser.add_argument('-d', '--directory', help='Defines directory to process', nargs='+')
    parser.add_argument('-m', '--mapping', help='Defines what mapping should be used [sw/hw]',
                        nargs='+')  # depricated in version 0.32
    parser.add_argument('-v', '--version', help='Prints version and change log [info/change]', nargs='+')
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

if __name__ == '__main__':
    os.system('color')
    to_process = arg_parser()
    print(f'{cgreen}######## {__app_name__} - {__version__} ########{cend}')
    file_name = to_process[1]
    file = to_process[0]
    mapping = None
    csv_files = None
    mapping_files_missing = False
    user_input = None
    if to_process[2] is None:
        mapping = mapping
        print(f'{cyellow}[<-] Checking file (mapping/sw_mapping.ini) path...{cend}')
        check = util_tools.check_file_or_folder_exists('mapping/sw_mapping.ini', 'file')
        if check is True:
            print(f'{cgreen}[->] File found...{cend}')
        if check is False:
            print(f'{cred}[!] Mapping file not found!{cend}')
            mapping_files_missing = True
        print(f'{cyellow}[<-] Checking file (mapping/hw_mapping.ini) path...{cend}')
        check = util_tools.check_file_or_folder_exists('mapping/hw_mapping.ini', 'file')
        if check is True:
            print(f'{cgreen}[->] File found...{cend}')
        if check is False:
            print(f'{cred}[!] Mapping file not found!{cend}')
            mapping_files_missing = True
        print(f'{cyellow}[<-] Checking file (mapping/license_mapping.ini) path...{cend}')
        check = util_tools.check_file_or_folder_exists('mapping/license_mapping.ini', 'file')
        if check is True:
            print(f'{cgreen}[->] File found...{cend}')
        if check is False:
            print(f'{cred}[!] Mapping file not found!{cend}')
            mapping_files_missing = True
        if mapping_files_missing is True:
            print(f'{cyellow}[#] Some of the mapping files are missing -> do you want to continue? (y/n){(cend)}')
            user_input = input(f'{cturq}Continue? {cend}')
        if user_input == 'n':
            exit()
        print(f'{cyellow}[<-] Checking file/folder path...{cend}')
        csv_files = util_tools.check_file_or_folder_exists(file_name, file)
        if csv_files == 0:
            print(f'{cred}[!] No files *.csv found from folder!{cend}')
            exit()
        else:
            print(f'{cgreen}[->] {csv_files} file(s) found from folder.{cend}')
# ---- This part is redundant old code and should be removed -----
    if mapping == 'sw':
        util_tools.check_file_or_folder_exists('mapping/sw_mapping.ini', 'file')
        if file == 'file':
            file_name = util_tools.check_file_type(file_name)
            util_tools.check_file_or_folder_exists(file_name, 'file')
        elif to_process[0] == 'dir':
            csv_files = util_tools.check_file_or_folder_exists(file_name, 'folder')
    elif mapping == 'hw':
        util_tools.check_file_or_folder_exists('mapping/hw_mapping.ini', 'file')
        if file == 'file':
            util_tools.check_file_or_folder_exists(file_name, 'file')
            file_name = util_tools.check_file_type(to_process[1])
        elif file == 'dir':
            csv_files = util_tools.check_file_or_folder_exists(file, 'folder')
# ---- This part is redundant old code and should be removed -----
    create_asset_json(file, file_name, mapping, csv_files)  # args: ['file' / 'dir'], [path], [mapping], [csv files]
