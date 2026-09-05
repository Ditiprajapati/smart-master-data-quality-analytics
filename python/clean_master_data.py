import pandas as pd
import re
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
CLEANED_FOLDER = PROJECT_ROOT / "data" / "cleaned"

CLEANED_FOLDER.mkdir(parents=True, exist_ok=True)


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
print("MASTER DATA CLEANING PIPELINE")
print("=" * 70)


# =========================================================
# 1. SUPPLIER NAME STANDARDIZATION
# =========================================================

print("\n1. STANDARDIZING SUPPLIER NAMES")
print("-" * 70)


def clean_text(value):

    if pd.isna(value):
        return value

    value = str(value)

    # Remove leading/trailing spaces
    value = value.strip()

    # Replace multiple spaces with one
    value = re.sub(r"\s+", " ", value)

    return value


suppliers["supplier_name"] = (
    suppliers["supplier_name"]
    .apply(clean_text)
)


# =========================================================
# 2. COUNTRY STANDARDIZATION
# =========================================================

print("2. STANDARDIZING COUNTRIES")
print("-" * 70)


country_mapping = {

    "india": "India",
    "INDIA": "India",
    "India": "India",
    "India ": "India",

    "germany": "Germany",
    "GERMANY": "Germany",
    "Germany": "Germany",
    "Germany ": "Germany",

    "USA": "United States",
    "US": "United States",
    "united states": "United States",
    "United States": "United States",

    "singapore": "Singapore",
    "SINGAPORE": "Singapore",
    "Singapore": "Singapore",

    "japan": "Japan",
    "JAPAN": "Japan",
    "Japan": "Japan",

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


suppliers["country"] = (
    suppliers["country"]
    .map(country_mapping)
)


# =========================================================
# 3. EMAIL STANDARDIZATION
# =========================================================

print("3. STANDARDIZING EMAILS")
print("-" * 70)


suppliers["email"] = (
    suppliers["email"]
    .astype("string")
    .str.strip()
    .str.lower()
)


# =========================================================
# 4. PHONE STANDARDIZATION
# =========================================================

print("4. STANDARDIZING PHONE NUMBERS")
print("-" * 70)


def clean_phone(value):

    if pd.isna(value):
        return value

    value = str(value)

    # Keep digits only
    value = re.sub(
        r"\D",
        "",
        value
    )

    return value


suppliers["phone"] = (
    suppliers["phone"]
    .apply(clean_phone)
)


# =========================================================
# 5. MATERIAL NAME STANDARDIZATION
# =========================================================

print("5. STANDARDIZING MATERIAL NAMES")
print("-" * 70)


materials["material_name"] = (
    materials["material_name"]
    .apply(clean_text)
)


# Standardize capitalization
materials["material_name"] = (
    materials["material_name"]
    .str.title()
)


# =========================================================
# 6. UNIT STANDARDIZATION
# =========================================================

print("6. STANDARDIZING UNITS")
print("-" * 70)


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


materials["unit"] = (
    materials["unit"]
    .map(unit_mapping)
)


# =========================================================
# 7. PRICE VALIDATION
# =========================================================

print("7. VALIDATING MATERIAL PRICES")
print("-" * 70)


materials["price"] = pd.to_numeric(
    materials["price"],
    errors="coerce"
)


materials["price_status"] = "Valid"


materials.loc[
    materials["price"].isna(),
    "price_status"
] = "Missing - Review Required"


materials.loc[
    materials["price"] <= 0,
    "price_status"
] = "Invalid - Review Required"


# We do NOT replace invalid prices with fake values.


# =========================================================
# 8. PURCHASE QUANTITY VALIDATION
# =========================================================

print("8. VALIDATING PURCHASE QUANTITIES")
print("-" * 70)


purchases["quantity"] = pd.to_numeric(
    purchases["quantity"],
    errors="coerce"
)


purchases["quantity_status"] = "Valid"


purchases.loc[
    purchases["quantity"].isna(),
    "quantity_status"
] = "Missing - Review Required"


purchases.loc[
    purchases["quantity"] <= 0,
    "quantity_status"
] = "Invalid - Review Required"


# =========================================================
# 9. EMAIL VALIDATION
# =========================================================

print("9. VALIDATING EMAIL ADDRESSES")
print("-" * 70)


email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"


suppliers["email_status"] = "Valid"


invalid_email_mask = (
    suppliers["email"].isna()
    | ~suppliers["email"].str.match(
        email_pattern,
        na=False
    )
)


suppliers.loc[
    invalid_email_mask,
    "email_status"
] = "Invalid / Missing - Review Required"


# =========================================================
# 10. NORMALIZED NAMES FOR DUPLICATE DETECTION
# =========================================================

print("10. DETECTING POTENTIAL DUPLICATES")
print("-" * 70)


def normalize_name(value):

    if pd.isna(value):
        return ""

    value = str(value).lower()

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


# =========================================================
# 11. DUPLICATE FLAGS
# =========================================================

suppliers["duplicate_status"] = "Unique"


supplier_duplicate_mask = (
    suppliers["normalized_name"]
    .duplicated(keep=False)
)


suppliers.loc[
    supplier_duplicate_mask,
    "duplicate_status"
] = "Potential Duplicate - Review"


materials["duplicate_status"] = "Unique"


material_duplicate_mask = (
    materials["normalized_name"]
    .duplicated(keep=False)
)


materials.loc[
    material_duplicate_mask,
    "duplicate_status"
] = "Potential Duplicate - Review"


# =========================================================
# 12. MATERIAL CATEGORY VALIDATION
# =========================================================

print("11. VALIDATING CATEGORY REFERENCES")
print("-" * 70)


valid_categories = set(
    categories["category_id"]
)


materials["category_status"] = "Valid"


materials.loc[
    materials["category_id"].isna(),
    "category_status"
] = "Missing - Review Required"


materials.loc[
    materials["category_id"].notna()
    & ~materials["category_id"].isin(
        valid_categories
    ),
    "category_status"
] = "Invalid - Review Required"


# =========================================================
# 13. CLEANED DATA OUTPUT
# =========================================================

print("\n12. SAVING CLEANED DATA")
print("-" * 70)


# Save cleaned datasets

categories.to_csv(
    CLEANED_FOLDER / "categories_clean.csv",
    index=False
)


suppliers.to_csv(
    CLEANED_FOLDER / "suppliers_clean.csv",
    index=False
)


materials.to_csv(
    CLEANED_FOLDER / "materials_clean.csv",
    index=False
)


purchases.to_csv(
    CLEANED_FOLDER / "purchases_clean.csv",
    index=False
)


# =========================================================
# 14. CLEANING SUMMARY
# =========================================================

print("\n")
print("=" * 70)
print("CLEANING SUMMARY")
print("=" * 70)


print(
    "Supplier records:",
    len(suppliers)
)


print(
    "Material records:",
    len(materials)
)


print(
    "Purchase records:",
    len(purchases)
)


print(
    "\nPotential duplicate suppliers:",
    supplier_duplicate_mask.sum()
)


print(
    "Potential duplicate materials:",
    material_duplicate_mask.sum()
)


print(
    "\nInvalid / missing emails:",
    invalid_email_mask.sum()
)


print(
    "Invalid / missing prices:",
    (
        materials["price_status"]
        != "Valid"
    ).sum()
)


print(
    "Invalid / missing quantities:",
    (
        purchases["quantity_status"]
        != "Valid"
    ).sum()
)


print(
    "Missing / invalid categories:",
    (
        materials["category_status"]
        != "Valid"
    ).sum()
)


print("\nCleaned files saved to:")

print(CLEANED_FOLDER)


print("\n")
print("=" * 70)
print("DATA CLEANING PIPELINE COMPLETED")
print("=" * 70)