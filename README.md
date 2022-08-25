# ToxValDB
> ToxValDB: Compiling Publicly Available In Vivo Toxicity Data

Install dvc and download toxvaldb with:
```
brew install dvc
dvc get -o toxvaldb https://github.com/biobricks-ai/toxvaldb data/
```

Install with biobricks-r:
```R
library(biobricks)
biobricks::brick_install("toxvaldb")
biobricks::brick_pull("toxvaldb")
toxvaldb <- biobricks::brick_load("toxvaldb")
```

# Resources
1. [ToxValDB Presentation In PDF](https://epa.figshare.com/ndownloader/files/14518088)
2. FTP private access ftp://newftp.epa.gov/COMPTOX/STAFF/rjudson/datasets/ToxValDB/