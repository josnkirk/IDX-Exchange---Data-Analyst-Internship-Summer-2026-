"""
Created on Mon Jul 27 17:26:12 2026

@author: josiekirk
"""

import pandas as pd
import os

# Folder containing internship datasets
folder = "/Users/josiekirk/Documents/IDX Internship"

# Load the mortgage-enriched datasets from Week 3
listings = pd.read_csv(
    os.path.join(folder, "listings_with_mortgage.csv"),
    low_memory=False
)

sold = pd.read_csv(
    os.path.join(folder, "sold_with_mortgage.csv"),
    low_memory=False
)

print("Listings loaded:", listings.shape)
print("Sold loaded:", sold.shape)

# Store original dimensions for the final before/after summary
listings_rows_before = len(listings)
sold_rows_before = len(sold)

listings_columns_before = listings.shape[1]
sold_columns_before = sold.shape[1]

# Remove columns with more than 90% missing values
def drop_high_missing_columns(df, label, threshold=0.90):
    missing_percent = df.isnull().mean()
    columns_to_drop = missing_percent[missing_percent > threshold].index.tolist()

    print(f"\n{label} columns with more than 90% missing values:")
    print(columns_to_drop)

    return df.drop(columns=columns_to_drop), columns_to_drop

sold, sold_high_missing = drop_high_missing_columns(
    sold,
    "Sold"
)

listings, listings_high_missing = drop_high_missing_columns(
    listings,
    "Listings"
)
# Remove duplicated columns ending in .1 when they match the original column
def drop_duplicate_suffix_columns(df, label):
    duplicate_columns = []

    for col in df.columns:
        if col.endswith(".1"):
            original = col[:-2]

            if original in df.columns and df[col].equals(df[original]):
                duplicate_columns.append(col)

    print(f"\nDuplicate .1 columns removed from {label}:")
    print(duplicate_columns)

    return df.drop(columns=duplicate_columns), duplicate_columns

sold, sold_duplicate_columns = drop_duplicate_suffix_columns(
    sold,
    "Sold"
)

listings, listings_duplicate_columns = drop_duplicate_suffix_columns(
    listings,
    "Listings"
)

print("\nColumns after cleanup:")
print("Listings:", listings.shape[1])
print("Sold:", sold.shape[1])

listings_columns_after_cleanup = listings.shape[1]
sold_columns_after_cleanup = sold.shape[1]

# Convert date fields to datetime
date_fields = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

for col in date_fields:
    if col in sold.columns:
        sold[col] = pd.to_datetime(
            sold[col],
            errors="coerce"
        )

    if col in listings.columns:
        listings[col] = pd.to_datetime(
            listings[col],
            errors="coerce"
        )

# Confirm date data types
print("\nSold date data types:")
print(
    sold[
        [col for col in date_fields if col in sold.columns]
    ].dtypes
)

print("\nListings date data types:")
print(
    listings[
        [col for col in date_fields if col in listings.columns]
    ].dtypes
)
# Convert numeric fields
numeric_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeSquareFeet",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket"
]

for col in numeric_fields:
    if col in sold.columns:
        sold[col] = pd.to_numeric(
            sold[col],
            errors="coerce"
        )

    if col in listings.columns:
        listings[col] = pd.to_numeric(
            listings[col],
            errors="coerce"
        )

# Confirm numeric data types
print("\nSold numeric data types:")
print(
    sold[
        [col for col in numeric_fields if col in sold.columns]
    ].dtypes
)

print("\nListings numeric data types:")
print(
    listings[
        [col for col in numeric_fields if col in listings.columns]
    ].dtypes
)

# Flag invalid numeric values in Sold
sold["invalid_closeprice_flag"] = sold["ClosePrice"] <= 0
sold["invalid_livingarea_flag"] = sold["LivingArea"] <= 0
sold["invalid_daysonmarket_flag"] = sold["DaysOnMarket"] < 0
sold["invalid_bedrooms_flag"] = sold["BedroomsTotal"] < 0
sold["invalid_bathrooms_flag"] = sold["BathroomsTotalInteger"] < 0

print("\nSold invalid value counts:")
print("ClosePrice <= 0:", sold["invalid_closeprice_flag"].sum())
print("LivingArea <= 0:", sold["invalid_livingarea_flag"].sum())
print("DaysOnMarket < 0:", sold["invalid_daysonmarket_flag"].sum())
print("BedroomsTotal < 0:", sold["invalid_bedrooms_flag"].sum())
print("BathroomsTotalInteger < 0:", sold["invalid_bathrooms_flag"].sum())

# Flag invalid numeric values in Listings
listings["invalid_listprice_flag"] = listings["OriginalListPrice"] <= 0
listings["invalid_livingarea_flag"] = listings["LivingArea"] <= 0
listings["invalid_daysonmarket_flag"] = listings["DaysOnMarket"] < 0
listings["invalid_bedrooms_flag"] = listings["BedroomsTotal"] < 0
listings["invalid_bathrooms_flag"] = listings["BathroomsTotalInteger"] < 0

print("\nListings invalid value counts:")
print("OriginalListPrice <= 0:", listings["invalid_listprice_flag"].sum())
print("LivingArea <= 0:", listings["invalid_livingarea_flag"].sum())
print("DaysOnMarket < 0:", listings["invalid_daysonmarket_flag"].sum())
print("BedroomsTotal < 0:", listings["invalid_bedrooms_flag"].sum())
print("BathroomsTotalInteger < 0:", listings["invalid_bathrooms_flag"].sum())

# Date consistency checks
sold["listing_after_close_flag"] = (
    sold["ListingContractDate"] > sold["CloseDate"]
)

sold["purchase_after_close_flag"] = (
    sold["PurchaseContractDate"] > sold["CloseDate"]
)

sold["negative_timeline_flag"] = (
    sold["PurchaseContractDate"] < sold["ListingContractDate"]
)

print("\nSold date consistency checks:")
print("Listing after Close:", sold["listing_after_close_flag"].sum())
print("Purchase after Close:", sold["purchase_after_close_flag"].sum())
print("Negative Timeline:", sold["negative_timeline_flag"].sum())

# Geographic checks
sold["missing_coordinates_flag"] = (
    sold["Latitude"].isna() | sold["Longitude"].isna()
)

sold["zero_coordinate_flag"] = (
    (sold["Latitude"] == 0) |
    (sold["Longitude"] == 0)
)

sold["longitude_error_flag"] = (
    sold["Longitude"] > 0
)

print("\nSold geographic checks:")
print("Missing Coordinates:", sold["missing_coordinates_flag"].sum())
print("Zero Coordinates:", sold["zero_coordinate_flag"].sum())
print("Positive Longitude:", sold["longitude_error_flag"].sum())


listings["missing_coordinates_flag"] = (
    listings["Latitude"].isna() | listings["Longitude"].isna()
)

listings["zero_coordinate_flag"] = (
    (listings["Latitude"] == 0) |
    (listings["Longitude"] == 0)
)

listings["longitude_error_flag"] = (
    listings["Longitude"] > 0
)

print("\nListings geographic checks:")
print("Missing Coordinates:", listings["missing_coordinates_flag"].sum())
print("Zero Coordinates:", listings["zero_coordinate_flag"].sum())
print("Positive Longitude:", listings["longitude_error_flag"].sum())

# Flag coordinates outside California

sold["implausible_coordinates_flag"] = (
    (sold["Latitude"] <= 32.53) |
    (sold["Latitude"] >= 42.00) |
    (sold["Longitude"] <= -124.44) |
    (sold["Longitude"] >= -114.13)
)

print("Sold Out-of-State Coordinates:",
      sold["implausible_coordinates_flag"].sum())


listings["implausible_coordinates_flag"] = (
    (listings["Latitude"] <= 32.53) |
    (listings["Latitude"] >= 42.00) |
    (listings["Longitude"] <= -124.44) |
    (listings["Longitude"] >= -114.13)
)

print("Listings Out-of-State Coordinates:",
      listings["implausible_coordinates_flag"].sum())

print("\nSummary")
print("-" * 40)

print(f"Listings rows: {listings_rows_before:,} -> {len(listings):,}")
print(f"Sold rows: {sold_rows_before:,} -> {len(sold):,}")

print(
    f"Listings columns: {listings_columns_before} "
    f"-> {listings_columns_after_cleanup} after cleanup "
    f"-> {listings.shape[1]} including flags"
)

print(
    f"Sold columns: {sold_columns_before} "
    f"-> {sold_columns_after_cleanup} after cleanup "
    f"-> {sold.shape[1]} including flags"
)
# Save cleaned datasets

sold.to_csv(
    os.path.join(folder, "sold_cleaned_week4_5.csv"),
    index=False
)

listings.to_csv(
    os.path.join(folder, "listings_cleaned_week4_5.csv"),
    index=False
)
print("\nWeek 4-5 cleaned datasets saved successfully")
