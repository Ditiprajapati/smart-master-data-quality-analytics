import pandas as pd
import math
import mysql.connector
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(r"D:\Clariant_Master_Data_Project")
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

def clean_value(value):
    """
    Convert pandas NaN values to Python None
    so MySQL stores them as NULL.
    """
    if pd.isna(value):
        return None
    return value
# --------------------------------------------------
# MYSQL CONNECTION
# --------------------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="master_data_quality"
)

cursor = conn.cursor()

print("=" * 70)
print("LOADING CLEANED DATA INTO MYSQL")
print("=" * 70)


# --------------------------------------------------
# LOAD CATEGORIES
# --------------------------------------------------

categories = pd.read_csv(
    CLEANED_DIR / "categories_clean.csv"
)

for _, row in categories.iterrows():

    cursor.execute(
        """
        INSERT INTO categories
        (category_id, category_name)
        VALUES (%s, %s)
        """,
        (
    clean_value(row["category_id"]),
    clean_value(row["category_name"])
)
    )

print(f"Categories loaded: {len(categories)}")


# --------------------------------------------------
# LOAD SUPPLIERS
# --------------------------------------------------

suppliers = pd.read_csv(
    CLEANED_DIR / "suppliers_clean.csv"
)

for _, row in suppliers.iterrows():

    cursor.execute(
        """
        INSERT INTO suppliers
        (supplier_id, supplier_name, country, email, phone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
    clean_value(row["supplier_id"]),
    clean_value(row["supplier_name"]),
    clean_value(row["country"]),
    clean_value(row["email"]),
    clean_value(row["phone"])
)
    )

print(f"Suppliers loaded: {len(suppliers)}")


# --------------------------------------------------
# LOAD MATERIALS
# --------------------------------------------------

materials = pd.read_csv(
    CLEANED_DIR / "materials_clean.csv"
)

for _, row in materials.iterrows():

    cursor.execute(
        """
        INSERT INTO materials
        (material_id, material_name, category_id,
         supplier_id, unit, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
    clean_value(row["material_id"]),
    clean_value(row["material_name"]),
    clean_value(row["category_id"]),
    clean_value(row["supplier_id"]),
    clean_value(row["unit"]),
    clean_value(row["price"])
)
    )

print(f"Materials loaded: {len(materials)}")


# --------------------------------------------------
# LOAD PURCHASES
# --------------------------------------------------

purchases = pd.read_csv(
    CLEANED_DIR / "purchases_clean.csv"
)

for _, row in purchases.iterrows():

    cursor.execute(
        """
        INSERT INTO purchases
        (purchase_id, material_id, supplier_id,
         purchase_date, quantity, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
    clean_value(row["purchase_id"]),
    clean_value(row["material_id"]),
    clean_value(row["supplier_id"]),
    clean_value(row["purchase_date"]),
    clean_value(row["quantity"]),
    clean_value(row["total_amount"])
)
    )

print(f"Purchases loaded: {len(purchases)}")


# --------------------------------------------------
# COMMIT
# --------------------------------------------------

conn.commit()

print()
print("=" * 70)
print("DATA LOADING COMPLETED SUCCESSFULLY")
print("=" * 70)

cursor.close()
conn.close()