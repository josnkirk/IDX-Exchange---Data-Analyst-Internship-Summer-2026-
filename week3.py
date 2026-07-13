import pandas as pd
import os

folder = "/Users/josiekirk/Documents/IDX Internship"

# Load cleaned datasets from Week 2
listings = pd.read_csv(
    os.path.join(folder, "listings_cleaned.csv"),
    low_memory=False
)

sold = pd.read_csv(
    os.path.join(folder, "sold_cleaned.csv"),
    low_memory=False
)

print("Listings:", listings.shape)
print("Sold:", sold.shape)

# Fetch weekly 30-year fixed mortgage rates from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(
    url,
    parse_dates=["observation_date"]
)

# Rename the columns to make them easier to use
mortgage.columns = [
    "date",
    "rate_30yr_fixed"
]

print(mortgage.head())

# Create a year-month key
mortgage["year_month"] = mortgage["date"].dt.to_period("M")

# Calculate the average mortgage rate for each month
mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)

print(mortgage_monthly.head())

print("\nMortgage dataset information:")
print(mortgage.info())

print("\nNumber of monthly mortgage observations:")
print(len(mortgage_monthly))

print("\nMost recent monthly rates:")
print(mortgage_monthly.tail())

# Create a year-month key in the Sold dataset
sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
sold["year_month"] = sold["CloseDate"].dt.to_period("M")

# Create a year-month key in the Listings dataset
listings["ListingContractDate"] = pd.to_datetime(listings["ListingContractDate"])
listings["year_month"] = listings["ListingContractDate"].dt.to_period("M")

print(sold[["CloseDate", "year_month"]].head())
print(listings[["ListingContractDate", "year_month"]].head())


# Merge monthly mortgage rates into the Sold dataset
sold_with_rates = sold.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

# Merge monthly mortgage rates into the Listings dataset
listings_with_rates = listings.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)
print("\nMissing mortgage rates in Sold:")
print(sold_with_rates["rate_30yr_fixed"].isnull().sum())

print("\nMissing mortgage rates in Listings:")
print(listings_with_rates["rate_30yr_fixed"].isnull().sum())

# Save the datasets with mortgage rates
sold_with_rates.to_csv(
    os.path.join(folder, "sold_with_mortgage.csv"),
    index=False
)

listings_with_rates.to_csv(
    os.path.join(folder, "listings_with_mortgage.csv"),
    index=False
)

print("Saved sold_with_mortgage.csv and listings_with_mortgage.csv")
