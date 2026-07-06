# IDX-Exchange Data Analyst Internship Summer-2026
This repository contains my internship project, which transforms raw monthly MLS listing and sales transaction data into cleaned datasets for analyzing real estate market trends and visualizing housing insights in a Tableau dashboard.
## Week 1 – Monthly Dataset Aggregation

The Week 1 script:

- Loads monthly CRMLS listing and sold CSV files.
- Combines all monthly files into master listing and sold datasets.
- Filters both datasets to include only Residential properties.
- Saves the cleaned datasets as `listings.csv` and `sold.csv`.
- Prints the number of records before and after filtering to verify the data processing steps

### Technologies Used

- Python 3
- Pandas
- Glob
- OS

## Week 2 – Exploratory Data Analysis (EDA)

The Week 2 script:

- Loads the cleaned `listings.csv` and `sold.csv` datasets from Week 1.
- Displays the number of rows and columns in each dataset.
- Reviews the data types of every column.
- Calculates missing value counts and percentages for each column.
- Identifies columns with more than 90% missing values.
- Removes highly incomplete columns from both datasets.
- Generates summary statistics for key housing market variables.
- Saves the cleaned datasets as `listings_cleaned.csv` and `sold_cleaned.csv`.

### Technologies Used

- Python 3
- Pandas
- Glob
- OS
- Spyder IDE
- Git & GitHub
