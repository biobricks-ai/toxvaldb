# ToxValDB

> EPA Toxicity Value Database - Compiling Publicly Available In Vivo Toxicity Data

## Current Version

| Attribute | Value |
|-----------|-------|
| **ToxValDB Version** | v9.7.0 |
| **Source Date** | September 24, 2025 |
| **Records** | ~242,000 |
| **Chemicals** | ~42,000 |
| **Sources** | 36+ |

## Description

ToxValDB is a large compilation of human health-relevant in vivo toxicology data from the U.S. EPA. It aggregates toxicity values from multiple public data sources into a standardized format, including:

- **Experimental data**: LD50, LC50, NOAEL, LOAEL from in vivo studies
- **Derived values**: RfD, RfC, cancer slope factors, OELs
- **Regulatory limits**: Drinking water standards, occupational exposure limits

### Data Sources

ToxValDB integrates data from 36+ sources including:
- EPA IRIS, ToxRefDB, AEGL, OPP, RSL
- ECHA IUCLID (European chemicals)
- ATSDR MRLs
- EFSA (European food safety)
- Health Canada
- ChemIDplus
- ECOTOX
- And many more...

## Installation

### R
```R
library(biobricks)
biobricks::brick_install("toxvaldb", pull=TRUE)
toxvaldb <- biobricks::brick_load("toxvaldb")[[1]]
```

### Python
```python
import biobricks as bb
toxvaldb = bb.assets("toxvaldb")
df = pd.read_parquet(toxvaldb.toxvaldb_parquet)
```

## Example Usage

```R
library(biobricks)
library(dplyr)

toxvaldb <- biobricks::brick_load("toxvaldb")[[1]] |> collect()

# Count by toxicity value type
toxvaldb |> count(toxval_type, sort=TRUE)
#  toxval_type      n
#  LC50        172533
#  LD50         98647
#  NOAEL        ...
#  LOAEL        ...

# Count chemicals by source
toxvaldb |>
  group_by(source) |>
  summarize(num_chem = n_distinct(dtxsid)) |>
  arrange(-num_chem)
#  source              num_chem
#  TEST                  13547
#  ECHA IUCLID            8911
#  ChemIDplus             ...
```

## Version History

| Version | Date | Records | Notes |
|---------|------|---------|-------|
| v9.7.0 | 2025-09-24 | ~242K | Current version |
| v9.6.1 | 2025-03 | ~242K | DCAP analysis added |
| v9.1 | 2021-06 | ~700K | Previous brick version (stale FTP) |

## Data Dictionary

Key columns in the parquet file (57 total columns):

| Column | Description |
|--------|-------------|
| `DTXSID` | DSSTox Substance ID (EPA chemical identifier) |
| `CASRN` | CAS Registry Number |
| `NAME` | Chemical name |
| `SOURCE` | Data source (ECHA IUCLID, IRIS, ToxRefDB, etc.) |
| `TOXVAL_TYPE` | Type of toxicity value (LD50, LC50, NOAEL, LOAEL, etc.) |
| `TOXVAL_NUMERIC` | Numeric toxicity value |
| `TOXVAL_UNITS` | Units of measurement |
| `SPECIES` | Test species |
| `EXPOSURE_ROUTE` | Route of exposure |
| `STUDY_TYPE` | Type of toxicity study |
| `RISK_ASSESSMENT_CLASS` | Risk assessment classification |

## Resources

1. [ToxValDB on Figshare](https://doi.org/10.23645/epacomptox.20394501) - Official EPA repository
2. [CompTox Chemicals Dashboard](https://comptox.epa.gov/dashboard/) - Search chemicals with ToxValDB data
3. [ToxValDB Publication](https://doi.org/10.1016/j.comtox.2025.100341) - Development paper

## License

Public domain (U.S. Government Work)

## Citation

If you use ToxValDB in your research, please cite:

> Wall T, Sayre R, Weitekamp C, Smith D. Development of the toxicity values database, ToxValDB: A curated resource for experimental and derived human health-relevant toxicity data. Computational Toxicology. 2025.
