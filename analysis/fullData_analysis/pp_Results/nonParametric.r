# Load necessary libraries
library(emmeans)
library(pwr)

# Enter data for each group
group1 <- c(2.48724348 ,2.15923711 ,3.70322287, 1.96552311, 2.57274485 ,2.95029697,
 4.44587959, 6.31989291,4.48065322 ,3.68430462 ,2.16100356 ,3.90194051)

group2 <- c(2.89851795 ,2.14522229 ,3.73233052 ,3.29317827, 3.18527363, 3.8251418,
 2.84543917 ,2.23242264 ,3.1281673,  2.51307554, 3.51075276 ,1.74651176)

group3 <- c(3.91016555, 2.83852048, 3.68176208 ,6.37219868, 6.25486452, 6.05718206,
 2.86208763 ,3.29847587 ,4.03315435 ,3.48560722 ,3.95407841 ,9.77222302)

# Load necessary libraries
library(dunn.test)
library(effsize)


# Combine data into a single dataframe
data <- data.frame(
  value = c(group1, group2, group3),
  group = factor(rep(c("Group1", "Group2", "Group3"), each = 12))
)

# Perform Kruskal-Wallis test
kruskal_result <- kruskal.test(value ~ group, data = data)

# Print Kruskal-Wallis test result
print(kruskal_result)

# Perform Dunn's test for post-hoc comparisons
dunn_result <- dunn.test(data$value, data$group, method = "bonferroni")

# Calculate effect size (epsilon-squared)
n <- nrow(data)
k <- length(unique(data$group))
epsilon_squared <- (kruskal_result$statistic - k + 1) / (n - k)

# Print effect size
cat("\nEffect size (epsilon-squared):", epsilon_squared, "\n")

# Perform post-hoc power analysis
# Note: There's no direct non-parametric equivalent for power analysis
# We'll use a conservative approach based on the asymptotic relative efficiency (ARE)
# of the Kruskal-Wallis test compared to one-way ANOVA (ARE ≈ 0.955)

library(pwr)

ARE <- 0.955
adjusted_n <- n * ARE
groups_n <- k
observations_per_group <- adjusted_n / groups_n
df_between <- groups_n - 1
df_within <- adjusted_n - groups_n

f_squared <- epsilon_squared / (1 - epsilon_squared)
power_result <- pwr.f2.test(u = df_between, v = df_within, f2 = f_squared, sig.level = 0.05)

# Print power analysis results
cat("\nApproximate post-hoc power analysis:\n")
print(power_result)