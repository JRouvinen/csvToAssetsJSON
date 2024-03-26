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

The converter script takes the following command-line arguments:

-   `-d --directory`: The path to the directory containing the *.csv files to be converted.
-   `-v --version`: Prints version and change log [info/change].

The converter script will create a new JSON file for each CSV file specified in the mapping file. Or if folder is given in the arguments script will create one JSON file from all CSV files in the folder.
The JSON file will contain an array of JSON objects, where each object corresponds to a row in the CSV file, grouped by the mapping INI files.

### Project structure
``` python
-> main folder
            |
            csvToAssetCsv_vX.Y.py
            csvToAssetCsv_Readme.md
            csvToJSON_Readme.md
            LICENSE
            |__main
            |       |__file_handler.py
            |       |__mapping.py
            |       |__progress_bar.py
            |       |__util_tools.py
            |__mapping
            |         |__csv_mapping.ini
            |__output #in this folder you will find the generated json files
            |__images #images for README file              
```

### Usage

To use the converter script, run the following command:

``` python
python csvToAssetCsv_vX.Y.py -d <folder path>
```
The skript tries to convert each *.csv file that has 'srv', 'software' or 'license' in its name into Asset compatible csv file.
Each file is written into output-folder under current day path


