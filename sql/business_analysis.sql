USE master_data_quality;

-- =====================================================
-- 1. DATABASE RECORD COUNTS
-- =====================================================

SELECT 'Categories' AS table_name, COUNT(*) AS record_count
FROM categories

UNION ALL

SELECT 'Suppliers', COUNT(*)
FROM suppliers

UNION ALL

SELECT 'Materials', COUNT(*)
FROM materials

UNION ALL

SELECT 'Purchases', COUNT(*)
FROM purchases;


-- =====================================================
-- 2. TOTAL PROCUREMENT SPEND
-- =====================================================

SELECT
    SUM(total_amount) AS total_procurement_spend
FROM purchases;

-- =====================================================
-- 3. TOP 10 SUPPLIERS BY PROCUREMENT SPEND
-- =====================================================

SELECT
    s.supplier_id,
    s.supplier_name,
    SUM(p.total_amount) AS total_spend
FROM suppliers s
JOIN purchases p
    ON s.supplier_id = p.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name
ORDER BY total_spend DESC
LIMIT 10;


-- =====================================================
-- 4. TOP 10 MATERIALS BY PURCHASE QUANTITY
-- =====================================================

SELECT
    m.material_id,
    m.material_name,
    SUM(p.quantity) AS total_quantity
FROM materials m
JOIN purchases p
    ON m.material_id = p.material_id
GROUP BY
    m.material_id,
    m.material_name
ORDER BY total_quantity DESC
LIMIT 10;


-- =====================================================
-- 5. PROCUREMENT SPEND BY CATEGORY
-- =====================================================

SELECT
    c.category_name,
    SUM(p.total_amount) AS category_spend
FROM categories c
JOIN materials m
    ON c.category_id = m.category_id
JOIN purchases p
    ON m.material_id = p.material_id
GROUP BY
    c.category_id,
    c.category_name
ORDER BY category_spend DESC;


-- =====================================================
-- 6. MONTHLY PROCUREMENT SPEND
-- =====================================================

SELECT
    DATE_FORMAT(purchase_date, '%Y-%m') AS purchase_month,
    SUM(total_amount) AS monthly_spend
FROM purchases
GROUP BY
    DATE_FORMAT(purchase_date, '%Y-%m')
ORDER BY purchase_month;

-- =====================================================
-- 7. SUPPLIER CONTACT DATA QUALITY
-- =====================================================

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
            WHEN email IS NULL OR phone IS NULL THEN 1
            ELSE 0
        END
    ) AS suppliers_with_missing_contact_data

FROM suppliers;


-- =====================================================
-- 8. MATERIAL DATA QUALITY
-- =====================================================

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
            WHEN price IS NOT NULL AND price <= 0 THEN 1
            ELSE 0
        END
    ) AS invalid_prices

FROM materials;


-- =====================================================
-- 9. DUPLICATE SUPPLIER DETECTION
-- =====================================================

SELECT
    LOWER(TRIM(supplier_name)) AS normalized_supplier_name,
    COUNT(*) AS duplicate_count
FROM suppliers
GROUP BY LOWER(TRIM(supplier_name))
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- =====================================================
-- 10. DUPLICATE MATERIAL DETECTION
-- =====================================================

SELECT
    LOWER(TRIM(material_name)) AS normalized_material_name,
    COUNT(*) AS duplicate_count
FROM materials
GROUP BY LOWER(TRIM(material_name))
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- =====================================================
-- 11. PURCHASE QUANTITY QUALITY
-- =====================================================

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
            WHEN quantity IS NOT NULL AND quantity <= 0 THEN 1
            ELSE 0
        END
    ) AS invalid_quantities,

    SUM(
        CASE
            WHEN quantity IS NULL OR quantity <= 0 THEN 1
            ELSE 0
        END
    ) AS total_quantity_issues

FROM purchases;

-- =====================================================
-- 12. PROCUREMENT SPEND RECONCILIATION
-- =====================================================

SELECT
    SUM(total_amount) AS total_procurement_spend,

    SUM(
        CASE
            WHEN material_id IN (
                SELECT material_id
                FROM materials
                WHERE category_id IS NULL
            )
            THEN total_amount
            ELSE 0
        END
    ) AS unclassified_material_spend,

    SUM(
        CASE
            WHEN material_id IN (
                SELECT material_id
                FROM materials
                WHERE category_id IS NOT NULL
            )
            THEN total_amount
            ELSE 0
        END
    ) AS classified_material_spend

FROM purchases;

-- =====================================================
-- 13. DATA QUALITY PERCENTAGES
-- =====================================================

SELECT
    COUNT(*) AS total_suppliers,

    ROUND(
        100 * SUM(
            CASE
                WHEN email IS NOT NULL
                 AND phone IS NOT NULL
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS complete_contact_percentage

FROM suppliers;


SELECT
    COUNT(*) AS total_materials,

    ROUND(
        100 * SUM(
            CASE
                WHEN category_id IS NOT NULL
                 AND price IS NOT NULL
                 AND price > 0
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS complete_material_percentage

FROM materials;


SELECT
    COUNT(*) AS total_purchases,

    ROUND(
        100 * SUM(
            CASE
                WHEN quantity IS NOT NULL
                 AND quantity > 0
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS valid_quantity_percentage

FROM purchases;