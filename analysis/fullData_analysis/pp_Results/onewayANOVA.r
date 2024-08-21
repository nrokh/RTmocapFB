# Load necessary libraries
library(emmeans)
library(pwr)

# Enter data for each group
group1 <- c(0.16043956, 0.17695473 ,0.42381716, 0.73885602, 0.50120968, 0.27954972,
 0.64351852, 0.88749214 ,0.6330859 , 0.14035088 ,0.9   ,     0.60748256)

group2 <- c(0.28170895, 1.01651652, 0.03422757, 0.60526316, 0.47058824 ,0.33705701,
 0.57667508, 0.57460317 ,0.29230317, 0.18342152, 0.13445378, 0.71195652)

group3 <- c(0.25038139, -0.05806797, -0.12417171 ,-0.14841849 ,-0.11203771, -0.34949495,
  0.27648352, -0.20751232 , 0.0185118 , -0.2560937 , -0.04374389, -0.17901012)

# Combine data into a single dataframe
data <- data.frame(
  value = c(group1, group2, group3),
  group = factor(rep(c("Group1", "Group2", "Group3"), each = 12))
)

# Perform one-way ANOVA
anova_result <- aov(value ~ group, data = data)

# Print ANOVA summary
print(summary(anova_result))

# Perform post-hoc tests (Tukey's HSD)
tukey_result <- TukeyHSD(anova_result)
print(tukey_result)

# Perform pairwise comparisons using emmeans
emmeans_result <- emmeans(anova_result, "group")
pairs_result <- pairs(emmeans_result)
print(pairs_result)

# Calculate effect size (eta-squared)
ss_total <- sum((data$value - mean(data$value))^2)
ss_between <- sum(tapply(data$value, data$group, function(x) length(x) * (mean(x) - mean(data$value))^2))
eta_squared <- ss_between / ss_total

# Perform post-hoc power analysis
groups_n <- 3
observations_per_group <- 12
total_n <- groups_n * observations_per_group
df_between <- groups_n - 1
df_within <- total_n - groups_n

f_squared <- eta_squared / (1 - eta_squared)
power_result <- pwr.f2.test(u = df_between, v = df_within, f2 = f_squared, sig.level = 0.05)

# Print power analysis results
print(power_result)
