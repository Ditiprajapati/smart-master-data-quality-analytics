import pandas as pd
import random
from faker import Faker
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------
# PROJECT: Smart Master Data Quality & Analytics System
# COMPANY: ChemCore Manufacturing (Fictional)
# ---------------------------------------------------------

fake = Faker()

# Make results reproducible
random.seed(42)
Faker.seed(42)

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"

RAW_FOLDER.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# MASTER DATA
# ---------------------------------------------------------

categories = [
    ("CAT001", "Raw Materials"),
    ("CAT002", "Solvents"),
    ("CAT003", "Specialty Chemicals"),
    ("CAT004", "Additives"),
    ("CAT005", "Intermediates"),
    ("CAT006", "Packaging Materials"),
    ("CAT007", "Industrial Chemicals"),
    ("CAT008", "Polymers"),
    ("CAT009", "Performance Chemicals"),
    ("CAT010", "Laboratory Chemicals")
]

# ---------------------------------------------------------
# SUPPLIERS
# ---------------------------------------------------------

supplier_names = [
    "Apex Chemical Solutions",
    "Global Industrial Materials",
    "Nova Specialty Chemicals",
    "Zenith Chemical Industries",
    "Prime Industrial Supplies",
    "Universal Chemical Products",
    "Vertex Materials",
    "GreenCore Chemicals",
    "Pioneer Specialty Materials",
    "Metro Chemical Industries"
]

countries = [
    "India",
    "Germany",
    "United States",
    "Singapore",
    "Japan",
    "United Kingdom",
    "France",
    "Netherlands",
    "Switzerland",
    "Belgium"
]

suppliers = []

for i in range(1, 501):

    supplier_id = f"SUP{i:03d}"

    base_name = random.choice(supplier_names)

    # Add a unique suffix so most suppliers remain unique
    supplier_name = f"{base_name} {i}"

    country = random.choice(countries)

    email = (
        supplier_name.lower()
        .replace(" ", ".")
        .replace(".", "", 1)
        + "@example.com"
    )

    phone = f"{random.randint(6000000000, 9999999999)}"

    suppliers.append([
        supplier_id,
        supplier_name,
        country,
        email,
        phone
    ])

suppliers_df = pd.DataFrame(
    suppliers,
    columns=[
        "supplier_id",
        "supplier_name",
        "country",
        "email",
        "phone"
    ]
)

# ---------------------------------------------------------
# MATERIALS
# ---------------------------------------------------------

material_names = [
    "Sodium Hydroxide",
    "Ethanol",
    "Acetone",
    "Methanol",
    "Hydrogen Peroxide",
    "Citric Acid",
    "Sulfuric Acid",
    "Hydrochloric Acid",
    "Sodium Chloride",
    "Calcium Carbonate",
    "Isopropyl Alcohol",
    "Toluene",
    "Xylene",
    "Ethylene Glycol",
    "Propylene Glycol",
    "Glycerol",
    "Ammonium Hydroxide",
    "Sodium Carbonate",
    "Acetic Acid",
    "Formaldehyde"
]

units = ["KG", "L", "TON", "BOX", "DRUM"]

materials = []

for i in range(1, 2001):

    material_id = f"MAT{i:04d}"

    base_material = random.choice(material_names)

    grade = random.choice([
    "A",
    "B",
    "Industrial",
    "Premium"
])

    material_name = (
     f"{base_material} {grade} "
        f"Material {i:04d}"
    )
    category_id = random.choice(categories)[0]

    supplier_id = random.choice(suppliers_df["supplier_id"].tolist())

    unit = random.choice(units)

    price = round(random.uniform(50, 5000), 2)

    country = random.choice(countries)

    materials.append([
        material_id,
        material_name,
        category_id,
        supplier_id,
        unit,
        price,
        country
    ])

materials_df = pd.DataFrame(
    materials,
    columns=[
        "material_id",
        "material_name",
        "category_id",
        "supplier_id",
        "unit",
        "price",
        "country"
    ]
)

# ---------------------------------------------------------
# PURCHASE TRANSACTIONS
# ---------------------------------------------------------

purchases = []

start_date = date(2025, 1, 1)

for i in range(1, 10001):

    purchase_id = f"PO{i:05d}"

    material = materials_df.sample(1).iloc[0]

    material_id = material["material_id"]

    supplier_id = material["supplier_id"]

    random_days = random.randint(0, 600)

    purchase_date = start_date + timedelta(days=random_days)

    quantity = round(random.uniform(10, 1000), 2)

    total_amount = round(quantity * material["price"], 2)

    purchases.append([
        purchase_id,
        material_id,
        supplier_id,
        purchase_date,
        quantity,
        total_amount
    ])

purchases_df = pd.DataFrame(
    purchases,
    columns=[
        "purchase_id",
        "material_id",
        "supplier_id",
        "purchase_date",
        "quantity",
        "total_amount"
    ]
)

# ---------------------------------------------------------
# INTRODUCE DATA QUALITY PROBLEMS
# ---------------------------------------------------------

print("Introducing realistic data-quality issues...")

# ---------------------------------------------------------
# 1. Supplier name inconsistencies
# ---------------------------------------------------------

for index in random.sample(range(len(suppliers_df)), 40):

    name = suppliers_df.loc[index, "supplier_name"]

    variation = random.choice([
        name.upper(),
        name.lower(),
        name + " ",
        name.replace("Chemicals", "Chemical"),
        name.replace("Industries", "Industry")
    ])

    suppliers_df.loc[index, "supplier_name"] = variation


# ---------------------------------------------------------
# 2. Country inconsistencies
# ---------------------------------------------------------

country_variations = {
    "India": ["india", "INDIA", "India "],
    "Germany": ["germany", "GERMANY", "Germany "],
    "United States": ["USA", "US", "united states"],
    "Singapore": ["singapore", "SINGAPORE"],
    "Japan": ["japan", "JAPAN"]
}

for index in random.sample(range(len(suppliers_df)), 30):

    current_country = suppliers_df.loc[index, "country"]

    if current_country in country_variations:

        suppliers_df.loc[index, "country"] = random.choice(
            country_variations[current_country]
        )


# ---------------------------------------------------------
# 3. Missing supplier emails
# ---------------------------------------------------------

for index in random.sample(range(len(suppliers_df)), 25):

    suppliers_df.loc[index, "email"] = None


# ---------------------------------------------------------
# 4. Missing phone numbers
# ---------------------------------------------------------

for index in random.sample(range(len(suppliers_df)), 20):

    suppliers_df.loc[index, "phone"] = None


# ---------------------------------------------------------
# 5. Invalid email addresses
# ---------------------------------------------------------

for index in random.sample(range(len(suppliers_df)), 15):

    suppliers_df.loc[index, "email"] = "invalid-email"


# ---------------------------------------------------------
# 6. Material name inconsistencies
# ---------------------------------------------------------

for index in random.sample(range(len(materials_df)), 80):

    name = materials_df.loc[index, "material_name"]

    materials_df.loc[index, "material_name"] = random.choice([
        name.upper(),
        name.lower(),
        name + " ",
        name.replace("Grade", "grade")
    ])


# ---------------------------------------------------------
# 7. Unit inconsistencies
# ---------------------------------------------------------

unit_variations = {
    "KG": ["kg", "Kg", "Kilogram"],
    "L": ["l", "Liter", "litre"],
    "TON": ["ton", "Tonne", "tonne"],
    "BOX": ["box", "Box"],
    "DRUM": ["drum", "Drum"]
}

for index in random.sample(range(len(materials_df)), 100):

    current_unit = materials_df.loc[index, "unit"]

    materials_df.loc[index, "unit"] = random.choice(
        unit_variations[current_unit]
    )


# ---------------------------------------------------------
# 8. Missing category
# ---------------------------------------------------------

for index in random.sample(range(len(materials_df)), 40):

    materials_df.loc[index, "category_id"] = None


# ---------------------------------------------------------
# 9. Missing price
# ---------------------------------------------------------

for index in random.sample(range(len(materials_df)), 30):

    materials_df.loc[index, "price"] = None


# ---------------------------------------------------------
# 10. Invalid negative prices
# ---------------------------------------------------------

for index in random.sample(range(len(materials_df)), 15):

    materials_df.loc[index, "price"] = -random.randint(100, 1000)


# ---------------------------------------------------------
# 11. Invalid purchase quantities
# ---------------------------------------------------------

for index in random.sample(range(len(purchases_df)), 20):

    purchases_df.loc[index, "quantity"] = -random.randint(1, 100)


# ---------------------------------------------------------
# SAVE DATA
# ---------------------------------------------------------

categories_df = pd.DataFrame(
    categories,
    columns=[
        "category_id",
        "category_name"
    ]
)

categories_df.to_csv(
    RAW_FOLDER / "categories_raw.csv",
    index=False
)

suppliers_df.to_csv(
    RAW_FOLDER / "suppliers_raw.csv",
    index=False
)

materials_df.to_csv(
    RAW_FOLDER / "materials_raw.csv",
    index=False
)

purchases_df.to_csv(
    RAW_FOLDER / "purchases_raw.csv",
    index=False
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()
print("=" * 60)
print("RAW DATA GENERATION COMPLETED")
print("=" * 60)

print(f"Categories : {len(categories_df)}")
print(f"Suppliers  : {len(suppliers_df)}")
print(f"Materials  : {len(materials_df)}")
print(f"Purchases  : {len(purchases_df)}")

print()
print("Files created:")
print("1. categories_raw.csv")
print("2. suppliers_raw.csv")
print("3. materials_raw.csv")
print("4. purchases_raw.csv")

print()
print("Location:")
print(RAW_FOLDER)

print("=" * 60)