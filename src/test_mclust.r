library(mclust)


train_data <- read.csv(file = 'tmp/result_train.csv')

model_mclust <- Mclust(train_data)
# summary(model_mclust)
saveRDS(model_mclust, "tmp/model_mclust.rds")


test_data <- read.csv(file = 'tmp/result_test.csv')

load_model <- readRDS("tmp/model_mclust.rds")
info_pred <- predict(load_model, test_data)

info_pred.classification

# # Open png file
# png("tmp/mclust_plot.png") 
# # Create plot
# plot(load_model, what = "classification")
# # Close png file
# dev.off() 
