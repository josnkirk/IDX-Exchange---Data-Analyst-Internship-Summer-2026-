
import pandas as pd
import os

# Folder containing the Week 2 cleaned datasets
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

print("Listings loaded:", listings.shape)
print("Sold loaded:", sold.shape)

# Convert date fields to datetime
date_fields = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

for col in date_fields:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")

    if col in listings.columns:
        listings[col] = pd.to_datetime(listings[col], errors="coerce")

print("\nSold date types:")
print(sold[[c for c in date_fields if c in sold.columns]].dtypes)

print("\nListings date types:")
print(listings[[c for c in date_fields if c in listings.columns]].dtypes)

# Numeric columns in Listings
listing_numeric = [
    "OriginalListPrice",
    "ClosePrice",
    "LivingArea",
    "LotSizeSquareFeet",
    "BedroomsTotal",
    "BathroomsTotalInteger"
]

# Numeric columns in Sold
sold_numeric = [
    "ClosePrice",
    "LivingArea",
    "LotSizeSquareFeet",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket"
]

for col in listing_numeric:
    listings[col] = pd.to_numeric(listings[col], errors="coerce")

for col in sold_numeric:
    sold[col] = pd.to_numeric(sold[col], errors="coerce")
    
# Remove invalid rows from Sold
sold_clean = sold[
    (sold["ClosePrice"] > 0) &
    (sold["LivingArea"] > 0) &
    (sold["DaysOnMarket"] >= 0) &
    (sold["BedroomsTotal"] >= 0) &
    (sold["BathroomsTotalInteger"] >= 0)
].copy()

# Remove invalid rows from Listings
listing_clean = listings[
    (listings["OriginalListPrice"] > 0) &
    (listings["LivingArea"] > 0) &
    (listings["BedroomsTotal"] >= 0) &
    (listings["BathroomsTotalInteger"] >= 0)
].copy()


print("\nSold rows before:", len(sold))
print("Sold rows after:", len(sold_clean))
print("Sold rows removed:", len(sold) - len(sold_clean))

print("\nListings rows before:", len(listings))
print("Listings rows after:", len(listing_clean))
print("Listings rows removed:", len(listings) - len(listing_clean))

# Save Week 4 cleaned datasets
sold_clean.to_csv(
    os.path.join(folder, "sold_cleaned.csv"),
    index=False
)

listing_clean.to_csv(
    os.path.join(folder, "listings_cleaned.csv"),
    index=False
)

print("\nWeek 4 cleaned datasets saved successfully") 
