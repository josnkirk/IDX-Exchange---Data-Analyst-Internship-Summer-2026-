#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 21:55:28 2026

@author: josiekirk
"""

import pandas as pd 
import os 


# Folder containing the cleaned datasets from Week 1
folder="/Users/josiekirk/Documents/IDX Internship"

# Load the cleaned listing and sold datasets
listings=pd.read_csv(
    os.path.join(folder,"listings.csv"),
    low_memory=False
)
sold=pd.read_csv(
    os.path.join(folder,"sold.csv"),
    low_memory=False
)

# Display the number of rows and columns in each dataset
listing_rows, listing_columns = listings.shape
sold_rows, sold_columns = sold.shape

print(f"Listings: {listing_rows:,} rows, {listing_columns} columns")
print(f"Sold: {sold_rows:,} rows, {sold_columns} columns")

# Display the data type of every column
print("\nListings data types:")
print(listings.dtypes)

print("\nSold data types:")
print(sold.dtypes)

# Display missing values for every column
print("\nMissing values in Listings:")
print(listings.isnull().sum())

print("\nMissing values in Sold:")
print(sold.isnull().sum())

# Calculate percentage of missing values
listing_missing_percent = (listings.isnull().sum() / len(listings)) * 100
sold_missing_percent = (sold.isnull().sum() / len(sold)) * 100

print("\nListing Missing Percentages:")
print(listing_missing_percent)

print("\nSold Missing Percentages:")
print(sold_missing_percent)

# Columns with more than 90% missing values
listing_over_90 = listing_missing_percent[listing_missing_percent > 90]
sold_over_90 = sold_missing_percent[sold_missing_percent > 90]

print("\nListing columns with >90% missing values:")
print(listing_over_90)

print("\nSold columns with >90% missing values:")
print(sold_over_90)

# Important numeric fields in Listings
listing_numeric = [
    "OriginalListPrice",
    "ClosePrice",
    "LivingArea",
    "LotSizeSquareFeet",
    "BedroomsTotal",
    "BathroomsTotalInteger"
]
# Important numeric fields in Sold
sold_numeric = [
    "ClosePrice",
    "LivingArea",
    "LotSizeSquareFeet",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket"
]

# Create cleaned copies without columns that have >90% missing values
listing_cleaned = listings.drop(columns=listing_over_90.index)
sold_cleaned = sold.drop(columns=sold_over_90.index)

print("Listing columns before:", listings.shape[1])
print("Listing columns after:", listing_cleaned.shape[1])

print("Sold columns before:", sold.shape[1])
print("Sold columns after:", sold_cleaned.shape[1])

print("\nListing Summary Statistics:")
print(listing_cleaned[listing_numeric].describe())

print("\nSold Summary Statistics:")
print(sold_cleaned[sold_numeric].describe())

# Save cleaned datasets
listing_cleaned.to_csv(
    os.path.join(folder, "listings_cleaned.csv"),
    index=False
)

sold_cleaned.to_csv(
    os.path.join(folder, "sold_cleaned.csv"),
    index=False
)

print("Saved listings_cleaned.csv and sold_cleaned.csv")

