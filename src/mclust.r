#!/usr/bin/env Rscript
library(mclust)


args <- commandArgs(trailingOnly = TRUE)


# Create the model
create_model <- function() {
    train_data <- read.csv(file = "tmp/result_train.csv")
    model_mclust <- Mclust(train_data)
    saveRDS(model_mclust, "tmp/mclust_model.RData")
}


# Get the labels
test_model <- function() {
    # Load the model
    load_model <- readRDS("tmp/mclust_model.RData")
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
predict_labels <- function(load_model) {
    test_data <- read.csv(file = "tmp/result_test.csv")
    test_labels <- predict(load_model, test_data)$classification
    return(test_labels)
}


# Rearrange the test labels
arrange_labels <- function(test_labels, order_model_labels) {
    sequence <- ""
    for (i in 1:length(test_labels)) {
        test_labels[i] <- grep(test_labels[i], order_model_labels)
        sequence <- paste(sequence, LETTERS[test_labels[i]])
    }
    print(sequence)
}


#Save the cluster figure
save_png <- function(load_model) {
    # Open png file
    png("tmp/mclust_cluster.png") 
    # Create plot
    plot(load_model, what = "classification")
    # Close png file
    garbage <- dev.off()
}


if (args[1] == "train") {
    create_model()
} else if (args[1] == "test") {
    lm <- test_model()
    oml <- order_model(lm)
    tl <- predict_labels(lm)
    arrange_labels(tl, oml)
    save_png(lm)
}
