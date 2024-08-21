# Load necessary libraries
library(nortest)
library(moments)

# Assume 'your_data' is your vector of data
your_data <- c(-0.3915303  ,-0.63000902  ,0.84265511 ,-0.22154115 ,-0.10839523 ,-0.63573049, -0.7635841  ,-0.42247606 ,-0.23852195 ,-0.43462269  ,0.42022575 ,-0.58673559)

# Visual methods
par(mfrow=c(2,2))
hist(your_data, main="Histogram")
qqnorm(your_data)
qqline(your_data)

# Statistical tests
sw_test <- shapiro.test(your_data)
ks_test <- ks.test(your_data, "pnorm", mean=mean(your_data), sd=sd(your_data))
ad_test <- ad.test(your_data)

# Numerical summaries
skew <- skewness(your_data)
kurt <- kurtosis(your_data)

# Print results
cat("Shapiro-Wilk test p-value:", sw_test$p.value, "\n")
cat("Kolmogorov-Smirnov test p-value:", ks_test$p.value, "\n")
cat("Anderson-Darling test p-value:", ad_test$p.value, "\n")
cat("Skewness:", skew, "\n")
cat("Kurtosis:", kurt, "\n")