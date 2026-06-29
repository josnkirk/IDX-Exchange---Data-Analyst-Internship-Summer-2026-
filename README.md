# IDX-Exchange Data Analyst Internship Summer-2026
This repository contains my internship project, which transforms raw monthly MLS listing and sales transaction data into cleaned datasets for analyzing real estate market trends and visualizing housing insights in a Tableau dashboard.
## Week 1 – Monthly Dataset Aggregation

The Week 1 script:

- Loads monthly CRMLS listing and sold CSV files.
- Combines all monthly files into master listing and sold datasets.
- Filters both datasets to include only Residential properties.
- Saves the cleaned datasets as `listings.csv` and `sold.csv`.
- Prints row counts before and after filtering for verification.

### Technologies Used

- Python 3
- Pandas
- Glob
- OS
