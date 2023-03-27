library(mclust)


# Create the model
train_data <- read.csv(file = "tmp/result_train.csv")
model_mclust <- Mclust(train_data)
saveRDS(model_mclust, "tmp/model_mclust.rds")


# Load the model
load_model <- readRDS("tmp/model_mclust.rds")
summary(load_model)


# Order the model labels
raw_model_labels <- table(load_model$classification)
order_model_labels <- order(raw_model_labels, decreasing = TRUE)
order_model_labels


# Predict the test labels
test_data <- read.csv(file = "tmp/result_test.csv")
test_labels <- predict(load_model, test_data)$classification


# Rearrange the test labels
for (i in 1:length(test_labels)) {
    test_labels[i] <- grep(test_labels[i], order_model_labels)
}
test_labels


# # Save the cluster figure
# # Open png file
# png("tmp/mclust_plot.png") 
# # Create plot
# plot(load_model, what = "classification")
# # Close png file
# dev.off() 
