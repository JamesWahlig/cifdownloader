import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pymatgen.core as pmc
import pymatgen.io as pmio

import sys
import os

data_dir = "./training_data"
        

if not os.path.exists(data_dir):
    os.mkdir(data_dir)
with open(data_dir + "/id_prop.csv", "w") as file:
    file.write("")
id_props = open(data_dir + "/id_prop.csv", "a")
target_property = "ordering"
materials_dataset = ds.dataset(sys.argv[1])
i = 0
for chunk in materials_dataset.to_batches():
    dict = chunk.to_pydict()
    for material_id, structure, prop in zip(dict['material_id'], dict['structure'], dict[target_property]):
        if(str(prop) == "Unknown" or prop is None): continue
        value = 1
        if(str(prop) == "NM"): value = 0

        structure_cif = pmc.IStructure.from_dict(structure).to(fmt="cif")
        with open(data_dir + "/" + material_id + ".cif", "w") as file:
            file.write(structure_cif)
            file.close()
        id_props.write(material_id + "," + str(value) + "\n")
        print("Processed " + str(i) + " CIF files", end='\r')
        i += 1
id_props.close()
print("Processed " + str(i) + " CIF files")
        