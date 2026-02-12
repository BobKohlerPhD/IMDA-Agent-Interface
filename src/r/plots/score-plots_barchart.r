library(ggplot2)
library(dplyr)
library(readr)

args <- commandArgs(trailingOnly = TRUE)
var_name <- args[1]
output_path <- args[2]

df <- readRDS("harmonized_registry_data.rds")
# Plotting logic...
