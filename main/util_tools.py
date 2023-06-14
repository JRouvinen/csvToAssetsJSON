############################# Description ################################
# This script is created for FINLION FMN project.                        #
# This script is part of csvToJSON.py.                                   #
#                                                                        #
# Author: Rouvinen Juha-Matti, Insta Advance                             #
# Date: 10/04/2023                                                       #
# Updated: 24/05/2023                                                    #
############################# License ####################################
#       Copyright [2023] [Insta Advance, Juha-Matti Rouvinen]            #
#                                                                        #
#   Licensed under the Apache License, Version 2.0 (the "License");      #
#   you may not use this file except in compliance with the License.     #
#   You may obtain a copy of the License at                              #
#                                                                        #
#       http://www.apache.org/licenses/LICENSE-2.0                       #
##########################################################################

#imports
from datetime import datetime
import os
#file type check
def check_file_type(file):
    end = file[-4:]
    if end != '.csv':
        file = file+'.csv'
    return file

#string cleaning
def clean_srt(string):
    cleaned_str = string.strip()
    cleaned_str = cleaned_str.replace('"', '')
    cleaned_str = cleaned_str.replace('\n', '')
    cleaned_str = cleaned_str.replace('\\', '')

    return cleaned_str

# Returns time/date
def get_date_time(type):
    now = datetime.now()  # current date and time
    time = now.strftime("%H:%M:%S")
    date = now.date()
    if type == 'time':
        return time
    elif type == 'date':
        return date

# check if file exists
def check_file_or_folder_exists(file,type):
    is_file = False
    is_folder = False

    if type == 'file':
        is_file = os.path.isfile(file)
        if is_file is False:
            if file.endswith('.csv'):
                is_file = os.path.isfile(file)
                if is_file is False:
                    directory = os.getcwd()
                    directory = directory.replace('\\', '/')
                    folder_dir = directory + file
                    is_file = os.path.isfile(folder_dir)

            else:
                csv_file = file+'.csv'
                is_file = os.path.isfile(csv_file)
                if is_file is False:
                    directory = os.getcwd()
                    directory = directory.replace('\\', '/')
                    folder_dir = directory + file
                    is_file = os.path.isfile(folder_dir)

            if is_file is True:
                return 1
            if is_file is False:
                return 0
    else:
        if is_folder is False:
            directory = os.getcwd()
            directory = directory.replace('\\', '/')
            folder_dir = directory + file
            is_folder = os.path.exists(folder_dir)

        if is_folder is False and is_file is False:
            return 0

        elif is_folder is True:
            csv_files = 0
            for fname in os.listdir(folder_dir):
                if fname.endswith('.csv'):
                    csv_files += 1
            else:
                pass

            return csv_files


