#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Week 1 - Monthly Dataset Aggregation

This script:
- Loads all monthly CRMLS listing and sold datasets.
- Combines each into a single DataFrame.
- Filters both datasets to Residential properties only.
- Saves the cleaned datasets as listings.csv and sold.csv.
"""

import pandas as pd 
import os
import glob 

# Folder containing all monthly CRMLS CSV files
folder="/Users/josiekirk/Documents/IDX Internship"

# Find all monthly listing and sold CSV files
listing_files=sorted(glob.glob(os.path.join(folder,"CRMLSListing*.csv")))
sold_files=sorted(glob.glob(os.path.join(folder,"CRMLSSold*.csv")))

print("Listing files found:",len(listing_files))
print("Sold files found:",len(sold_files))

# Load all listing CSV files into a list of DataFrames
listing_dfs=[]
for listing_file in listing_files:
    df=pd.read_csv(listing_file,low_memory=False)
    listing_dfs.append(df)
 
# Combine all monthly listing DataFrames into one dataset
combined_listings_df=pd.concat(listing_dfs,ignore_index=True)
print(combined_listings_df.shape)

# Record row count before Residential filtering
listings_before_filter=len(combined_listings_df)
print("Listings before Residential filter:",listings_before_filter)


# Keep only Residential property listings
combined_listings_df=combined_listings_df[
    combined_listings_df["PropertyType"]=="Residential"
]

# Record row count after Residential filtering
listings_after_filter=len(combined_listings_df)
print("Listings after Residential filter:",listings_after_filter)

# Save the filtered listings dataset as a CSV
listing_csv=os.path.join(folder,"listings.csv")
combined_listings_df.to_csv(listing_csv,index=False)

folder="/Users/josiekirk/Documents/IDX Internship"
listing_files=sorted(glob.glob(os.path.join(folder,"CRMLSSOLD*.csv")))
sold_files=sorted(glob.glob(os.path.join(folder,"CRMLSSold*.csv")))
print("Sold files found:",len(sold_files))
print("Sold files found:",len(sold_files))

# Load all listing CSV files into a list of DataFrames
sold_dfs=[]
for sold_file in sold_files:
    df=pd.read_csv(sold_file,low_memory=False)
    sold_dfs.append(df)
    
# Combine all monthly listing DataFrames into one dataset
combined_sold_df=pd.concat(sold_dfs,ignore_index=True)
print(combined_sold_df.shape)

# Record row count before Residential filtering
sold_before_filter=len(combined_sold_df)
print("Sold before Residential filter:",sold_before_filter)

# Keep only Residential property listings
combined_sold_df=combined_sold_df[
    combined_sold_df["PropertyType"]=="Residential"
]

# Record row count after Residential filtering
sold_after_filter=len(combined_sold_df)
print("Sold after Residential filter:",sold_after_filter)

# Save the filtered listings dataset as a CSV
sold_csv=os.path.join(folder,"sold.csv")
combined_sold_df.to_csv(sold_csv,index=False)

