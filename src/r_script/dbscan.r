#!/usr/bin/env Rscript
library(dbscan)

args <- commandArgs(trailingOnly = TRUE)
temp_dir <- args[2]


# Create the model
create_model <- function(dir, mol) {
    path_train_data <- paste(dir, "train_values.csv", sep = "/")
    train_data <- read.csv(file = path_train_data, colClasses = c("numeric",
    "numeric", "NULL", "NULL", "NULL", "NULL"))
    train_data <- na.omit(train_data)

    # DBSCAN method with all parameters
    model_dbscan <- dbscan(train_data, eps = 8, minPts = 12, weights = NULL,
    borderPoints = TRUE)

    path_save_model <- paste("models/dbscan_", mol, "_model.Rds",
    sep = "")
    saveRDS(model_dbscan, path_save_model)

    #Save the cluster figure
    # Open png file
    path_png <- paste("figures_clust/dbscan_", mol, "_cluster.png",
    sep = "")
    png(path_png)

    # Create plot
    plot(train_data, col = model_dbscan$cluster + 1, main = "DBSCAN")

    # Close png file
    invisible(dev.off())
    path_save_png <- paste("\nClustering save: figures_clust/dbscan_",
    mol, "_cluster.png\n\n", sep = "")
    cat(path_save_png)
}


# Load the model
test_model <- function(dir, model_path) {
    load_model <- readRDS(model_path)
    print(summary(load_model))
    return(load_model)
}


# Rank the model labels
rank_model <- function(load_model) {
    raw_model_labels <- table(load_model$classification)
    ranked_model_labels <- order(raw_model_labels, decreasing = TRUE)
    return(ranked_model_labels)
}


# Predict the test labels
predict_labels <- function(load_model, dir) {
    path_train_data <- paste(dir, "train_values.csv", sep = "/")
    train_data <- read.csv(file = path_train_data, colClasses = c("numeric",
    "numeric", "NULL", "NULL", "NULL", "NULL"))
    train_data <- na.omit(train_data)

    path_test_data <- paste(dir, "test_values.csv", sep = "/")
    test_data <- read.csv(file = path_test_data)[, 1:2]
    test_data <- na.omit(test_data)

    test_labels <- predict(load_model, test_data, train_data)
    return(test_labels)
}


# Return a sequence from the labels
arrange_labels <- function(test_labels, ranked_model_labels) {
    sequence <- ""
    for (i in 1:length(test_labels)) { # nolint: seq_linter.
        sequence <- paste(sequence, LETTERS[test_labels[i]], sep = "")
    }
    cat(sequence, file = "list_seq.fasta", sep = "\n", append = TRUE)
}


if (args[1] == "train") {
    mol <- args[3]
    create_model(temp_dir, mol)
} else if (args[1] == "test") {
    model_path <- args[3]
    load_model <- test_model(temp_dir, model_path)
    ranked_model_labels <- rank_model(load_model)

    test_labels <- predict_labels(load_model, temp_dir)
    arrange_labels(test_labels, ranked_model_labels)
}
