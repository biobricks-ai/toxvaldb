pacman::p_load(tidyverse)

# only one csv right now
csv <- fs::dir_ls("download",recurse=T, type="file", regexp=".csv$")
tbl <- readr::read_csv(csv[1])
tbl <- tbl |> rename(year=year...48, publication.year=year...62)
arrow::write_parquet(tbl,"brick/toxvaldb.parquet") # parquet is less than 200mb
