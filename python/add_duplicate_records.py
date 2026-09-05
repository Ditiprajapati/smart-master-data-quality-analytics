import pandas as pd
import random
from pathlib import Path

# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"

random.seed(42)

# ---------------------------------------------------------
# LOAD EXISTING RAW DATA
# ---------------------------------------------------------

suppliers = pd.read_csv(
    RAW_FOLDER / "suppliers_raw.csv"
)

materials = pd.read_csv(
    RAW_FOLDER / "materials_raw.csv"
)

# ---------------------------------------------------------
# CREATE SUPPLIER DUPLICATES
# ---------------------------------------------------------

supplier_duplicates = []

selected_suppliers = random.sample(
    range(len(suppliers)),
    20
)

for index in selected_suppliers:

    original = suppliers.iloc[index].copy()

    duplicate = original.copy()

    # Give the duplicate a different ID
    old_id = original["supplier_id"]

    new_id = f"DUP{old_id[3:]}"

    duplicate["supplier_id"] = new_id

    # Introduce small formatting variations
    name = str(original["supplier_name"])

    duplicate["supplier_name"] = random.choice([
        name.upper(),
        name.lower(),
        name + " ",
        name.replace(" ", "  ")
    ])

    supplier_duplicates.append(duplicate)


supplier_duplicates_df = pd.DataFrame(
    supplier_duplicates
)

suppliers = pd.concat(
    [suppliers, supplier_duplicates_df],
    ignore_index=True
)

# ---------------------------------------------------------
# CREATE MATERIAL DUPLICATES
# ---------------------------------------------------------

material_duplicates = []

selected_materials = random.sample(
    range(len(materials)),
    30
)

for index in selected_materials:

    original = materials.iloc[index].copy()

    duplicate = original.copy()

    # Give duplicate a different ID
    old_id = original["material_id"]

    new_id = f"DUP{old_id[3:]}"

    duplicate["material_id"] = new_id

    # Introduce formatting variations
    name = str(original["material_name"])

    duplicate["material_name"] = random.choice([
        name.upper(),
        name.lower(),
        name + " ",
        name.replace(" ", "  ")
    ])

    material_duplicates.append(duplicate)


material_duplicates_df = pd.DataFrame(
    material_duplicates
)

materials = pd.concat(
    [materials, material_duplicates_df],
    ignore_index=True
)

# ---------------------------------------------------------
# SAVE UPDATED RAW DATA
# ---------------------------------------------------------

suppliers.to_csv(
    RAW_FOLDER / "suppliers_raw.csv",
    index=False
)

materials.to_csv(
    RAW_FOLDER / "materials_raw.csv",
    index=False
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print("=" * 60)
print("DUPLICATE RECORD INJECTION COMPLETED")
print("=" * 60)

print("Supplier duplicates added :", len(supplier_duplicates_df))
print("Material duplicates added :", len(material_duplicates_df))

print()
print("New supplier count :", len(suppliers))
print("New material count :", len(materials))

print()
print("Updated files:")
print("suppliers_raw.csv")
print("materials_raw.csv")

print("=" * 60)