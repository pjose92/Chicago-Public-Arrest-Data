# Chicago Crime Data Cleaning Project

This project focuses on cleaning and preparing publicly available crime data from the [Chicago Police Department](https://www.chicagopolice.org/statistics-data/public-arrest-data/) for further analysis and visualization. The original dataset is large (over 2GB) and contains inconsistencies, formatting issues, and unnecessary data that were cleaned using Python and pandas.

## 📂 Data Source
- [Chicago Police Department - Public Arrest Data](https://www.chicagopolice.org/statistics-data/public-arrest-data/)
- File: `chicago_crimes.csv`  
- Format: CSV  
- Size: ~2GB  
- Date Range: All years, filtered down to 2020–present

---

## 🧼 Cleaning Steps (Performed in `clean_csv.py`)

### ✅ General Cleaning
- Converted all column names to lowercase and stripped whitespace
- Dropped fully empty rows and duplicate entries
- Cleaned string columns by removing quotes and trimming spaces

### 🧱 Column-Specific Normalization
- **`block`**: Normalized partial address structure (e.g. `0000X` ➝ `0XX`) and applied title casing
- **Categorical Fields**: Standardized text case for `primary_type`, `description`, and `location_description`
- **`arrest` & `domestic`**: Converted `"TRUE"`/`"FALSE"` string values to actual boolean values

### 🕒 Date Columns
- Converted `date` and `updated_on` columns to datetime format
- Dropped time component, keeping only `YYYY-MM-DD`
- Filtered the data to include only entries from **2020 onward**

### 🌍 Geographic Filtering
- Dropped rows with invalid or missing `latitude`/`longitude`
- Removed geographic outliers based on latitude (41–43) and longitude (-89 to -87)

### 🗺️ Location Field Processing
- Cleaned the `location` field by removing parentheses
- Split `location` string into separate `lat2` and `lon2` columns (float type)
- Dropped the original `location` column

### 📌 Data Validation
- Removed rows with invalid `case_number` formatting
- Converted `ward` to a numeric value (non-numeric entries like `"04A"` become `NaN`)
- Ensured essential fields (`case_number`, `date`, `latitude`, `longitude`, `primary_type`) are present

---

## 💾 Output
- Cleaned data saved to `chicago_crimes_cleaned.csv`
- Preview of the top 5 cleaned rows printed after processing

---

## 🛠 Tools Used
- Python 3.12
- pandas
- VS Code

---

## 📈 Next Steps (Suggestions)
- Load the cleaned dataset into MySQL or PostgreSQL
- Perform visual analysis in Tableau or Power BI
- Use geospatial libraries for mapping (e.g. `folium`, `geopandas`)
- Build dashboards or predictive models on arrest patterns

---

## 👤 Author
Jose Perez Guerrero  
[GitHub Profile](https://github.com/pjose92) | [LinkedIn](https://linkedin.com/in/jose-perez-guerrero)

