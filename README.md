# ToxValDB
> ToxValDB: Compiling Publicly Available In Vivo Toxicity Data

Install dvc and download toxvaldb with:
```
brew install dvc
dvc get -o toxvaldb https://github.com/biobricks-ai/toxvaldb data/
```

Install with biobricks-r:
```R
library(biobricks) # devtools::install_github("biobricks-ai/biobricks-r")
biobricks::brick_install("toxvaldb", pull=T) # install & pull database
toxvaldb <- biobricks::brick_load("toxvaldb")
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

toxvaldb |> group_by(source) |> 
  summarize(num_chem=n_distinct(dtxsid)) |> 
  arrange(-num_chem)
# # A tibble: 43 × 2
#    source                         num_chem
#    <chr>                            <int>
#  1 TEST                             13547
#  2 ECHA IUCLID                       8911
#  3 ECHA eChemPortal 2020             8309
# … with 40 more rows
```

# Resources
1. [ToxValDB Presentation In PDF](https://epa.figshare.com/ndownloader/files/14518088)
2. FTP private access ftp://newftp.epa.gov/COMPTOX/STAFF/rjudson/datasets/ToxValDB/