-- ShopEase E-Commerce Database - master script
-- Runs everything in order. Target: MySQL 8+
-- Usage:  mysql -u root -p < 00_master_run_all.sql
-- Or inside the MySQL shell:  SOURCE /full/path/to/00_master_run_all.sql

SOURCE 01_schema_setup.sql;
SOURCE 02_data_insertion.sql;
SOURCE 03_section_A_basics.sql;
SOURCE 04_section_B_filtering.sql;
SOURCE 05_section_C_aggregation.sql;
SOURCE 06_section_D_joins.sql;
SOURCE 07_section_E_advanced.sql;
SOURCE 08_use_cases_and_validation.sql;
