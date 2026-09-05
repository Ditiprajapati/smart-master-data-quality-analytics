import pandas as pd
import re
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
CLEANED_FOLDER = PROJECT_ROOT / "data" / "cleaned"


# =========================================================
# LOAD DATA
# =========================================================

raw_suppliers = pd.read_csv(
    RAW_FOLDER / "suppliers_raw.csv"
)

raw_materials = pd.read_csv(
    RAW_FOLDER / "materials_raw.csv"
)

raw_purchases = pd.read_csv(
    RAW_FOLDER / "purchases_raw.csv"
)


clean_suppliers = pd.read_csv(
    CLEANED_FOLDER / "suppliers_clean.csv"
)

clean_materials = pd.read_csv(
    CLEANED_FOLDER / "materials_clean.csv"
)

clean_purchases = pd.read_csv(
    CLEANED_FOLDER / "purchases_clean.csv"
)


# =========================================================
# EMAIL VALIDATION
# =========================================================

email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def count_invalid_emails(df):

    mask = (
        df["email"].isna()
        | ~df["email"]
        .fillna("")
        .str.match(
            email_pattern,
            na=False
        )
    )

    return mask.sum()


# =========================================================
# INVALID PRICE
# =========================================================

def count_invalid_prices(df):

    return (
        df["price"].isna()
        | (df["price"] <= 0)
    ).sum()


# =========================================================
# INVALID QUANTITY
# =========================================================

def count_invalid_quantities(df):

    return (
        df["quantity"].isna()
        | (df["quantity"] <= 0)
    ).sum()


# =========================================================
# MISSING CATEGORIES
# =========================================================

def count_missing_categories(df):

    return df["category_id"].isna().sum()


# =========================================================
# UNIT STANDARDIZATION CHECK
# =========================================================

valid_units = {
    "KG",
    "L",
    "TON",
    "BOX",
    "DRUM"
}


def count_nonstandard_units(df):

    return (
        ~df["unit"].isin(valid_units)
    ).sum()


# =========================================================
# COUNTRY STANDARDIZATION CHECK
# =========================================================

valid_countries = {
    "India",
    "Germany",
    "United States",
    "Singapore",
    "Japan",
    "Belgium",
    "France",
    "Netherlands",
    "Switzerland",
    "United Kingdom"
}


def count_nonstandard_countries(df):

    return (
        ~df["country"].isin(valid_countries)
    ).sum()


# =========================================================
# DUPLICATE DETECTION
# =========================================================

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


def count_duplicate_records(
    df,
    column
):

    normalized = (
        df[column]
        .apply(normalize_name)
    )

    return normalized.duplicated(
        keep=False
    ).sum()


# =========================================================
# CALCULATE METRICS
# =========================================================

results = []


# ---------------------------------------------------------
# RAW
# ---------------------------------------------------------

raw_metrics = {

    "Invalid / Missing Emails":
        count_invalid_emails(
            raw_suppliers
        ),

    "Invalid / Missing Prices":
        count_invalid_prices(
            raw_materials
        ),

    "Invalid / Missing Quantities":
        count_invalid_quantities(
            raw_purchases
        ),

    "Missing Categories":
        count_missing_categories(
            raw_materials
        ),

    "Non-standard Units":
        count_nonstandard_units(
            raw_materials
        ),

    "Non-standard Countries":
        count_nonstandard_countries(
            raw_suppliers
        ),

    "Potential Duplicate Suppliers":
        count_duplicate_records(
            raw_suppliers,
            "supplier_name"
        ),

    "Potential Duplicate Materials":
        count_duplicate_records(
            raw_materials,
            "material_name"
        )
}


# ---------------------------------------------------------
# CLEANED
# ---------------------------------------------------------

clean_metrics = {

    "Invalid / Missing Emails":
        count_invalid_emails(
            clean_suppliers
        ),

    "Invalid / Missing Prices":
        count_invalid_prices(
            clean_materials
        ),

    "Invalid / Missing Quantities":
        count_invalid_quantities(
            clean_purchases
        ),

    "Missing Categories":
        count_missing_categories(
            clean_materials
        ),

    "Non-standard Units":
        count_nonstandard_units(
            clean_materials
        ),

    "Non-standard Countries":
        count_nonstandard_countries(
            clean_suppliers
        ),

    "Potential Duplicate Suppliers":
        count_duplicate_records(
            clean_suppliers,
            "supplier_name"
        ),

    "Potential Duplicate Materials":
        count_duplicate_records(
            clean_materials,
            "material_name"
        )
}


# =========================================================
# DISPLAY COMPARISON
# =========================================================

print("=" * 80)
print("BEFORE vs AFTER DATA QUALITY COMPARISON")
print("=" * 80)

print()

print(
    f"{'QUALITY CHECK':35}"
    f"{'BEFORE':>15}"
    f"{'AFTER':>15}"
    f"{'CHANGE':>15}"
)

print("-" * 80)


for metric in raw_metrics:

    before = raw_metrics[metric]

    after = clean_metrics[metric]

    change = after - before

    print(
        f"{metric:35}"
        f"{before:>15}"
        f"{after:>15}"
        f"{change:>15}"
    )


print()
print("=" * 80)
print("COMPARISON COMPLETED")
print("=" * 80)