## About
This project is a series of scripts to download materials data from the Materials Project into a format that can be fed into [CGCNN](https://github.com/txie-93/cgcnn). The download_cif.py file has two functions that can be used to either download individual files, or generate large datasets from a pre-download Materials Project Parquet file. 

## Dependencies
This script requires the following packages to be installed
- mp_api (Materials Project API)
- pyarrow
- pymatgen (Should come with Materials Project API)

## Usage
When download_cif is called from the terminal, it will download CIF files from the Materials Project database and output an id_prop.csv with dummy property data.
```shell
python download_cif.py output_path mp-1 mp-2 mp-3...
```

The function download_cif downloads CIF's from the Materials Project database and outputs them into the target directory with a corresponding id_prop.csv and atom_init.json file. A map can be provided to the function to convert non-numerical data into numerical data.

The function download_cif_parquet takes CIF files from a pre-download Materials Project parquet file that contains your target properties, which can be obtained using the Materials Project API. The function processes the database into CIF files with the according id_prop.csv and atom_init.json files in the output_directory. A map can be provided to the function to convert non-numerical data into numerical data.

## Examples
Examples of usage for these functions can be found in the two additional python files.

## Credits
The purpose of this script is primarily to convert data into a format usable by [CGCNN](https://github.com/txie-93/cgcnn), so credit for the format and usage goes to the authors of that project.