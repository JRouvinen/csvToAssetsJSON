## CSV to JSON Converter vB01

The CSV to JSON converter is a Python script that converts CSV files into JSON files. It supports Python version 3.8 or newer.

### Requirements

-   Python >=3.8
-   Required Python modules:
    -   argparse
    -   os
    -   sys
    -  datetime

### Functionality

The converter script can convert CSV files into JSON files based on a mapping file that determines the data type of each CSV file. The mapping file specifies whether a CSV file contains hardware, software, or license data.

The mapping files are INI files that are automatically processed, they can be passed as an argument to the converter script. The mapping file specifies the following information for each data type:

- HW mapping: what units should be nested under component
- SW mapping: what units should be nested under component
- License mapping: what licenses should be nested under license

The converter script takes the following command-line arguments:

-   `-f, --file`: The path to single *.csv file to be converted.
-   `-d --directory`: The path to the directory containing the *.csv files to be converted.
-   `-m --mapping`: Defines used mapping type [empty].
-   `-v --version`: Prints version and change log [info/change].

The converter script will create a new JSON file for each CSV file specified in the mapping file. Or if folder is given in the arguments script will create one JSON file from all CSV files in the folder.
The JSON file will contain an array of JSON objects, where each object corresponds to a row in the CSV file, grouped by the mapping INI files.

### Project structure
``` python
-> main folder
            |
            csvToJSON_vX.XX.py
            Readme.md
            LICENSE
            |__main
            |       |__file_handler.py
            |       |__mapping.py
            |       |__procedss_file_b.py
            |       |__process_folder_b.py
            |       |__progress_bar.py
            |       |__util_tools.py
            |__mapping
            |         |__hw_mapping.ini
            |         |__sw_mapping.ini
            |         |__license_mapping.ini
            |__output #in this folder you will find the generated json files
            |__images #images for README file              
```

### Usage

To use the converter script, run the following command:

``` python
python csvToJSON.py -f <single_file_path> 
#or
python csvToJSON.py -d <folder_path> 
#or to create empty object schema
python csvToJSON.py -d <folder_path> -m empty 
```

### Example

Suppose we have the following CSV file `hw_version_info.csv`:
``` csv
Component,Name,Data,  
ext-srv-esxi;BIOS version;U32  
ext-srv-esxi;Enclosure SN;CZJ906029B  
ext-srv-esxi;Product Name;ProLiant DL360 Gen10  
firewall1;Forcepoint NGFW;6.10.11  
firewall1;Product name;1101-0-C1  
firewall1;Serial number;N0C2902071
```

To convert the CSV file located in the directory `/path/to/csv` into JSON file we would run the following command:

``` python
python csvToJSON.py -f /path/to/csv/hw_version_info.csv 
```

This would create single JSON files in the `/output/<date>/` directory: `hw_version_info.json`. JSON file would contain an array of JSON objects, where each object corresponds to a row in the corresponding CSV file specified in the mapping file.

------------------------------------------------------------------------
## File structure

### Processed files
This script can only process '.csv' files into JIRA Asset JSON.
The '.csv' - files should have following inner structrure:

| File    | Structure                                                                  |
| ------- | -------------------------------------------------------------------------- |
| License | First line: 'Name','exp-date', data from second line on                    |
| SW file | First line: 'Component', 'Name', 'Version', data lines from second line on |
| HW file | First line: 'Component', 'Name', 'Data', data lines from second line on |

### Mapping files

#### HW mapping

hw_mapping.ini structure:
```
[SVR1]  
Unit = ext-srv-esxi
[SVR2]  
Unit = int-srv2-esxi
```

Each mapped component should be its own header (marked with brackets [header]) and sub-units market with 'Unit' tag and name 

#### SW mapping

sw_mapping.ini structure:
```
[Pääkomponentit]  
Unit = dns-mgmt
[Palvelinohjelmistot-SRV1]  
Unit = internal-dns-ns  
Unit = internal-geo
```

Each mapped component should be its own header (marked with brackets [header]) and sub-units market with 'Unit' tag and name 

#### License mapping

license_mapping.ini structure:
```
[Lisenssit]  
Unit = CFBLNET-PINK  
Unit = CFBLNET-BLUE
```

All mapped licenses should be nested under single [header] and marked with 'Unit' tag

## Components

![csvToJSON_v0411.png](images%2FcsvToJSON_v0411.png)

## CSV to JSON Converter vC01

## CSV to CSV Converter v1.3
