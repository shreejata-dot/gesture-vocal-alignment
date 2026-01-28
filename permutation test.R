#permutation analysis of gesture–vocalization associations


#libraries
library(tidyverse)
library(readxl)

#load data
data <- read_excel("perm_long.xlsx")

#data preparation
data <- data %>%
  mutate(
    gesture = factor(
      gesture,
      levels = c("R", "N"),
      labels = c("Referential", "Non-referential")
    ),
    vocal = factor(
      vocal,
      levels = c("VS", "VC", "NTH"),
      labels = c("SV", "LV", "NTH")
    )
  ) %>%
  filter(ID %in% c("madeleine", "theophile", "marie", "anais"))

#compute actual proportions
actual_counts <- table(data$gesture, data$vocal)
actual_proportions <- prop.table(actual_counts, margin = 1)

actual_df <- as.data.frame(as.table(actual_proportions)) %>%
  rename(
    Gesture = Var1,
    Vocalization = Var2,
    Proportion = Freq
  ) %>%
  mutate(Type = "Actual")

#permutation test (chance distributions)
set.seed(123)

n_permutations <- 5000
n_gesture <- nrow(actual_counts)
n_vocal <- ncol(actual_counts)

results <- array(
  0,
  dim = c(n_permutations, n_gesture, n_vocal),
  dimnames = list(
    Iteration = seq_len(n_permutations),
    Gesture = rownames(actual_counts),
    Vocalization = colnames(actual_counts)
  )
)

for (i in seq_len(n_permutations)) {
  shuffled_vocal <- sample(data$vocal)
  shuffled_counts <- table(data$gesture, shuffled_vocal)
  shuffled_props <- prop.table(shuffled_counts, margin = 1)
  results[i, , ] <- as.matrix(shuffled_props)
}

shuffled_df <- as.data.frame(as.table(results)) %>%
  rename(
    Iteration = Var1,
    Gesture = Var2,
    Vocalization = Var3,
    Proportion = Freq
  ) %>%
  mutate(Type = "Chance")

#Confidence intervals from shuffled data
ci_data <- shuffled_df %>%
  group_by(Gesture, Vocalization) %>%
  summarise(
    Lower = quantile(Proportion, 0.05, na.rm = TRUE),
    Upper = quantile(Proportion, 0.95, na.rm = TRUE),
    .groups = "drop"
  )

#plot
ggplot() +
  geom_histogram(
    data = shuffled_df,
    aes(x = Proportion, fill = Gesture),
    bins = 30,
    alpha = 0.7,
    position = "identity"
  ) +
  geom_vline(
    data = ci_data,
    aes(xintercept = Lower),
    linetype = "dotted",
    linewidth = 1
  ) +
  geom_vline(
    data = ci_data,
    aes(xintercept = Upper),
    linetype = "dotted",
    linewidth = 1
  ) +
  geom_point(
    data = actual_df,
    aes(x = Proportion, y = 0, color = Gesture),
    size = 3
  ) +
  facet_wrap(~ Vocalization + Gesture, scales = "free", ncol = 2) +
  labs(
    title = "Chance distributions with observed proportions",
    x = "Proportion",
    y = "Density",
    fill = "Gesture type",
    color = "Gesture type"
  ) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    strip.text = element_text(face = "bold"),
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank()
  )

#compute one-tailed p-values ----
p_values_df <- shuffled_df %>%
  group_by(Gesture, Vocalization) %>%
  summarise(
    p_value = mean(
      Proportion >= actual_df$Proportion[
        actual_df$Gesture == unique(Gesture) &
          actual_df$Vocalization == unique(Vocalization)
      ]
    ),
    .groups = "drop"
  )

p_values_df
