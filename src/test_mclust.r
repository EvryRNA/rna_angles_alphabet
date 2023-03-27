library(mclust)


train_data <- read.csv(file = "tmp/result_train.csv")

model_mclust <- Mclust(train_data)
saveRDS(model_mclust, "tmp/model_mclust.rds")


test_data <- read.csv(file = "tmp/result_test.csv")

load_model <- readRDS("tmp/model_mclust.rds")
summary(load_model)

info_pred <- predict(load_model, test_data)
labels <- info_pred$classification

labels




# # Open png file
# png("tmp/mclust_plot.png") 
# # Create plot
# plot(load_model, what = "classification")
# # Close png file
# dev.off() 
