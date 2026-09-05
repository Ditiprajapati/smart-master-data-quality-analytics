import pandas as pd
from pathlib import Path
import re


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
CLEANED_FOLDER = PROJECT_ROOT / "data" / "cleaned"
REPORT_FOLDER = PROJECT_ROOT / "excel"

CLEANED_FOLDER.mkdir(parents=True, exist_ok=True)
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)


# =========================================================
# LOAD RAW DATA
# =========================================================

suppliers = pd.read_csv(
    RAW_FOLDER / "suppliers_raw.csv"
)

materials = pd.read_csv(
    RAW_FOLDER / "materials_raw.csv"
)

categories = pd.read_csv(
    RAW_FOLDER / "categories_raw.csv"
)

purchases = pd.read_csv(
    RAW_FOLDER / "purchases_raw.csv"
)


print("=" * 70)
print("MASTER DATA QUALITY ENGINE")
print("=" * 70)


# =========================================================
# 1. COMPLETENESS CHECK
# =========================================================

print("\n1. COMPLETENESS CHECK")
print("-" * 70)


def completeness_check(df, dataset_name):

    results = []

    for column in df.columns:

        missing = df[column].isna().sum()

        total = len(df)

        completeness = (
            (total - missing) / total
        ) * 100

        results.append({
            "dataset": dataset_name,
            "column": column,
            "total_records": total,
            "missing_records": missing,
            "completeness_percent": round(
                completeness, 2
            )
        })

    return pd.DataFrame(results)


supplier_completeness = completeness_check(
    suppliers,
    "Suppliers"
)

material_completeness = completeness_check(
    materials,
    "Materials"
)

purchase_completeness = completeness_check(
    purchases,
    "Purchases"
)


completeness_report = pd.concat([
    supplier_completeness,
    material_completeness,
    purchase_completeness
])


print(
    completeness_report.to_string(
        index=False
    )
)


# =========================================================
# 2. VALIDITY CHECK
# =========================================================

print("\n\n2. VALIDITY CHECK")
print("-" * 70)


# ---------------------------------------------------------
# Email validation
# ---------------------------------------------------------

email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

valid_email_mask = (
    suppliers["email"]
    .fillna("")
    .str.match(
        email_pattern
    )
)

invalid_emails = suppliers[
    ~valid_email_mask
]

print(
    "Invalid / missing emails:",
    len(invalid_emails)
)


# ---------------------------------------------------------
# Price validation
# ---------------------------------------------------------

invalid_prices = materials[
    materials["price"].isna()
    | (materials["price"] <= 0)
]

print(
    "Invalid / missing prices:",
    len(invalid_prices)
)


# ---------------------------------------------------------
# Quantity validation
# ---------------------------------------------------------

invalid_quantities = purchases[
    purchases["quantity"].isna()
    | (purchases["quantity"] <= 0)
]

print(
    "Invalid / missing quantities:",
    len(invalid_quantities)
)


# =========================================================
# 3. CONSISTENCY CHECK
# =========================================================

print("\n\n3. CONSISTENCY CHECK")
print("-" * 70)


# ---------------------------------------------------------
# Unit standardization mapping
# ---------------------------------------------------------

unit_mapping = {

    "kg": "KG",
    "Kg": "KG",
    "KG": "KG",
    "Kilogram": "KG",

    "l": "L",
    "L": "L",
    "Liter": "L",
    "litre": "L",
    "Litre": "L",

    "ton": "TON",
    "TON": "TON",
    "Tonne": "TON",
    "tonne": "TON",

    "box": "BOX",
    "Box": "BOX",
    "BOX": "BOX",

    "drum": "DRUM",
    "Drum": "DRUM",
    "DRUM": "DRUM"
}


materials["unit_standardized"] = (
    materials["unit"]
    .map(unit_mapping)
)


unit_inconsistencies = materials[
    materials["unit"].notna()
    & (
        materials["unit"]
        != materials["unit_standardized"]
    )
]

print(
    "Unit inconsistencies:",
    len(unit_inconsistencies)
)


# ---------------------------------------------------------
# Country standardization
# ---------------------------------------------------------

country_mapping = {

    # India
    "india": "India",
    "INDIA": "India",
    "India": "India",
    "India ": "India",

    # Germany
    "germany": "Germany",
    "GERMANY": "Germany",
    "Germany": "Germany",
    "Germany ": "Germany",

    # United States
    "USA": "United States",
    "US": "United States",
    "united states": "United States",
    "United States": "United States",

    # Singapore
    "singapore": "Singapore",
    "SINGAPORE": "Singapore",
    "Singapore": "Singapore",

    # Japan
    "japan": "Japan",
    "JAPAN": "Japan",
    "Japan": "Japan",

    # Other countries
    "Belgium": "Belgium",
    "belgium": "Belgium",

    "France": "France",
    "france": "France",

    "Netherlands": "Netherlands",
    "netherlands": "Netherlands",

    "Switzerland": "Switzerland",
    "switzerland": "Switzerland",

    "United Kingdom": "United Kingdom",
    "united kingdom": "United Kingdom"
}

suppliers["country_standardized"] = (
    suppliers["country"]
    .map(country_mapping)
)


country_inconsistencies = suppliers[
    suppliers["country"].notna()
    & (
        suppliers["country"]
        != suppliers["country_standardized"]
    )
]

print(
    "Country inconsistencies:",
    len(country_inconsistencies)
)


# =========================================================
# 4. UNIQUENESS CHECK
# =========================================================

print("\n\n4. UNIQUENESS CHECK")
print("-" * 70)


# ---------------------------------------------------------
# Normalize supplier names
# ---------------------------------------------------------

def normalize_name(value):

    if pd.isna(value):
        return ""

    value = str(value)

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9 ]",
        "",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


suppliers["normalized_name"] = (
    suppliers["supplier_name"]
    .apply(normalize_name)
)


materials["normalized_name"] = (
    materials["material_name"]
    .apply(normalize_name)
)


# ---------------------------------------------------------
# Potential duplicate suppliers
# ---------------------------------------------------------

duplicate_suppliers = suppliers[
    suppliers["normalized_name"].duplicated(
        keep=False
    )
].sort_values(
    "normalized_name"
)


print(
    "Potential duplicate suppliers:",
    len(duplicate_suppliers)
)


# ---------------------------------------------------------
# Potential duplicate materials
# ---------------------------------------------------------

duplicate_materials = materials[
    materials["normalized_name"].duplicated(
        keep=False
    )
].sort_values(
    "normalized_name"
)


print(
    "Potential duplicate materials:",
    len(duplicate_materials)
)


# =========================================================
# 5. REFERENTIAL INTEGRITY CHECK
# =========================================================

print("\n\n5. REFERENTIAL INTEGRITY CHECK")
print("-" * 70)


# ---------------------------------------------------------
# Material → Supplier
# ---------------------------------------------------------

invalid_material_suppliers = materials[
    ~materials["supplier_id"].isin(
        suppliers["supplier_id"]
    )
]


print(
    "Materials with invalid supplier IDs:",
    len(invalid_material_suppliers)
)


# ---------------------------------------------------------
# Material → Category
# ---------------------------------------------------------

invalid_material_categories = materials[
    materials["category_id"].notna()
    & ~materials["category_id"].isin(
        categories["category_id"]
    )
]


print(
    "Materials with invalid category IDs:",
    len(invalid_material_categories)
)


# ---------------------------------------------------------
# Purchase → Material
# ---------------------------------------------------------

invalid_purchase_materials = purchases[
    ~purchases["material_id"].isin(
        materials["material_id"]
    )
]


print(
    "Purchases with invalid material IDs:",
    len(invalid_purchase_materials)
)


# ---------------------------------------------------------
# Purchase → Supplier
# ---------------------------------------------------------

invalid_purchase_suppliers = purchases[
    ~purchases["supplier_id"].isin(
        suppliers["supplier_id"]
    )
]


print(
    "Purchases with invalid supplier IDs:",
    len(invalid_purchase_suppliers)
)


# =========================================================
# QUALITY SCORE
# =========================================================

print("\n\n6. DATA QUALITY SCORE")
print("-" * 70)


# ---------------------------------------------------------
# Completeness score
# ---------------------------------------------------------

total_cells = 0
missing_cells = 0

for df in [
    suppliers,
    materials,
    purchases
]:

    total_cells += df.size

    missing_cells += (
        df.isna().sum().sum()
    )


completeness_score = (
    1 -
    missing_cells / total_cells
) * 100


# ---------------------------------------------------------
# Validity score
# ---------------------------------------------------------

total_validity_checks = (
    len(suppliers)
    + len(materials)
    + len(purchases)
)

validity_errors = (
    len(invalid_emails)
    + len(invalid_prices)
    + len(invalid_quantities)
)

validity_score = (
    1 -
    validity_errors
    / total_validity_checks
) * 100


# ---------------------------------------------------------
# Consistency score
# ---------------------------------------------------------

total_consistency_checks = (
    len(materials)
    + len(suppliers)
)

consistency_errors = (
    len(unit_inconsistencies)
    + len(country_inconsistencies)
)

consistency_score = (
    1 -
    consistency_errors
    / total_consistency_checks
) * 100


# ---------------------------------------------------------
# Uniqueness score
# ---------------------------------------------------------

total_uniqueness_records = (
    len(suppliers)
    + len(materials)
)

uniqueness_errors = (
    len(duplicate_suppliers)
    + len(duplicate_materials)
)

uniqueness_score = (
    1 -
    uniqueness_errors
    / total_uniqueness_records
) * 100


# ---------------------------------------------------------
# Overall score
# ---------------------------------------------------------

overall_score = (
    completeness_score
    + validity_score
    + consistency_score
    + uniqueness_score
) / 4


print(
    f"Completeness Score : "
    f"{completeness_score:.2f}%"
)

print(
    f"Validity Score     : "
    f"{validity_score:.2f}%"
)

print(
    f"Consistency Score  : "
    f"{consistency_score:.2f}%"
)

print(
    f"Uniqueness Score   : "
    f"{uniqueness_score:.2f}%"
)

print(
    f"Overall Quality    : "
    f"{overall_score:.2f}%"
)


# =========================================================
# SAVE REPORTS
# =========================================================

print("\n\n7. SAVING REPORTS")
print("-" * 70)


# ---------------------------------------------------------
# Excel report
# ---------------------------------------------------------

report_file = (
    REPORT_FOLDER
    / "data_quality_report.xlsx"
)


with pd.ExcelWriter(
    report_file,
    engine="openpyxl"
) as writer:

    completeness_report.to_excel(
        writer,
        sheet_name="Completeness",
        index=False
    )

    invalid_emails.to_excel(
        writer,
        sheet_name="Invalid_Emails",
        index=False
    )

    invalid_prices.to_excel(
        writer,
        sheet_name="Invalid_Prices",
        index=False
    )

    invalid_quantities.to_excel(
        writer,
        sheet_name="Invalid_Quantities",
        index=False
    )

    duplicate_suppliers.to_excel(
        writer,
        sheet_name="Duplicate_Suppliers",
        index=False
    )

    duplicate_materials.to_excel(
        writer,
        sheet_name="Duplicate_Materials",
        index=False
    )

    invalid_material_suppliers.to_excel(
        writer,
        sheet_name="Invalid_Material_Suppliers",
        index=False
    )

    invalid_material_categories.to_excel(
        writer,
        sheet_name="Invalid_Material_Categories",
        index=False
    )

    invalid_purchase_materials.to_excel(
        writer,
        sheet_name="Invalid_Purchase_Materials",
        index=False
    )

    invalid_purchase_suppliers.to_excel(
        writer,
        sheet_name="Invalid_Purchase_Suppliers",
        index=False
    )


# =========================================================
# FINAL MESSAGE
# =========================================================

print()
print("=" * 70)
print("DATA QUALITY ENGINE COMPLETED")
print("=" * 70)

print()
print("Excel report created:")
print(report_file)

print("=" * 70)