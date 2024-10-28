data <- read.csv(
  "analysis/fullData_analysis/vbtest_accuracy_sides.csv"
)

# Make a data frame with the accuracy and side column
data <- data.frame(
  accuracy = data$Accuracy,
  side = data$Vibration.Side
)

contable <- table(data)
chi_sq <- chisq.test(contable)
print(chi_sq) #p-value = 0.08429