# ToxValDB
> ToxValDB: Compiling Publicly Available In Vivo Toxicity Data

Install with biobricks-r:
```R
library(biobricks) # devtools::install_github("biobricks-ai/biobricks-r")
biobricks::brick_install("toxvaldb", pull=T) # install & pull database
toxvaldb <- biobricks::brick_load("toxvaldb")[[1]]
```

# Example

## Install and load toxvaldb
```R
library(biobricks) # devtools::install_github("biobricks-ai/biobricks-r")
biobricks::brick_install("toxvaldb", pull=T) # install & pull database
toxvaldb <- biobricks::brick_load("toxvaldb")[[1]] |> collect()

toxvaldb |> count(toxval_type,sort=T)  # count tox types
#  toxval_type      n
#  LC50        172533
#  LD50         98647
# … with 3391 more rows

toxvaldb |> group_by(source) |> # count chems by source
  summarize(num_chem=n_distinct(dtxsid)) |> 
  arrange(-num_chem)
#  source                         num_chem
#  TEST                             13547
#  ECHA IUCLID                       8911
#  ECHA eChemPortal 2020             8309
# … with 40 more rows
```

# Resources
1. [ToxValDB Presentation In PDF](https://epa.figshare.com/ndownloader/files/14518088)
2. FTP private access ftp://newftp.epa.gov/COMPTOX/STAFF/rjudson/datasets/ToxValDB/