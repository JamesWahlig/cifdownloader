import download_cif as dc
import sys
import subprocess

def ordering_to_float(ordering: str) -> float:
    if(ordering == "Unknown"): return None
    val = 1
    if(ordering == "NM"): val = 0
    return val

warnings.filterwarnings(UserWarning)
dc.download_cifs(sys.argv[2:], sys.argv[1], "ordering", ordering_to_float)