import os
from main import util_tools

opened_files = []
#print colors
cred = '\033[91m'
cgreen = '\033[92m'
cyellow = '\033[93m'
cblue = '\033[94m'
cturq = '\033m[34m'
cend = '\033[0m'
chead = '\033[42m'

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
        #if to_print is True:
            #print(f'{(cyellow)}[<-] Reading file: {file}{(cend)}')
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
        date = str(util_tools.get_date_time('date'))
        date_dir = output_dir+date
        if not os.path.exists(date_dir):
            os.mkdir(date_dir)
        new_file_name = file + '.json'
        newfile_already_exists = True
        number = 0
        path = date_dir+'/'+new_file_name
        newfile_already_exists = os.path.isfile(path)
        while newfile_already_exists is True:
            newfile_already_exists = os.path.isfile(path)
            if newfile_already_exists is True:
                number += 1
            new_file_name = file+'_'+str(number)+'.json'
            path = date_dir + '/' + new_file_name
        #check_file_or_folder_exists(new_file_name, 'file')
        if number == 0:
            new_file_name = file + '.json'
        new_file = open(date_dir+'/'+new_file_name, 'w')
        print(f'{(cgreen)}[->] Writing file: {date_dir}/{new_file_name}{(cend)}')
        new_file.write(str(to_print))
        new_file.close()
    #close file
    if operation == 'close':
        file_to_close = opened_files[0]
        file_to_close.close()