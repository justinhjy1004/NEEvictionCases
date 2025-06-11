# Nebraska Eviction Cases

A modular, reproducible pipeline for scraping, cleaning, extracting, and analyzing eviction case data in Nebraska civil courts.

## Table of Contents

- [Description](#description)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Scraping](#1-scraping)
  - [2. Cleaning & Extraction](#2-cleaning--extraction)
  - [3. Defendant Information](#3-defendant-information)
  - [4. Address Geocoding](#4-address-geocoding)
  - [5. Document Extraction](#5-document-extraction)
  - [6. Cross-Validation & Analysis](#6-cross-validation--analysis)
- [Dependencies](#dependencies)
  - [Python](#python)
  - [R](#r)
- [Data](#data)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Description

NEEvictionCases provides a step-by-step workflow to:

- **Scrape** eviction case HTML pages (targeted and brute-force) via Selenium
- **Extract & Clean** structured case details (JSON → CSV)
- **Combine** datasets into a unified `AllEvictionCases.csv`
- **Enrich** with defendant demographics and predict missing data
- **Geocode** addresses using the U.S. Census Bureau API
- **Extract** referenced documents and images from case actions
- **Cross-Validate** hearing and demographic data with custom R scripts

## Directory Structure

```
├── 00_Scrapers              # Selenium-based scraping scripts
├── 01_CleanAndExtract       # JSON→CSV extraction, cleaning, and combining
├── 02_DefendantInformation   # Named-defendant extraction & demographics
├── 03_AddressGeocoding      # Address prep, batch geocoding, parsing
├── 04_Documents             # Extracts document numbers & images
├── 05_CrossValidate         # R scripts for cross-validation & analyses
├── LICENSE                  # CC0 1.0 Universal
└── README.md                # This document
```

## Prerequisites

- **Python 3.7+**
- **R 4.0+**
- **Bash shell** (for provided scripts)
- **WebDriver** (e.g., ChromeDriver) in your `PATH`
- Internet access (for scraping & geocoding)

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/NEEvictionCases.git
   cd NEEvictionCases
   ```

2. **Python environment**:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install pandas numpy requests selenium beautifulsoup4
   ```

3. **R packages**:

   ```r
   install.packages(c("tidyverse", "readxl", "lubridate", "stringr"))
   ```

4. **Credentials**:

   - Create `00_Scrapers/credentials.py` with your court-URL:
     ```python
     url = "https://your-court-website-url"
     ```

## Usage

### 1. Scraping

```sh
cd 00_Scrapers
bash script.sh
```

Modify `script.sh` to specify counties, years, and case ranges as needed.

### 2. Cleaning & Extraction

```sh
cd ../01_CleanAndExtract
bash script.sh
```

### 3. Defendant Information

```sh
cd ../02_DefendantInformation
bash script.sh
```

### 4. Address Geocoding

```sh
cd ../03_AddressGeocoding
bash script.sh
```

### 5. Document Extraction

```sh
python3 ../04_Documents/AttachedDocs.py
```

### 6. Cross-Validation & Analysis

```sh
cd ../05_CrossValidate
Rscript cross_validate.R
Rscript hearings.R
```

## Dependencies

### Python

- pandas
- numpy
- requests
- selenium
- beautifulsoup4

### R

- tidyverse
- readxl
- lubridate
- stringr

## Data

The `Data/` directory (created at runtime) holds all intermediate and final outputs:

- `CourtCases/`: Raw JSON pages
- `targeted_cases.csv`, `bruteforce_cases.csv`: Intermediate CSVs
- `AllEvictionCases.csv`: Combined dataset
- `Documents.csv`, `Images.csv`: Extracted references
- `AddressMatches.csv`, `AddressNoMatch.csv`: Geocoding results
- Excel files from cross-validation (e.g., `Sullivan.xlsx`)


## License

This project is released under **CC0 1.0 Universal**. See `LICENSE` for details.

## Author

Justin Ho 
