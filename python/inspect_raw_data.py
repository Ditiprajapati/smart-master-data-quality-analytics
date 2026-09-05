import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

suppliers = pd.read_csv(RAW_FOLDER / "suppliers_raw.csv")
materials = pd.read_csv(RAW_FOLDER / "materials_raw.csv")
categories = pd.read_csv(RAW_FOLDER / "categories_raw.csv")
purchases = pd.read_csv(RAW_FOLDER / "purchases_raw.csv")


# ---------------------------------------------------------
# BASIC INFORMATION
# ---------------------------------------------------------

print("=" * 70)
print("RAW DATA INSPECTION")
print("=" * 70)

print("\nDATASET SIZES")
print("-" * 70)

print(f"Categories : {len(categories)} rows")
print(f"Suppliers  : {len(suppliers)} rows")
print(f"Materials  : {len(materials)} rows")
print(f"Purchases  : {len(purchases)} rows")


# ---------------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------------

print("\n\nMISSING VALUES")
print("-" * 70)

print("\nSuppliers:")
print(suppliers.isnull().sum())

print("\nMaterials:")
print(materials.isnull().sum())

print("\nPurchases:")
print(purchases.isnull().sum())


# ---------------------------------------------------------
# DUPLICATES
# ---------------------------------------------------------

print("\n\nDUPLICATE RECORDS")
print("-" * 70)

print(
    "Duplicate supplier IDs:",
    suppliers["supplier_id"].duplicated().sum()
)

print(
    "Duplicate material IDs:",
    materials["material_id"].duplicated().sum()
)

print(
    "Duplicate purchase IDs:",
    purchases["purchase_id"].duplicated().sum()
)


# ---------------------------------------------------------
# INVALID PRICES
# ---------------------------------------------------------

print("\n\nINVALID MATERIAL PRICES")
print("-" * 70)

invalid_prices = materials[materials["price"] <= 0]

print("Number of invalid prices:", len(invalid_prices))

if len(invalid_prices) > 0:
    print(invalid_prices[
        [
            "material_id",
            "material_name",
            "price"
        ]
    ].head(10))


# ---------------------------------------------------------
# INVALID PURCHASE QUANTITIES
# ---------------------------------------------------------

print("\n\nINVALID PURCHASE QUANTITIES")
print("-" * 70)

invalid_quantities = purchases[purchases["quantity"] <= 0]

print(
    "Number of invalid quantities:",
    len(invalid_quantities)
)

if len(invalid_quantities) > 0:
    print(
        invalid_quantities[
            [
                "purchase_id",
                "material_id",
                "quantity"
            ]
        ].head(10)
    )


# ---------------------------------------------------------
# INVALID EMAILS
# ---------------------------------------------------------

print("\n\nPOTENTIALLY INVALID EMAILS")
print("-" * 70)

invalid_email_mask = (
    suppliers["email"].notna()
    & ~suppliers["email"].str.contains("@", regex=False)
)

invalid_emails = suppliers[invalid_email_mask]

print(
    "Number of potentially invalid emails:",
    len(invalid_emails)
)

if len(invalid_emails) > 0:
    print(
        invalid_emails[
            [
                "supplier_id",
                "supplier_name",
                "email"
            ]
        ].head(10)
    )


# ---------------------------------------------------------
# UNIT VARIATIONS
# ---------------------------------------------------------

print("\n\nUNIT VALUES FOUND")
print("-" * 70)

print(
    sorted(
        materials["unit"]
        .dropna()
        .unique()
        .tolist()
    )
)


# ---------------------------------------------------------
# COUNTRY VARIATIONS
# ---------------------------------------------------------

print("\n\nSUPPLIER COUNTRY VALUES FOUND")
print("-" * 70)

print(
    sorted(
        suppliers["country"]
        .dropna()
        .unique()
        .tolist()
    )
)


# ---------------------------------------------------------
# SAMPLE RECORDS
# ---------------------------------------------------------

print("\n\nSAMPLE SUPPLIER RECORDS")
print("-" * 70)

print(suppliers.head(10).to_string(index=False))


print("\n\nSAMPLE MATERIAL RECORDS")
print("-" * 70)

print(materials.head(10).to_string(index=False))


print("\n\nSAMPLE PURCHASE RECORDS")
print("-" * 70)

print(purchases.head(10).to_string(index=False))


print("\n")
print("=" * 70)
print("RAW DATA INSPECTION COMPLETED")
print("=" * 70)