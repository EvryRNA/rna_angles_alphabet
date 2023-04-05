#!/usr/bin/env Rscript
library(mclust)


args <- commandArgs(trailingOnly = TRUE)
temp_dir <- args[2]


# Create the model
create_model <- function(dir) {
    path_train_data <- paste(dir, "train_values.csv", sep = "/")
    train_data <- read.csv(file = path_train_data)

    model_mclust <- Mclust(train_data)
    path_save_model <- paste(dir, "mclust_model.Rds", sep = "/")
    saveRDS(model_mclust, path_save_model)
}


#Save the cluster figure
save_png <- function(dir) {
    # Open png file
    path_png <- paste(dir, "mclust_cluster.png", sep = "/")
    png(path_png)
    # Create plot
    path_model <- paste(dir, "mclust_model.Rds", sep = "/")
    plot(readRDS(path_model), what = "classification")
    # Close png file
    invisible(dev.off())
}


# Load the model
test_model <- function(dir) {
    path_load_model <- paste(dir, "mclust_model.Rds", sep = "/")
    load_model <- readRDS(path_load_model)
    print(summary(load_model))
    return(load_model)
}


# Order the model labels
order_model <- function(load_model) {
    raw_model_labels <- table(load_model$classification)
    order_model_labels <- order(raw_model_labels, decreasing = TRUE)
    return(order_model_labels)
}


# Predict the test labels
predict_labels <- function(load_model, dir) {
    path_test_data <- paste(dir, "test_values.csv", sep = "/")
    test_data <- read.csv(file = path_test_data)
    test_labels <- predict(load_model, test_data)$classification
    return(test_labels)
}


# Return a sequence from the labels
arrange_labels <- function(test_labels, order_model_labels) {
    sequence <- ""
    for (i in 1:length(test_labels)) { # nolint: seq_linter.
        test_labels[i] <- grep(test_labels[i], order_model_labels)
        sequence <- paste(sequence, LETTERS[test_labels[i]])
    }
    print(sequence)
}


if (args[1] == "train") {
    create_model(temp_dir)
    save_png(load_model, temp_dir)
} else if (args[1] == "test") {
    load_model <- test_model(temp_dir)
    order_model_labels <- order_model(load_model)

    test_labels <- predict_labels(load_model, temp_dir)
    arrange_labels(test_labels, order_model_labels)
}
