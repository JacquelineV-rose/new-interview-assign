import os
import json
from dotenv import load_dotenv
from mp_api.client import MPRester

load_dotenv()

FIELDS = [
    "material_id", 
    "formula_pretty", 
    "energy_above_hull", 
    "band_gap", 
    "formation_energy_per_atom",  
    "total_magnetization",
    "is_stable",
    "is_magnetic",
    "ordering",
    "symmetry"
]

with MPRester(os.getenv("api_code")) as mpr:
    docs_data = mpr.materials.summary.search(fields=FIELDS, num_chunks=1, chunk_size=100)


docs = []

for d in docs_data:
    doc = {
        "material_id": d.material_id,
        "pretty_formula": d.formula_pretty,
        "energy_above_hull": d.energy_above_hull,
        "band_gap": d.band_gap,
        "formation_energy_per_atom": d.formation_energy_per_atom,
        "total_magnetization": d.total_magnetization,
        "is_stable": d.is_stable,
        "is_magnetic": d.is_magnetic,
        "magnetic_ordering": getattr(d, "ordering", "~~"),
        #Space group?
        "symmetry": d.symmetry.symbol if d.symmetry else "—"


    }
    docs.append(doc)

with open("materials_data.json", "w") as f:
    json.dump(docs, f, indent=4)

print(f"Retrieved {len(docs)} documents and saved to 'materials_data.json'.")