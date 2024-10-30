# Load data
data <- read.csv(
  "analysis/fullData_analysis/survey_analysis/parsed_survey_data.csv"
)
data <- data[order(data$test_group), ]

# # RTLX
# nf_group <- data[data$test_group == "NF", ]$RTLX
# sf_group <- data[data$test_group == "SF", ]$RTLX
# tf_group <- data[data$test_group == "TF", ]$RTLX

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - RTLX... p = 0.14
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - RTLX... p = 0.57
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - RTLX... p = 0.111
# anova_result_rtlx <- aov(value ~ group, data = data)
# print(summary(anova_result_rtlx))

# # Perform t-test - RTLX... p = 0.0357*, 0.0597 --> this is shown in the survey figure
# fb_group <- c(sf_group, tf_group)
# ind_ttest_rtlx <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_rtlx <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Mental demand (md)
# nf_group <- data[data$test_group == "NF", ]$mental_demand
# sf_group <- data[data$test_group == "SF", ]$mental_demand
# tf_group <- data[data$test_group == "TF", ]$mental_demand

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - mental demand... p = 0.002*
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - mental demand... p = 0.5405
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - mental demand... p = 0.0914
# anova_result_md <- aov(value ~ group, data = data)
# print(summary(anova_result_md))

# # Normality cannot be assumed, perform Kruskal-Wallis test - mental demand... p = 0.0825
# kruskal_result_md <- kruskal.test(value ~ group, data = data)
# print(kruskal_result_md)

# # Perform t-test - mental demand... p = 0.0283*, 0.0489*
# fb_group <- c(sf_group, tf_group)
# ind_ttest_md <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_md <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Physical demand (pd)
# nf_group <- data[data$test_group == "NF", ]$physical_demand
# sf_group <- data[data$test_group == "SF", ]$physical_demand
# tf_group <- data[data$test_group == "TF", ]$physical_demand

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - physical demand... p = 0.00563*
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - physical demand... p = 0.9947
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - physical demand... p = 0.183
# anova_result_pd <- aov(value ~ group, data = data)
# print(summary(anova_result_pd))

# # Normality cannot be assumed, perform Kruskal-Wallis test - physical demand... p = 0.106
# kruskal_result_pd <- kruskal.test(value ~ group, data = data)
# print(kruskal_result_pd)

# # Perform t-test - physical demand... p = 0.0792, 0.0825
# fb_group <- c(sf_group, tf_group)
# ind_ttest_pd <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_pd <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Temporal demand (td)
# nf_group <- data[data$test_group == "NF", ]$temporal_demand
# sf_group <- data[data$test_group == "SF", ]$temporal_demand
# tf_group <- data[data$test_group == "TF", ]$temporal_demand

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - temporal demand... p = 0.00488*
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - temporal demand... p = 0.602
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - temporal demand... p = 0.832
# anova_result_td <- aov(value ~ group, data = data)
# print(summary(anova_result_td))

# # Normality cannot be assumed, perform Kruskal-Wallis test - temporal demand... p = 0.6602
# kruskal_result_td <- kruskal.test(value ~ group, data = data)
# print(kruskal_result_td)

# # Perform t-test - temporal demand... p = 0.6956, 0.6928
# fb_group <- c(sf_group, tf_group)
# ind_ttest_td <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_td <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Effort (efrt)
# nf_group <- data[data$test_group == "NF", ]$effort
# sf_group <- data[data$test_group == "SF", ]$effort
# tf_group <- data[data$test_group == "TF", ]$effort

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - effort... p = 0.00105*
# sw_test <- shapiro.test(data$value)
# print(sw_test)

# # Test for equal variance - effort... p = 0.7966
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - effort... p = 0.123
# anova_result_efrt <- aov(value ~ group, data = data)
# print(summary(anova_result_efrt))

# # Normality cannot be assumed, perform Kruskal-Wallis test - effort... p = 0.0988
# kruskal_result_md <- kruskal.test(value ~ group, data = data)
# print(kruskal_result_md)

# # Perform t-test - effort... p = 0.064, 0.0562
# fb_group <- c(sf_group, tf_group)
# ind_ttest_md <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_md <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Frustration (frstrn)
# nf_group <- data[data$test_group == "NF", ]$frustration
# sf_group <- data[data$test_group == "SF", ]$frustration
# tf_group <- data[data$test_group == "TF", ]$frustration

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - frustration... p = 0.00085*
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - frustration... p = 0.2117
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - frustration... p = 0.29
# anova_result_frstrn <- aov(value ~ group, data = data)
# print(summary(anova_result_frstrn))

# # Normality cannot be assumed, perform Kruskal-Wallis test - frustration... p = 0.2839
# kruskal_result_frstrn <- kruskal.test(value ~ group, data = data)
# print(kruskal_result_frstrn)

# # Perform t-test - frsutration... p = 0.1361, 0.089
# fb_group <- c(sf_group, tf_group)
# ind_ttest_frstrn <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_frstrn <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Performance (perform)
# nf_group <- data[data$test_group == "NF", ]$performance
# sf_group <- data[data$test_group == "SF", ]$performance
# tf_group <- data[data$test_group == "TF", ]$performance

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - performance... p = 0.0459*
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - performance... p = 0.487
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - performance... p = 0.926
# anova_result_perform <- aov(value ~ group, data = data)
# print(summary(anova_result_perform))

# # Normality cannot be assumed (slight), perform Kruskal-Wallis test - effort... p = 0.941
# kruskal_result_perform <- kruskal.test(value ~ group, data = data)
# print(kruskal_result_perform)

# # Perform t-test - performance... p = 0.9552, 0.9577
# fb_group <- c(sf_group, tf_group)
# ind_ttest_perform <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_perform <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Perceived usefulness (PU)
# nf_group <- data[data$test_group == "NF", ]$PU
# sf_group <- data[data$test_group == "SF", ]$PU
# tf_group <- data[data$test_group == "TF", ]$PU

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - perceived usefulness... p = 0.2398
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - perceived usefulness... p = 0.7253
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - perceived usefulness... p = 0.126
# anova_result_pu <- aov(value ~ group, data = data)
# print(summary(anova_result_pu))

# # Perform t-test - PU... p = 0.167, 0.1976
# fb_group <- c(sf_group, tf_group)
# ind_ttest_pu <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_pu <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Perceived ease of use (PEOU)
# nf_group <- data[data$test_group == "NF", ]$PEOU
# sf_group <- data[data$test_group == "SF", ]$PEOU
# tf_group <- data[data$test_group == "TF", ]$PEOU

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - perceived ease of use... p = 0.0816
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - perceived ease of use... p = 0.1954
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - perceived ease of use... p = 0.722
# anova_result_peou <- aov(value ~ group, data = data)
# print(summary(anova_result_peou))

# # Perform t-test - PEOU... p = 0.9587, 0.9628
# fb_group <- c(sf_group, tf_group)
# ind_ttest_peou <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_peou <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

# #########################################################################################################

# # Borg
# nf_group <- data[data$test_group == "NF", ]$Borg_RPE
# sf_group <- data[data$test_group == "SF", ]$Borg_RPE
# tf_group <- data[data$test_group == "TF", ]$Borg_RPE

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - Borg... p = 0.08143
# sw_test <- shapiro.test(data$value) 
# print(sw_test)

# # Test for equal variance - Borg... p = 0.8488
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - Borg... p = 0.434
# anova_result_borg <- aov(value ~ group, data = data)
# print(summary(anova_result_borg))

# # Perform t-test - Borg... p = 0.2471, 0.2374
# fb_group <- c(sf_group, tf_group)
# ind_ttest_borg <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_borg <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

#########################################################################################################

# # Borg retention
# nf_group <- data[data$test_group == "NF", ]$Borg_RPE_ret
# sf_group <- data[data$test_group == "SF", ]$Borg_RPE_ret
# tf_group <- data[data$test_group == "TF", ]$Borg_RPE_ret

# # Combine into single dataframe
# data <- data.frame(
#   value = c(nf_group, sf_group, tf_group),
#   group = factor(rep(c("NF", "SF", "TF"), each = 12))
# )

# # Test for normality - Borg Ret... p = 0.05757
# sw_test <- shapiro.test(data$value)
# print(sw_test)

# # Test for equal variance - Borg Ret... p = 0.6153
# blt_test <- bartlett.test(value ~ group, data = data)
# print(blt_test)

# # Perform one-way ANOVA - Borg Ret... p = 0.242
# anova_result_borgr <- aov(value ~ group, data = data)
# print(summary(anova_result_borgr))

# # Perform t-test - Borg Ret... p = 0.5159, 5464
# fb_group <- c(sf_group, tf_group)
# ind_ttest_borgr <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
# w_ttest_borgr <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

#########################################################################################################

# Pulse rate mean during retention trial (using biomarkers from Empatica) 
nf_group <- data[data$test_group == "NF", ]$pulse_rate_mean
sf_group <- data[data$test_group == "SF", ]$pulse_rate_mean
tf_group <- data[data$test_group == "TF", ]$pulse_rate_mean

# Combine into single dataframe
data <- data.frame(
  value = c(nf_group, sf_group, tf_group),
  group = factor(rep(c("NF", "SF", "TF"), each = 12))
)

# Test for normality - Pulse Rate... p = 0.3172
sw_test <- shapiro.test(data$value)
print(sw_test)

# Test for equal variance - Pulse Rate... p = 0.8742
blt_test <- bartlett.test(value ~ group, data = data)
print(blt_test)

# Perform t-test - Pulse Rate... p = 0.3351, 0.3094
fb_group <- c(sf_group, tf_group)
ind_ttest_pr <- t.test(nf_group, fb_group, paired = FALSE, var.equal = TRUE)
w_ttest_pr <- t.test(nf_group, fb_group, paired = FALSE, var.equal = FALSE)

