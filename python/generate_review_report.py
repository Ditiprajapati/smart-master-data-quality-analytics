import pandas as pd
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_FOLDER = PROJECT_ROOT / "data" / "cleaned"
REPORT_FOLDER = PROJECT_ROOT / "excel"

REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# LOAD CLEANED DATA
# =========================================================

suppliers = pd.read_csv(
    CLEANED_FOLDER / "suppliers_clean.csv"
)

materials = pd.read_csv(
    CLEANED_FOLDER / "materials_clean.csv"
)

purchases = pd.read_csv(
    CLEANED_FOLDER / "purchases_clean.csv"
)


# =========================================================
# REVIEW ITEMS
# =========================================================

# ---------------------------------------------------------
# Invalid / missing emails
# ---------------------------------------------------------

email_review = suppliers[
    suppliers["email_status"]
    != "Valid"
].copy()


# ---------------------------------------------------------
# Invalid / missing prices
# ---------------------------------------------------------

price_review = materials[
    materials["price_status"]
    != "Valid"
].copy()


# ---------------------------------------------------------
# Invalid / missing quantities
# ---------------------------------------------------------

quantity_review = purchases[
    purchases["quantity_status"]
    != "Valid"
].copy()


# ---------------------------------------------------------
# Missing / invalid categories
# ---------------------------------------------------------

category_review = materials[
    materials["category_status"]
    != "Valid"
].copy()


# ---------------------------------------------------------
# Potential duplicate suppliers
# ---------------------------------------------------------

supplier_duplicate_review = suppliers[
    suppliers["duplicate_status"]
    != "Unique"
].copy()


# ---------------------------------------------------------
# Potential duplicate materials
# ---------------------------------------------------------

material_duplicate_review = materials[
    materials["duplicate_status"]
    != "Unique"
].copy()


# =========================================================
# CREATE EXCEL REPORT
# =========================================================

report_path = (
    REPORT_FOLDER
    / "master_data_review.xlsx"
)


with pd.ExcelWriter(
    report_path,
    engine="openpyxl"
) as writer:

    email_review.to_excel(
        writer,
        sheet_name="Email Review",
        index=False
    )

    price_review.to_excel(
        writer,
        sheet_name="Price Review",
        index=False
    )

    quantity_review.to_excel(
        writer,
        sheet_name="Quantity Review",
        index=False
    )

    category_review.to_excel(
        writer,
        sheet_name="Category Review",
        index=False
    )

    supplier_duplicate_review.to_excel(
        writer,
        sheet_name="Supplier Duplicates",
        index=False
    )

    material_duplicate_review.to_excel(
        writer,
        sheet_name="Material Duplicates",
        index=False
    )


# =========================================================
# SUMMARY
# =========================================================

print("=" * 70)
print("MASTER DATA REVIEW REPORT")
print("=" * 70)

print()

print(
    "Email issues       :",
    len(email_review)
)

print(
    "Price issues       :",
    len(price_review)
)

print(
    "Quantity issues    :",
    len(quantity_review)
)

print(
    "Category issues    :",
    len(category_review)
)

print(
    "Supplier duplicates:",
    len(supplier_duplicate_review)
)

print(
    "Material duplicates:",
    len(material_duplicate_review)
)

print()

print(
    "Report created:"
)

print(report_path)

print()
print("=" * 70)
print("REVIEW REPORT COMPLETED")
print("=" * 70)