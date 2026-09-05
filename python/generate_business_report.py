import pandas as pd
import mysql.connector
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(r"D:\Clariant_Master_Data_Project")

OUTPUT_FILE = (
    BASE_DIR
    / "excel"
    / "business_analysis_report.xlsx"
)


# ============================================================
# MYSQL CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="master_data_quality"
)

print("=" * 70)
print("GENERATING BUSINESS ANALYSIS REPORT")
print("=" * 70)


# ============================================================
# 1. EXECUTIVE SUMMARY
# ============================================================

executive_summary = pd.read_sql(
    """
    SELECT
        (SELECT COUNT(*) FROM categories) AS total_categories,
        (SELECT COUNT(*) FROM suppliers) AS total_suppliers,
        (SELECT COUNT(*) FROM materials) AS total_materials,
        (SELECT COUNT(*) FROM purchases) AS total_purchases,
        (SELECT SUM(total_amount) FROM purchases)
            AS total_procurement_spend
    """,
    conn
)

print("Executive Summary generated.")


# ============================================================
# 2. SUPPLIER ANALYSIS
# ============================================================

supplier_analysis = pd.read_sql(
    """
    SELECT
        s.supplier_id,
        s.supplier_name,
        s.country,
        s.email,
        s.phone,
        COALESCE(SUM(p.total_amount), 0) AS total_spend
    FROM suppliers s
    LEFT JOIN purchases p
        ON s.supplier_id = p.supplier_id
    GROUP BY
        s.supplier_id,
        s.supplier_name,
        s.country,
        s.email,
        s.phone
    ORDER BY total_spend DESC
    """,
    conn
)

print("Supplier Analysis generated.")


# ============================================================
# 3. MATERIAL ANALYSIS
# ============================================================

material_analysis = pd.read_sql(
    """
    SELECT
        m.material_id,
        m.material_name,
        c.category_name,
        m.supplier_id,
        m.unit,
        m.price,
        COALESCE(SUM(p.quantity), 0) AS total_quantity,
        COALESCE(SUM(p.total_amount), 0) AS total_spend
    FROM materials m
    LEFT JOIN categories c
        ON m.category_id = c.category_id
    LEFT JOIN purchases p
        ON m.material_id = p.material_id
    GROUP BY
        m.material_id,
        m.material_name,
        c.category_name,
        m.supplier_id,
        m.unit,
        m.price
    ORDER BY total_spend DESC
    """,
    conn
)

print("Material Analysis generated.")


# ============================================================
# 4. CATEGORY ANALYSIS
# ============================================================

category_analysis = pd.read_sql(
    """
    SELECT
        c.category_id,
        c.category_name,
        COUNT(DISTINCT m.material_id) AS material_count,
        COALESCE(SUM(p.quantity), 0) AS total_quantity,
        COALESCE(SUM(p.total_amount), 0) AS category_spend
    FROM categories c
    LEFT JOIN materials m
        ON c.category_id = m.category_id
    LEFT JOIN purchases p
        ON m.material_id = p.material_id
    GROUP BY
        c.category_id,
        c.category_name
    ORDER BY category_spend DESC
    """,
    conn
)

print("Category Analysis generated.")


# ============================================================
# 5. MONTHLY PROCUREMENT TREND
# ============================================================

monthly_trend = pd.read_sql(
    """
    SELECT
        DATE_FORMAT(purchase_date, '%Y-%m')
            AS purchase_month,
        COUNT(*) AS purchase_count,
        SUM(quantity) AS total_quantity,
        SUM(total_amount) AS monthly_spend
    FROM purchases
    GROUP BY
        DATE_FORMAT(purchase_date, '%Y-%m')
    ORDER BY purchase_month
    """,
    conn
)

print("Monthly Trend generated.")


# ============================================================
# 6. DATA QUALITY SUMMARY
# ============================================================

supplier_quality = pd.read_sql(
    """
    SELECT
        COUNT(*) AS total_suppliers,

        SUM(
            CASE
                WHEN email IS NULL THEN 1
                ELSE 0
            END
        ) AS missing_emails,

        SUM(
            CASE
                WHEN phone IS NULL THEN 1
                ELSE 0
            END
        ) AS missing_phones,

        SUM(
            CASE
                WHEN email IS NULL OR phone IS NULL
                THEN 1
                ELSE 0
            END
        ) AS suppliers_with_missing_contact_data

    FROM suppliers
    """,
    conn
)


material_quality = pd.read_sql(
    """
    SELECT
        COUNT(*) AS total_materials,

        SUM(
            CASE
                WHEN category_id IS NULL THEN 1
                ELSE 0
            END
        ) AS missing_categories,

        SUM(
            CASE
                WHEN price IS NULL THEN 1
                ELSE 0
            END
        ) AS missing_prices,

        SUM(
            CASE
                WHEN price IS NOT NULL AND price <= 0
                THEN 1
                ELSE 0
            END
        ) AS invalid_prices

    FROM materials
    """,
    conn
)


purchase_quality = pd.read_sql(
    """
    SELECT
        COUNT(*) AS total_purchases,

        SUM(
            CASE
                WHEN quantity IS NULL THEN 1
                ELSE 0
            END
        ) AS missing_quantities,

        SUM(
            CASE
                WHEN quantity IS NOT NULL AND quantity <= 0
                THEN 1
                ELSE 0
            END
        ) AS invalid_quantities,

        SUM(
            CASE
                WHEN quantity IS NULL OR quantity <= 0
                THEN 1
                ELSE 0
            END
        ) AS total_quantity_issues

    FROM purchases
    """,
    conn
)


data_quality = pd.concat(
    [
        supplier_quality,
        material_quality,
        purchase_quality
    ],
    axis=1
)

print("Data Quality generated.")


# ============================================================
# WRITE TO EXCEL
# ============================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    executive_summary.to_excel(
        writer,
        sheet_name="Executive Summary",
        index=False
    )

    supplier_analysis.to_excel(
        writer,
        sheet_name="Supplier Analysis",
        index=False
    )

    material_analysis.to_excel(
        writer,
        sheet_name="Material Analysis",
        index=False
    )

    category_analysis.to_excel(
        writer,
        sheet_name="Category Analysis",
        index=False
    )

    monthly_trend.to_excel(
        writer,
        sheet_name="Monthly Trend",
        index=False
    )

    data_quality.to_excel(
        writer,
        sheet_name="Data Quality",
        index=False
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

conn.close()


print()
print("=" * 70)
print("BUSINESS ANALYSIS REPORT CREATED SUCCESSFULLY")
print("=" * 70)
print()
print(f"Report location:")
print(OUTPUT_FILE)
print()
print("=" * 70)