library(ggplot2)
library(dplyr)
library(readr)
library(gridExtra)

# IMDA Unified Plotting Engine
# This script handles different clinical data types and generates comprehensive visualizations.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("Usage: Rscript clinical-plots_unified.r <var_name> <output_path> <datatype>")
}

var_name <- args[1]
output_path <- args[2]
datatype <- args[3]

# Load harmonized data
if (!file.exists("harmonized_registry_data.rds")) {
  stop("Error: harmonized_registry_data.rds not found.")
}
df <- readRDS("harmonized_registry_data.rds")

if (!var_name %in% names(df)) {
  stop(paste("Error: Variable", var_name, "not found in dataset."))
}

# Clean data for plotting
plot_df <- df %>% 
  select(all_of(var_name), subject_sex) %>%
  filter(!is.na(.[[var_name]]))

# Convert subject_sex to factor for grouping
if ("subject_sex" %in% names(plot_df)) {
  plot_df$subject_sex <- factor(plot_df$subject_sex, 
                               levels = c(1, 2), 
                               labels = c("Male", "Female"))
}

# Define plotting functions
create_categorical_plots <- function(data, var) {
  # Bar chart with counts
  p1 <- ggplot(data, aes_string(x = var, fill = var)) +
    geom_bar() +
    theme_minimal() +
    labs(title = paste("Distribution of", var),
         y = "Count", x = var) +
    theme(legend.position = "none") +
    scale_fill_brewer(palette = "Set3")

  # Grouped bar chart by sex
  p2 <- ggplot(data, aes_string(x = var, fill = "subject_sex")) +
    geom_bar(position = "dodge") +
    theme_minimal() +
    labs(title = paste(var, "by Biological Sex"),
         y = "Count", fill = "Sex") +
    scale_fill_manual(values = c("#56B4E9", "#E69F00"))

  return(list(p1, p2))
}

create_continuous_plots <- function(data, var) {
  # Density plot with histogram
  p1 <- ggplot(data, aes_string(x = var)) +
    geom_histogram(aes(y = ..density..), bins = 30, fill = "lightgray", color = "white") +
    geom_density(fill = "#69b3a2", alpha = 0.4) +
    theme_minimal() +
    labs(title = paste("Distribution of", var),
         y = "Density", x = var)

  # Violin + Boxplot by sex
  p2 <- ggplot(data, aes_string(x = "subject_sex", y = var, fill = "subject_sex")) +
    geom_violin(alpha = 0.5) +
    geom_boxplot(width = 0.1, color = "black", outlier.shape = NA) +
    theme_minimal() +
    labs(title = paste(var, "by Biological Sex"),
         y = var, x = "Sex") +
    theme(legend.position = "none") +
    scale_fill_manual(values = c("#56B4E9", "#E69F00"))

  return(list(p1, p2))
}

# Logic based on datatype
plots <- list()
if (datatype %in% c("nominal", "ordinal")) {
  plots <- create_categorical_plots(plot_df, var_name)
} else {
  # Default to continuous for ratio, interval, etc.
  plots <- create_continuous_plots(plot_df, var_name)
}

# Save multi-panel plot
png(output_path, width = 1000, height = 500, res = 100)
grid.arrange(grobs = plots, ncol = 2)
dev.off()

print(paste("Successfully generated plot for", var_name, "at", output_path))
