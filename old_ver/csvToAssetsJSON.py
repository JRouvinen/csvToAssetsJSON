import os
import argparse
#Description
# This script is created to convert csv files into JIRA Asset JSON formats
# Author: Rouvinen Juha-Matti, Insta Advance
#
#change log
# 0.22 -> first working version
# 0.23 -> argparser and added print colors #12/04/2023
# 0.24 -> configparser support #12/04/2023
#
#
#
#
#
#variables
opened_files = []
__app_name__ = "CSV to JIRA Asset JSON"
__version__ = "0.24"

#print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cend = '\033[0m'
chead = '\033[44m'


def check_if_file_is_there(file):
    # check file
    print(f'{(cblue)}[#] Checking file path{(cend)}')
    is_file = os.path.isfile(file)
    print(f'{(cgreen)}[#] File found: {is_file}{(cend)}')
    if is_file is False:
        print(f'{(cred)}[!] File ({file}) not found! -> stopping program{(cend)}')
        exit()

#check if folder is there
def check_if_folder_is_there(folder):
    print(f'{(cblue)}[#] Checking folder path{(cend)}')
    is_folder = os.path.exists(folder)
    if is_folder is False:
        print(f'{(cred)}[!] Folder ({file}) not found! -> stopping program{(cend)}')
        exit()
    print(f'{(cgreen)}[#] Folder found: {is_folder}{(cend)}')
    print(f'{(cblue)}[#] Checking files inside the folder{(cend)}')
    csv_files = 0
    for fname in os.listdir(folder):
        if fname.endswith('.csv'):
            csv_files += 1
            
    else:
        pass
    
    if csv_files == 0:
        print(f'{(cred)}[!] No CSV files found inside the folder{(cend)}')
        exit()    
    else:
        print(f'{(cgreen)}[#] {csv_files} files found in the folder{(cend)}')

    #count lines in file
def count_all_lines(file):
    lines = 0
    for line in file:
        lines += 1
    return lines

    #create json from csv
def create_asset_json(*args): # args: ['file' / 'dir'], [path]
    file_folder = args[0]
    if file_folder == 'file':
        file = args[1]
        #open file
        csv_file = file_handling('open', file)
        csv_file = csv_file.read()
        #get file name
        file_name_short = file[:-4]
        asset_json_dict = {file_name_short: []}
        component = None
        component_list = []
        component_dict = None
        lines_processed = 0
        print(f'{(cblue)}[#] Creating JSON from CSV{(cend)}')
        csv_file_list = csv_file.splitlines()
        lines = len(csv_file_list)
        print(f'{(cblue)}[#] Reading lines in file: {lines} lines found{(cend)}')
        #loop through lines
        for line in csv_file_list:
            if lines_processed == 0:
                pass
            else:
                percents = int(lines_processed/lines*100)
                if percents % 2 == 0:
                    percents = str(percents)
                    print(f'{(cblue)}[-] Creating JSON file - {percents}% done{(cend)}'+'\r', end='')
                else:
                    percents = str(percents)
                    print(f'{(cblue)}[|] Creating JSON file - {percents}% done{(cend)}'+'\r', end='')
                unit = ''
                ver = ''
                count_semicolon = line.count(';')
                if count_semicolon == 0:
                    concate = ','
                else:
                    concate = ';'
                #get component data
                component_loc = line.find(concate)
                component = line[:component_loc]
                component = clean_srt(component)
                component_on_list = component_list.count(component)
                #check if component is already created
                if component_on_list == 0:
                    if component_dict != None:
                        asset_json_dict[file_name_short].append(component_dict)
                    component_dict = None
                    component_list.append(component)
                    component_dict = {component: []}
                #get unit data
                unit_loc = line.rfind(concate)
                unit = line[component_loc+1:unit_loc]
                unit = clean_srt(unit)
                #get version data
                ver = line[unit_loc+1:]
                ver = clean_srt(ver)
                unit_dict = {'name':unit,'version':ver}
                #add unit data to component
                component_dict[component].append(unit_dict)
                #print(component_dict)
                
            lines_processed = lines_processed+1
            if lines_processed == lines:
                asset_json_dict[file_name_short].append(component_dict)
                

        #close file
        file_handling('close', csv_file)
        asset_json_dict_to_write = str(asset_json_dict)
        asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
        print('')
        #write file
        file_handling('write', file_name_short, asset_json_dict_to_write)

    else:
        folder = args[1]
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            if os.path.isfile(f):
                if filename.endswith('.csv'):
                    file = filename
                    #open file
                    csv_file = file_handling('open', file)
                    csv_file = csv_file.read()
                    #get file name
                    file_name_short = file[:-4]
                    asset_json_dict = {file_name_short: []}
                    component = None
                    component_list = []
                    component_dict = None
                    lines_processed = 0
                    print(f'{(cblue)}[#] Creating JSON from CSV{(cend)}')
                    csv_file_list = csv_file.splitlines()
                    lines = len(csv_file_list)
                    print(f'{(cblue)}[#] Reading lines in file: {lines} lines found{(cend)}')
                    #loop through lines
                    for line in csv_file_list:
                        if lines_processed == 0:
                            pass
                        else:
                            percents = int(lines_processed/lines*100)
                            if percents % 2 == 0:
                                percents = str(percents)
                                print(f'{(cblue)}[-] Creating JSON file - {percents}% done{(cend)}'+'\r', end='')
                            else:
                                percents = str(percents)
                                print(f'{(cblue)}[|] Creating JSON file - {percents}% done{(cend)}'+'\r', end='')                
                            unit = ''
                            ver = ''
                            count_semicolon = line.count(';')
                            if count_semicolon == 0:
                                concate = ','
                            else:
                                concate = ';'
                            #get component data
                            component_loc = line.find(concate)
                            component = line[:component_loc]
                            component = clean_srt(component)
                            component_on_list = component_list.count(component)
                            #check if component is already created
                            if component_on_list == 0:
                                if component_dict != None:
                                    asset_json_dict[file_name_short].append(component_dict)
                                component_dict = None
                                component_list.append(component)
                                component_dict = {component: []}
                            #get unit data
                            unit_loc = line.rfind(concate)
                            unit = line[component_loc+1:unit_loc]
                            unit = clean_srt(unit)
                            #get version data
                            ver = line[unit_loc+1:]
                            ver = clean_srt(ver)
                            unit_dict = {'name':unit,'version':ver}
                            #add unit data to component
                            component_dict[component].append(unit_dict)
                            #print(component_dict)
                            
                        lines_processed = lines_processed+1
                        if lines_processed == lines:
                            asset_json_dict[file_name_short].append(component_dict)
                            

                    #close file
                    file_handling('close', csv_file)
                    asset_json_dict_to_write = str(asset_json_dict)
                    asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
                    #write file
                    file_handling('write', file_name_short, asset_json_dict_to_write)
    
    print(f'{(cgreen)}[#] Done!{(cend)}')
    

def file_handling(*args): #open, filename | write, filename,text | close, filename
    if len(args) == 2:
        operation = args[0]
        type = args[1]
    else:
        operation = args[0]
        type = args[1]
        text = args[2]

    if operation == 'open':
        print(f'{(cblue)}[#] Opening file: {type}{(cend)}')
        f = open(type, 'r')
        opened_files.append(f)
        return f

    if operation == 'write':
        directory = os.getcwd()
        output_dir = directory+'/output/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        new_file_name = type + '.json'
        new_file = open(output_dir+new_file_name, 'w')
        print(f'{(cblue)}[->] Writing file: {new_file_name}{(cend)}')
        new_file.write(str(text))
        new_file.close()

    if operation == 'close':
        file_to_close = opened_files[0]
        file_to_close.close()


def clean_srt(string):
    cleaned_str = string.strip()
    cleaned_str = cleaned_str.replace('"', '')
    cleaned_str = cleaned_str.replace('\n', '')
    return cleaned_str

def check_file_type(file):
    end = file[-4:]
    if end != '.csv':
        file = file+'.csv'
    return file

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to input .csv file")
    parser.add_argument("-d", "--dir", help="Path to input .csv directory")
    args = vars(parser.parse_args())
    if args['file'] != None:
        target_file = args['file']
        return 'file', target_file
    else:
        target_dir = args['dir']
        return 'dir', target_dir
    

if __name__ == '__main__':
    #version = '0.22'
    #csv_to_process = 'sample_version_inf_modded_v5.csv'
    print(f'{(chead)}##### {__app_name__} - {__version__} #####{(cend)}')
    to_process = arg_parser()
    #print(to_process[0])
    if to_process[0] == 'file':
        file_name = check_file_type(to_process[1])
        check_if_file_is_there(to_process[1])
    if to_process[0] == 'dir':
        check_if_folder_is_there(to_process[1])
    create_asset_json(to_process[0],to_process[1])


