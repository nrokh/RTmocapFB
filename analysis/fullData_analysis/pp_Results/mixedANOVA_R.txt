# install packages
if (!require("ez")) install.packages("ez")
library(ez)

if (!require("emmeans")) install.packages("emmeans")
library(emmeans)

if (!require("lme4")) install.packages("lme4")
library(lme4)

# Create vectors for each group (SF, TF, NF) and sample (NF, RT4, RET)
group1_sample1 <- c(2.50185862,  1.5548734,   4.07692357,  5.7896682,   3.28695714,  3.93631991,
  5.55045399, 10.99351834,  7.50758052,  9.16712041,  8.6378882,   8.64835465)
group1_sample2 <- c(1.78005578, 1.05527914, 1.4849368,  1.71880965, 1.98680689, 1.97986865,
 2.69193187, 2.07870968, 1.66718146, 3.47794883, 1.33689041, 1.91688828)
group2_sample1 <- c( 4.23926086,  6.04410744,  1.64800772,  3.93900245,  3.15665398,  9.86831281,
 11.30674591,  3.59809065,  3.41049906,  3.90690546,  2.12434873,  4.37429503)
group2_sample2 <- c(2.42353478, 1.22638499, 1.31520481, 1.61987855, 1.49174586, 2.89843018,
 2.08410304, 1.59899546, 2.09195119, 1.83877343, 1.3691238,  1.33214528)
group3_sample1 <- c(5.90263623, 2.47305937, 4.1490774,  3.2921931,  7.71200872, 2.11918558,
 5.39251328, 2.17806487, 3.68084577, 2.91918247, 2.82585021, 3.31588742)
group3_sample2 <- c(3.33686699, 2.45695143, 4.675189,   5.87263998, 6.35454374, 4.36309441,
 2.96152882, 2.46361546, 3.26516891, 4.27160602, 3.55546313, 6.72229066)

# make the dataframe
df <- data.frame(
  Subject = rep(1:12, 6),
  Group = rep(rep(c("Group1", "Group2", "Group3"), each = 12), 2),
  Sample = rep(c("Sample1", "Sample2"), each = 36),
  Value = c(group1_sample1, group1_sample2, 
            group2_sample1, group2_sample2, 
            group3_sample1, group3_sample2)
)

# make each subject unique across groups
df$Subject <- paste(df$Group, df$Subject, sep = "_")

# convert group and sample to factors
df$Group <- factor(df$Group)
df$Sample <- factor(df$Sample)

# view the first few rows of the dataframe
head(df)

# check the structure of the dataframe
str(df)

# run the mixed ANOVA
anova_result <- ezANOVA(
  data = df,
  dv = .(Value),
  wid = .(Subject),
  within = .(Sample),
  between = .(Group),
  detailed = TRUE,
  type = 3
)

# print the results
print(anova_result)


# fit the model using lmer from lme4 package
model <- lmer(Value ~ Group * Sample + (1|Subject), data = df)

# post-hoc tests:
# main effect of group:
group_means <- emmeans(model, "Group")
pairs(group_means)

# main effect of sample:
sample_means <- emmeans(model, "Sample")
pairs(sample_means)

# interaction effects:
interaction_means <- emmeans(model, c("Group", "Sample"))
pairs(interaction_means)