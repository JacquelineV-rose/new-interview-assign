import os
import json
from dotenv import load_dotenv
from mp_api.client import MPRester
from tqdm import tqdm

load_dotenv()
api_key = os.getenv("api_code")

FIELDS = [
    "material_id",
    "formula_pretty",
    "energy_above_hull",
    "symmetry",
    "band_gap",
    "formation_energy_per_atom",
    "is_magnetic",
    "total_magnetization"
]

all_materials = []

with MPRester(api_key) as mpr:
    print("Getting materials...")

    results = mpr.materials.summary.search(
        fields=FIELDS,
        all_fields=False,
        chunk_size=500
    )

    for mat in tqdm(results, desc="Loading"):
        all_materials.append({
            "material_id": mat.material_id,
            "pretty_formula": mat.formula_pretty,
            "energy_above_hull": mat.energy_above_hull,
            "space_group": mat.symmetry.symbol if mat.symmetry else "-",
            "band_gap": mat.band_gap,
            "formation_energy_per_atom": mat.formation_energy_per_atom,
            "magnetic_ordering": "Magnetic" if mat.is_magnetic else "Non-magnetic",
            "total_magnetization": mat.total_magnetization,
            "experimentally_observed": False  # placeholder for now
        })

# Save to JSON
out_file = os.path.join("data", "api_result.json")
os.makedirs("data", exist_ok=True)

with open(out_file, "w") as f:
    json.dump(all_materials, f, indent=2)

print(f"Saved {len(all_materials)} materials to {out_file}")
