
"""
Airbnb NYC 2019 Data Cleaning Script
Author: [Your Name]
Description: This script loads, cleans, and prepares the Airbnb New York City 2019 dataset
             for analysis and visualization. Outputs a clean CSV ready for Power BI or further analysis.
"""

import pandas as pd

# 1. Load Data
df = pd.read_csv('Airbnb_NY_2019.csv')

# 2. Clean 'name' column
df['name'] = df['name'].replace('', 'N/A')  # Replace empty strings
df['name'] = df['name'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)  # Remove special characters
df = df.dropna(subset=['name'])  # Drop rows where 'name' is NaN
df['name'] = df['name'].str.title()  # Capitalize each word

# 3. Clean 'host_name' column
df['host_name'] = df['host_name'].replace('', 'N/A')
df['host_name'] = df['host_name'].fillna('N/A')
df['host_name'] = df['host_name'].str.strip().str.title()

# 4. Convert 'last_review' to datetime
df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')

# 5. Fill missing values in 'reviews_per_month' with median
median_reviews = df['reviews_per_month'].median()
df['reviews_per_month'].fillna(median_reviews, inplace=True)

# 6. Convert 'price' to float
df['price'] = df['price'].astype(float)

# 7. Remove outliers in 'price' and 'minimum_nights'
# Define IQR for price
Q1_price = df['price'].quantile(0.25)
Q3_price = df['price'].quantile(0.75)
IQR_price = Q3_price - Q1_price
price_lower = Q1_price - 1.5 * IQR_price
price_upper = Q3_price + 1.5 * IQR_price

# Define IQR for minimum nights
Q1_nights = df['minimum_nights'].quantile(0.25)
Q3_nights = df['minimum_nights'].quantile(0.75)
IQR_nights = Q3_nights - Q1_nights
nights_lower = Q1_nights - 1.5 * IQR_nights
nights_upper = Q3_nights + 1.5 * IQR_nights

# Filter based on IQR
df = df[
    (df['price'] >= price_lower) & (df['price'] <= price_upper) &
    (df['minimum_nights'] >= nights_lower) & (df['minimum_nights'] <= nights_upper)
]

# 8. Validate and filter geographic coordinates (New York City bounds)
df = df.dropna(subset=['latitude', 'longitude'])
df = df[
    (df['latitude'] >= 40.49) & (df['latitude'] <= 40.92) &
    (df['longitude'] >= -74.25) & (df['longitude'] <= -73.70)
]

# 9. Standardize categorical text fields
text_cols = ['neighbourhood', 'neighbourhood_group', 'room_type']
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# 10. Save cleaned dataset
df.to_csv('cleaned_airbnb_data.csv', index=False)

# Optional: Download cleaned file if running on Google Colab
# from google.colab import files
# files.download('cleaned_airbnb_data.csv')

# 11. Display a sample of the cleaned data
print(df.head(10))
