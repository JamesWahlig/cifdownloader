import os
from typing import Callable
from dotenv import load_dotenv
import sys
from mp_api.client import MPRester
import requests
import warnings
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pymatgen.core as pmc
import pymatgen.io as pmio

load_dotenv()

def main():
    download_cifs(sys.argv[3:], sys.argv[1], "material_id", property_transform=map_to_0)

def default_transform(input: str) -> float: 
    return float(input)

def map_to_0(input: str) -> float:
    return 0

def download_cifs(mp_ids: list[str], path: str, target_property: str, property_transform: Callable[[str], float]=default_transform, mp_api_key=os.getenv("MP_API")
):
    atom_resp = requests.get("https://raw.githubusercontent.com/txie-93/cgcnn/refs/heads/master/data/sample-regression/atom_init.json")
    if atom_resp.status_code != 200:
        warnings.warn("Failed to download atom_init file")
    else:
        with open(path + "/" + "atom_init.json", "wb") as file:
            file.write(atom_resp.content)
    with open(path + "/" + "id_prop.csv", "w") as file:
        file.write("")
    with MPRester(api_key=mp_api_key) as mpr:
        data_blocks = mpr.materials.summary.search(material_ids=mp_ids, fields=["material_id", "structure", target_property])
        for data in data_blocks:
            prop = data[target_property]
            value = property_transform(prop)
            if(value is None): continue
            with open(path + "/" + data.material_id + ".cif", "w") as file:
                file.write(data.structure.to(fmt="cif"))
            with open(path + "/" + "id_prop.csv", "a") as file:
                file.write(data.material_id + "," + str(value) + "\n")

def cifs_from_parquet(database_dir: str, output_dir: str, target_property: str, property_transform: Callable[[str], float]=default_transform):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    atom_resp = requests.get("https://raw.githubusercontent.com/txie-93/cgcnn/refs/heads/master/data/sample-regression/atom_init.json")
    if atom_resp.status_code != 200:
        warnings.warn("Failed to download atom_init file")
    else:
        with open(output_dir + "/" + "atom_init.json", "wb") as file:
            file.write(atom_resp.content)
    with open(output_dir + "/id_prop.csv", "w") as file:
        file.write("")
    id_props = open(output_dir + "/id_prop.csv", "a")
    materials_dataset = ds.dataset(database_dir)
    i = 0
    for chunk in materials_dataset.to_batches():
        dict = chunk.to_pydict()
        for material_id, structure, prop in zip(dict['material_id'], dict['structure'], dict[target_property]):
            value = property_transform(prop)
            if value is None: continue
            structure_cif = pmc.IStructure.from_dict(structure).to(fmt="cif")
            with open(output_dir + "/" + material_id + ".cif", "w") as file:
                file.write(structure_cif)
                file.close()
            id_props.write(material_id + "," + str(value) + "\n")
            print("Processed " + str(i) + " CIF files", end='\r')
            i += 1
    id_props.close()
    print("Processed " + str(i) + " CIF files")


if(__name__ == "__main__"):
    main()