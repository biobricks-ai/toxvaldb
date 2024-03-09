pacman::p_load(tidyverse)

# read the 
# only one csv right now
csv <- fs::dir_ls("download",recurse=T, type="file", regexp=".csv$")
tbl <- readr::read_csv(csv[1])
tbl <- tbl |> rename(year=year...48, publication.year=year...62)

path <- fs::dir_create("brick") |> fs::path("toxvaldb.parquet")
arrow::write_parquet(tbl,path) # parquet is less than 200mb
