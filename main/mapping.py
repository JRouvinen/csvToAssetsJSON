
from main import file_handler

#mapping parser
def get_mapping(type, folder):
    if type == 'vm':
        vm_file = file_handler.file_handling('open', folder + '/' + 'vm_inventory.csv', True)
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

    else:
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
        #create sw mapping
        sw_mapping = file_handler.file_handling('open', '/mapping/sw_mapping.ini', False)
        sw_mapping = sw_mapping.read()
        sw_mapping = sw_mapping.splitlines()
        sw_mapping_dic = create_dict(sw_mapping)
        #create hw mapping
        hw_mapping = file_handler.file_handling('open', '/mapping/hw_mapping.ini', False)
        hw_mapping = hw_mapping.read()
        hw_mapping = hw_mapping.splitlines()
        hw_mapping_dic = create_dict(hw_mapping)
        # create license mapping
        lic_mapping = file_handler.file_handling('open', '/mapping/license_mapping.ini', False)
        lic_mapping = lic_mapping.read()
        lic_mapping = lic_mapping.splitlines()
        lic_mapping_dic = create_dict(lic_mapping)
        return sw_mapping_dic, hw_mapping_dic, lic_mapping_dic