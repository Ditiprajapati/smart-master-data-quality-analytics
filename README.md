# Smart Master Data Quality & Analytics System

An end-to-end master data quality and procurement analytics project built using **Python, MySQL, SQL, Excel, and Power BI** for a simulated manufacturing environment.

---

## 📌 Project Overview

Master data is critical for enterprise processes such as procurement, inventory, finance, and reporting. Poor-quality master data can lead to duplicate records, missing information, inconsistent values, and unreliable business analysis.

This project demonstrates a practical approach to identifying, validating, standardizing, and analyzing **supplier and material master data** before it is used in an enterprise database or reporting environment.

The project uses a simulated manufacturing company named **ChemCore Manufacturing**.

> **Note:** This is an academic simulation using synthetic data. It is not connected to Clariant's actual systems, SAP systems, or real company data.

---

## 🎯 Objectives

The main objectives of this project are:

- Identify master data quality problems
- Detect duplicate supplier and material records
- Identify missing and invalid values
- Standardize inconsistent country and unit values
- Validate emails, prices, quantities, and relationships
- Store cleaned data in a relational MySQL database
- Perform business analysis using SQL
- Generate data-quality review reports using Excel
- Build interactive dashboards using Power BI
- Provide actionable information for human data review

---

## 🏭 Business Scenario

The project simulates a manufacturing procurement environment containing four main entities:

- **Suppliers**
- **Materials**
- **Categories**
- **Purchases**

The system focuses on two areas.

### 1. Master Data Quality

The project identifies issues such as:

- Missing supplier emails
- Missing supplier phone numbers
- Missing material categories
- Missing or invalid material prices
- Invalid purchase quantities
- Inconsistent country names
- Inconsistent units of measurement
- Potential duplicate suppliers
- Potential duplicate materials

### 2. Procurement Analytics

The project analyzes:

- Total procurement spend
- Procurement spend by category
- Monthly procurement trends
- Top suppliers by procurement spend
- Top materials by purchased quantity
- Supplier contact quality
- Material data quality

---

## 🔄 Project Workflow

```text
Raw CSV Data
      ↓
Python Cleaning & Validation
      ↓
Cleaned Data
      ↓
MySQL Relational Database
      ↓
SQL Business Analysis
      ↓
 ┌─────────────────┬─────────────────┐
 ↓                 ↓                 ↓
Excel Reports   Power BI Dashboard   Review Data
                   ↓
          Final Business Insights
