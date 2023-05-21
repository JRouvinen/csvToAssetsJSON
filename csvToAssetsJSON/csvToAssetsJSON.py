import os

#variables
opened_files = []

def check_if_file_is_there(file):
    # check file
    is_file = os.path.isfile(file)
    print(f'[#] File found: {is_file}')
    if is_file is False:
        print(f'[!] File not found in ({file})! -> stopping')
        exit()

def count_all_lines(file):
    lines = 0
    for line in file:
        lines += 1
    return lines

def create_asset_json(file):
    csv_file = file_handling('open', file)
    csv_file = csv_file.read()
    file_name_short = file[:-4]
    asset_json_dict = {file_name_short: []}
    component = None
    component_list = []
    component_dict = None
    lines_processed = 0
    print(f'[#] Creating JSON from CSV')
    csv_file_list = csv_file.splitlines()
    lines = len(csv_file_list)
    print(f'Lines: {lines}')
    for line in csv_file_list:
        if lines_processed == 0:
            pass
        else:
            unit = ''
            ver = ''
            #needs also support for ; separator
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
            print(component_dict)
            
        lines_processed = lines_processed+1
        if lines_processed == lines:
            asset_json_dict[file_name_short].append(component_dict)
            


    file_handling('close', csv_file)
    asset_json_dict_to_write = str(asset_json_dict)
    asset_json_dict_to_write = asset_json_dict_to_write.replace("'", '"')
    file_handling('write', file_name_short, asset_json_dict_to_write)



def file_handling(*args): #open, filename | write, filename,text | close, filename
    if len(args) == 2:
        operation = args[0]
        type = args[1]
    else:
        operation = args[0]
        type = args[1]
        text = args[2]

    if operation == 'open':
        print(f'[#] Opening file: {type}')
        f = open(type, 'r')
        opened_files.append(f)
        return f

    if operation == 'write':

        new_file_name = type + '.json'
        new_file = open(new_file_name, 'w')
        print(f'[->] Writing file: {new_file_name}')
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

if __name__ == '__main__':
    version = '0.21'
    #csv_to_process = 'sample_version_inf_modded_v5.csv'
    print(f'##### CSV to JIRA Asset JSON - {version} #####')
    csv_to_process = input('[<-] Give CSV filename: ')
    file_name = check_file_type(csv_to_process)
    check_if_file_is_there(file_name)
    create_asset_json(file_name)


