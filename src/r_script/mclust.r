#!/usr/bin/env Rscript
library(mclust)


args <- commandArgs(trailingOnly = TRUE)
temp_dir <- args[2]


# Create the model
create_model <- function(dir, mol) {
    path_train_data <- paste(dir, "train_values.csv", sep = "/")
    train_data <- read.csv(file = path_train_data, colClasses = c("numeric",
    "numeric", "NULL", "NULL", "NULL", "NULL"))
    train_data <- na.omit(train_data)

    # Mclust method with all parameters
    model_mclust <- Mclust(train_data, G = NULL, modelNames = NULL,
    prior = NULL, control = emControl(), initialization = NULL,
    warn = mclust.options("warn"), x =  NULL, verbose = interactive())

    path_save_model <- paste("models/mclust_", mol, "_model.Rds", sep = "")
    saveRDS(model_mclust, path_save_model)
}


#Save the cluster figure
save_png <- function(dir, mol) {
    # Open png file
    path_png <- paste("figures_clust/mclust_", mol, "_cluster.png", sep = "")
    png(path_png)
    # Create plot
    path_model <- paste("models/mclust_", mol, "_model.Rds", sep = "")
    plot(readRDS(path_model), what = "classification")
    # Close png file
    invisible(dev.off())
    path_save_png <- paste("\nClustering save: figures_clust/mclust_",
    mol, "_cluster.png\n\n", sep = "")
    cat(path_save_png)
}


# Load the model
test_model <- function(dir, model_path) {
    load_model <- readRDS(model_path)
    return(load_model)
}


# Rank the model labels
rank_model <- function(load_model) {
    raw_model_labels <- table(load_model$classification)
    ranked_model_labels <- order(raw_model_labels, decreasing = TRUE)
    return(ranked_model_labels)
}


# Predict the test labels
predict_labels <- function(load_model, dir, file_name) {
    path_test_data <- paste(dir, "/", file_name, "_values.csv", sep = "")

    test_data <- read.csv(file = path_test_data)[, 1:2]
    test_data <- na.omit(test_data)

    test_labels <- predict(load_model, test_data)$classification
    return(test_labels)
}


# Return a sequence from the labels
arrange_labels <- function(test_labels, ranked_model_labels) {
    sequence <- ""
    for (i in 1:length(test_labels)) { # nolint: seq_linter.
        test_labels[i] <- grep(test_labels[i], ranked_model_labels)
        sequence <- paste(sequence, LETTERS[test_labels[i]], sep = "")
    }
    cat(sequence, file = "list_seq.fasta", sep = "\n", append = TRUE)
}


if (args[1] == "train") {
    mol <- args[3]
    create_model(temp_dir, mol)
    save_png(temp_dir, mol)
} else if (args[1] != "train") {
    file_name <- args[1]
    model_path <- args[3]
    load_model <- test_model(temp_dir, model_path)
    ranked_model_labels <- rank_model(load_model)

    test_labels <- predict_labels(load_model, temp_dir, file_name)
    arrange_labels(test_labels, ranked_model_labels)
}
