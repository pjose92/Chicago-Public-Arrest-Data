import pandas as pd

input_file = "chicago_crimes.csv"
output_file = "chicago_crimes_cleaned.csv"
chunksize = 100_000

cleaned_chunks = []

for chunk in pd.read_csv(input_file, chunksize=chunksize, low_memory=False):

    # Lowercase column names and strip spaces
    chunk.columns = chunk.columns.str.lower().str.strip()

    # Drop fully empty rows
    chunk.dropna(how='all', inplace=True)

    # Remove duplicates
    chunk.drop_duplicates(inplace=True)

    # Clean string columns
    for col in chunk.select_dtypes(include='object').columns:
        chunk[col] = (
            chunk[col]
            .astype(str)
            .str.strip()
            .str.replace(r'"', '', regex=True)
            .str.replace(r"'", '', regex=True)
        )

    # Normalize 'block' field
    chunk['block'] = chunk['block'].str.replace(r'\d{4}X', '0XX', regex=True)
    chunk['block'] = chunk['block'].str.title()

    # Standardize categorical text fields
    for col in ['primary_type', 'description', 'location_description']:
        chunk[col] = chunk[col].str.title()

    # Normalize and convert arrest/domestic columns
    chunk['arrest'] = chunk['arrest'].astype(str).str.upper().map({'TRUE': True, 'FALSE': False})
    chunk['domestic'] = chunk['domestic'].astype(str).str.upper().map({'TRUE': True, 'FALSE': False})

    # Convert datetime columns
    chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')
    chunk['updated_on'] = pd.to_datetime(chunk['updated_on'], errors='coerce')

    # Remove rows with missing or malformed case numbers
    chunk = chunk[chunk['case_number'].str.match(r'^[A-Z0-9]+$', na=False)]

    # Convert 'ward' to numeric (e.g. "04A" becomes NaN)
    chunk['ward'] = pd.to_numeric(chunk['ward'], errors='coerce')

    # Remove rows with invalid lat/lon (null or 0)
    chunk = chunk[(chunk['latitude'] != 0) & (chunk['longitude'] != 0)]
    chunk = chunk.dropna(subset=['latitude', 'longitude'])

    # Filter out geographic outliers
    chunk = chunk[(chunk['latitude'] >= 41) & (chunk['latitude'] <= 43)]
    chunk = chunk[(chunk['longitude'] <= -87) & (chunk['longitude'] >= -89)]

    # Filter data from 2020 onward (AFTER date conversion but BEFORE .dt.date)
    chunk = chunk[chunk['date'].dt.year >= 2020]

    # Drop time portion after filtering
    chunk['date'] = chunk['date'].dt.date
    chunk['updated_on'] = chunk['updated_on'].dt.date

# Split 'location' into lat2/lon2 if present and valid
if 'location' in chunk.columns:
    # Clean parentheses and whitespace
    chunk['location'] = chunk['location'].str.replace(r"[()]", "", regex=True).str.strip()

    # Filter rows where location contains a comma (valid ones)
    valid_locs = chunk['location'].str.contains(",", na=False)

    # Proceed only if any rows are valid
    if valid_locs.any():
        # Split into two parts
        split_location = chunk.loc[valid_locs, 'location'].str.split(",", n=1, expand=True)

        # Safely assign lat2 and lon2
        chunk.loc[valid_locs, 'lat2'] = pd.to_numeric(split_location.iloc[:, 0].str.strip(), errors='coerce')
        chunk.loc[valid_locs, 'lon2'] = pd.to_numeric(split_location.iloc[:, 1].str.strip(), errors='coerce')

    # Drop the original location column
    chunk.drop(columns=['location'], inplace=True, errors='ignore')


    # Ensure required fields are present
    required = ['case_number', 'date', 'latitude', 'longitude', 'primary_type']
    chunk.dropna(subset=required, inplace=True)

    cleaned_chunks.append(chunk)

# Combine and export
cleaned_df = pd.concat(cleaned_chunks)
cleaned_df.to_csv(output_file, index=False)

print(f"✅ Cleaned CSV saved to: {output_file}")

# Preview the top 5 rows from the cleaned version
preview = pd.read_csv(output_file, nrows=5)
print("\n🧪 Preview of cleaned data:\n", preview)
