import os
import json
from dotenv import load_dotenv
from mp_api.client import MPRester
from tqdm import tqdm

# Load API key from .env
load_dotenv()
api_key = os.getenv("api_code")

# Fields to retrieve
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

# Initialize API client
all_materials = []

with MPRester(api_key) as mpr:
    print("Querying Materials Project...")

    # Use paginator generator
    results = mpr.materials.summary.search(
        fields=FIELDS,
        all_fields=False,  # only return selected fields
        chunk_size=500  # you can try 1000, but 500 is safer for rate limits
    )

    # Collect all results
    for mat in tqdm(results, desc="Collecting materials"):
        all_materials.append({
            "material_id": mat.material_id,
            "pretty_formula": mat.formula_pretty,
            "energy_above_hull": mat.energy_above_hull,
            "space_group": mat.symmetry.symbol if mat.symmetry else "—",
            "band_gap": mat.band_gap,
            "formation_energy_per_atom": mat.formation_energy_per_atom,
            "magnetic_ordering": "Magnetic" if mat.is_magnetic else "Non-magnetic",
            "total_magnetization": mat.total_magnetization,
            "experimentally_observed": False  # Placeholder
        })

# Save to JSON
output_path = os.path.join(os.path.dirname(__file__), "data", "api_result.json")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(all_materials, f, indent=4)

print(f"Saved {len(all_materials)} materials to {output_path}")
